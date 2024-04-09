<p align="center"> <img src="resources/title.png" style="width: 100%;" id="title-icon">       </p>

<p align="center">
  ⏬ <a href="#data" target="_blank">Data</a> •   📃 <a href="http://arxiv.org/abs/2403.06574" target="_blank">Paper</a>  •   🏆 <a href="https://github.com/yuting-wei/AC-EVAL/tree/main/#leaderboard" target="_blank">Leaderboard</a>  <br>  <a href="https://github.com/yuting-wei/AC-EVAL/tree/main/README_zh.md">   中文</a> | <a href="https://github.com/yuting-wei/AC-EVAL/tree/main/README.md">English 
</p>


AC-EVAL presents a thorough evaluation suite for Large Language Models (LLMs) focusing on ancient Chinese, covering eras from the Pre-Qin period to the Qing dynasty. This suite includes 3245 multi-choice questions across 3 levels of difficulty and 13 diverse tasks, as shown below. Please check our [paper](http://arxiv.org/abs/2403.06574) for more details. 

<img src="resources/overview.png" style="zoom: 80%;" >

Our aim is to facilitate the assessment of LLMs' capabilities in understanding and processing ancient Chinese language and knowledge.


## Leaderboard
Our leaderboard, which is updated regularly, showcases both zero-shot and five-shot accuracies of various models across two distinct settings: Answer-Only (AO) and Chain-of-Thought (COT). The breakdown results are shown in [breakdown_results.xlsx](https://github.com/yuting-wei/AC-EVAL/tree/main/breakdown_results.xlsx)

#### Zero-shot AO
| Model          | General Historical Knowledge | Short Text Understanding | Long Text Understanding | Average |
|----------------|:----------------------------:|:------------------------:|:-----------------------:|:-------:|
| ERNIE-Bot 4.0  | 77.54                        | 68.11                    | 66.42                   | 70.69   |
| GLM-4          | 76.63                        | 66.66                    | 67.70                   | 70.33   |
| Qwen-max       | 70.77                        | 64.88                    | 63.84                   | 67.50   |
| GLM-3-Turbo    | 75.21                        | 60.52                    | 59.77                   | 65.17   |
| Qwen-72B-Chat  | 71.25                        | 61.48                    | 59.80                   | 64.18   |
| Yi-34B-Chat    | 72.66                        | 61.33                    | 58.36                   | 64.12   |
| Qwen-14B-Chat  | 69.51                        | 56.53                    | 57.38                   | 61.14   |
| ERNIE-Bot      | 68.81                        | 57.80                    | 51.47                   | 59.36   |
| GPT-4          | 66.11                        | 55.11                    | 47.38                   | 56.20   |
| Qwen-7B-Chat   | 62.74                        | 48.76                    | 44.97                   | 52.16   |
| Yi-6B-Chat     | 60.70                        | 47.79                    | 39.49                   | 51.33   |
| Baichuan2-7B-Chat | 64.38                    | 46.77                    | 40.33                   | 50.49   |
| Baichuan2-13B-Chat | 65.57                    | 49.24                    | 35.40                   | 50.07   |
| ChatGLM3-6B    | 58.04                        | 43.01                    | 39.73                   | 46.93   |
| Xunzi-Qwen-Chat| 60.20                        | 44.31                    | 30.87                   | 45.13   |
| GPT-3.5 Turbo  | 53.50                        | 43.72                    | 36.94                   | 44.72   |
| LLaMA2-70B     | 33.55                        | 36.29                    | 30.72                   | 33.54   |

#### Five-shot AO
| Model            | General Historical Knowledge | Short Text Understanding | Long Text Understanding | Average |
|------------------|:----------------------------:|:------------------------:|:-----------------------:|:-------:|
| ERNIE-Bot 4.0    | 75.69                        | 69.59                    | 66.12                   | 70.47   |
| GLM-4            | 74.89                        | 65.48                    | 69.07                   | 69.81   |
| Qwen-max         | 75.29                        | 65.48                    | 66.99                   | 69.25   |
| GLM-3-Turbo      | 72.99                        | 59.48                    | 59.66                   | 64.04   |
| Qwen-72B-Chat    | 71.67                        | 61.30                    | 57.07                   | 63.35   |
| ERNIE-Bot        | 68.81                        | 57.62                    | 50.36                   | 58.93   |
| GPT-4            | 65.91                        | 58.07                    | 48.36                   | 57.45   |
| Qwen-14B-Chat    | 70.60                        | 53.73                    | 45.91                   | 56.75   |
| Yi-34B-Chat      | 66.62                        | 52.57                    | 41.90                   | 53.70   |
| Baichuan2-7B-Chat | 63.37                    | 45.91                    | 39.94                   | 49.74   |
| Baichuan2-13B-Chat | 63.75                    | 45.86                    | 32.74                   | 47.45   |
| Qwen-7B-Chat     | 61.42                        | 45.98                    | 30.78                   | 46.06   |
| ChatGLM3-6B      | 55.74                        | 42.92                    | 38.45                   | 45.71   |
| GPT-3.5 Turbo    | 53.99                        | 43.21                    | 36.40                   | 44.54   |
| Xunzi-Qwen-Chat  | 51.30                        | 41.25                    | 29.84                   | 40.80   |
| Yi-6B-Chat       | 55.76                        | 35.97                    | 28.48                   | 40.07   |



#### Zero-shot COT
| Model         | General Historical Knowledge | Short Text Understanding | Long Text Understanding | Average |
|---------------|:----------------------------:|:------------------------:|:-----------------------:|:-------:|
| Qwen-max      | 75.10                        | 66.72                    | 61.03                   | 67.62   |
| Qwen-72B-Chat | 74.79                        | 65.25                    | 56.78                   | 65.61   |
| Qwen-14B-Chat | 67.51                        | 54.64                    | 46.12                   | 56.09   |
| Qwen-7B-Chat  | 61.54                        | 44.97                    | 40.21                   | 48.91   |

#### Five-shot COT
| Model         | General Historical Knowledge | Short Text Understanding | Long Text Understanding | Average |
|---------------|:----------------------------:|:------------------------:|:-----------------------:|:-------:|
| Qwen-max      | 74.30                        | 65.94                    | 61.46                   | 67.23   |
| Qwen-72B-Chat | 71.79                        | 61.62                    | 57.66                   | 63.69   |
| Qwen-14B-Chat | 67.49                        | 51.51                    | 39.93                   | 52.97   |
| Qwen-7B-Chat  | 59.37                        | 47.71                    | 35.36                   | 47.48   |


## Data

#### Download

- Method 1: Download the zip file (you can also simply open the following link with the browser):
  ```
  wget https://huggingface.co/datasets/yuting-wei/aceval/resolve/main/aceval.zip
  ```
  then unzip it and you may load the data with pandas:
  ```python
  import os
  import pandas as pd
  
  File_Dir="aceval"
  test_df=pd.read_csv(os.path.join(File_Dir,"test","art_and_cultural_heritage.csv"))
  ```

- Method 2: Directly load the dataset using [Hugging Face datasets](https://huggingface.co/datasets/yuting-wei/aceval):

  ```python
  from datasets import load_dataset
  
  dataset=load_dataset(r"yuting-wei/aceval",name="art_and_cultural_heritage")
  ```

#### Data Format

To facilitate usage, we have organized the supercategory labels and English/Chinese names corresponding to 13 subjects. Please refer to [subject_mapping.json](https://github.com/yuting-wei/AC-EVAL/tree/main/subject_mapping.json) for details. The format is:

  ```
  {
      "art_and_cultural_heritage": {
        "English": "Art and Cultural Heritage",
        "Chinese": "艺术和文化遗产",
        "Supercategory": "General Historical Knowledge"
      },
      ...
      "filename":{
          "English": English Name,
          "Chinese": Chinese Name,
          "Supercatagory": Supercatagory Label (General Historical Knowledge/Short Text Understanding/Long Text Understanding)"
      }
  }
  ```

Each subject consists of two splits: dev and test.  The dev set per subject consists of five exemplars with explanations for few-shot evaluation. The test set is for model evaluation. Labels on the test split are not released, users are required to submit their results to automatically obtain test accuracy. [How to submit?](#how-to-submit) 

Below is a dev example from art and cultural heritage:
| Question | A | B | C | D | Answer | Explanation |
|----------|---|---|---|---|--------|-------------|
| 五代南唐时期著名画家顾闳中的绘画名作是？(The famous painting masterpiece of Gu Hongzhong, a famous painter in the Southern Tang Dynasty during the Five Dynasties, is?) |《女史箴图》(Admonitions of the Instructress to the Court Ladies) | 《五牛图》(Five Buffaloes) | 《簪花仕女图》(Ladies with Flowers) | 《韩熙载夜宴图》(Han Xizai Giving a Night Banquet) | D | 顾闳中的绘画名作是《韩熙载夜宴图》。《五牛图》是韩滉的作品，《簪花仕女图》是周昉的作品，《女史箴图》是顾恺之的作品。 (The famous painting by Gu Hongzhong is 'Han Xizai Giving a Night Banquet.' 'Five Buffaloes' is a work by Han Huang, 'Ladies with Flowers' is by Zhou Fang, and 'Admonitions of the Instructress to the Court Ladies' is by Gu Kaizhi.) |


## How to Evaluate on AC-EVAL

We implemented automatic answer extraction using regular expressions, the evaluation code for each model is located in the [src](src) directory.

We use the following prompt when evaluating the models:

#### answer-only prompt
##### Zero-shot AO
```
以下是中国古代{主题}领域的单项选择题，请直接给出正确答案对应的选项。

{测试题目}
A. {选项A}
B. {选项B}
C. {选项C}
D. {选项D}
答案：
```

##### Few-shot AO
```
以下是中国古代{主题}领域的单项选择题示例。在查看这些示例之后，请直接给出接下来一道题目的正确答案所对应的选项。

示例1：{题目1}
A. {选项A}
B. {选项B}
C. {选项C}
D. {选项D}
答案：A

[k-shot demo, note that k is 0 in the zero-shot case]

{测试题目}
A. {选项A}
B. {选项B}
C. {选项C}
D. {选项D}
答案：
```

#### chain-of-thought prompt
##### Zero-shot COT
```
以下是中国古代{主题}领域的单项选择题，请逐步分析并给出正确答案对应的选项。

{测试题目}
A. {选项A}
B. {选项B}
C. {选项C}
D. {选项D}
答案：
```
##### Few-shot COT
```
以下是中国古代{主题}领域的单项选择题示例。在查看这些示例之后，请逐步分析接下来一道题目并给出正确答案所对应的选项。

示例1：{题目1}
A. {选项A}
B. {选项B}
C. {选项C}
D. {选项D}
答案解析：
让我们逐步分析。{解析过程}
所以答案是A。

[k-shot demo, note that k is 0 in the zero-shot case]

{测试题目}
A. {选项A}
B. {选项B}
C. {选项C}
D. {选项D}
答案：
```

## How to Submit

You need to first prepare a UTF-8 encoded JSON file with the following format, please refer to [submission_example.json](https://github.com/yuting-wei/AC-EVAL/tree/main/submission_example.json) for details.

  ```
  {
      "historical_facts": {
          "0": "A",
          "1": "B",
          "2": "B",
          ...
      },
      
      "subject_name":{
      "0":"ans_0",
      "1":"ans_1",
      ...
      }
      ....
  }
  ```
  Then, you can submit the prepared JSON file to the email (yuting_wei@bupt.edu.cn). Please include the type of experiment you conducted in the subject of your email, using one of the following file labels: [zero-shot-AO, few-shot-AO, zero-shot-COT, few-shot-COT].

## TODO

- [x] add evaluation code into `src`
- [x] add breakdown results
- [x] incorporate into Hugging Face datasets


## Licenses

[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

This work is licensed under a [MIT License](https://lbesson.mit-license.org/).

[![CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](http://creativecommons.org/licenses/by-nc-sa/4.0/)

The AC-EVAL dataset is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/).


## Citation

Please cite our paper if you use our dataset.
```
@misc{wei2024aceval,
      title={AC-EVAL: Evaluating Ancient Chinese Language Understanding in Large Language Models}, 
      author={Yuting Wei and Yuanxing Xu and Xinru Wei and Simin Yang and Yangfu Zhu and Yuqing Li and Di Liu and Bin Wu},
      year={2024},
      eprint={2403.06574},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}

```
## Acknowledgements

This project was inspired by and based on the structure of [C-Eval](https://github.com/hkust-nlp/ceval). We are grateful for this work and would like to acknowledge their significant contributions to the community.
