import os
import pandas as pd
import json


class ACEVALDataset:
    data_dir: str
    file_name: str | None
    file_extension: str
    topic: str
    data_path: str
    _data: pd.DataFrame | None = None
    _dev_data: pd.DataFrame | None = None

    def __init__(self, data_dir: str, file_name: str) -> None:
        self.data_dir = data_dir
        self.file_name = file_name

        # Get data file extension
        file_extension = None
        for file in os.listdir(data_dir):
            if file.startswith(file_name + ".") or file == file_name:
                file_extension = os.path.splitext(file)[1]
                break
        if file_extension is None:
            raise ValueError(f"File not found: {file_name}")
        self.file_extension = file_extension

        if file_extension == ".xlsx":
            self.read_func = pd.read_excel
        elif file_extension == ".csv":
            self.read_func = pd.read_csv
        else:
            raise ValueError(
                f"Reading files with the extension {file_extension} is not yet supported!"
            )

        # Get dataset subject
        with open("../../subject_mapping.json", "r") as file:
            subject_map: dict[str, dict[str, str]] = json.load(file)
        dataset_subject = subject_map.get(file_name)
        if dataset_subject is None:
            raise ValueError(f"Failed to obtain dataset subject: {file_name}")
        self.topic = dataset_subject["Chinese"]

        # Record data file path
        data_path = os.path.join(data_dir, file_name + file_extension)
        self.data_path = data_path

    @property
    def data(self):
        if self._data is None:
            self._data = self.read_func(self.data_path)
        return self._data

    @property
    def dev_data(self):
        if self._dev_data is None:
            self._dev_data = self.read_func(self.data_path.replace("test", "dev"))
        return self._dev_data

    @property
    def num_few_shot(self):
        keywords_to_check = ["sentence_pauses", "translation", "poetry_appreciation"]
        if any(keyword in self.file_name for keyword in keywords_to_check):
            return 3
        elif "summarization_and_analysis" in self.file_name:
            return 1
        else:
            return 5
