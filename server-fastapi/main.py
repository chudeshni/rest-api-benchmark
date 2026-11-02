from fastapi import FastAPI # type: ignore
from pydantic import BaseModel # type: ignore
app = FastAPI() # type: ignore

class Item(BaseModel): # type: ignore
    name: str
    value: int
@app.get("/api/small") # type: ignore
def get_small(): # type: ignore
    return {"message":"ok", "data":[1,2,3]} # type: ignore
@app.get("/api/large") # type: ignore
def get_large(): # type: ignore
    return{"items":[{"id":i,"name":f"item_{i}","value":i*10} for i in range(1000)]} # type: ignore
@app.post("/api/items") # type: ignore
def create_item(item:Item): # type: ignore
    return {"received": item.model_dump()} # type: ignore

