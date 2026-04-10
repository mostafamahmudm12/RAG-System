from fastapi import APIRouter,FastAPI,Depends,UploadFile,status,Request
from fastapi.responses import JSONResponse
from helpers.config import get_settings,Settings
from controllers import DataController,ProjectController,ProcessController
from models import ResponseSignal
from .schemes.data import ProcessRequest
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from models.DB_Schemes import project, data_chunk
from models.DB_Schemes.data_chunk import DataChunk
from bson.objectid import ObjectId
import os
import aiofiles
import logging
date_router=APIRouter(
    prefix="/api/v1/data",
    tags=["qpi_v1","data"]
)
logger=logging.getLogger('uvicorn.error')

# endpoint to upload file for a project
@date_router.post("/upload/{Project_id}")
async def upload_date(request : Request ,Project_id: str,file: UploadFile,
                    app_setings : Settings =Depends(get_settings)):
    
    # project_model = ProjectModel(db_client=request.app.db_client)
    project_model = await ProjectModel.create_instance(db_client=request.app.mongodb) 

    project= await project_model.get_project_or_create_one(
        project_id=Project_id
    )
    
    # validate file type and size
    data_controller=DataController()
    is_valid ,result_message =data_controller.validate_file(file=file)

    if not is_valid:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"message":result_message})
    
    # save file to disk

    project_dir_path=ProjectController().get_project(project_id=Project_id)
    file_path,file_id=data_controller.generate_unique_filepath(original_filename=file.filename,project_id=Project_id)

    try:
        async with aiofiles.open(file_path, 'wb') as out_file:
            while chunk := await file.read(app_setings.FILE_DEFAULT_CHUNK_SIZE):
                await out_file.write(chunk) 
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content={"message":ResponseSignal.FILE_UPLOAD_FAILED.value,"error":str(e)})

    return JSONResponse(status_code=status.HTTP_200_OK,content={"message":ResponseSignal.FILE_UPLOAD_SUCCESS.value,
                                                                "file_path":file_path, "file_id":file_id,
                                                                # "project_id":str(project._id)
                                                                })



# endpoint to process file and split it into chunks
@date_router.post("/process/{project_id}")
async def process_endpoint(request : Request,project_id: str, process_request: ProcessRequest):

    file_id=process_request.file_id
    chunk_size=process_request.chunk_size
    overlap_size=process_request.overlap_size
    do_reset=process_request.do_reset

    proccess_controller=ProcessController(project_id=project_id)

    chunk_model = await ChunkModel.create_instance(db_client=request.app.mongodb) 

    project_model = await ProjectModel.create_instance(db_client=request.app.mongodb) 

    project= await project_model.get_project_or_create_one(
        project_id=project_id
    )




    file_content=proccess_controller.get_file_content(file_id=file_id)

    file_chunks=proccess_controller.process_file_content(
        file_content=file_content,
        file_id=file_id,
        chunk_size=chunk_size,
        overlap_size=overlap_size
        
    )

    if file_chunks is None or len(file_chunks)== 0:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"message":ResponseSignal.PROCCESSING_FAILED.value})
    

    file_chunks = [DataChunk(
        chunk_text=chunk.page_content,
        chunk_metadata=chunk.metadata,
        chunk_order=i+1,
        chunk_project_id=project.id,


    ) for i, chunk in enumerate(file_chunks)]

    if do_reset== 1:
        _=  await chunk_model.delete_chunks_by_project_id(project_id=project.id)

    no_records= await chunk_model.insert_many_chunks(chunks=file_chunks)

    return JSONResponse(status_code=status.HTTP_200_OK,content={"message":ResponseSignal.PROCCESSING_SUCCESS.value,
                                                                "inserted_chunks": no_records,
    })