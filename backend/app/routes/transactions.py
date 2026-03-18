from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.database import transactions_collection
from app.utils import decode_token
from bson import ObjectId

router = APIRouter()

security = HTTPBearer()


# ➕ ADD
@router.post("/add")
def add_transaction(
    data: dict,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    payload = decode_token(token)

    data["user"] = payload["email"]
    transactions_collection.insert_one(data)

    return {"message": "Transaction added"}


# 📥 GET ALL
@router.get("/")
def get_transactions(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    payload = decode_token(token)

    transactions = list(transactions_collection.find({"user": payload["email"]}))

    for t in transactions:
        t["_id"] = str(t["_id"])

    return transactions


# 🗑 DELETE
@router.delete("/{id}")
def delete_transaction(
    id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    decode_token(token)

    transactions_collection.delete_one({"_id": ObjectId(id)})

    return {"message": "Deleted"}


# ✏️ UPDATE
@router.put("/{id}")
def update_transaction(
    id: str,
    data: dict,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    decode_token(token)

    transactions_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": data}
    )

    return {"message": "Updated"}


# 📊 SUMMARY
@router.get("/summary")
def summary(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    payload = decode_token(token)

    transactions = list(transactions_collection.find({"user": payload["email"]}))

    income = sum(t["amount"] for t in transactions if t["type"] == "income")
    expense = sum(t["amount"] for t in transactions if t["type"] == "expense")

    return {
        "income": income,
        "expense": expense,
        "balance": income - expense
    }