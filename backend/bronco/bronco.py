from abc import ABC, abstractmethod
import openai
import google.generativeai as genai

# Constants representing the names of different language models.
GPT_3_5_TURBO = 'gpt-3.5-turbo'
GPT_4 = 'gpt-4'
GEMINI_PRO = 'gemini-pro'

# A tuple of valid model names for validation.
VALID_MODELS = (GPT_3_5_TURBO, GPT_4, GEMINI_PRO)

# Abstract class for a Large Language Model
class LargeLanguageModel(ABC):
    @abstractmethod
    def generate_response(self, prompt, temperature):
        pass

# Concrete class for GPT-3.5 Turbo
class GPT35TurboModel(LargeLanguageModel):
    def generate_response(self, prompt, temperature):
        # Implementation for GPT-3.5 Turbo
        response = openai.ChatCompletion.create(
            model=GPT_3_5_TURBO,
            temperature=temperature,
            messages=[{'role': 'user', 'content': prompt}]
        )
        return response.choices[0]['message']['content']

# Concrete class for GPT-4
class GPT4Model(LargeLanguageModel):
    def generate_response(self, prompt, temperature):
        # Implementation for GPT-4
        response = openai.ChatCompletion.create(
            model=GPT_4,
            temperature=temperature,
            messages=[{'role': 'user', 'content': prompt}]
        )
        return response.choices[0]['message']['content']

# Concrete class for Gemini Pro
class GeminiProModel(LargeLanguageModel):
    def generate_response(self, prompt, temperature):
        # Implementation for Gemini Pro
        return genai.GenerativeModel(GEMINI_PRO).generate_content(prompt).text

# Factory class
class LLMFactory:
    def get_llm_model(self, model_name):
        if model_name == GPT_3_5_TURBO:
            return GPT35TurboModel()
        elif model_name == GPT_4:
            return GPT4Model()
        elif model_name == GEMINI_PRO:
            return GeminiProModel()
        else:
            raise ValueError(f'Must provide a valid model. {model_name} not in {VALID_MODELS}')

# Function to use the factory
def llm_call(prompt, model_name=GPT_3_5_TURBO, temperature=0.0):
    factory = LLMFactory()
    llm_model = factory.get_llm_model(model_name)
    return llm_model.generate_response(prompt, temperature)


class LLMFunction:
    """
    A class representing a function that utilizes a large language model (LLM).

    Attributes:
    prompt_template (str): Template for the prompt to be sent to the model.
    model_name (str): Name of the language model to be used.
    parser (function): A function to parse the model's response.
    succeeded (function): A function to determine if the response is successful.

    Methods:
    inject_data_into_prompt(data): Injects data into the prompt template.
    inference(prompt, temperature): Calls the LLM with a given prompt and temperature.
    parse_response(response): Parses the LLM response using the parser function.
    generate(data, temperature, return_raw_results): Generates a response from the LLM based on the given data.
    """

    def __init__(self, prompt_template=None, model_name=GPT_3_5_TURBO, parser=None, success_func=None):
        """
        Initializes the LLMFunction class with given parameters.

        Parameters:
        prompt_template (str): The template for creating prompts.
        model_name (str, optional): The name of the model to use. Defaults to GPT_3_5_TURBO.
        parser (function, optional): A function to parse model responses. Defaults to a lambda that returns the input.
        success_func (function, optional): A function to determine success of a response. Defaults to a lambda that always returns True.

        Raises:
        ValueError: If no prompt template is provided or an invalid model name is given.
        """
        if not prompt_template:
            raise ValueError('Must provide a prompt template')

        if model_name not in VALID_MODELS:
            raise ValueError(f'Must provide a valid model. {model_name} not in {VALID_MODELS}')
        
        self.prompt_template = prompt_template
        self.model_name = model_name
        self.parser = parser or (lambda x: x)
        self.succeeded = success_func or (lambda x: True)

    def inject_data_into_prompt(self, data):
        """
        Formats the prompt template with the given data.

        Parameters:
        data (dict): Data to be injected into the prompt template.

        Returns:
        str: The formatted prompt.
        """
        return self.prompt_template.format(**data)

    def inference(self, prompt, temperature):
        """
        Calls the LLM with a given prompt and temperature.

        Parameters:
        prompt (str): The prompt to be sent to the LLM.
        temperature (float): The creativity of the model's response.

        Returns:
        str: The model's response.
        """
        return llm_call(prompt, self.model_name, temperature=temperature)

    def parse_response(self, response):
        """
        Parses the LLM response using the provided parser function.

        Parameters:
        response (str): The response from the LLM.

        Returns:
        The output of the parser function applied to the response.
        """
        return self.parser(response)

    def generate(self, data, temperature=0.0, return_raw_results=False):
        """
        Generates a response from the LLM based on the given data.

        Parameters:
        data (dict): Data to be used for generating the prompt.
        temperature (float, optional): The creativity of the model's response. Defaults to 0.0.
        return_raw_results (bool, optional): Whether to return raw results along with the parsed response. Defaults to False.

        Returns:
        Depending on return_raw_results, either the parsed response or a dictionary with parsed response, raw response, and success status.
        """
        full_prompt = self.inject_data_into_prompt(data)
        raw_response = self.inference(full_prompt, temperature=temperature)
        parsed_response = self.parse_response(raw_response)
    
        if return_raw_results:
            return {
                'parsed_response': parsed_response,
                'raw_response': raw_response,
                'succeeded': self.succeeded(parsed_response)
            }
        return parsed_response