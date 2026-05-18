from ..LLMInterface import LLMInterface
from ..LLMEnums import OpenAIEnum
from openai import OpenAI
import logging


class OpenAiProvider(LLMInterface):

    def __init__(self , api_key: str, api_url: str=None, 
                        defult_input_max_characters: int= 1000,
                        defult_generation_max_output_tokens: int= 1000,
                        defult_generation_temperature: float= 0.1):

        self.api_key = api_key
        self.api_url = api_url
        self.defult_input_max_characters = defult_input_max_characters
        self.defult_generation_max_output_tokens = defult_generation_max_output_tokens
        self.defult_generation_temperature = defult_generation_temperature

        self.generation_model_id=None
        self.embedding_model_id=None
        self.embedding_size=None


        self.client = OpenAI(api_key=self.api_key, base_url=self.api_url)

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
                self.logger.error("OpenAI client is not initialized.")
                return None
            
            if not self.genration_model_id:
                self.logger.error("Generation model for OpenAI was  not set.")
                return None
            
            max_output_tokens= max_output_tokens if max_output_tokens  else self.defult_generation_max_output_tokens
            temperature= temperature if temperature else self.defult_generation_temperature


            chat_history.append(
                self.construct_prompt(prompt=prompt, role=OpenAIEnum.USER.value)
            )

            response = self.client.chat.completions.create(
                model=self.generation_model_id,
                messages=chat_history,
                max_tokens=max_output_tokens,
                temperature=temperature,

            )

            if not response or not response.choices or len(response.choices) == 0 or not response.choices[0].message or not response.choices[0].message.content:
                self.logger.error("No valid response returned from OpenAI.")
                return None

            return response.choices[0].message["content"]



        
        def emded_text(self, text: str , document_type: str=None ):

            if not self.client:
                self.logger.error("OpenAI client is not initialized.")
                return None
            
            if not self.embedding_model_id:
                self.logger.error("Embedding model for OpenAI was  not set.")
                return None
            
            response=self.client.embeddings.create(
                model=self.embedding_model_id,
                input=text,

            )

            if not response or not response.data or len(response.data) == 0 or not response.data[0].embedding:
                self.logger.error("No embedding data returned from OpenAI.")
                return None 
            
            return response.data[0].embedding
        

        def construct_prompt(self, prompt: str ,role: str):
            
            return{
                "role": role,
                "content": self.process_text(prompt)
            }