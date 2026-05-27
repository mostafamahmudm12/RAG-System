from fastapi import APIRouter,FastAPI,Depends,UploadFile,status,Request
from fastapi.responses import JSONResponse
from routes.schemes.nlp import PushRequest, SearchRequest
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from controllers.NLPController import NLPController
from models.enums.ResponseEnum import ResponseSignal
import os
import aiofiles
import logging

nlp_router=APIRouter(
    prefix="/api/v1/nlp",
    tags=["qpi_v1","nlp"]
)
logger=logging.getLogger('uvicorn.error')


@nlp_router.post("/index/push/{Project_id}")
async def index_project(request : Request, Project_id :str ,push_request : PushRequest):

    project_model= await ProjectModel.create_instance(db_client=request.app.mongodb)    
    project= await project_model.get_project_or_create_one(
        project_id=Project_id
    )

    chunk_model = await  ChunkModel.create_instance(db_client=request.app.mongodb)

    if not project:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": ResponseSignal.PROJECT_NOT_FOUND.value})
    
    nlp_controller= NLPController(
        vectordb_client=request.app.vectordb_client,
        embedding_client=request.app.embedding_client,
        generation_client=request.app.generation_client
    )

    has_records = True
    page_num = 1
    inserted_item_count=0
    idx=0
    while has_records:
        page_chunks =await chunk_model.get_chunks_by_project(
            project_id=project.id,
            page_num=page_num,
        )
        if len(page_chunks):
            page_num += 1

        if not page_chunks or len(page_chunks) == 0:
            has_records = False
            break

        chunks_ids = list(range(idx, idx +len(page_chunks)))
        idx += len(page_chunks)

        is_inserted = nlp_controller.index_into_vector_db(
            project=project,
            chunks=page_chunks,
            do_reset= push_request.do_reset,
            chunks_ids=chunks_ids
        )

        if not is_inserted:
            logger.error(f"Failed to index chunks for project {Project_id} on page {page_num}.")
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": ResponseSignal.INDEXING_FAILED.value})

        inserted_item_count += len(page_chunks)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": ResponseSignal.INDEXING_SUCCESS.value,
                                                        "indexed_items": inserted_item_count
    })


@nlp_router.get("/index/info/{Project_id}")
async def get_project_index_info(request: Request , Project_id : str):
    project_model= await ProjectModel.create_instance(db_client=request.app.mongodb)    

    project= await project_model.get_project_or_create_one(
        project_id=Project_id
    )

    nlp_controller= NLPController(
        vectordb_client=request.app.vectordb_client,
        embedding_client=request.app.embedding_client,
        generation_client=request.app.generation_client
    )


    collection_info = nlp_controller.get_vector_db_collection(project=project)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": ResponseSignal.INDEX_INFO_RETRIEVED.value,
                                                                "collection_info": collection_info
    })



@nlp_router.post("/index/search/{Project_id}")
async def search_index(request :Request ,Project_id: str , search_rquest: SearchRequest):

    project_model= await ProjectModel.create_instance(db_client=request.app.mongodb)    

    project= await project_model.get_project_or_create_one(
        project_id=Project_id
    )

    nlp_controller= NLPController(
        vectordb_client=request.app.vectordb_client,
        embedding_client=request.app.embedding_client,
        generation_client=request.app.generation_client
    )

    results = nlp_controller.search_vector_db_collection(
        project=project,
        text=search_rquest.text,
        limit=search_rquest.limit
    )

    if not results :
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": ResponseSignal.NO_SEARCH_RESULTS.value})


    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": ResponseSignal.VECTORDB_SEARCH_SUCCESS.value,
                                                                "results": results
    })