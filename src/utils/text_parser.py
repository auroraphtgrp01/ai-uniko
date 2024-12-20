from typing import Dict, List
import re
from src.models.wallet import Wallet
from src.utils.amount_parser import AmountParser

class TextParser:
    def __init__(self):
        self.amount_parser = AmountParser()
        self.category_keywords = {
            "4287f00a-9f2c-4ec9-bfac-9310a5430b13": {  # Ăn uống
                "keywords": ["ăn", "cơm", "bữa", "trưa", "tối", "sáng", "phở", "bún", "cháo", "đồ ăn", "cơm văn phòng", "quán ăn"],
                "name": "🍲 Ăn uống",
                "type": "EXPENSE"
            },
            "0b8f45d7-53f3-4404-ace0-23935b502e32": {  # Giải trí
                "keywords": ["ăn vặt", "nem chua", "trà sữa", "cafe", "xem phim", "karaoke", "du lịch", "giải trí", "game", "netflix", "spotify"],
                "name": "🎬 Giải trí",
                "type": "EXPENSE"
            },
            "36f9961f-2be4-4c01-bdd5-26f1873fde89": {  # Mua sắm
                "keywords": ["mua", "quần áo", "giày", "túi", "đồ", "shopping", "thời trang", "phụ kiện"],
                "name": "🛍️ Mua sắm",
                "type": "EXPENSE"
            },
            "8835247e-28b7-4668-a2b6-2ddb29ba35f4": {  # Xăng xe
                "keywords": ["xăng", "đổ xăng", "dầu", "nhiên liệu"],
                "name": "⛽ Xăng xe",
                "type": "EXPENSE"
            },
            "1eead838-d02f-4d2e-b5b1-ba98f10eb9b6": {  # Tiền điện
                "keywords": ["điện", "tiền điện", "hóa đơn điện", "điện lực"],
                "name": "💡 Tiền điện",
                "type": "EXPENSE"
            },
            "4ad0cb83-54fb-4cbf-b7ee-4689b1128a60": {  # Thuê trọ
                "keywords": ["thuê", "trọ", "nhà trọ", "phòng", "tiền nhà", "tiền trọ", "tiền thuê nhà"],
                "name": "🏠 Thuê trọ",
                "type": "EXPENSE"
            },
            "26fe0933-4ded-4674-99a7-8b0eb8950763": {  # Điện thoại, internet
                "keywords": ["điện thoại", "internet", "wifi", "4g", "5g", "data", "cước"],
                "name": "📱 Điện thoại, internet",
                "type": "EXPENSE"
            },
            "a02de534-75ef-4198-86ea-ec3875dc16cb": {  # Sức khỏe
                "keywords": ["thuốc", "bệnh viện", "khám", "bác sĩ", "y tế", "sức khỏe", "bảo hiểm"],
                "name": "💊 Sức khỏe",
                "type": "EXPENSE"
            },
            "960a249d-0c94-4f67-a814-348e77fa40e8": {  # Tiền nước
                "keywords": ["nước", "tiền nước", "hóa đơn nước"],
                "name": "🚰 Tiền nước",
                "type": "EXPENSE"
            },
            "61ad994c-9b06-4abb-b26a-f3e138c1c68b": {  # Giáo dục
                "keywords": ["học", "sách", "khóa học", "học phí", "giáo dục", "đào tạo", "thi"],
                "name": "📚 Giáo dục",
                "type": "EXPENSE"
            },
            "0d39a602-78c4-43b9-b3a1-99349d4b849b": {  # Tình yêu
                "keywords": ["quà", "hẹn hò", "valentine", "sinh nhật", "kỷ niệm", "người yêu"],
                "name": "💖 Tình yêu",
                "type": "EXPENSE"
            },
            "db2dedb1-1d5c-4c8a-83ba-62d77e3f334f": {  # Đi lại
                "keywords": ["taxi", "grab", "xe bus", "xe buýt", "tàu", "vé", "gửi xe", "đi lại"],
                "name": "🚕 Đi lại",
                "type": "EXPENSE"
            },
            # Thu nhập
            "cc13076d-54d2-43d6-a924-2b69ca0e7642": {  # Tiền thưởng
                "keywords": ["thưởng", "bonus", "thưởng tết", "thưởng dự án"],
                "name": "💵 Tiền thưởng",
                "type": "INCOMING"
            },
            "739366b8-0f04-4de7-910a-8b72e163c785": {  # Phụ cấp công việc
                "keywords": ["phụ cấp", "trợ cấp", "phụ cấp ăn trưa", "phụ cấp đi lại"],
                "name": "🏢 Phụ cấp công việc",
                "type": "INCOMING"
            },
            "c0e527cc-0387-433e-ba0e-64b6a44f774a": {  # Lương
                "keywords": ["lương", "salary", "tiền lương", "lương tháng"],
                "name": "💼 Lương",
                "type": "INCOMING"
            },
            "1bbb0811-8a9d-4d55-b4dc-7cd7432dfdf4": {  # Phụ cấp gia đình
                "keywords": ["tiền mừng", "lì xì", "trợ cấp", "tiền gia đình"],
                "name": "👪 Phụ cấp gia đình",
                "type": "INCOMING"
            },
            "6b31159b-333f-4942-9e61-06689304440c": {  # Bán tài sản
                "keywords": ["bán", "thanh lý", "bán đồ", "bán xe"],
                "name": "🏠 Bán tài sản",
                "type": "INCOMING"
            },
            "14cd8426-26ca-4700-bb80-9bbeaa74f480": {  # Làm thêm
                "keywords": ["làm thêm", "part time", "freelance", "ngoài giờ"],
                "name": "⏰ Làm thêm",
                "type": "INCOMING"
            }
        }

    def parse_transactions(self, text: str, wallets: List[Dict]) -> List[Dict]:
        """Phân tích thông minh n giao dịch từ văn bản"""
        text = text.lower()
        results = []
        
        # Tách các giao dịch bằng từ khóa liên kết
        transactions = re.split(r'\s*(?:rồi|sau đó|tiếp theo|và|với|cùng với|,)\s*', text)
        
        for transaction in transactions:
            if not transaction.strip():
                continue
            
            # Tìm số tiền và đơn vị trong văn bản
            amount_pattern = r'(\d+|một|hai|ba|bốn|năm|sáu|bảy|tám|chín|mười)\s*(xị|củ|k|nghìn|ngàn|triệu|tỷ|đồng|vnd)?'
            amount_matches = list(re.finditer(amount_pattern, transaction))
            
            if amount_matches:
                # Lấy match cuối cùng làm số tiền
                amount_match = amount_matches[-1]
                amount_str = transaction[amount_match.start():amount_match.end()]
                
                # Tách mô tả (phần trước số tiền)
                description = transaction[:amount_match.start()].strip()
                
                # Tách phần ví (phần sau số tiền)
                wallet_str = transaction[amount_match.end():].strip()
                
                # Xử lý số tiền bằng AmountParser
                amount = self.amount_parser.normalize_amount(amount_str)
                
                # Xác định ví
                wallet = None
                if wallet_str:
                    wallet = Wallet.find_wallet_by_text(wallets, wallet_str)
                if not wallet and wallets:
                    wallet = next((w for w in wallets if w["type"] == "WALLET" and "tiền mặt" in w["name"].lower()), wallets[0])
                
                # Làm sạch mô tả
                description = description.strip()
                money_keywords = ['đồng', 'vnd', 'nghìn', 'ngàn', 'k', 'hết', 'mất', 'tốn', 'chi', 'xị', 'củ']
                for keyword in money_keywords:
                    description = description.replace(keyword, '')
                
                # Xác định loại giao dịch
                transaction_type = "EXPENSE"
                income_keywords = ['nhận', 'lương', 'thưởng', 'được', 'cho', 'tặng', 'trợ cấp', 'hoàn tiền']
                if any(keyword in description for keyword in income_keywords):
                    transaction_type = "INCOMING"
                
                # Tìm category
                best_category = self.categorize_transaction(description)
                
                # Làm sạch mô tả cuối cùng
                description = ' '.join(description.split())
                
                # Thêm vào kết quả nếu hợp lệ
                if description and amount > 0 and wallet:
                    result = {
                        "item": description.strip(),
                        "amount": int(amount),
                        "category": best_category,
                        "type": transaction_type,
                        "wallet": wallet
                    }
                    results.append(result)
                
        return results

    def categorize_transaction(self, description: str) -> dict:
        """Phân loại giao dịch dựa trên mô tả"""
        description = description.lower()
        
        # Tìm category phù hợp nhất dựa trên từ khóa
        best_match = None
        max_matches = 0
        
        for category_id, category in self.category_keywords.items():
            matches = 0
            for keyword in category["keywords"]:
                if keyword in description:
                    matches += 1
            
            if matches > max_matches:
                max_matches = matches
                best_match = {
                    "id": category_id,
                    "name": category["name"],
                    "type": category["type"]
                }
        
        # Nếu không tìm thấy category phù hợp, trả về mặc định
        if not best_match:
            return {
                "id": "4287f00a-9f2c-4ec9-bfac-9310a5430b13",  # ID của category Ăn uống
                "name": "🍲 Ăn uống",
                "type": "EXPENSE"
            }
        
        return best_match
