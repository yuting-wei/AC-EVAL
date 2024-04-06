import os
import re
import time
import logging
from tqdm import tqdm
from typing import Type

from evaluate.data import ACEVALDataset
from evaluate.model_api import *
from evaluate.model_local import *


MODEL_2_PLATFORM: dict[str, Type[BaseCaller | BaseModel]] = {
    # 通义千问Qwen
    "qwen-turbo": LingjiCaller,
    "qwen-plus": LingjiCaller,
    "qwen-max": LingjiCaller,
    "qwen-max-1201": LingjiCaller,
    "Qwen-1_8B-Chat": QwenModel,
    "Qwen-7B-Chat": QwenModel,
    "Qwen-14B-Chat": QwenModel,
    "Qwen-72B-Chat": QwenModel,
    # 荀子Xunzi
    "Xunzi-Qwen-Chat": QwenModel,
    # 文心一言ERNIE
    "ernie-bot-4.0": QianfanCaller,
    "ernie-bot": QianfanCaller,
    # 零一万物Yi
    "Yi-6B-Chat": YiModel,
    "Yi-34B-Chat": YiModel,
    # GPT
    "gpt-3.5-turbo": OpenAICaller,
    "gpt-3.5-turbo-0613": OpenAICaller,
    "gpt-3.5-turbo-1106": OpenAICaller,
    "gpt-3.5-turbo-0125": OpenAICaller,
    "gpt-4": OpenAICaller,
    "gpt-4-0613": OpenAICaller,
    "gpt-4-turbo-preview": OpenAICaller,
    "gpt-4-0125-preview": OpenAICaller,
    "gpt-4-1106-preview": OpenAICaller,
    # GLM
    "glm-4": ZhipuAICaller,
    "glm-3-turbo": ZhipuAICaller,
    "chatglm3-6b": GLMModel,
    # 百川Baichuan
    "Baichuan2-7B-Chat": BaichuanModel,
    "Baichuan2-13B-Chat": BaichuanModel,
}


