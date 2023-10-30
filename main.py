from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
import random
import os
import uvicorn

app = FastAPI()

value_types = [ #value types to compare DataEntrys against each other
    "number",
    "time",
    "date"
]


class DataEntry:
    def __init__(self, name: str, value: int or str, value_type: str,  image_url: str = None):
        self.name = name
        self.value = value
        self.value_type = value_type
        self.image_url = image_url
    
    def __str__(self) -> str:
        return f"DataEntry: {self.name} ({self.value_type})"
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, DataEntry):
            return self.name == __value.name and self.value == __value.value and self.value_type == __value.value_type
    
    def value_to_num(self):
        match self.value_type:
            case "number":
                return float(self.value)
            case "time":
                return float(self.value)
            case "date":
                year, month, day = self.value.split("_")
                return float(day) + float(month) * 30 + float(year) * 365 #days since 0 AD

def Max(a: DataEntry, b: DataEntry) -> DataEntry or None:

    if a.value_type != b.value_type:
        raise Exception("Cannot compare DataEntrys of different value types")
    if a.value_to_num() == b.value_to_num():
        return a
    elif a.value_to_num() > b.value_to_num():
        return a
    else:
        return b

def Min(a: DataEntry, b: DataEntry) -> DataEntry or None:
    
    if a.value_type != b.value_type:
        raise Exception("Cannot compare DataEntrys of different value types")
    higher = Max(a, b)
    if higher is None:
        return None
    elif higher == a:
        return b
    else:
        return a


def load_data(name) -> list[DataEntry]:
    csv_path = f"./data/{name}.csv"
    
    dataset = []
    
    with open(csv_path, "r") as f:
        for line in f.readlines():
            data = line.split(",")
            
            name = data[0]
            value = data[1]
            value_type = data[2]
            image_url = data[3] if len(data) > 3 else None
            
            if value_type not in value_types:
                raise Exception(f"Invalid value type: {value_type}")
            
            dataset.append(DataEntry(name, value, value_type, image_url))

    return dataset

global dataset
dataset = load_data("important_history")
dataset = {
    idx: entry for idx, entry in enumerate(dataset)
}

@app.get("/random")
def get_random() -> dict:
    global dataset
    random_id = random.randint(0, len(dataset) - 1)
    random_data = dataset[random_id]
    json_data = {
        "id": random_id,
        "name": random_data.name,
        "value": random_data.value,
        "image_url": random_data.image_url
    }
    
    return json_data

@app.get("/correct")
def is_correct(id1: int, id2: int, id_guess: int) -> bool:
    #url: /correct?id1={id1}&id2={id2}&id_guess={id_guess}
    #return True if id_guess is the same as Max(id1, id2)
    d1 = dataset[id1]
    d2 = dataset[id2]
    d_guess = dataset[id_guess]
    
    return Max(d1, d2) == d_guess

@app.get("/change_data")
def change_data_set(name: str) -> bool:
    #url = /change_data?name={name}
    global dataset
    try:
        dataset = load_data(name)
        dataset = {
            idx: entry for idx, entry in enumerate(dataset)
        }
        return True
    except Exception as e:
        print(e)
        return False

@app.get("/data_options")
def get_datasets() -> list[str]:
    files = os.listdir("./data")
    file_names = [file.split(".")[0] for file in files]
    return file_names

@app.get("/")
def root():
    return FileResponse("./index.html")

@app.get("/script.js")
def script():
    return FileResponse("./script.js")

@app.get("/style.css")
def style():
    return FileResponse("./style.css")



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port = 5000)