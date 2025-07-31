# import openai
import json
import os
from django.core.validators import URLValidator
from chatbot.models import LLMModel
from langfuse.openai import openai
import logging


logger = logging.getLogger('django')
validate = URLValidator()


# @observe()
def handle_openai_model(
        messages, max_token=None, temperature=None, company_bot=None, model_name=None, is_json_response=True,
        stream=False, key_name='OPENAI_API_KEY', is_actual_key=False, tools=None, tool_choice=None, client_choice=None
):
    if client_choice:
        client = client_choice
    else:
        client = openai

    if is_actual_key:
        client_api_key = key_name
    else:
        client_api_key = os.getenv(key_name)

    client.api_key = client_api_key

    if not client.api_key:
        raise ValueError(f"No API key found for '{key_name}'. Please set the environment variable correctly.")

    if model_name:
        model_to_use = model_name
    elif company_bot:
        model_to_use = company_bot.llm_model
    else:
        model_to_use = LLMModel.GPT4_O_MINI

    request_data = {
        "model": model_to_use,
        "messages": messages,
    }

    if max_token:
        if model_name == LLMModel.O1:
            request_data["max_completion_tokens"] = max_token
        else:
            request_data["max_tokens"] = max_token
    if temperature:
        request_data['temperature'] = temperature
    if is_json_response:
        request_data["response_format"] = {"type": "json_object"}
    if stream:
        request_data["stream"] = stream
    if tools:
        request_data["tools"] = tools
        if tool_choice:
            request_data["tool_choice"] = tool_choice

    response = client.chat.completions.create(**request_data)

    if is_json_response:
        response_content = response.choices[0].message.content
        response_json = json.loads(response_content)
        return response_json
    else:
        return response
