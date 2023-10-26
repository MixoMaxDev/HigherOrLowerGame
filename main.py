from fastapi import FastAPI
import datetime

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
        return None
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


def load_data() -> list[DataEntry]:
    csv_path = "./data.csv"
    
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

dataset = load_data()