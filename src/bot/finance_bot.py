from datetime import datetime
import random
from typing import List, Dict, Optional

from utils.amount_parser import AmountParser
from src.utils.text_parser import TextParser
from bot.personality import BotPersonality
from utils.openai_handler import OpenAIHandler

class FinanceBot:
    def __init__(self, openai_api_key: str = None):
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

        self.openai_handler = OpenAIHandler(openai_api_key) if openai_api_key else None

    def set_wallets(self, wallets: list) -> None:
        """Cập nhật danh sách ví"""
        self.wallets = wallets
        # Đặt ví tiền mặt làm ví mặc định
        self.default_wallet = next(
            (w for w in wallets if w["type"] == "WALLET" and "tiền mặt" in w["name"].lower()),
            wallets[0] if wallets else None
        )

    def process_message(self, message: str) -> dict:
        """Xử lý tin nhắn từ người dùng"""
        try:
            message = message.lower().strip()
            
            # 0. Xử lý khi bị chửi
            insult_type = self.personality.check_insult(message)
            if insult_type:
                return {
                    "message": random.choice(self.personality.responses[insult_type]),
                    "result": ""
                }

            # 1. Xử lý các câu hỏi ngoài luồng
            off_topic_keywords = [
                "thời tiết", "chính trị", "thể thao", "bóng đá", 
                "âm nhạc", "phim ảnh", "game", "trò chơi",
                "tình yêu", "hẹn hò", "tâm sự", "du lịch",
                "ẩm thực", "nấu ăn", "công thức", "thời trang",
                "làm đẹp", "sức khỏe", "bệnh tật", "thuốc",
                "học tập", "thi cử", "trường học"
            ]
            
            if any(keyword in message for keyword in off_topic_keywords) or \
               any(q in message for q in ["tại sao", "thế nào", "là gì", "bao giờ", "khi nào"]):
                return {
                    "message": random.choice([
                        "*khoanh tay* ! tớ là trợ lý tài chính, không phải là Google đâu nhé! Hỏi mấy cái này làm gì chứ! 😤",
                        
                        "*thở dài* Này... tớ chỉ giỏi về quản lý tiền thôi... Đừng hỏi mấy thứ ngoài chuyên môn của tớ! M-mà không phải là tớ kém hiểu biết đâu... ! 💢",
                        
                        "*gõ gõ đầu cậu* Đồ ngốc! tớ là AI chuyên về tài chính, không phải là chatbot đa năng! Muốn biết mấy cái này thì đi hỏi Google ấy! 😠",
                        
                        "*liếc nhìn* Hừm... tớ chỉ giúp cậu quản lý tiền thôi... Mấy câu hỏi khác... t-tớ không muốn trả lời! Không phải là không biết đâu nhé! 🤨",
                        
                        "*đỏ mặt* ! Đừng hỏi những thứ ngoài chuyên môn của tớ! tớ... tớ chỉ quan tâm đến tiền của cậu thôi! À không, không phải là quan tâm... Mou! 😳"
                    ]),
                    "result": ""
                }

            # 1. Xử lý chào hỏi
            if any(word in message for word in ["chào", "hi", "hello", "xin chào"]):
                return {
                    "message": random.choice(self.personality.responses["greeting"]),
                    "result": ""
                }
            
            # 2. Xử lý chúc ngủ ngon
            if any(word in message for word in ["ngủ ngon", "oyasumi", "good night"]):
                return {
                    "message": random.choice(self.personality.responses["goodnight"]),
                    "result": ""
                }
            
            # 3. Xử lý hỏi về bot
            if any(phrase in message for phrase in ["cậu là ai", "cậu tên gì", "cậu là gì", "giới thiệu"]):
                return {
                    "message": random.choice(self.personality.responses["introduction"]),
                    "result": ""
                }
            
            # 4. Xử lý cảm ơn
            if any(word in message for word in ["cảm ơn", "thank", "thanks"]):
                return {
                    "message": random.choice(self.personality.responses["praise"]),
                    "result": ""
                }
            
            # 5. Xử lý yêu cầu trợ giúp
            if any(word in message for word in ["giúp", "help", "hướng dẫn", "cách dùng"]):
                return {
                    "message": random.choice(self.personality.responses["help"]),
                    "result": ""
                }
            
            # 6. Xử lý tạm biệt
            if any(word in message for word in ["tạm biệt", "bye", "goodbye", "sayonara"]):
                return {
                    "message": random.choice(self.personality.responses["farewell"]),
                    "result": ""
                }
            
            # 7. Xử lý thống kê/báo cáo
            if any(word in message for word in ["thống kê", "xem thống kê", "báo cáo", "phân tích"]):
                stats = self.get_statistics()
                return {
                    "message": random.choice(self.personality.responses["praise"]),
                    "result": stats
                }
            
            # 8. Xử lý giao dịch
            transactions = self.text_parser.parse_transactions(message, self.wallets)
            if transactions:
                response = []
                transaction_details = ""
                
                for trans in transactions:
                    wallet_name = trans["wallet"]["name"]
                    amount = f"{trans['amount']:,}đ".replace(",", ".")
                    item = trans["item"].title()
                    category = trans['category']['name']
                    trans_type = "Giao dịch đi" if trans["type"] == "EXPENSE" else "Giao dịch đến"
                    
                    # Thêm vào danh sách giao dịch
                    self.transactions.append(trans)
                    
                    # Tạo phản ứng tsundere dựa trên giao dịch
                    reaction = self.get_tsundere_reaction(trans)
                    
                    # Thêm vào response
                    response.append(f"{reaction}\n")
                    
                    # Format HTML với line breaks rõ ràng và kiểu dáng
                    transaction_details = f"""
                    <div style="">
                        <p style="margin: 5px 0;"><strong>📄 Tên giao dịch:</strong> <span style="font-weight: bold;">{item}</span></p>
                        <p style="margin: 5px 0;"><strong>💰 Số Tiền:</strong> <span style="font-weight: bold;">{amount}</span></p>
                        <p style="margin: 5px 0;"><strong>🏦 Ví:</strong> <span style="font-weight: bold;">{wallet_name}</span></p>
                        <p style="margin: 5px 0;"><strong>📊 Phân loại:</strong> <span style="font-weight: bold;">{category}</span></p>
                        <p style="margin: 5px 0;"><strong>🔄 Loại:</strong> <span style="font-weight: bold;">{trans_type}</span></p>
                    </div>
                    """
                
                return {
                    "message": ''.join(response),
                    "result": transaction_details,
                    "transactions": transactions
                }
            
            # 9. Xử lý hỏi về người tạo
            if any(phrase in message for phrase in [
                "ai tạo ra", "ai làm ra", "ai viết ra", "ai tạo", "ai phát triển",
                "do ai", "của ai", "ai là người tạo", "ai là người làm"
            ]):
                return {
                    "message": random.choice(self.personality.responses["creator"]),
                    "result": ""
                }
            
            # Xử lý hỏi về khả năng của bot
            if any(phrase in message for phrase in [
                "làm được gì",
                "có thể làm gì",
                "chức năng",
                "khả năng",
                "giúp được gì",
                "hướng dẫn",
                "help",
                "giúp đỡ"
            ]):
                return {
                    "message": random.choice(self.personality.responses["capabilities"]),
                    "result": ""
                }
            
            # Nếu không khớp với các trường hợp trên và có OpenAI handler
            if self.openai_handler:
                try:
                    import asyncio
                    # Tạo event loop mới nếu cần
                    try:
                        loop = asyncio.get_event_loop()
                    except RuntimeError:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                    
                    # Chạy coroutine và đợi kết quả
                    ai_response = loop.run_until_complete(
                        self.openai_handler.get_response(message)
                    )
                    
                    if ai_response:
                        return {
                            "message": ai_response,
                            "result": ""
                        }
                except Exception as e:
                    print(f"Error in OpenAI processing: {str(e)}")

            # Fallback nếu không có OpenAI hoặc có lỗi
            return {
                "message": random.choice(self.personality.responses["confused"]),
                "result": ""
            }
                
        except Exception as e:
            print(f"Error in process_message: {str(e)}")
            return {
                "message": "! Có gì đó không đúng rồi! 😤",
                "result": ""
            }

    def get_statistics(self) -> str:
        """Lấy thống kê chi tiêu"""
        if not self.transactions:
            return "Chưa có giao dịch nào ược ghi nhận..."
            
        total = sum(t['amount'] for t in self.transactions)
        items = [f"📝 {t['item']}: {t['amount']:,}đ" for t in self.transactions]
        
        return f"""📊 Thống kê chi tiêu của cậu:
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
        response = f"📊 {self.personality.bot_name} đã phân tích chi tiêu của cậu:\n\n"
        for cat_name, total in sorted_categories:
            response += f"{cat_name}: {total:,}đ\n"
        
        # Thêm nhận xét
        if sorted_categories:
            top_category = sorted_categories[0][0]
            response += f"\n💡 Nhận xét: cậu chi tiêu nhiều nhất cho {top_category}. "
            if len(sorted_categories) > 1:
                second_category = sorted_categories[1][0]
                response += f"Kế đến là {second_category}."
        
        return response

    def get_tsundere_reaction(self, transaction: dict) -> str:
        """Tạo phản ứng tsundere dựa trên loại giao dịch"""
        try:
            amount = transaction['amount']
            item = transaction['item']
            trans_type = transaction['type']  # INCOMING hoặc EXPENSE
            category = transaction['category']['name']  # Lấy tên category với emoji
            
            # Debug log
            print(f"Processing transaction:")
            print(f"- Type: {trans_type}")
            print(f"- Category: {category}")
            print(f"- Amount: {amount}")
            print(f"- Item: {item}")

            # Xác định level dựa vào amount và category
            if trans_type == "INCOMING":
                if category == "💼 Lương":
                    if amount < 5000000:
                        level = "low"
                    elif amount < 15000000:
                        level = "medium"
                    else:
                        level = "high"
                elif category == "🎉 Tiền thưởng":
                    if amount < 1000000:
                        level = "low"
                    elif amount < 5000000:
                        level = "medium"
                    else:
                        level = "high"
                elif category == "⏰ Làm thêm":
                    if amount < 500000:
                        level = "low"
                    elif amount < 2000000:
                        level = "medium"
                    else:
                        level = "high"
                else:  # OTHER
                    if amount < 1000000:
                        level = "low"
                    elif amount < 5000000:
                        level = "medium"
                    else:
                        level = "high"
            else:  # EXPENSE
                if category == "🍲 Ăn uống":
                    if amount < 50000:
                        level = "low"
                    elif amount < 200000:
                        level = "medium"
                    else:
                        level = "high"
                elif category == "🛍️ Mua sắm":
                    if amount < 100000:
                        level = "low"
                    elif amount < 500000:
                        level = "medium"
                    else:
                        level = "high"
                elif category == "🎬 Giải trí":
                    if amount < 100000:
                        level = "low"
                    elif amount < 300000:
                        level = "medium"
                    else:
                        level = "high"
                elif category == "💖 Tình yêu":
                    if amount < 100000:
                        level = "low"
                    elif amount < 300000:
                        level = "medium"
                    else:
                        level = "high"
                else:  # OTHER
                    if amount < 100000:
                        level = "low"
                    elif amount < 500000:
                        level = "medium"
                    else:
                        level = "high"

            print(f"- Determined level: {level}")

            # Lấy reactions cho category cụ thể hoặc fallback về OTHER
            reactions = self.personality.tsundere_reactions[trans_type].get(
                category,
                self.personality.tsundere_reactions[trans_type]["OTHER"]
            )
            
            # Chọn ngẫu nhiên một reaction và format
            reaction = random.choice(reactions[level])
            formatted_reaction = reaction.format(amount=f"{amount:,}đ", item=item)
            
            print(f"- Selected reaction: {formatted_reaction}")
            return formatted_reaction
            
        except Exception as e:
            print(f"Error in get_tsundere_reaction: {str(e)}")
            # Fallback về reaction mặc định nếu có lỗi
            default_reaction = "Hừm... {amount} cho {item}... T-tạm được! 💭"
            try:
                return default_reaction.format(amount=f"{amount:,}đ", item=item)
            except:
                return "! Có gì đó không đúng rồi! 😤"

    def remember_context(self, message: str, response: str) -> None:
        """Ghi nhớ ngữ cảnh cuộc trò chuyện"""
        self.conversation_history.append({
            "message": message,
            "response": response,
            "timestamp": datetime.now()
        })
        
        # H���c từ cuộc trò chuyện
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
                return f"Dựa vào cuộc trò chuyện trước, mình hiểu là cậu đang nói về {self.conversation_context['last_topic']}"

        # Xử lý dựa trên sở thích đã học được
        for pref in self.conversation_context["user_preferences"]:
            if pref in message:
                return f"Mình nhớ là cậu đã từng nói về việc này..."

        return None

