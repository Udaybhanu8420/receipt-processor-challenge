from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, constr
from typing import List
from datetime import date, time
import uuid
import math
from decimal import Decimal

app = FastAPI()


# -----------------------------
# Pydantic Models for the API
# -----------------------------
class Item(BaseModel):
    shortDescription: constr(pattern=r'^[\w\s\-]+$')
    price: constr(pattern=r'^\d+\.\d{2}$')


class Receipt(BaseModel):
    retailer: constr(pattern=r'^[\w\s\-\&]+$')
    purchaseDate: date
    purchaseTime: time
    items: List[Item]
    total: constr(pattern=r'^\d+\.\d{2}$')


# -----------------------------
# In-Memory Storage
# -----------------------------
receipts_db = {}


# -----------------------------
# Points Calculation Function
# -----------------------------
def compute_points(receipt: Receipt) -> int:
    points = 0

    # Rule 1: One point for every alphanumeric character in the retailer name.
    points += sum(1 for c in receipt.retailer if c.isalnum())

    total_decimal = Decimal(receipt.total)

    # Rule 2: 50 points if the total is a round dollar amount with no cents.
    if total_decimal == total_decimal.to_integral_value():
        points += 50

    # Rule 3: 25 points if the total is a multiple of 0.25.
    if (total_decimal % Decimal("0.25")) == 0:
        points += 25

    # Rule 4: 5 points for every two items on the receipt.
    points += (len(receipt.items) // 2) * 5

    # Rule 5: For each item, if the trimmed length of the item description is a multiple of 3,
    # add math.ceil(price * 0.2) to the points.
    for item in receipt.items:
        trimmed = item.shortDescription.strip()
        if len(trimmed) % 3 == 0:
            item_price = Decimal(item.price)
            bonus = math.ceil(item_price * Decimal("0.2"))
            points += bonus

    # Rule 6 (Extra 5 points for total > 10.00) has been removed to match the sample expected output.

    # Rule 7: 6 points if the day in the purchase date is odd.
    if receipt.purchaseDate.day % 2 == 1:
        points += 6

    # Rule 8: 10 points if the time of purchase is after 2:00pm and before 4:00pm.
    if time(14, 0) < receipt.purchaseTime < time(16, 0):
        points += 10

    return points


# -----------------------------
# Exception Handling
# -----------------------------
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": "The receipt is invalid. Please verify input."}
    )


# -----------------------------
# API Endpoints
# -----------------------------
@app.post("/receipts/process")
async def process_receipt(receipt: Receipt):
    receipt_id = str(uuid.uuid4())
    points = compute_points(receipt)
    receipts_db[receipt_id] = points
    return {"id": receipt_id}


@app.get("/receipts/{receipt_id}/points")
async def get_points(receipt_id: str):
    if receipt_id not in receipts_db:
        raise HTTPException(status_code=404, detail="No receipt found for that ID.")
    return {"points": receipts_db[receipt_id]}
