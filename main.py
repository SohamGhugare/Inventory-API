from fastapi import FastAPI, Query, Path, HTTPException
import json
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

with open('inventory.json', 'r') as f:
    inventory = json.load(f)

def updateJson(data):
    with open('inventory.json', 'w') as f:
        json.dump(data, f)

class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None

class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None

@app.get('/')
def home():
    return {"Endpoints":[
        {"get-item":"Get item info by id or name."}, 
        {"create-item": "Create an item."}, 
        {"update-item": "Update an item."}, 
        {"delete-item": "Delete an item"}]}

# Get item
@app.get('/get-item')
def get_item(item_id: Optional[int] = None, name: Optional[str] = None):

    if item_id is None and name is None:
        raise HTTPException(status_code=400, detail="Please provide any 1 argument.")

    if str(item_id) in inventory:
        return inventory[str(item_id)]

    elif item_id is None and name is not None:
        for item_id in inventory:
            if inventory[item_id]["name"] == name:
                return inventory[str(item_id)]
            else:
                raise HTTPException(status_code=404, detail="Item not found.")

    elif str(item_id) not in inventory:
        raise HTTPException(status_code=404, detail="Item ID does not exist.")

# Create item
@app.post("/create-item")
def create_item(item_id: int, item: Item):
    if str(item_id) in inventory:
        raise HTTPException(status_code=400, detail="Item ID already exists.")

    inventory[item_id] = item.dict()
    updateJson(inventory)
    return inventory[item_id]

# Update item
@app.put("/update-item")
def update_item(item_id: int, item: UpdateItem):
    item = item.dict()

    if str(item_id) not in inventory:
        raise HTTPException(status_code=404, detail="Item ID does not exist.")

    if item["name"] != None:
        inventory[str(item_id)]["name"] = item["name"]
        
    if item["price"] != None:
        inventory[str(item_id)]["price"] = item["price"]

    if item["brand"] != None:
        inventory[str(item_id)]["brand"] = item["brand"]

    updateJson(inventory)
    return inventory[str(item_id)]

# Delete item
@app.delete("/delete-item")
def delete_item(item_id:int):
    if str(item_id) not in inventory:
        raise HTTPException(status_code=404, detail="Item ID does not exist.")

    del inventory[str(item_id)]
    updateJson(inventory)
    raise HTTPException(status_code=200, detail="Item deleted")
    
