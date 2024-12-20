from datetime import datetime
import random
from typing import List, Dict, Optional

from src.models.wallet import Wallet
from src.utils.amount_parser import AmountParser
from src.utils.text_parser import TextParser
from src.bot.personality import BotPersonality

class FinanceBot:
    def __init__(self):
        self.transactions = []
        self.conversation_history = []
        self.personality = BotPersonality()
        self.wallets = []
        self.default_wallet = None
        self.text_parser = TextParser()
        self.amount_parser = AmountParser()
        
        # Khởi tạo context cho conversation
        self.conversation_context = {
            "last_topic": None,
            "user_preferences": {},
            "common_transactions": {}
        }

    def set_wallets(self, wallets: list) -> None:
        """Cập nhật danh sách ví"""
        self.wallets = wallets
        # Đặt ví tiền mặt làm ví mặc định
        self.default_wallet = next(
            (w for w in wallets if w["type"] == "WALLET" and "tiền mặt" in w["name"].lower()),
            wallets[0] if wallets else None
        )

    def process_message(self, message: str) -> str:
        """Xử lý tin nhắn từ người dùng"""
        try:
            message = message.lower().strip()
            
            # 1. Xử lý chào hỏi
            if any(word in message for word in ["chào", "hi", "hello", "xin chào"]):
                return random.choice(self.personality.responses["introduction"])
            
            # 2. Xử lý hỏi về bot
            if any(phrase in message for phrase in ["bạn là ai", "bạn tên gì", "bạn là gì", "giới thiệu"]):
                return random.choice(self.personality.responses["about_me"])
            
            # 3. Xử lý cảm ơn
            if any(word in message for word in ["cảm ơn", "thank", "thanks"]):
                return random.choice(self.personality.responses["user_thank"])
            
            # 4. Xử lý yêu cầu trợ giúp
            if any(word in message for word in ["giúp", "help", "hướng dẫn", "cách dùng"]):
                return random.choice(self.personality.responses["help"])
            
            # 5. Xử lý thống kê/báo cáo
            if any(word in message for word in ["thống kê", "xem thống kê", "báo cáo", "phân tích"]):
                reply = random.choice(self.personality.responses["expense_analysis"])
                stats = self.get_statistics()
                return f"{reply}\n\n{stats}"
            
            # 6. Xử lý giao dịch
            transactions = self.text_parser.parse_transactions(message, self.wallets)
            if transactions:
                response = []
                for trans in transactions:
                    wallet_name = trans["wallet"]["name"]
                    amount = trans["amount"]
                    item = trans["item"]
                    
                    # Thêm vào danh sách giao dịch
                    self.transactions.append(trans)
                    
                    # Tạo phản ứng tsundere dựa trên giao dịch
                    reaction = self.get_tsundere_reaction(trans)
                    
                    # Thêm vào response
                    response.append(f"- {item}: {amount:,}đ từ {wallet_name}")
                
                return f"{reaction}\n" + "\n".join(response)
            
            # 7. Nếu không khớp với các trường hợp trên
            return random.choice(self.personality.responses["error"])
                
        except Exception as e:
            print(f"Error in process_message: {e}")
            return random.choice(self.personality.responses["error"])

    def get_statistics(self) -> str:
        """Lấy thống kê chi tiêu"""
        if not self.transactions:
            return "Chưa có giao dịch nào ��ược ghi nhận..."
            
        total = sum(t['amount'] for t in self.transactions)
        items = [f"📝 {t['item']}: {t['amount']:,}đ" for t in self.transactions]
        
        return f"""📊 Thống kê chi tiêu của bạn:
{chr(10).join(items)}
------------------------
💰 Tổng cộng: {total:,}đ"""

    def analyze_spending_trends(self) -> str:
        """Phân tích xu hướng chi tiêu"""
        if not self.transactions:
            return "Mình chưa có đủ dữ liệu để phân tích. Hãy ghi nhận thêm các khoản chi tiêu nhé!"

        # Phân tích theo category
        category_totals = {}
        for trans in self.transactions:
            cat_name = trans['category']['name']
            category_totals[cat_name] = category_totals.get(cat_name, 0) + trans['amount']

        sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
        
        # Tạo phân tích được cá nhân hóa
        response = f"📊 {self.personality.bot_name} đã phân tích chi tiêu của bạn:\n\n"
        for cat_name, total in sorted_categories:
            response += f"{cat_name}: {total:,}đ\n"
        
        # Thêm nhận xét
        if sorted_categories:
            top_category = sorted_categories[0][0]
            response += f"\n💡 Nhận xét: Bạn chi tiêu nhiều nhất cho {top_category}. "
            if len(sorted_categories) > 1:
                second_category = sorted_categories[1][0]
                response += f"Kế đến là {second_category}."
        
        return response

    def get_tsundere_reaction(self, transaction: dict) -> str:
        """Tạo phản ứng tsundere dựa trên giao dịch"""
        category = transaction['category']['name']
        amount = transaction['amount']
        item = transaction['item']
        
        # Lấy reactions cho category
        reactions = self.personality.tsundere_reactions.get(
            category, 
            self.personality.tsundere_reactions['DEFAULT']
        )
        
        # Xác định mức độ chi tiêu
        if category == "🍲 Ăn uống":
            level = "high" if amount > 100000 else "low" if amount < 50000 else "normal"
        elif category == "🎬 Giải trí":
            level = "high" if amount > 200000 else "normal"
        elif category == "🛍️ Mua sắm":
            level = "high" if amount > 500000 else "normal"
        elif category == "💖 Tình yêu":
            level = "high" if amount > 300000 else "normal"
        else:
            level = "high" if amount > 200000 else "normal"
        
        # Format reaction với thông tin chi tiêu
        reaction = random.choice(reactions[level])
        return reaction.format(amount=f"{amount:,}đ", item=item)

    def remember_context(self, message: str, response: str) -> None:
        """Ghi nhớ ngữ cảnh cuộc trò chuyện"""
        self.conversation_history.append({
            "message": message,
            "response": response,
            "timestamp": datetime.now()
        })
        
        # Học từ cuộc trò chuyện
        self.learn_from_conversation(message)

    def learn_from_conversation(self, message: str) -> None:
        """Học từ nội dung cuộc trò chuyện"""
        # Học về thói quen chi tiêu
        if "thường" in message or "hay" in message:
            words = message.lower().split()
            for i, word in enumerate(words):
                if word in ["thường", "hay"]:
                    if i + 1 < len(words):
                        self.conversation_context["common_transactions"][words[i+1]] = True

        # Học về sở thích
        if "thích" in message or "ghét" in message:
            self.conversation_context["user_preferences"][message] = True

    def get_personalized_response(self, message: str) -> Optional[str]:
        """Tạo câu trả lời dựa trên ngữ cảnh và tính cách"""
        message = message.lower()

        # Xử lý dựa trên ngữ cảnh trước đó
        if self.conversation_context["last_topic"]:
            if "như vậy" in message or "thế" in message:
                return f"Dựa vào cuộc trò chuyện trước, mình hiểu là bạn đang nói về {self.conversation_context['last_topic']}"

        # Xử lý dựa trên sở thích đã học được
        for pref in self.conversation_context["user_preferences"]:
            if pref in message:
                return f"Mình nhớ là bạn đã từng nói về việc này..."

        return None

    # ... các method khác
