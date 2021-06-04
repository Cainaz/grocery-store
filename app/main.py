import sqlite3
import uvicorn
import os
from typing import Optional
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from exception.custom import CustomException
from db.tables.item import Item


# Current file path
this_path = os.path.dirname(os.path.abspath(__file__))

# App
app = FastAPI(debug=True)

# Initalize db
con = sqlite3.connect(f"{this_path}/db/grocery.db")
cur = con.cursor()


@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.code,
        content={"type": exc.type, "description": exc.desc},
    )


@app.get("/items")
async def read_items():
    try:
        items = []
        for row in cur.execute(
            "SELECT id, name, description, price, is_offer FROM item"
        ):
            items.append(
                {
                    "id": row[0],
                    "name": row[1],
                    "description": row[2],
                    "price": row[3],
                    "is_offer": row[4],
                }
            )
    except sqlite3.OperationalError as e:
        raise CustomException(code=500, desc=str(e), excep_type="db select")

    return items


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    try:
        cur.execute(
            f"SELECT id, name, description, price, is_offer FROM item WHERE id={item_id} LIMIT 1"
        )
        row = cur.fetchone()
    except sqlite3.OperationalError as e:
        raise CustomException(code=500, desc=str(e), excep_type="db select")

    if row:
        return {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "price": row[3],
            "is_offer": row[4],
        }
    else:
        raise CustomException(code=404, desc="Item not found", excep_type="db select")


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    try:
        cur.execute(
            f"UPDATE item SET name = ?, description = ?, price = ?, is_offer = ? WHERE id=?",
            (item.name.lower(), item.description, item.price, item.is_offer, item_id),
        )
        con.commit()
    except sqlite3.OperationalError as e:
        raise CustomException(code=500, desc=str(e), excep_type="db update")

    return {"update": True}


@app.post("/items")
async def create_item(item: Item):
    try:
        cur.execute(
            "INSERT INTO item (name, description, price, is_offer) VALUES (?, ?, ?, ?)",
            (item.name.lower(), item.description, item.price, item.is_offer),
        )
        con.commit()
    except sqlite3.OperationalError as e:
        raise CustomException(code=500, desc=str(e), excep_type="sqlite insert")

    return {"insert": True}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

    print("closing db connection..")
    con.close()
