from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Buz"}]

@app.get('/')
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/user/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: int):
    return {"user_id": user_id}

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}

@app.get("files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

# Query parameter
@app.get("/fake/items/")
async def read_fake_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip+limit]

@app.get("/fake/items/{item_id}")
async def read_fake_item(item_id: str, q: Optional[str] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

@app.post("/items/")
async def create_item(item: Item):
    return item
