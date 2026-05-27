from .LLMEnums import LLMEnum
from .providers import OpenAiProvider, CoHereProvider

class LLMProviderFactory:
    def __init__(self, config: dict):
        self.config = config

    def create(self, Provider: str):
        
        if Provider == LLMEnum.OPENAI.value:
            return OpenAiProvider(
                api_key=self.config.OPENAI_API_KEY,
                api_url=self.config.OPENAI_API_URL,
                defult_input_max_characters=self.config.INPUT_DAFAULT_MAX_CHARACTERS,
                defult_generation_max_output_tokens=self.config.GENERATION_DEFULT_MAX_TOKENS,
                defult_generation_temperature=self.config.GENERATION_DEFULT_TEMPERATURE,

            )

        if Provider == LLMEnum.COHERE.value:
            return CoHereProvider(
                api_key=self.config.COHERE_API_KEY,
                defult_input_max_characters=self.config.INPUT_DAFAULT_MAX_CHARACTERS,
                defult_generation_max_output_tokens=self.config.GENERATION_DEFULT_MAX_TOKENS,
                defult_generation_temperature=self.config.GENERATION_DEFULT_TEMPERATURE,
            )

        