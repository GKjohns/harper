from ..bronco import (GPT_3_5_TURBO, GPT_4, GEMINI_PRO, VALID_MODELS, llm_call, LLMFunction)

def test_func(word):
    return f'Hello from agents! The word is "{word}".'