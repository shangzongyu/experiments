from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
import logging

app = FastAPI(
    title="Simple Inventory API", description="A simple CRUD API with in-memory storage"
)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 定义数据模型
class Item(BaseModel):
    name: str = Field(
        ..., min_length=1, max_length=100, description="The name of the item"
    )
    description: Optional[str] = Field(
        None, max_length=500, description="A brief description of the item"
    )
    price: float = Field(..., gt=0, description="The price of the item in USD")
    quantity: int = Field(0, ge=0, description="The quantity of the item in stock")


# 内存中的“数据库”
items: Dict[int, Item] = {}


# 创建物品
@app.post("/items/", response_model=dict)
async def create_item(item: Item):
    item_id = len(items) + 1
    items[item_id] = item
    logger.info(f"Created item with ID {item_id}: {item}")
    return {"item_id": item_id, "item": item}


# 读取单个物品
@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    if item_id not in items:
        logger.warning(f"Item with ID {item_id} not found")
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]


# 获取物品列表（支持分页）
@app.get("/items/", response_model=List[Item])
async def list_items(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(
        10, ge=1, le=100, description="Maximum number of items to return"
    ),
):
    item_list = list(items.values())[skip : skip + limit]
    logger.info(f"Listed items: skip={skip}, limit={limit}, returned={len(item_list)}")
    return item_list


# 更新物品
@app.put("/items/{item_id}", response_model=dict)
async def update_item(item_id: int, item: Item):
    if item_id not in items:
        logger.warning(f"Item with ID {item_id} not found for update")
        raise HTTPException(status_code=404, detail="Item not found")
    items[item_id] = item
    logger.info(f"Updated item with ID {item_id}: {item}")
    return {"item_id": item_id, "item": item}


# 删除物品
@app.delete("/items/{item_id}", response_model=dict)
async def delete_item(item_id: int):
    if item_id not in items:
        logger.warning(f"Item with ID {item_id} not found for deletion")
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_id]
    logger.info(f"Deleted item with ID {item_id}")
    return {"message": "Item deleted"}


# 启动应用
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
