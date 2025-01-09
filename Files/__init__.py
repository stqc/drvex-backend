from flask import Flask
import os
from openai import OpenAI
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

LLMapi  = os.environ.get('NVIDIA_KEY')
IMAGEapi = os.environ.get('HUGGING_FACE')

llm_client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=LLMapi
)

image_client=InferenceClient("stqc/kai-lora", token=IMAGEapi)

pattern = r"<PROMPT>(.*?)</PROMPT>"
