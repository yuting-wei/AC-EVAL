import os
import requests
import json
import logging
from http import HTTPStatus

import dashscope
from openai import OpenAI
from zhipuai import ZhipuAI


class BaseCaller:
    MODEL_ZOO: list[str]
    model_name: str
    __api_key: str | None
    api_name: str
    THRESHOLD: dict[str, int]
    threshold: float

    def __init__(self, model: str, api_key: str | None = None) -> None:
        if model not in self.__class__.THRESHOLD:
            raise ValueError(
                f"{self.__class__}does not yet support {model} model API calls!"
            )
        if api_key is None and os.environ.get(self.__class__.api_name) is None:
            raise ValueError(f"API key not set: {self.__class__.api_name}")
        self.model_name = model
        self.__api_key = api_key
        self.threshold = 60 / self.__class__.THRESHOLD[model]

    @property
    def api_key(self):
        return self.__api_key

    @api_key.setter
    def api_key(self, new_api_key: str):
        self.__api_key = new_api_key

    def call_with_messages(self, query: str):
        raise NotImplementedError(
            "Please rewrite and call this function in a subclass!"
        )


class LingjiCaller(BaseCaller):
    api_name = "DASHSCOPE_API_KEY"
    THRESHOLD = {
        "qwen-turbo": 500,
        "qwen-plus": 200,
        "qwen-max": 80,
        "qwen-max-1201": 80,
    }

    def __init__(self, model: str, api_key: str | None = None) -> None:
        super().__init__(model, api_key)

    def call_with_messages(self, query: str):
        messages = [{"role": "user", "content": query}]
        response = dashscope.Generation.call(
            self.model_name,
            api_key=self.api_key,
            messages=messages,
            result_format="message",  # set the result is message format.
        )
        answer, token_usage = None, None
        if response.status_code == HTTPStatus.OK:
            answer = response.output.choices[0].message.content
            token_usage = response.usage.input_tokens + response.usage.output_tokens
        else:
            logging.error(
                f"Request id: {response.request_id}, Status code: {response.status_code}, error code: {response.code}, error message: {response.message}"
            )
        return answer, token_usage


class QianfanCaller(BaseCaller):
    api_name = "QIANFAN_API_KEY"
    secret_name = "QIANFAN_SECRET_KEY"
    THRESHOLD = {
        "ernie-bot-4.0": 120,
        "ernie-bot": 300,
        "ernie-bot-8k": 300,
    }
    __secret_key: str
    __access_token: str | None = None

    def __init__(self, model: str, api_key: str | None = None) -> None:
        super().__init__(model, api_key)
        self.__secret_key = os.environ[QianfanCaller.secret_name]
        if self.api_key is None:
            self.api_key = os.environ[QianfanCaller.api_name]

    @property
    def secret_key(self):
        return self.__secret_key

    @property
    def access_token(self):
        if self.__access_token is None:
            self.__access_token = self.get_access_token()
        return self.__access_token

    def get_access_token(self):
        url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={self.api_key}&client_secret={self.secret_key}"

        payload = json.dumps("")
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        response = requests.request("POST", url, headers=headers, data=payload)
        access_token: str = response.json().get("access_token")

        return access_token

    def call_with_messages(self, query: str):
        if self.model_name == "ernie-bot-4.0":
            model_in_url = "completions_pro"
        elif self.model_name == "ernie-bot":
            model_in_url = "completions"
        else:
            model_in_url = self.model_name

        url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/{model_in_url}?access_token={self.access_token}"

        messages = {"messages": [{"role": "user", "content": query}]}
        payload = json.dumps(messages)
        headers = {"Content-Type": "application/json"}

        response = requests.request("POST", url, headers=headers, data=payload)
        response_dict = response.json()
        if "error_code" in response_dict:
            raise Exception(f"API call failed: {response_dict['error_msg']}")
        response_txt: str = response_dict["result"]
        token_usage: int = response_dict["usage"]["total_tokens"]

        return response_txt, token_usage


class OpenAICaller(BaseCaller):
    api_name = "OPENAI_API_KEY"
    THRESHOLD = {
        "gpt-3.5-turbo": 500,
        "gpt-3.5-turbo-0613": 500,
        "gpt-3.5-turbo-1106": 500,
        "gpt-3.5-turbo-0125": 500,
        "gpt-4": 500,
        "gpt-4-0613": 500,
        "gpt-4-turbo-preview": 500,
        "gpt-4-0125-preview": 500,
        "gpt-4-1106-preview": 500,
    }

    def __init__(self, model: str, api_key: str | None = None) -> None:
        super().__init__(model, api_key)
        self.client = OpenAI(api_key=self.api_key)

    def call_with_messages(self, query: str):
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                # {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query},
            ],
        )
        response_txt = response.choices[0].message.content
        finish_reason = response.choices[0].finish_reason
        token_usage = response.usage.total_tokens
        if finish_reason != "stop":
            logging.warning(f"API call ended abnormally, end reason: {finish_reason}")

        return response_txt, token_usage


class ZhipuAICaller(BaseCaller):
    api_name = "ZHIPUAI_API_KEY"
    THRESHOLD = {
        "glm-4": float("inf"),
        "glm-3-turbo": float("inf"),
    }

    def __init__(self, model: str, api_key: str | None = None) -> None:
        super().__init__(model, api_key)
        self.client = ZhipuAI(api_key=self.api_key)

    def call_with_messages(self, query: str):
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "user", "content": query},
            ],
        )
        response_txt = response.choices[0].message.content
        finish_reason = response.choices[0].finish_reason
        token_usage = response.usage.total_tokens
        if finish_reason != "stop":
            logging.warning(f"API call ended abnormally, end reason: {finish_reason}")

        return response_txt, token_usage


if __name__ == "__main__":
    query = "你好！你是谁？"
    model = "qwen-max"

    caller = LingjiCaller(model)
    answer, token_usage = caller.call_with_messages(query)
    print(answer, token_usage, sep="\n")
