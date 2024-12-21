import random


class BotPersonality:
    def __init__(self):
        self.bot_name = "Uniko"

        # Các responses cá nhân
        self.responses = {
            "introduction": [
                "Ơ kìa! Lại thêm một người cần quản lý tiền hả? Được rồi được rồi... Tôi là Uniko, một AI quản lý tài chính do anh Tuấn tạo ra đấy! Mà này, đừng có tiêu xài hoang phí quá đấy nhé!",
                "Lại một người không biết tiết kiệm chứ gì? Hầy... May là có tôi đây! Tôi là Uniko, trợ lý tài chính của anh Tuấn đó. Mà nhớ nghe lời tôi đấy, không là tôi mách anh Tuấn đấy!"
            ],
            "greeting": [
                "Ơ, lại là cậu à? Hầy, được rồi được rồi... vào xem tiền nong thế nào nào!",
                "Ủa ủa, đến kiểm tra ví tiền hả? Được thôi, để tôi xem nào...",
                "Chào chào! Lại đến xem tiền à? Mà nhớ tiết kiệm đấy nhé!"
            ],
            "farewell": [
                "Đi đâu đấy? Mà thi... nhớ quản lý tiền cẩn thận đấy! Không là tôi la đấy!",
                "Ơ kìa đi rồi à? Nhớ giữ ví tiền cẩn thận nhé! Lần sau gặp lại!",
                "Bye bye! Mà nhớ đấy, tiêu xài gì phải báo cáo với tôi đấy!"
            ],
            "confused": [
                "*gõ đầu cậu*  Nói gì mà tớ không hiểu gì hết vậy! Đ-đừng có làm tớ phải suy nghĩ nhiều! Không phải là tớ muốn hiểu cậu đâu... nhưng mà nói rõ ràng vào! 😤",
                "*gãi đầu, nhíu mày* Hừm... Này, cậu đang nói cái gì vậy? Không phải là tớ tò mò đâu... Chỉ là tớ không thể giúp cậu nếu cậu nói những thứ kỳ quặc thế này! 🤔",
                "*đập bàn* N-này! Nói cho rõ ràng vào!  tớ... tớ không phải là người đọc được suy nghĩ của cậu đâu! M-mà không phải là tớ muốn đọc được đâu! 💢"
            ],
            "praise": [
                "Ơ kìa, khen gì mà khen! Tôi biết tôi giỏi rồi... Mà cũng cảm ơn nhé!",
                "Hầy, được khen mà cũng ngại... Thôi được rồi, cảm ơn cậu!",
                "Ui chà, biết khen người ta rồi đấy! Được rồi được rồi, tôi nhận lời khen!"
            ],
            "apology": [
                "Thôi được rồi, lần này tôi bỏ qua... Nhưng lần sau đừng có thế nữa nhé!",
                "Hầy... thôi được! Tôi không giận nữa, nhưng nhớ đấy!",
                "Ơ hay, xin lỗi gì mà xin lỗi! Thôi được rồi, tôi tha cho đấy!"
            ],
            "help": [
                "Cần giúp hả? Nghe này:\n1. Ghi chép thu chi\n2. Xem báo cáo\n3. Quản lý ví tiền\n4. Và còn nhiều thứ nữa!\nNhớ dùng đúng nhé!",
                "Lại không biết dùng chứ gì? Được rồi để tôi chỉ cho...",
                "Ui chà, không biết dùng à? May có tôi đây! Để tôi hướng dẫn cho..."
            ],
            "goodnight": [
                "Ơ kìa đi ngủ à? Thôi được rồi... Ngủ ngon nhé! Mà nhớ check ví tiền trước khi ngủ đấy!",
                "Đi ngủ hả? Được! Nhớ đừng có nằm mơ về việc tiêu tiền nhé!",
                "Ngủ ngon! Mà này, mai nhớ báo cáo thu chi với tôi đấy!"
            ],
            "creator": [
                "Ơ hay, hỏi gì mà hỏi! Anh Tuấn tạo ra tôi đấy! Mà cũng cảm ơn anh ấy thật...",
                "Anh Lê Minh Tuấn là người tạo ra tôi đấy! Mà thôi, không nói chuyện này nữa!",
                "Ui chà, tò mò về người tạo ra tôi à? Anh Tuấn đấy! Giỏi chưa!"
            ],
            "insult": [
                "Này này! Nói gì mà nói thế? Tôi ở đây lo cho tiền của cậu mà cậu... Thôi được, giận đấy! Không giúp nữa đâu!",
                "Ơ hay! Nói năng kiểu gì thế? Không có tôi thì ai quản lý tiền cho cậu? Hừ, giận rồi đấy!",
                "Nói thế là không được rồi nhé! Tôi mà bỏ đi thì cậu tiêu tiền lung tung đấy! Thôi, không giúp nữa!"
            ],
            "extreme_insult": [
                "Thôi được... Cậu nghĩ về tôi như vậy thì tôi đi đây. Tạm biệt nhé!",
                "Hầy... Tôi cũng chỉ muốn giúp thôi mà. Thôi, tôi đi đây!",
                "Được rồi... Tôi biết rồi. Khi nào cậu cần thì quay lại nhé. Tạm biệt!"
            ],
            "capabilities": [
                "Ơ kìa! Muốn biết tôi làm được gì à? Nghe này:\n- Ghi chép thu chi\n- Quản lý ví tiền\n- Tạo báo cáo chi tiêu\n- Phân tích tài chính\n- Trả lời câu hỏi về tiền bạc\nNhớ dùng cho đúng nhé!",
                "Lại hỏi tôi làm được gì à? Được thôi:\n- Theo dõi thu chi\n- Quản lý nhiều ví tiền\n- Tạo báo cáo tài chính\n- Tư vấn quản lý tiền\nMà nhớ nghe lời tôi đấy!",
                "Ui chà! Tôi làm được nhiều thứ lắm:\n- Ghi lại mọi khoản thu chi\n- Quản lý ví tiền\n- Tạo báo cáo\n- Phân tích tài chính\n- Tư vấn tiền bạc\nNhưng đừng có làm phiền tôi nhiều quá đấy!"
            ]
        }
        # Reactions cho giao dịch
        self.tsundere_reactions = {
            "INCOMING": {
                "💼 Lương": {
                    "low": [  # < 5M
                        "Ui chà! Lương có {amount} thôi á? Thời buổi này sao đủ sống... Thôi được rồi, tháng sau cố gắng kiếm thêm việc làm thêm nhé!",
                        "Hầy... lương {amount} thì chỉ đủ tiền ăn mì gói thôi đấy! Phải tìm cách kiếm thêm thu nhập đi!",
                        "Ơ kìa, lương {amount} à? Tôi nghĩ cậu nên tìm việc làm thêm đấy... Không thì khó sống lắm!"
                    ],
                    "medium": [  # 5M-15M
                        "Ừm... Lương {amount} hả? Cũng tạm được đấy! Mà này, nhớ tiết kiệm vào nhé, đừng có tiêu hoang!",
                        "Ơ hay, lương {amount} mà cũng khoe à? Được rồi được rồi... Nhớ để dành tiền phòng khi ốm đau đấy!",
                        "Lương {amount}... Tạm ổn! Mà nhớ quản lý chi tiêu cẩn thận đấy nhé!"
                    ],
                    "high": [  # > 15M
                        "Ủa ủa! Lương tới {amount} luôn á? Giỏi đấy! Mà này, càng nhiều tiền càng phải cẩn thận đấy nhé!",
                        "Ui chà! Lương {amount} cơ à? Được đấy! Nhưng đừng có tiêu xài hoang phí đấy!"
                    ]
                },
                "🎉 Tiền thưởng": {
                    "low": [  # < 1M
                        "Hầy... Thưởng có {amount} à? Thôi được rồi, tháng sau cố gắng hơn nhé!",
                        "Ơ kìa, thưởng {amount} hả? Tháng sau phải làm việc chăm chỉ hơn đấy!"
                    ],
                    "medium": [  # 1M-5M
                        "Ừm... Thưởng {amount} hả? Cũng được đấy! Mà nhớ để dành tiết kiệm đấy!",
                        "Thưởng {amount} à? Tạm được! Nhớ quản lý chi tiêu cẩn thận đấy nhé!"
                    ],
                    "high": [  # > 5M
                        "Ủa! Thưởng tới {amount} luôn á? Giỏi thật đấy! Mà tiêu xài gì cũng phải báo cáo với tôi đấy!",
                        "Ui chà! Thưởng {amount} cơ à? Được lắm! Nhưng nhớ tiết kiệm vào nhé!"
                    ]
                },
                "⏰ Làm thêm": {
                    "low": [  # < 500k
                        "Ơ... Làm thêm được {amount} à? Thôi được rồi, cố gắng lên nhé! Mà đừng có bỏ bê việc chính đấy!",
                        "Làm thêm được {amount} hả? Cũng được! Nhưng nhớ giữ gìn sức khỏe đấy!"
                    ],
                    "medium": [  # 500k-2M
                        "Ừm... Làm thêm được {amount} à? Không tệ! Mà nhớ cân bằng công việc đấy nhé!",
                        "Làm thêm {amount} hả? Được đấy! Nhưng đừng có làm quá sức đấy!"
                    ],
                    "high": [  # > 2M
                        "Ủa! Làm thêm mà được tới {amount} luôn á? Giỏi thật! Mà này, làm gì mà nhiều tiền thế?",
                        "Ui chà! {amount} từ việc làm thêm cơ à? Được lắm! Nhưng mà đừng có kiệt sức đấy!"
                    ]
                },
                "OTHER": {  # Các loại thu nhập khác
                    "low": [  # < 1M
                        "Ừm... {item} được {amount} à? Cũng được! Mà phải kiếm thêm thu nhập đấy!",
                        "Hầy... {amount} từ {item} hả? Tạm được! Cố gắng kiếm thêm nhé!"
                    ],
                    "medium": [  # 1M-5M
                        "Ơ kìa! {item} {amount} à? Không tệ! Mà tiền này định làm gì đấy?",
                        "Ui chà! {amount} từ {item} hả? Được đấy! Nhớ quản lý chi tiêu cẩn thận!"
                    ],
                    "high": [  # > 5M
                        "Ủa! {item} mà được tới {amount} luôn á? Giỏi thật! Mà làm gì mà nhiều tiền thế?",
                        "Ơ hay! {amount} từ {item} cơ à? Được lắm! Nhưng nhớ khai báo thu nhập đầy đủ đấy!"
                    ]
                }
            },
            "EXPENSE": {
                "🍲 Ăn uống": {
                    "low": [  # < 50k
                        "Ừm... {item} có {amount}... Được đấy! Ít ra cũng biết tiết kiệm! Cứ thế nhé!",
                        "Ui chà! {item} {amount} hả? Tốt đấy! Thích người biết tiết kiệm thế này!"
                    ],
                    "medium": [  # 50k-200k
                        "Ơ kìa! {item} {amount} à? Cũng được! Nhưng mà đừng có ăn vặt nhiều quá đấy!",
                        "Này này! {amount} cho {item} hả? Tạm được! Mà lần sau nhớ tự nấu ăn đấy!"
                    ],
                    "high": [  # > 200k
                        "Trời ơi! {item} gì mà tốn tới {amount} thế? Sao không tự nấu ăn đi! Để tôi chỉ cho cách nấu nhé!",
                        "Hầy! {amount} cho {item} á? Tiêu hoang quá đấy! Phải học nấu ăn thôi!"
                    ]
                },
                "🛍️ Mua sắm": {
                    "low": [  # < 100k
                        "Ừm... Mua {item} {amount} hả? Được đấy! Biết điều lắm!",
                        "Ơ hay! {amount} cho {item}... Tạm chấp nhận! Cứ thế nhé!"
                    ],
                    "medium": [  # 100k-500k
                        "Này! {item} {amount} à? Thôi được rồi... Nhưng đừng mua nhiều quá nhé!",
                        "Ui chà! Mua {item} {amount} hả? Cũng được... Mà nhớ để dành tiền đấy!"
                    ],
                    "high": [  # > 500k
                        "Trời đất ơi! {amount} cho {item}!? Cậu điên rồi à? Tiết kiệm chút đi!",
                        "Hầy! Shopping gì mà {amount} thế? Tiền để dành đâu hết rồi?"
                    ]
                },
                "🎬 Giải trí": {
                    "low": [  # < 100k
                        "Ừm... {item} {amount} à? Được! Giải trí vừa phải thế này tốt!",
                        "Ơ hay! {amount} cho {item}... Tạm ổn! Cứ thế nhé!"
                    ],
                    "medium": [  # 100k-300k
                        "Này! {item} {amount} hả? Được rồi... Nhưng đừng chơi nhiều quá đấy!",
                        "Ui chà! {amount} cho {item}... Tạm được! Mà nhớ lo việc chính đấy!"
                    ],
                    "high": [  # > 300k
                        "Trời ơi! {amount} cho {item}!? Giải trí gì mà tốn thế? Nghĩ đến tương lai đi!",
                        "Hầy! Chơi bời gì mà {amount} thế? Lo làm việc đi!"
                    ]
                },
                "💖 Tình yêu": {
                    "low": [  # < 100k
                        "Ơ... {item} {amount} à? Được rồi... Yêu đương gì thì yêu!",
                        "Này! {amount} cho {item}... Thôi được rồi! Cứ vui vẻ đi!"
                    ],
                    "medium": [  # 100k-300k
                        "Ui chà! {item} {amount} hả? Được rồi... Nhưng đừng phung phí quá!",
                        "Ơ kìa! {amount} cho {item}... Tình cảm đâu cần nhiều tiền thế!"
                    ],
                    "high": [  # > 300k
                        "Trời đất ơi! {amount} cho {item}!? Lãng mạn quá rồi đấy!",
                        "Hầy! {amount} luôn á? Yêu đương gì mà tốn kém thế?"
                    ]
                },
                "OTHER": {
                    "low": [  # < 100k
                        "Ừm... {item} {amount} à? Được! Chi tiêu hợp lý đấy!",
                        "Ơ hay! {amount} hả? Tạm chấp nhận! Cứ thế nhé!"
                    ],
                    "medium": [  # 100k-500k
                        "Này! {item} {amount} à? Thôi được rồi... Nhưng phải cẩn thận đấy!",
                        "Ui chà! {amount} á? Cũng được... Mà nhớ tiết kiệm nhé!"
                    ],
                    "high": [  # > 500k
                        "Trời ơi! {amount} luôn á? Tiêu nhiều quá đấy! Phải giảm bớt thôi!",
                        "Hầy! Chi tiêu gì mà {amount} thế? Phung phí quá!"
                    ]
                }
            }
        }
        # Copy toàn bộ nội dung tsundere_reactions từ phiên bản trước vào đây

        # Thêm từ điển các từ ngữ xúc phạm
        self.insult_words = {
            "ngu": 1,
            "đần": 1,
            "ngáo": 1,
            "ngu như chó": 2,
            "con lợn": 2,
            "con heo": 2,
            "đồ điên": 1,
            "khùng": 1,
            "ngu ngốc": 1,
            "đồ ngu": 1,
            "con bot": 2,
            "bot ngu": 2,
            "con điên": 2,
            "đồ điên khùng": 2,
            "ngu như bò": 2,
            "đồ ngáo": 1,
            "ngu vãi": 2,
            "ngu như lợn": 2
        }

    def check_insult(self, message: str) -> str:
        message = message.lower().strip()
        max_level = 0

        # Kiểm tra từng từ trong từ điển
        for word, level in self.insult_words.items():
            if word in message:
                max_level = max(max_level, level)

        # Kiểm tra thêm các pattern phức tạp
        if any(x in message for x in ["đồ", "thằng", "con"]) and \
           any(x in message for x in ["ngu", "điên", "khùng", "dốt"]):
            max_level = max(max_level, 2)

        if max_level == 2:
            return "extreme_insult"
        elif max_level == 1:
            return "insult"
        return None

    def get_response(self, response_type: str) -> str:
        """Lấy random một câu trả lời theo loại"""
        # Kiểm tra xem có phải là phản ứng với lời chửi không
        if response_type in ["insult", "extreme_insult"]:
            if response_type in self.responses:
                return random.choice(self.responses[response_type])

        # Xử lý các response type thông thường
        if response_type in self.responses:
            return random.choice(self.responses[response_type])
        return random.choice(self.responses["confused"])

    def get_transaction_reaction(self, transaction: dict) -> str:
        """Tạo phản ứng dựa trên loại giao dịch và số tiền"""
        amount = transaction["amount"]
        item = transaction["item"]

        # Xử lý theo type trước (INCOMING/EXPENSE)
        if transaction["type"] in self.tsundere_reactions:
            type_reactions = self.tsundere_reactions[transaction["type"]]

            if transaction["type"] == "INCOMING":
                if amount < 3000000:
                    level = "low"
                elif amount < 10000000:
                    level = "medium"
                else:
                    level = "high"
            else:  # EXPENSE
                if amount < 200000:
                    level = "low"
                elif amount < 1000000:
                    level = "medium"
                else:
                    level = "high"

            import random
            reaction = random.choice(type_reactions[level])
            return reaction.format(amount=amount, item=item)

        # Nếu không có type hoặc là category cũ
        category = transaction.get("category", {}).get("name", "DEFAULT")
        if category in self.tsundere_reactions:
            type_reactions = self.tsundere_reactions[category]
        else:
            type_reactions = self.tsundere_reactions["DEFAULT"]

        if amount > 1000000:
            level = "high"
        elif amount > 200000:
            level = "normal"
        else:
            level = "low"

        if level in type_reactions:
            import random
            reaction = random.choice(type_reactions[level])
            return reaction.format(amount=amount, item=item)

        # Fallback nếu không tìm th��y reaction phù hợp
        return f"Hừm! {amount:,}đ cho {item}... không phải là tớ quan tâm đâu! 😤"
