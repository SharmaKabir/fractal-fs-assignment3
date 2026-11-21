import json
from pathlib import Path

#class for oops principles
class FileRepository:
    #code for read write save reuqests in json file insside data folder

    def __init__(self, file_path="data/requests.json"):
        self.file_path = Path(file_path)

    def load(self):
        if not self.file_path.exists():
            return []

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                content = file.read().strip()
                if not content:
                    return []
                data = json.loads(content)
        except json.JSONDecodeError as error:
            raise ValueError("The requests json file is invalid") from error

        if not isinstance(data, list):
            raise ValueError("The requests json file must have a json list inside of it!")
        return data

    def save(self, requests): #for saving data using dump
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(requests, file, indent=4)
            file.write("\n")
