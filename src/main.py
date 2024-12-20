import sys
import os

# Thêm thư mục gốc vào PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.bot.finance_bot import FinanceBot

def main():
    bot = FinanceBot()
    # Khởi tạo ví mặc định
    bot.set_wallets([{
        "id": "default",
        "name": "Ví tiền mặt",
        "type": "WALLET",
        "currency": "VND",
        "currentAmount": 0
    }])
    
    while True:
        user_input = input("Bạn: ")
        if user_input.lower() == "quit":
            break
            
        response = bot.process_message(user_input)
        print(f"Bot: {response}")

if __name__ == "__main__":
    main()
