from .BaseController import BaseController
from models.DB_Schemes import project, DataChunk
from stores.llm.LLMEnums import DocumentTypeEnum
from typing import List
import time
import json
class NLPController(BaseController):

    def __init__(self,vectordb_client , embedding_client , generation_client):
        super().__init__()
        self.vectordb_client=vectordb_client
        self.embedding_client=embedding_client
        self.generation_client=generation_client

    
    def create_colloection_name(self, project_id):
        return f"collection_{project_id}".strip()
    
    def reset_vector_db_collection (self, project : project):
        collection_name= self.create_colloection_name(project_id=project.project_id)
        return self.vectordb_client.delete_collection(collection_name=collection_name)
    

    def get_vector_db_collection(self , project : project):
        collection_name= self.create_colloection_name(project_id=project.project_id)
        collection_info= self.vectordb_client.get_collection_info(collection_name=collection_name)
        
        return json.loads(
            json.dumps(collection_info, default=lambda x: x.__dict__)
        )
    
    def index_into_vector_db(self,  project : project , chunks: List[DataChunk], chunks_ids: List[int] ,do_reset: bool=False):

        # step 1 : get collection name
        collection_name= self.create_colloection_name(project_id=project.project_id)
        # in this code we are using the collection name as the project id because we want to have one collection per project and we want to use the project id as the collection name because it is unique and it is easy to remember and it is also easy to query later when we want to retrieve the data from the vector db based on the project id
        # and add time to sleep between each embedding request to avoid rate limit error from the embedding provider and we will use a sleep time of 0.7 seconds which is a good time to avoid rate limit error and also to have a good performance when we are processing a large number of chunks and we will also add a logger to log the progress of the indexing process and to log any errors that may occur during the indexing process
        # step 2 : manage items 
        # texts = [ chunk.chunk_text for chunk in chunks ]
        # metadatas = [ chunk.chunk_metadata for chunk in chunks ]
        # vectors=[
        #     self.embedding_client.emded_text(text=text , document_type=DocumentTypeEnum.DOCUMENT.value)
        #     for text in texts
        # ]

        texts = [chunk.chunk_text for chunk in chunks]
        metadatas = [chunk.chunk_metadata for chunk in chunks]

        vectors = []
        for text in texts:
            vector = self.embedding_client.emded_text(
                text=text,
                document_type=DocumentTypeEnum.DOCUMENT.value
            )
            vectors.append(vector)
            time.sleep(0.7)
        # step 3 : create collection if not exists
        _ = self.vectordb_client.create_collection(
            collection_name=collection_name,
            embedding_size=self.embedding_client.embedding_size,
            do_rest=do_reset
        )

        # step 4 : insert into vector db
        _ =self.vectordb_client.insert_many(
            collection_name=collection_name,
            texts=texts,
            vectors=vectors,
            metadatas=metadatas,
            record_ids=chunks_ids,

        )

        return True
    
    def search_vector_db_collection(self , project : project , text : str , limit : int = 5):

        # step 1 : get collection name
        collection_name= self.create_colloection_name(project_id=project.project_id)

        # step 2 : get text embadding vector
        text_vector= self.embedding_client.emded_text(
            text=text,
            document_type=DocumentTypeEnum.QUERY.value
        )

        if not text_vector or len(text_vector) == 0:
            return False
        
        # step # : do semantic search
        results = self.vectordb_client.search_by_vector(
            collection_name=collection_name,
            vector=text_vector,
            limit=limit
        )
        if not results :
            return False

        return json.loads(
            json.dumps(results, default=lambda x: x.__dict__)
        )