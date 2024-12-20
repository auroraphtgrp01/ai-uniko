from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, Generator
import uvicorn
import sys
import os
import asyncio
import json

# Thêm thư mục gốc vào PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.finance_bot import FinanceBot

app = FastAPI(
    title="Uniko Finance Bot API",
    description="API for Uniko Finance Bot",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Khởi tạo bot
bot = FinanceBot()
bot.set_wallets([{
    "id": "default",
    "name": "Ví tiền mặt",
    "type": "WALLET",
    "currency": "VND",
    "currentAmount": 0
}])

class Message(BaseModel):
    content: str
    user_id: Optional[str] = None

async def stream_response(response: str) -> Generator:
    """Stream response character by character with random delays"""
    for char in response:
        # Tạo JSON chunk
        chunk = {
            "type": "message",
            "content": char,
            "done": False
        }
        yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"
        # Thêm delay ngẫu nhiên để giống chat
        await asyncio.sleep(0.02)
    
    # Gửi transactions và statistics sau khi message hoàn thành
    final_chunk = {
        "type": "message",
        "content": "",
        "done": True,
        "transactions": bot.transactions[-5:] if bot.transactions else [],
        "statistics": {
            "total_expense": sum(t["amount"] for t in bot.transactions if t["type"] == "EXPENSE"),
            "total_income": sum(t["amount"] for t in bot.transactions if t["type"] == "INCOMING"),
            "transaction_count": len(bot.transactions)
        }
    }
    yield f"data: {json.dumps(final_chunk, ensure_ascii=False)}\n\n"

@app.post("/chat/stream")
async def chat_stream(message: Message):
    """Stream chat response"""
    try:
        # Xử lý tin nhắn
        response = bot.process_message(message.content)
        
        return StreamingResponse(
            stream_response(response),
            media_type="text/event-stream"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(message: Message):
    try:
        response = bot.process_message(message.content)
        recent_transactions = bot.transactions[-5:] if bot.transactions else []
        
        return {
            "message": response,
            "transactions": recent_transactions,
            "statistics": {
                "total_expense": sum(t["amount"] for t in bot.transactions if t["type"] == "EXPENSE"),
                "total_income": sum(t["amount"] for t in bot.transactions if t["type"] == "INCOMING"),
                "transaction_count": len(bot.transactions)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/transactions")
async def get_transactions():
    """Lấy danh sách giao dịch"""
    return bot.transactions

@app.get("/statistics")
async def get_statistics():
    """Lấy thống kê chi tiêu"""
    if not bot.transactions:
        return {
            "message": "Chưa có giao dịch nào được ghi nhận",
            "statistics": None
        }
    
    stats = {
        "total_expense": sum(t["amount"] for t in bot.transactions if t["type"] == "EXPENSE"),
        "total_income": sum(t["amount"] for t in bot.transactions if t["type"] == "INCOMING"),
        "transaction_count": len(bot.transactions),
        "categories": {}
    }
    
    # Thống kê theo category
    for trans in bot.transactions:
        cat_name = trans["category"]["name"]
        if cat_name not in stats["categories"]:
            stats["categories"][cat_name] = 0
        stats["categories"][cat_name] += trans["amount"]
    
    return {
        "message": "Thống kê chi tiêu",
        "statistics": stats
    }

@app.delete("/reset")
async def reset_bot():
    """Reset bot về trạng thái ban đầu"""
    bot.transactions = []
    return {"message": "Đã reset bot thành công"}

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True) 