class Evaluator:
    prompt_zero = "以下是中国古代{}领域的单项选择题，请直接给出正确答案对应的选项。\n\n{}题目：{}\n{}\n答案："
    prompt_zero_cot = "以下是中国古代{}领域的单项选择题，请逐步分析并给出正确答案对应的选项。\n\n{}题目：{}\n{}\n答案："
    prompt_few = "以下是中国古代{}领域的单项选择题。在查看这些示例之后，请直接给出接下来一道题目的正确答案所对应的选项。\n\n{}题目：{}\n{}\n答案："
    prompt_few_cot = "以下是中国古代{}领域的单项选择题。在查看这些示例之后，请逐步分析接下来一道题目并给出正确答案所对应的选项。\n\n{}题目：{}\n{}\n答案："

    output_dir: str
    output_path: str
    dataset: ACEVALDataset
    model_caller: BaseCaller | BaseModel
    MAX_RETRIES = 5
    pattern = [
        r"答案(?:应该?)?(?:是|为|选择?)?[：:]?\s?(?:选项)?\s?[（(]?([A-D])[）)]?",
        r"正确的?(?:一项|答案|选项)(?:所?对应的选项(?:字母)?)?(?:应该?)?[是为]?[：:]?[\s#]*[（(]?([A-D])[）)]?",
        r"^选择?\s?[（(]?([A-D])[）)]?",
        r"(?:综上所述|综合考[虑量]).*?([A-D])",
        r"(?:##(?:因此|故|所以|综上所述|(?:基于|综合|根据)以上[分解]析).*)([A-D])(?=[^A-D]*$)",
        r"(?:故|因此|所以|综上所述)?[,，]?(?:本题)?选择?[：:]?\s?[（(]?([A-D])[）)]?",
        r"[（(]?([A-D])[）)]?\s?(?:选?项)?[是为]?(?:正确|符合题意)的?",
        r"(?:选项)?\s?[（(]?([A-D])[）)]?\s?[是为]?(?:正确|符合题意)的?",
        r"(?:^|：|:)\s?[（(]?([A-D])[）)]?(?:#|。|$)",
        r"^(?:选项?)?[是为]?\s?[（(]?([A-D])[）)]?[.。]?.*?##",
    ]
    English_pattern = [
        r"[Cc]orrect answer (?:is)?[:：]?\s?#*[（(]?([A-D])[）)]?",
        r"(?:[Bb]est)? answer (?:is)?[:：]?\s?#*[（(]?([A-D])[）)]?",
    ]
    no_answer_pattern = [
        r"抱歉，",
        r"无法(?:从给出的选项中)?(?:直接)?(?:给出|确定|判断|得出|选择)(?:唯一)?(?:一个)?(?:确定|确切|正确|明确)?的?(?:答案|选项)",
        r"(?:无|没有)(?:一个)?(?:唯一)?(?:(?:不?正确|错误)?的?(?:答案|选项|解|一项))",
        r"所有(?:答案|选项)都是正确的",
        r"正确答案是?[：:]?无",
    ]
    acc: float | None = None

    def __init__(
        self,
        model_name: str | None = None,
        data_dir: str | None = None,
        file_name: str | None = None,
        api_key: str | None = None,
        output_dir: str | None = None,
        mode="zero-shot",
    ) -> None:
        """
        Params:
            model_name(Optional) - The name of the model, case sensitive.
            data_dir(Optional) - The directory path of the dataset.
            file_name(Optional) - The name or list of names of the dataset file(s) without the extension.
            api_key(Optional) - Manually specify the key for calling the model API, effective only when the model operates via API calls. The default value is stored in the .env file.
            output_dir(Optional) - The directory path where the model's output files are stored.
        """

        # Output file path settings
        if output_dir is None and model_name is not None:
            output_dir = os.path.join("output", model_name)
        if output_dir is not None and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        self.output_dir = output_dir

        if data_dir and file_name:
            self.update_data(data_dir, file_name)
        if model_name:
            self.update_model(model_name, api_key, empty_cache=False)

        self.mode = mode
        if mode == "zero-shot":
            self.prompt = Evaluator.prompt_zero
        elif mode == "zero-shot-cot":
            self.prompt = Evaluator.prompt_zero_cot
        elif mode == "few-shot":
            self.prompt = Evaluator.prompt_few
        elif mode == "few-shot-cot":
            self.prompt = Evaluator.prompt_few_cot
        else:
            raise ValueError(
                "Parameter 'mode' must be in ['zero-shot', 'zero-shot-cot', 'few-shot', 'few-shot-cot']."
            )

    @property
    def model(self):
        return self.model_caller.model_name

    def update_model(
        self, new_model_name: str, new_api_key: str | None = None, empty_cache=True
    ):
        model_caller_cls = MODEL_2_PLATFORM.get(new_model_name)
        if model_caller_cls is None:
            raise ValueError(f"The {new_model_name} model is not supported yet!")

        self.model_caller = None
        # if empty_cache and torch.cuda.is_available():
        #     torch.cuda.empty_cache()

        if issubclass(model_caller_cls, BaseCaller):
            self.model_caller = model_caller_cls(new_model_name, new_api_key)
        elif issubclass(model_caller_cls, BaseModel):
            self.model_caller = model_caller_cls(new_model_name)
        else:
            raise ValueError(
                f"Inheritance error for {model_caller_cls} class, it can only inherit from {BaseCaller} or {BaseModel}"
            )

    def update_data(self, new_data_dir: str, new_file_name: str):
        self.output_path = os.path.join(self.output_dir, f"{new_file_name}.txt")
        self.answer_path = os.path.join(self.output_dir, f"{new_file_name}_answer.txt")
        self.dataset = ACEVALDataset(new_data_dir, new_file_name)

    @property
    def threshold(self):
        return self.model_caller.threshold

    def format_dev_examples(self, df, num_few_shot, cot=False):
        dev_examples = ""
        if num_few_shot:
            dev_sub_df = df.iloc[:num_few_shot]
            for i, row in dev_sub_df.iterrows():
                question = row["Question"]
                # print(question)
                options = [
                    f"{option_letter}. {row[option_letter]}"
                    for option_letter in ["A", "B", "C", "D"]
                ]
                options_txt = "\n".join(options)
                answer = row["Answer"]
                if cot:
                    explanation = row["Explanation"]
                    dev_examples += f"示例{i+1}：{question}\n{options_txt}\n答案解析：\n让我们逐步分析。{explanation}\n所以答案是{answer}。\n\n"
                else:
                    dev_examples += (
                        f"示例{i+1}：{question}\n{options_txt}\n答案：{answer}\n\n"
                    )
            return dev_examples
        else:
            return dev_examples

    def call_and_save(
        self, start_index: int | None = None, limited=True, save_mode="a"
    ):
        if self.dataset is None:
            raise ValueError("Dataset not specified!")
        if self.model_caller is None:
            raise ValueError("Model not specified!")

        if self.threshold is None or self.threshold == 0.0:
            limited = False
        else:
            min_loop_time = self.threshold

        if start_index is None:
            start_index = 0
            if os.path.exists(self.output_path):
                with open(self.output_path, "r", encoding="utf-8") as out:
                    start_index = sum(1 for _ in out)

        with open(self.output_path, save_mode, encoding="utf-8") as out:
            df = self.dataset.data
            dev_df = self.dataset.dev_data
            sub_df = df.iloc[start_index:]
            cot = False
            if self.mode not in ["few-shot", "few-shot-cot"]:
                num_few_shot = None
            else:
                num_few_shot = self.dataset.num_few_shot
                if self.mode == "few-shot-cot":
                    cot = True
            dev_examples = self.format_dev_examples(dev_df, num_few_shot, cot)
            print(dev_examples)

            start_time = time.time()
            total_token_usage = 0
            for i, row in tqdm(sub_df.iterrows(), initial=start_index, total=len(df)):
                question = row["Question"]
                # print(question)
                options = [
                    f"{option_letter}. {row[option_letter]}"
                    for option_letter in ["A", "B", "C", "D"]
                ]
                options_txt = "\n".join(options)
                query = self.prompt.format(
                    self.dataset.topic, dev_examples, question, options_txt
                )

                retry_count = 0
                while retry_count < self.MAX_RETRIES:
                    try:
                        (
                            response_txt,
                            token_usage,
                        ) = self.model_caller.call_with_messages(query)
                        if limited:
                            elapsed_time = time.time() - start_time
                            if elapsed_time < min_loop_time:
                                time.sleep(min_loop_time - elapsed_time + 0.0)
                            start_time = time.time()
                        if token_usage is not None:
                            total_token_usage += token_usage
                        if response_txt is None:
                            retry_count += 1
                            if retry_count < self.MAX_RETRIES:
                                logging.warning(
                                    f"API call failed. Attempting retry number {retry_count + 1}."
                                )
                            else:
                                logging.error(f"API call failed {retry_count} times!")
                                response_txt = ""
                        else:
                            break
                    except Exception as e:
                        if limited:
                            elapsed_time = time.time() - start_time
                            if elapsed_time < min_loop_time:
                                time.sleep(min_loop_time - elapsed_time + 0.0)
                            start_time = time.time()
                        retry_count += 1
                        if retry_count < self.MAX_RETRIES:
                            logging.warning(
                                f"An exception occurs: {e}. Attempting retry number {retry_count + 1}."
                            )
                        else:
                            logging.error(f"API call failed {retry_count} times!")
                            response_txt = ""

                response_txt = response_txt.replace("\r\n", "#").replace("\n", "#")
                out.write(response_txt + "\n")

    def extract_answer(self, response_txt: str):
        ans_list = []
        initial_ans_list = re.findall(r"\b[A-D]\b", response_txt)
        if len(initial_ans_list) == 0:
            initial_ans_list = re.findall(r"[A-D]", response_txt)
        initial_ans_list = list(set(initial_ans_list))
        if len(initial_ans_list) == 1:
            return initial_ans_list
        else:
            # print(initial_ans_list)
            for p in Evaluator.no_answer_pattern:
                if re.search(p, response_txt):
                    return ["无"]
            for p in Evaluator.pattern:
                ans_list = re.findall(p, response_txt)
                if len(ans_list) != 0:
                    return ans_list
            if self.model.startswith("llama"):
                for p in Evaluator.English_pattern:
                    ans_list = re.findall(p, response_txt)
                    if len(ans_list) != 0:
                        return ans_list
            if response_txt != "":
                logging.warning(f"No answer matched：{response_txt}")
                return ["未匹配到"]
            return ["空"]

    # Extract the answer as a letter and the accuracy calculation is done by us
    # Please submit your model's answer file following the example in submission_example.json
    def calculate_accuracy(self):
        with open(self.output_path, "r", encoding="utf-8") as out, open(
            self.answer_path, "w", encoding="uft=8"
        ) as ans:
            for i, line in enumerate(out):
                line = line.strip()
                pred_list = self.extract_answer(line)
                # print(pred_list)
                if len(pred_list) > 1 and any(el != pred_list[0] for el in pred_list):
                    logging.warning(
                        f"The extracted predicted answers are more than one and different: Question {i+1} {pred_list}"
                    )
                    pred = "多选或矛盾"
                else:
                    pred = pred_list[0] if len(pred_list) else "无"

                if pred not in ["A", "B", "C", "D", "空", "无"]:
                    logging.warning(f"Question {i+1}: {line} -> {pred_list} -> {pred}")
                if pred not in [
                    "A",
                    "B",
                    "C",
                    "D",
                    "空",
                    "无",
                    "多选或矛盾",
                    "未匹配到",
                ]:
                    raise ValueError(f"{pred} is not A-D!")
                ans.write(pred + "\n")
