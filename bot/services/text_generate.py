import requests
from yandex_cloud_ml_sdk import YCloudML
from langchain_core.language_models import LLM
from dotenv import load_dotenv
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from utils import config

load_dotenv()

OAUTH_TOKEN = config.get_config()['OAUTH_TOKEN']

response = requests.post(
    "https://iam.api.cloud.yandex.net/iam/v1/tokens",
    json={"yandexPassportOauthToken": OAUTH_TOKEN}
)
IAM_TOKEN = response.json().get('iamToken')

class YandexGPT(LLM):
    def __init__(self, folder_id: str, api_key: str, model_version: str = "rc"):
        super().__init__()
        self.__dict__["sdk"] = YCloudML(folder_id=folder_id, auth=api_key)
        self.__dict__["model"] = self.sdk.models.completions("yandexgpt-lite", model_version=model_version)
        self.__dict__["model"] = self.model.configure(temperature=0.3)
    
    def _call(self, prompt: str, stop=None) -> str:
        result = self.model.run([{"role": "user", "text": prompt}])
        return result.alternatives[0].text  if result else ""

    @property
    def _llm_type(self) -> str:
        return "yandex_gpt"

def create_llm():
    yandex_llm = YandexGPT(
        folder_id=config.get_config()['folder_id'],
        api_key=IAM_TOKEN    
    )
    
    return yandex_llm

# response = yandex_llm._call("Скажи привет на любых 3 языках")
# print(response)



