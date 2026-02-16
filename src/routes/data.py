from fastapi import APIRouter,FastAPI,Depends,UploadFile,status
from fastapi.responses import JSONResponse
from helpers.config import get_settings,Settings
from controllers import DataController,ProjectController
from models import ResponseSignal
import os
import aiofiles
import logging
date_router=APIRouter(
    prefix="/api/v1/data",
    tags=["qpi_v1","data"]
)
logger=logging.getLogger('uvicorn.error')


@date_router.post("/upload/{Project_id}")
async def upload_date(Project_id: str,file: UploadFile,
                    app_setings : Settings =Depends(get_settings)):
    
    # validate file type and size
    data_controller=DataController()
    is_valid ,result_message =data_controller.validate_file(file=file)

    if not is_valid:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"message":result_message})
    
    # save file to disk

    project_dir_path=ProjectController().get_project(project_id=Project_id)
    file_path=data_controller.generate_unique_filename(original_filename=file.filename,project_id=Project_id)
    try:
        async with aiofiles.open(file_path, 'wb') as out_file:
            while chunk := await file.read(app_setings.FILE_DEFAULT_CHUNK_SIZE):
                await out_file.write(chunk) 
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content={"message":ResponseSignal.FILE_UPLOAD_FAILED.value,"error":str(e)})

    return JSONResponse(status_code=status.HTTP_200_OK,content={"message":ResponseSignal.FILE_UPLOAD_SUCCESS.value,"file_path":file_path})


