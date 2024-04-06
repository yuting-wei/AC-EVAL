import os

os.environ["HF_HOME"] = "/your/huggingface/cache/path"
os.environ["MODELSCOPE_CACHE"] = "/your/modelscope/cache/path"

import torch
from transformers import (
    PreTrainedModel,
    PreTrainedTokenizer,
    AutoModelForCausalLM as AutoModelForCausalLMHF,
    AutoTokenizer as AutoTokenizerHF,
)
from modelscope import AutoModelForCausalLM, AutoTokenizer, GenerationConfig, AutoModel


class BaseModel:
    MODEL_ZOO: list[str]
    model_name: str
    _model: PreTrainedModel | None = None
    _tokenizer: PreTrainedTokenizer | None = None
    threshold: float | None = None

    def __init__(self, model_name: str) -> None:
        full_name = self.__class__.get_full_name(model_name)
        if full_name is None:
            raise ValueError(f"The {model_name} model is not supported yet!")
        self.model_name = full_name

    @classmethod
    def get_full_name(cls, model_name: str):
        if "/" in model_name:
            if model_name in cls.MODEL_ZOO:
                return model_name
        else:
            # FIXME: 重名
            for item in cls.MODEL_ZOO:
                if model_name == item.split("/", 1)[1]:
                    return item
        return None

    @property
    def model(self):
        return self._model

    @property
    def tokenizer(self):
        return self._tokenizer

    def call_with_messages(self, query: str):
        raise NotImplementedError(
            "Please rewrite and call this function in a subclass!"
        )


class YiModel(BaseModel):
    MODEL_ZOO = [
        "01ai/Yi-6B-Chat",
        "01ai/Yi-34B-Chat",
    ]

    def __init__(self, model_name: str) -> None:
        super().__init__(model_name)

    @property
    def model(self):
        if self._model is None:
            self._model = AutoModelForCausalLM.from_pretrained(
                self.model_name, device_map="auto", torch_dtype="auto"
            ).eval()

        return self._model

    @property
    def tokenizer(self):
        if self._tokenizer is None:
            self._tokenizer = AutoTokenizer.from_pretrained(
                self.model_name, use_fast=False
            )

        return self._tokenizer

    def call_with_messages(self, query: str):
        messages = [{"role": "user", "content": query}]

        input_ids = self.tokenizer.apply_chat_template(
            conversation=messages,
            tokenize=True,
            add_generation_prompt=True,
            return_tensors="pt",
        )
        output_ids = self.model.generate(input_ids.to("cuda"))
        response = self.tokenizer.decode(
            output_ids[0][input_ids.shape[1] :], skip_special_tokens=True
        )

        token_usage = None

        return response, token_usage


class QwenModel(BaseModel):
    MODEL_ZOO = [
        "qwen/Qwen-1_8B-Chat",
        "qwen/Qwen-7B-Chat",
        "qwen/Qwen-14B-Chat",
        "qwen/Qwen-72B-Chat",
        "Xunzillm4cc/Xunzi-Qwen-Chat",
    ]

    def __init__(self, model_name: str) -> None:
        super().__init__(model_name)

    @property
    def model(self):
        if self._model is None:
            self._model = AutoModelForCausalLM.from_pretrained(
                self.model_name, device_map="auto", trust_remote_code=True
            ).eval()

            self._model.generation_config = GenerationConfig.from_pretrained(
                self.model_name, trust_remote_code=True
            )

        return self._model

    @property
    def tokenizer(self):
        if self._tokenizer is None:
            self._tokenizer = AutoTokenizer.from_pretrained(
                self.model_name, trust_remote_code=True
            )

        return self._tokenizer

    def call_with_messages(self, query: str) -> str:
        response, history = self.model.chat(self.tokenizer, query, history=None)

        token_usage = None

        return response, token_usage


class BaichuanModel(BaseModel):
    MODEL_ZOO = [
        "baichuan-inc/Baichuan2-7B-Chat",
        "baichuan-inc/Baichuan2-13B-Chat",
    ]

    def __init__(self, model_name: str) -> None:
        super().__init__(model_name)
        self.model_name = os.path.join(os.environ["MODELSCOPE_CACHE"], self.model_name)

    @property
    def model(self):
        if self._model is None:
            self._model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                device_map="auto",
                trust_remote_code=True,
                torch_dtype=torch.float16,
            ).eval()

            self._model.generation_config = GenerationConfig.from_pretrained(
                self.model_name
            )

        return self._model

    @property
    def tokenizer(self):
        if self._tokenizer is None:
            self._tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                device_map="auto",
                trust_remote_code=True,
                torch_dtype=torch.float16,
            )

        return self._tokenizer

    def call_with_messages(self, query: str) -> str:
        messages = [{"role": "user", "content": query}]
        response = self.model.chat(self.tokenizer, messages)

        token_usage = None

        return response, token_usage


class GLMModel(BaseModel):
    MODEL_ZOO = [
        "ZhipuAI/chatglm3-6b",
    ]

    def __init__(self, model_name: str) -> None:
        super().__init__(model_name)
        # self.model_name = os.path.join(os.environ["MODELSCOPE_CACHE"], self.model_name)

    @property
    def model(self):
        if self._model is None:
            self._model = (
                AutoModel.from_pretrained(self.model_name, trust_remote_code=True)
                .half()
                .cuda()
                .eval()
            )

        return self._model

    @property
    def tokenizer(self):
        if self._tokenizer is None:
            self._tokenizer = AutoTokenizer.from_pretrained(
                self.model_name, trust_remote_code=True
            )

        return self._tokenizer

    def call_with_messages(self, query: str) -> str:
        response, history = self.model.chat(self.tokenizer, query, history=[])

        token_usage = None

        return response, token_usage


if __name__ == "__main__":
    query = "你好！你叫什么名字？"

    model = BaichuanModel("baichuan-inc/Baichuan2-7B-Chat")
    response = model.call_with_messages(query)
    print(response)
