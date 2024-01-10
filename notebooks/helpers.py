import openai
import google.generativeai as genai


GPT_3_5_TURBO = 'gpt-3.5-turbo'
GPT_4 = 'gpt-4'
GEMINI_PRO = 'gemini-pro'

VALID_MODELS = (GPT_3_5_TURBO, GPT_4, GEMINI_PRO)


def llm_call(prompt, model_name=GPT_3_5_TURBO, temperature=0.0):
    
    if model_name not in VALID_MODELS:
        raise ValueError(f'Must provide a valid model. {model_name} not in {VALID_MODELS}')

    if model_name in [GPT_3_5_TURBO, GPT_4]:
        response = openai.ChatCompletion.create(
            model=model_name,
            temperature=temperature,
            messages=[{'role': 'user', 'content': prompt}]
        )
        model_output = response.choices[0]['message']['content']
        
    elif model_name == GEMINI_PRO:
        model_output = genai.GenerativeModel(model_name).generate_content(prompt).text
    
    return model_output


class LLMFunction:
    
    def __init__(self, prompt_template=None, model_name=GPT_3_5_TURBO, parser=None, success_func=None):
        
        if not prompt_template:
            raise ValueError('Must provide a prompt template')

        if model_name not in VALID_MODELS:
            raise ValueError(f'Must provide a valid model. {model_name} not in {VALID_MODELS}')
        
        self.prompt_template = prompt_template
        self.model_name = model_name
        self.parser = parser or (lambda x: x)
        self.succeeded = success_func or (lambda x: True)

    def inject_data_into_prompt(self, data):
        return self.prompt_template.format(**data)

    def inference(self, prompt, temperature):
        return llm_call(prompt, self.model_name, temperature=temperature)

    def parse_response(self, response):
        return self.parser(response)

    def generate(self, data, temperature=0.0, return_raw_results=False):
        
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