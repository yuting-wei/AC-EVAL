from dotenv import load_dotenv

load_dotenv()

import os
import logging
from datetime import datetime
from arg_parser import parse_args
from evaluate.eval import Evaluator

# model_list = [
#     "Qwen-7B-Chat",
#     "Qwen-14B-Chat",
#     "Qwen-72B-Chat",
#     "Xunzi-Qwen-Chat",
#     "qwen-max",
#     "ernie-bot",
#     "ernie-bot-4.0",
#     "glm-4",
#     "glm-3-turbo",
#     "chatglm3-6b",
#     "Yi-6B-Chat",
#     "Yi-34B-Chat",
#     "Baichuan2-7B-Chat", 
#     "Baichuan2-13B-Chat",
#     "gpt-3.5-turbo-0125",
#     "gpt-4-0125-preview",
# ]

args = parse_args()

model_list: list[str] = [model.strip() for model in args.models.split(",")]
assert len(model_list) >= 1, "Select at least one model for evaluation."

data_dir: str = args.data_dir
mode: str = args.mode
times: int = args.times

# Generate dataset list
dataset_list = [os.path.splitext(file)[0] for file in sorted(os.listdir(data_dir))]

if mode == "zero-shot":
    out_root = "output"
elif mode == "zero-shot-cot":
    out_root = "output_zero_cot"
elif mode == "few-shot":
    out_root = "output_few"
elif mode == "few-shot-cot":
    out_root = "output_few_cot"

# Log configuration
formatted_time = datetime.now().strftime("%m%d%H%M")
run_log = os.path.join(out_root, f"run_{model_list[0]}_{formatted_time}.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler(run_log, encoding="utf-8")],
)

for count in range(1, times + 1):
    for model in model_list:
        logging.info(f"Model {model} is being evaluated...")

        out_dir = os.path.join(out_root, model)
        evaluator = Evaluator(
            model_name=model,
            output_dir=out_dir,
            mode=mode,
        )

        for file in dataset_list:
            logging.info(f"Current evaluation dataset: {file}")

            evaluator.update_data(data_dir, file)
            evaluator.call_and_save()
            evaluator.calculate_accuracy()
