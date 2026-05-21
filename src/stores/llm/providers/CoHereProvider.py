from ..LLMInterface import LLMInterface
from ..LLMEnums import CohereEnum , DocumentTypeEnum
import cohere
import logging

class CoHereProvider(LLMInterface):

    def __init__(self , api_key: str, 
                        defult_input_max_characters: int= 1000,
                        defult_generation_max_output_tokens: int= 1000,
                        defult_generation_temperature: float= 0.1):
        

        self.api_key = api_key
        self.defult_input_max_characters = defult_input_max_characters
        self.defult_generation_max_output_tokens = defult_generation_max_output_tokens
        self.defult_generation_temperature = defult_generation_temperature

        self.generation_model_id=None
        self.embedding_model_id=None
        self.embedding_size=None


        self.client = cohere.Client(api_key=self.api_key)
        self.logger = logging.getLogger(__name__)


    def set_generate_model(self, model_id: str):
            self.generation_model_id = model_id
        
    def set_embedding_model(self,model_id: str, embedding_size: int):
            self.embedding_model_id = model_id
            self.embedding_size = embedding_size

    def process_text(self, text: str):
        return text[:self.defult_input_max_characters].strip()
    
    def generate_text(self,prompt : str, max_output_tokens: int=None,chat_history: list =[], temperature: float = None,):
        
        if not self.client:
            self.logger.error("Cohere client is not initialized.")
            return None
        
        if not self.generation_model_id:
            self.logger.error("Generation model for Cohere was  not set.")
            return None
        
        max_output_tokens= max_output_tokens if max_output_tokens  else self.defult_generation_max_output_tokens
        temperature= temperature if temperature else self.defult_generation_temperature
        
        resopnse= self.client.chat(
            model=self.generation_model_id,
            chat_history=chat_history,
            message=self.process_text(prompt),
            temperature=temperature,
            max_tokens=max_output_tokens
        )

        if not resopnse or not resopnse.text:
            self.logger.error("Failed to generate text from Cohere.")
            return None
        return resopnse.text
    
    def emded_text(self, text: str , document_type: str=None ):
        if not self.client:
            self.logger.error("Cohere client is not initialized.")
            return None
        if not self.embedding_model_id:
            self.logger.error("Embedding model for Cohere was  not set.")
            return None
        
        input_type= CohereEnum.DOCUMENT
        if document_type == DocumentTypeEnum.QUERY:
            input_type= CohereEnum.QUERY


        response = self.client.embed(
            model= self.embedding_model_id,
            texts= [self.process_text(text)],
            input_type= input_type,
            embedding_types=['float'],
        )

        if not response or not response.embeddings or not response.embeddings.float:
            self.logger.error("Failed to generate embeddings from Cohere.")
            return None
        
        return response.embeddings.float[0]
    
    
    def construct_prompt(self, prompt: str ,role: str):
            
        return{
                "role": role,
                "text": self.process_text(prompt)
            }
        