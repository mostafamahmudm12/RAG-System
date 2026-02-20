from .BaseController import BaseController
from .ProjectController import ProjectController
import os
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models import ProcessingEnum


class ProcessController(BaseController):

    def __init__(self,project_id:str):
        super().__init__()
        self.project_id=project_id
        self.project_path=ProjectController().get_project(project_id=self.project_id)


    def get_file_extensions(self,file_id: str):
        return os.path.splitext(file_id)[-1]
    

    def get_file_loader(self,file_id: str):
        file_path=os.path.join(
        self.project_path,
        file_id
    )
        file_ext=self.get_file_extensions(file_id=file_id)

        if file_ext == ProcessingEnum.TXT.value:
            return TextLoader(file_path,encoding="utf-8")

        if file_ext == ProcessingEnum.PDF.value:
            return PyMuPDFLoader(file_path)
        
        return None
    
    def get_file_content(self,file_id: str):

        loader=self.get_file_loader(file_id=file_id)
        return loader.load()
    

    def process_file_content(self,file_id: str, file_content: list , 
                            chunk_size: int = 1000, overlap_size: int =20):
        
        text_spilter=RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap_size,
            length_function=len,
        )

        file_content_texts=[
            rec.page_content 
            for rec in file_content
        ]

        file_content_metadata=[
            rec.metadata
            for rec in file_content
        ]

        chunks=text_spilter.create_documents(
            file_content_texts,
            metadatas=file_content_metadata
        )

        return chunks
        