import os
from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import JSONResponse
from deta import Deta

myProjectKey = os.getenv("DETA_PROJECT_KEY")
deta = Deta(myProjectKey) # configure your Deta project
todos = deta.Base('todos')  # access your DB

class Todo(BaseModel):
    title: str
    priority: int
    description: str

class TodoUpdate(BaseModel):
    priority: int = None
    description: str = None
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Buz"}]

@app.get("/")
async def root():
    return {"message": "Hello world!"}

@app.post("/todos", status_code=201)
def create_todo(todo: Todo):
    item = todos.put(todo.dict())
    return item

@app.get("/todos")
def list_todos():
    res = todos.fetch()
    return res.items

@app.get("/todos/{uid}")
def get_todo(uid: str):
    item = todos.get(uid)
    if item:
        return item
    return JSONResponse({ "message": "item not found" }, status_code=404)

@app.patch("todos/{uid}")
def update_todo(uid: str, uu: TodoUpdate):
    updates = {k:v for k,v in uu.dict().items() if v is not None}
    try:
        todos.update(updates, uid)
        return todos.get(uid)
    except Exception:
        return JSONResponse({"message": "item not found"}, status_code=404)

@app.delete("/todos/{uid}")
def delete_todo(uid: str):
    todos.delete(uid)
    return

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

@app.get("/fake/items/bool/{item_id}")
async def read_fake_item_bool(item_id: str, q: Optional[str] = None, short: bool = False):
    item =  {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

@app.get("/fake/items/required/{item_id}")
async def read_fake_item_required(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

@app.post("/items/")
async def create_item(item: Item):
    return item
