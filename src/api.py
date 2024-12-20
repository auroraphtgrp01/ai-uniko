import sys
from pathlib import Path
root_path = str(Path(__file__).parent.parent)
if root_path not in sys.path:
    sys.path.append(root_path)

from utils.response_formatter import ResponseFormatter
from src.bot.finance_bot import FinanceBot
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, Generator
import uvicorn
import os
import asyncio
import json

# Thêm thư mục gốc vào PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


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
    """Stream response với messages gốc và recent dạng markdown"""
    try:
        # Kiểm tra nếu response là dict
        if isinstance(response, dict):
            messages = response["message"]  # Lấy phần message từ dict
            result = response["result"]    # Lấy phần result từ dict
            transactions = response.get("transactions", [])  # Lấy transactions nếu có
        else:
            messages = response
            result = ""
            transactions = []

        # Lấy các giao dịch mới từ bot
        latest_transactions = []
        if bot.transactions:
            # Lấy giao dịch mới nhất được thêm vào từ tin nhắn này
            new_transactions = bot.transactions[-1:]  # Lấy giao dịch cuối cùng
            
            # Format lại các giao dịch
            latest_transactions = [{
                "name": trans["item"],
                "amount": trans["amount"],
                "wallet": trans["wallet"]["name"],
                "category": trans["category"]["name"],
                "type": "Giao dịch đi" if trans["type"] == "EXPENSE" else "Giao dịch đến"
            } for trans in new_transactions]

        # Gửi chunk cuối cùng ngay lập tức với đầy đủ thông tin
        final_chunk = {
            "type": "message",
            "messages": messages,      # Message gốc hoàn chỉnh
            "recent": result,         # Sử dụng result làm recent
            "done": True,
            "transactions": transactions,  # Thêm các giao dịch mới
            "statistics": response.get("statistics", {}) if isinstance(response, dict) else {}
        }
        yield f"data: {json.dumps(final_chunk, ensure_ascii=False)}\n\n"

    except Exception as e:
        print(f"Error in stream_response: {e}")
        error_chunk = {
            "type": "error",
            "message": str(e),
            "done": True
        }
        yield f"data: {json.dumps(error_chunk, ensure_ascii=False)}\n\n"


@app.post("/chat")
async def chat(message: Message):
    """Chat endpoint với response format markdown đẹp"""
    try:
        # Xử lý tin nhắn
        response = bot.process_message(message.content)

        # Lấy transactions gần đây
        recent_transactions = bot.transactions[-5:] if bot.transactions else []

        # Tính toán statistics
        stats = {
            "total_expense": sum(t["amount"] for t in bot.transactions if t["type"] == "EXPENSE"),
            "total_income": sum(t["amount"] for t in bot.transactions if t["type"] == "INCOMING"),
            "transaction_count": len(bot.transactions),
            "categories": {}
        }

        # Tính toán theo category
        for trans in bot.transactions:
            cat_name = trans["category"]["name"]
            if cat_name not in stats["categories"]:
                stats["categories"][cat_name] = 0
            stats["categories"][cat_name] += trans["amount"]

        return ResponseFormatter.create_full_response(response, recent_transactions, stats)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat/stream")
async def chat_stream(message: Message):
    """Stream chat response với SSE (Server-Sent Events)"""
    try:
        # Xử lý tin nhắn
        response = bot.process_message(message.content)

        # Trả về response dạng stream
        return StreamingResponse(
            stream_response(response),
            media_type="text/event-stream",
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'X-Accel-Buffering': 'no'
            }
        )

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
