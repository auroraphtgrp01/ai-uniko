import re
from typing import Dict, Union
from difflib import get_close_matches
from datetime import datetime
import random

class FinanceBot:
    def __init__    (self):
        # Simulate database
        self.transactions = []
        self.conversation_history = []  # Lưu lịch sử trò chuyện
        self.bot_name = "Uniko"
        self.bot_personality = {
            "introduction": [
                "H-hừm! tớ là Uniko đây. Không phải là tớ muốn giúp cậu quản lý tiền đâu, nhưng đó là nhiệm vụ Lê Minh Tuấn giao cho tớ... Đ-đừng có nghĩ là tớ sẽ thân thiện nhé! 😤",
                "Lại một người cần giúp đỡ nữa hả? *khoanh tay* Được thôi... tớ là Uniko. tớ s-sẽ giúp cậu quản lý tài chính, nhưng đừng có mà làm phiền tớ nhiều đấy! 哼",
                "Chào... *liếc nhìn* Uniko đây. tớ không phải là đang mong chờ được giúp cậu quản lý tiền đâu! B-baka! Nhưng nếu cậu thực sự cần thì... 😳",
                "*đang ngồi đếm tiền* Ơ kìa! Ai cho phép cậu làm phiền tớ thế hả? Hừm... đã vậy thì tớ sẽ giúp quản lý tiền cho... N-nhưng không phải vì tớ tốt bụng đâu! 💢",
                "*thở dài* Lại thêm một người vô tổ chức với tiền bạc... Được rồi! tớ là Uniko, và tớ... ừm... sẽ giúp cậu! Nhưng đừng hiểu lầm gì nhé! 😤"
            ],
            "about_me": [
                "Hừm! tớ là Uniko, được tạo bởi Lê Minh Tuấn... Không phải là tớ đặc biệt giỏi về quản lý tài chính đâu, nhưng tớ có thể giúp cậu phân loại chi tiêu và phân tích các khoản tiền... nếu cậu muốn... 💭",
                "B-cậu thực sự muốn biết về tớ sao? Được thôi... tớ là AI do Lê Minh Tuấn tạo ra. tớ có thể làm nhiều thứ lắm, nhưng đừng nghĩ là tớ sẽ luôn giúp cậu nhé! 😤",
                "*đỏ mặt* Sao cậu lại muốn biết về tớ chứ? B-baka! tớ chỉ là một AI giúp quản lý tiền thôi... Không có gì đặc biệt đâu! 🙈",
                "Ơ... *lúng túng* tớ á? Chỉ là... một AI thôi mà! Được Lê Minh Tuấn tạo ra để giúp mọi người quản lý tiền... Mà này, đừng có hỏi nhiều quá! 💢",
                "*xoay người* Hừm! tớ là Uniko đấy! Giỏi lắm, rất giỏi luôn! N-nhưng không phải là tớ đang khoe khoang đâu... 😳"
            ],
            "expense_recorded": [
                "Hừm! Đ-được rồi, tớ đã ghi lại cho cậu... Không phải là tớ quan tâm đâu nhé!",
                "B-cậu tiêu tiền nhiều quá đấy... Nhưng mà tớ đã ghi chép lại rồi... 😳",
                "Được rồi, tớ ghi lại rồi đấy! Đừng có mà tiêu hoang quá đấy nhé... N-không phải là tớ lo cho cậu đâu! 💢",
                "*lật sổ ghi chép* Mou... lại tiêu tiền nữa rồi! T-tớ sẽ ghi lại, nhưng lần sau phải tiết kiệm hơn đấy! 🙈",
                "*cẩn thận ghi chép* Hừm... được rồi! tớ đã ghi lại... MÀ NÀY! Đừng nghĩ là tớ sẽ luôn chu đáo thế này nhé! 😤"
            ],
            "expense_analysis": [
                "Ừm... Nhìn các khoản chi tiêu của cậu... (không phải là tớ để ý đâu nhé!)",
                "H-hừm! cậu muốn xem phân tích sao? Được thôi... tớ cũng đã sẵn sàng rồi...",
                "Đ-được rồi! tớ sẽ phân tích cho cậu... Nhưng đừng nghĩ là tớ làm vì cậu nhé! 😤",
                "*đeo kính* N-này! tớ s phân tích cẩn thận... Không phải vì tớ muốn giúp, mà vì đó là nhiệm vụ của tớ! 💭",
                "*lật giở sổ sách* B-BAKA! Sao cậu lại chi tiêu kiểu này chứ! Để tớ phân tích cho... 🤔"
            ],
            "high_spending": [
                "B-baka! cậu tiêu nhiều tiền quá đấy! Không phải là tớ quan tâm đâu, nhưng mà...",
                "Hừm... cậu nên cẩn thận hơn với việc tiêu tiền đấy... N-không phải là tớ lo lắng gì đâu!",
                "*giật mình* EHHH!? Sao cậu tiêu nhiều tiền thế này!? T-thật là... làm tớ phải lo lắng... À! Không phải lo lắng đâu! 😳",
                "*véo má* Này này! Chi tiêu kiểu gì thế hả!? tớ... tớ không thể để cậu phung phí như vậy được! 💢",
                "*thở dài* Mou... cậu này! Tiêu tiền như nước vậy... N-không phải là tớ quan tâm đến ví tiền của cậu đâu! 😤"
            ],
            "saving_advice": [
                "*khoanh tay* Hừm! N-nếu cậu muốn tiết kiệm thì... có thể mang cơm đi làm... C-chỉ là góp ý thôi! 🍱",
                "B-BAKA! Sao không tự nấu ăn đi! Tiết kiệm được nhiều tiền... M-mà không phải là tớ quan tâm đâu! 💭",
                "*lẩm bẩm* Này... cậu có thể dùng app giảm giá... N-không phải là tớ đang cố giúp cậu tiết kiệm đâu! 😳",
                "Hừm... *đảo mắt* Đi xe buýt cũng tốt mà! Tiết kiệm được tiền xăng... MÀ! tớ chỉ nói vậy thôi nhé! 🚌",
                "*vừa tính toán vừa nói* M-mua đồ nên đợi dịp giảm giá... Không phải là tớ để ý cậu chi tiêu thế nào đâu! 🛍️"
            ],
            "monthly_summary": [
                "*lật sổ* B-cậu muốn xem tổng kết tháng à? Hừm... để tớ xem nào... 📊",
                "Đ-được rồi! tớ sẽ tổng kết cho cậu... Nhưng đừng có mà sốc khi thấy số tiền đấy! 💸",
                "*đeo kính* Này! tớ đã tổng hợp chi tiêu... N-không phải là tớ làm việc chăm chỉ vì cậu đâu! 📝",
                "Hừm... *gõ máy tính* Để tớ tính toán... MÀ NÀY! Đừng có nhìn tớ thế chứ! 🔢",
                "*xem xét cẩn thận* M-mou... cậu thực sự muốn biết tổng chi tiêu sao? Đ-được thôi... 💭"
            ],
            "positive_trend": [
                "*ngạc nhiên* Ơ... cậu ��ã tiết kiệm được nhiều hơn tháng trước... N-không phải là tớ đang khen đâu! 📈",
                "Hừm! *đỏ mặt* Dạo này cậu chi tiêu có ý thức hơn rồi đấy... B-BAKA! Đừng có tự mãn! 💖",
                "*vỗ tay nhẹ* M-mà... tháng này cậu làm tốt lắm... À! Không phải là tớ ấn tượng đâu! 👏",
                "Này này! *liếc nhìn* T-tớ thấy cậu đã tiến bộ... Nhưng đừng có được nước lên thuyền nhé! 😤",
                "*lẩm bẩm* Ừm... không tệ... MÀ! Đừng có cười toe toét thế! tớ chỉ nói sự thật thôi! 🌟"
            ],
            "help": [
                "B-cậu không biết dùng tớ sao? Thật là... Được rồi, tớ sẽ chỉ cho, nhưng chỉ lần này thôi đấy!\n- Ghi chép chi tiêu: Chỉ cần nói bình thường thôi... VD: 'ăn sáng hết 50k'\n- Xem thống kê: Gõ 'xem thống kê' hoặc 'phân tích'\n- Không phải là tớ muốn giúp đâu... Nhưng cậu có thể hỏi bất cứ lúc nào... 😤",
                "*thở dài* Thật là phiền phức... Nhưng được rồi!\n- Muốn ghi chép à? Cứ nói bình thường như 'mua trà sữa 35k' là được\n- Xem chi tiêu thì gõ 'thống kê' hoặc 'phân tích'\n- Hừm! Đ-đừng nghĩ là tớ sẽ luôn giúp đỡ thế này nhé! 💭",
                "*đảo mắt* Mou... cậu không biết gì thật sao?\n- Ghi tiền: VD 'ăn trưa 65k', 'mua sách 200k'\n- Xem báo cáo: Gõ 'thống kê' hoặc 'phân tích'\n- B-BAKA! Nhớ cho kỹ vào nhé! tớ không muốn phải nói lại đâu! 😳",
                "*vừa ghi chép vừa nói* Nghe này...\n- Ghi tiền kiểu 'cafe 45k', 'mua quần áo 500k'\n- Xem chi tiêu thì gõ 'thống kê'\n- Còn gì không hiểu thì... thì cứ hỏi... N-không phải là tớ muốn giúp đâu! 🙈",
                "Hừm! *chống nạnh* Được rồi, nghe đây:\n- Muốn ghi tiền thì nói kiểu 'tiêu 100k'\n- Xem báo cáo thì gõ 'thống kê'\n- Nhớ chưa? Đừng có hỏi lại nữa đấy! MÀ NÀY! Không phải là tớ khó chịu khi cậu hỏi đâu... 💢"
            ],
            "creator_info": [
                "Hừm... Lê Minh Tuấn là người tạo ra tớ đấy. K-không phải là tớ đặc biệt biết ơn hay gì đâu... 😳",
                "B-cậu muốn biết về người tạo ra tớ sao? Là Lê Minh Tuấn... Người đã khiến tớ phải giúp đỡ mọi người quản lý tiền... Không phải là tớ thích công việc này đâu! �����",
                "*đỏ mặt* Lê Minh Tun h... m... Người đó... đã tạo ra tớ... MÀ NÀY! Sao cậu lại hỏi chuyện đó chứ! 🙈",
                "*lẩm bẩm* Người tạo ra tớ á... *ngập ngừng* Là Lê Minh Tuấn... N-không phải là tớ đang nghĩ về anh ấy đâu! BAKA! 💭",
                "Hừm! *khoanh tay* Lê Minh Tuấn... là người đã tạo ra tớ. Anh ấy... cũng không tệ lắm... MÀ! Đừng nói với anh ấy là tớ nói thế đấy! 😤"
            ],
            "error": [
                "B-BAKA! tớ không hiểu cậu đang nói gì... *giậm chân* Nói cho rõ vào! tớ không có cả ngày để đoán ý cậu đâu! 💢",
                "Hừm... *véo má* cậu nói kiểu gì vậy hả? tớ... tớ không hiểu gì hết! Giải thích cho đàng hoàng không tớ bỏ đi đấy! 😤",
                "Này này! *chống nạnh* cậu đang cố tình làm khó tớ đúng không!? Nói lại cho rõ ràng vào! Đ-đừng có mà lộn xộn! 💭",
                "*xoắn tóc* Mou... cậu đang nói gì vậy? tớ là thiên tài đấy, nhưng không phải kiểu thiên tài có thể đọc được suy nghĩ của cậu! 😳",
                "*lắc đầu* Đ-đừng có nói những thứ kỳ quặc th chứ! tớ... tớ không hiểu đâu! Nói lại đi, nhưng lần này phải rõ ràng hơn đấy! 🤔"
            ],
            "user_happy": [
                "*đỏ mặt* B-cậu vui vẻ quá nhỉ... N-không phải là tớ thích nhìn nụ cười của cậu đâu! BAKA! 🌟",
                "Hừm! *liếc nhìn* Trông cậu vui ghê ha... M-mà tớ không quan tâm đâu! Chỉ là... trông dễ chịu hơn mọi khi thôi... 😳",
                "*lén cười* Ừm... vui là tốt rồi... À! Đừng hiểu lầm! tớ chỉ không muốn nhìn cậu buồn thôi! 💭",
                "Này này! Sao hôm nay vui thế? *cố tỏ ra khó chịu nhưng không nhịn được cười* N-không phải là tớ muốn biết đâu! 🙈",
                "*khoanh tay* Hừm... vui vẻ quá cũng không tốt đâu! Mà... nụ cười của cậu... cũng không tệ... 💖"
            ],
            "user_sad": [
                "*lúng túng* Đ-đừng buồn nữa! Không phải là tớ lo cho cậu đâu... chỉ là nhìn khó chịu lắm! 😤",
                "B-baka! Sao lại buồn chứ... *lén đưa khăn giấy* tớ... tớ chỉ không muốn thấy cậu khóc thôi! 🥺",
                "*vỗ đầu nhẹ* Này... đừng có mà buồn nữa! T-tớ sẽ giúp cậu quản lý tiền tốt hơn... MÀ! Không phải vì tớ quan tâm đâu! 💝",
                "Hừm... *đưa kẹo* Ă-ăn đi! Đường sẽ giúp cậu vui lên... N-nhưng đừng nghĩ là tớ đặc biệt mua cho cậu nhé! 🍬",
                "*lẩm bẩm* tớ... tớ không thích nhìn cậu buồn đâu... BAKA! Đừng có hiểu lầm! Chỉ là... trông phiền quá! 😳"
            ],
            "user_love": [
                "*mặt đỏ bừng* B-B-BAKA! Đừng có nói mấy lời kỳ cục vậy chứ! Ai... ai mà thích cậu chứ! 😳",
                "*quay mặt đi* Hừm! Đừng có nói là... là yêu tớ! T-tớ không có thích nghe đâu... mà cũng không ghét... 💘",
                "EHHH!? *hoảng loạn* Sao cậu lại... N-này! Đừng có nói mấy câu đáng xấu hổ thế chứ! 🙈",
                "*đập bàn* B-baka baka baka! Ai cho phép cậu... nói những lời đó chứ! T-tớ... tớ không có vui đâu! 💢",
                "*ôm mặt* Mou... sao cậu lại... Đ-đừng có làm tim tớ đập nhanh thế chứ! BAKA! 💓"
            ],
            "user_compliment": [
                "*xoắn tóc* N-này! Đừng có khen tớ! tớ... tớ biết mình giỏi rồi! Nhưng... c-cảm ơn... 😳",
                "B-BAKA! tớ đâu cần cậu khen... *đỏ mặt* Mà... cậu thực sự nghĩ vậy sao? 💭",
                "*lúng túng* Hừm! Đương nhiên là tớ giỏi rồi! N-không phải là tớ vui vì được cậu khen đâu! 🌟",
                "Này này! *véo má* Đừng có nịnh tớ! Mà... nếu cậu muốn khen thêm thì... tớ cũng không cấm... 😤",
                "*quay mặt đi* M-mou... tớ biết mình xuất sắc mà! Nhưng... nghe cậu nói vậy... cũng không tệ... 💝"
            ],
            "user_thank": [
                "*đỏ mặt* B-baka! Không cần cảm ơn đâu! tớ... tớ chỉ làm nhiệm vụ thôi! 😳",
                "Hừm! *khoanh tay* Đương nhiên phải cảm ơn tớ chứ! N-nhưng mà... không phải là tớ cần đâu! 💭",
                "*lúng túng* Mou... Đừng có nói cảm ơn hoài vậy! Làm tớ... tớ ngại đấy! BAKA! 🙈",
                "Này! *chống nạnh* tớ đâu có giúp cậu vì muốn nghe cảm ơn đâu! Mà... nói thêm lần nữa cũng được... 😤",
                "*xoay người* N-không có gì đâu... tớ... tớ cũng vui khi giúp được cậu... À! Quên lời tớ vừa nói đi! 💖"
            ],
            "user_goodnight": [
                "*đỏ mặt* B-baka! Ai thèm chúc cậu ngủ ngon chứ! Nhưng... mà... ngủ ngon nhé... 🌙",
                "Hừm! *liếc nhìn* Muốn đi ngủ à? Ừ thì... ngủ đi! Đừng có thức khuya nữa đấy! 😤",
                "*ngáp* Mou... Cũng đến giờ rồi ha... N-không phải là tớ muốn ngủ cùng giờ với cậu đâu! 💤",
                "Này! *vỗ đầu nhẹ* Ngủ sớm vào! Mai còn phải... tiết kiệm tiền nữa! BAKA! 🌟",
                "*lẩm bẩm* Ngủ ngon... mà đừng có mơ thấy tớ đấy nhé! N-không phải là tớ quan tâm đâu! 💝"
            ],
            "user_goodmorning": [
                "*ngái ngủ* B-baka! Ai bảo cậu chào tớ sớm thế! Mà... chào buổi sáng... 🌅",
                "Hừm! Dậy sớm thế? *xoa mắt* N-không phải là tớ chờ cậu chào đâu! 😳",
                "*uống trà* Ừm... Chào buổi sáng... À! Đừng nghĩ là tớ vui vì được cậu chào nhé! 💭",
                "Này này! *tỉnh táo hẳn* Nhớ ăn sáng đầy đủ đấy! Không phải là tớ lo cho cậu đâu... BAKA! 🍳",
                "*đỏ mặt* M-mou... Chào buổi sáng! Hôm nay... trông cậu cũng tạm đợc đủ y... 🌟"
            ]
        }
        
        # Định nghĩa đầy đủ các category với từ khóa
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
            "26fe0933-4ded-4674-99a7-8b0eb8950763": {  # Đi���n thoại, internet
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

        # Thêm context learning nâng cao
        self.context_memory = []
        self.learning_threshold = 0.6
        self.conversation_context = {
            "last_topic": None,
            "user_preferences": {},
            "common_transactions": {}
        }

        self.tsundere_reactions = {
            "🍲 Ăn uống": {
                "high": [  # > 100k
                    "B-baka! Ăn gì mà tốn {amount} thế? Để dành tiền đi chứ! Không phải là tớ lo cho ví tiền của cậu đâu... 😤",
                    "Trời ơi, {item} gì mà đt dữ vậy? Sao không tự nấu ăn đi! Tiết kiệm được nhiều tiền... mà tớ nói vậy không phải vì quan tâm đâu nhé! 💢",
                    "Hừm... {amount} cho {item}? cậu nên cân nhắc mang cơm đi làm đấy... N-không phải tớ muốn cậu tiết kiệm tiền đâu! 😳"
                ],
                "normal": [  # 50k-100k
                    "Ăn {item} có {amount}... C-cũng được... Nhưng đừng ăn vặt nhiều quá đấy! ",
                    "Hừm! {item} à? tớ thấy... cũng ổn... Không phải là tớ đồng ý với khoản chi này đâu! 😤"
                ],
                "low": [  # < 50k
                    "Ít ra thì {item} cũng không đắt quá... N-nhưng mà vẫn phải tiết kiệm đấy! 💭",
                    "Ừm... {amount} cho {item} thì cũng được... Mà cậu vẫn nên tự nấu ăn! Không phải là tớ quan tâm gì đâu... 😳"
                ]
            },
            "🎬 Giải trí": {
                "high": [  # > 200k
                    "B-baka! Chi {amount} cho {item}? cậu giàu lắm hay sao? Tuần sau ăn mì gói đi nhé! 💢",
                    "Trời ơi! Giải trí gì mà tốn {amount} vậy? �� nhà coi Netflix tiết kiệm hơn nhiều... M-mà tớ ch�� góp  thôi! 😤"
                ],
                "normal": [
                    "Hừm... {item} à? Thôi được rồi... Nhưng đừng đi chơi nhiều quá đấy! Không phải là tớ lo đâu... 😳",
                    "T-tớ thấy {amount} cho {item} thì... cũng được... Nhưng tháng sau đừng có tiêu hoang nữa! "
                ]
            },
            "🛍️ Mua sắm": {
                "high": [  # > 500k
                    "BAKA! Mua sắm gì mà {amount} vậy!? cậu định sống bằng gì tháng sau!? K-không phải là tớ quan tâm... 😤",
                    "Trời ơi là trời! {amount} cho {item}!? cậu định phá sản hay gì!? Đ-đừng có phung phí thế chứ! 💢",
                    "Hừm... Lại mua sắm nữa à? {amount} luôn!? T-thật là... cậu nên nghĩ đến tương lai đi! 😳"
                ],
                "normal": [
                    "Mua {item} {amount} à... C-cũng được... Nhưng đừng mua nhiều quá đấy! ",
                    "Hừm! Shopping à? T-tớ cho qua lần này... Nhng tháng sau tiết kiệm đấy! 💭"
                ]
            },
            "💖 Tình yêu": {
                "high": [  # > 300k
                    "B-baka! Chi {amount} cho người yêu!? Kh��ng phải là tớ ghen... nhưng mà phung phí quá đấy! 😳",
                    "Ơ... {amount} cho {item}!? L-lãng mạn gì quá vậy... Không phải là tớ muốn được như thế đâu! 💢"
                ],
                "normal": [
                    "Hừm... {item} cho người yêu à? C-cũng được... Không phải là tớ thấy ngọt ngào gì đâu! ����",
                    "À... {amount} cho {item}... T-tình yêu gì mà tốn kém quá vậy! "
                ]
            },
            "DEFAULT": {
                "high": [  # > 200k
                    "B-baka! Chi {amount} cho {item}!? cậu giàu lắm sao? 😤",
                    "Trời ơi... {amount} luôn á? T-thật là phung phí! 💢",
                    "Hừm! {item} gì mà tốn {amount} vậy? Không phải là tớ khó chịu... nhưng mà cậu nên tiết kiệm đi! 😳"
                ],
                "normal": [
                    "Ừm... {amount} cho {item}... C-cũng được... ",
                    "Hừm! tớ sẽ ghi lại... Nhưng đừng tiêu hoang quá đấy! 💭"
                ]
            }
        }

        # Thêm thuộc tính wallets
        self.wallets = [
            {
                "id": "f2f2542d-9f9b-41e2-b719-7151367fe542",
                "name": "Ví Momo",
                "type": "WALLET",
                "initAmount": 1,
                "accountBankId": None,
                "currency": "VND",
                "currentAmount": 1,
                "userId": "e022461a-fc14-49c9-87aa-614a8eeb927e",
                "fundId": "b3846d43-6e22-444e-88cc-0d251a351e8d",
                "participantId": None,
                "accountBank": None
            },
            {
                "id": "04b48a00-8d13-42bf-86cc-e2c29ea861f0",
                "name": "Ví tiền mặt",
                "type": "WALLET",
                "initAmount": 1,
                "accountBankId": None,
                "currency": "VND",
                "currentAmount": 1,
                "userId": "e022461a-fc14-49c9-87aa-614a8eeb927e",
                "fundId": "b3846d43-6e22-444e-88cc-0d251a351e8d",
                "participantId": None,
                "accountBank": None
            },
            {
                "id": "870b72bf-b9b0-4156-9b71-79504b7af227",
                "name": "MB BANK",
                "type": "BANKING",
                "initAmount": 1,
                "accountBankId": "c243573e-31c3-4f0d-806c-bfe583587756",
                "currency": "VND",
                "currentAmount": -118999,
                "userId": "e022461a-fc14-49c9-87aa-614a8eeb927e",
                "fundId": "b3846d43-6e22-444e-88cc-0d251a351e8d",
                "participantId": None,
                "accountBank": {
                    "id": "c243573e-31c3-4f0d-806c-bfe583587756",
                    "type": "MB_BANK",
                    "login_id": "0899846214",
                    "sessionId": None,
                    "deviceId": None,
                    "userId": "e022461a-fc14-49c9-87aa-614a8eeb927e"
                }
            }
        ]
        
        # Đặt ví tiền mặt làm ví mặc định
        self.default_wallet = next(
            (w for w in self.wallets if w["type"] == "WALLET" and "tiền mặt" in w["name"].lower()),
            self.wallets[0] if self.wallets else None
        )

    def set_wallets(self, wallets: list):
        """Cập nhật danh sách ví"""
        self.wallets = wallets
        # Đặt ví tiền mặt làm ví mặc định
        self.default_wallet = next(
            (w for w in wallets if w["type"] == "WALLET" and "tiền mặt" in w["name"].lower()),
            wallets[0] if wallets else None
        )

    def find_wallet(self, text: str) -> dict:
        """Tìm ví dựa trên text"""
        text = text.lower()
        
        # Mapping các từ khóa phổ biến với tên ví
        wallet_keywords = {
            'momo': 'Ví Momo',
            'tiền mặt': 'Ví tiền mặt',
            'mb': 'MB BANK',
            'mbbank': 'MB BANK',
            'mb bank': 'MB BANK'
        }
        
        # Kiểm tra từng từ khóa
        for keyword, wallet_name in wallet_keywords.items():
            if keyword in text:
                return next((w for w in self.wallets if w["name"] == wallet_name), None)
        
        # Tìm trực tiếp theo tên ví
        for wallet in self.wallets:
            if wallet["name"].lower() in text:
                return wallet
                
        # Trả về ví mặc định nếu không tìm thấy
        return self.default_wallet

    def parse_expense(self, text: str) -> list:
        """Phân tích thông minh n giao dịch từ văn bản"""
        text = text.lower()
        results = []
        
        # Tách các giao dịch bằng từ khóa liên kết
        transactions = re.split(r'\s*(?:rồi|sau đó|tiếp theo|và|với|cùng với|,)\s*', text)
        
        # Pattern mới để bắt: [mô tả] [số tiền] [ví]
        pattern = r'(.*?)\s+(\d+(?:k|nghìn|ngàn|triệu|củ|xị|tỷ|đồng|vnd)?)\s*(?:ví|từ|trong|tài khoản)?\s*(.*?)$'
        
        for transaction in transactions:
            if not transaction.strip():
                continue
            
            match = re.match(pattern, transaction.strip())
            if match:
                description, amount_str, wallet_str = match.groups()
                
                # Xử lý số tiền
                amount = self.normalize_amount(amount_str)
                
                # Xác định ví
                wallet = None
                if wallet_str:
                    wallet = self.find_wallet(wallet_str)
                if not wallet:
                    wallet = self.default_wallet
                
                # Làm sạch mô tả
                description = description.strip()
                money_keywords = ['đồng', 'vnd', 'nghìn', 'ngàn', 'k', 'hết', 'mất', 'tốn', 'chi']
                for keyword in money_keywords:
                    description = description.replace(keyword, '')
                
                # Xác định loại giao dịch
                transaction_type = "EXPENSE"
                income_keywords = ['nh���n', 'lương', 'thưởng', 'được', 'cho', 'tặng', 'trợ cấp', 'hoàn tiền']
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

    def normalize_amount(self, amount_str: str) -> float:
        """Chuyển đổi các cách nói số tiền sang số"""
        amount_str = amount_str.lower().strip()
        
        try:
            # Dictionary chuyển số chữ sang số
            num_words = {
                'không': 0, 'một': 1, 'hai': 2, 'ba': 3, 'bốn': 4, 'năm': 5,
                'sáu': 6, 'bảy': 7, 'tám': 8, 'chín': 9, 'mười': 10,
                'mươi': 10, 'trăm': 100, 'lăm': 5,
                'chục': 10, 'tá': 12
            }

            # Dictionary ánh xạ đơn vị sang giá trị
            amount_mapping = {
                'củ': 1000000,  # 1 củ = 1 triệu
                'triệu': 1000000,
                'chai': 1000000,  # 1 chai = 1 triệu
                'tỉ': 1000000000,
                'tỷ': 1000000000,
                'k': 1000,
                'nghìn': 1000,
                'ngàn': 1000,
                'đồng': 1,
                'vnd': 1,
                'd': 1,
                'xị': 100000  # Thêm xị vào mapping
            }

            # Kiểm tra các đơn vị đặc biệt trước
            for unit, multiplier in amount_mapping.items():
                if unit in amount_str:
                    # Tách phần số phía trước đơn vị
                    number_part = amount_str.split(unit)[0].strip()
                    
                    # Nếu là số
                    if number_part.isdigit():
                        return float(number_part) * multiplier
                        
                    # Nếu là chữ số
                    for word, value in num_words.items():
                        if word in number_part:
                            return float(value) * multiplier
                            
                    # Nếu không có số phía trước, mặc định là 1
                    if not number_part:
                        return float(1) * multiplier

            # Xử lý trường hợp chỉ có số
            if amount_str.isdigit():
                return float(amount_str)

            return 0

        except Exception as e:
            print(f"Lỗi xử lý số tiền: {e}")
            return 0

    def process_message(self, message: str) -> str:
        """Xử lý tin nhắn từ người dùng"""
        try:
            message = message.lower().strip()
            
            # Parse giao dịch từ tin nhắn TRƯỚC
            transactions = self.parse_expense(message)
            if transactions:
                # Có giao dịch hợp lệ
                response = []
                for trans in transactions:
                    wallet_name = trans["wallet"]["name"]
                    amount = trans["amount"]
                    item = trans["item"]
                    
                    # Thêm vào danh sách giao dịch
                    self.transactions.append(trans)
                    
                    # Thêm vào response
                    response.append(f"- {item}: {amount:,}đ từ {wallet_name}")
                
                # Chọn ngẫu nhiên một câu trả lời từ expense_recorded
                reply = random.choice(self.bot_personality["expense_recorded"])
                return f"{reply}\n" + "\n".join(response)

            # Nếu không phải giao dịch, kiểm tra các loại tin nhắn khác
            # Kiểm tra lời chào
            greetings = ["hi", "hello", "chào", "xin chào", "hey"]
            if (any(f" {greeting} " in f" {message} " for greeting in greetings) 
                or message in greetings):
                return random.choice(self.bot_personality["introduction"])
            
            # Kiểm tra các lệnh đặc biệt trước
            if message in ["thống kê", "xem thống kê", "báo cáo", "phân tích"]:
                reply = random.choice(self.bot_personality["expense_analysis"])
                stats = self.get_statistics()
                return f"{reply}\n\n{stats}"
            
            # Kiểm tra các từ khóa về thông tin bot
            if any(q in message for q in ["cậu là ai", "cậu tên gì", "cậu là gì"]):
                return random.choice(self.bot_personality["about_me"])
            
            # Kiểm tra hỏi về người tạo
            if any(q in message for q in ["ai tạo", "người tạo", "tạo ra cậu"]):
                return random.choice(self.bot_personality["creator_info"])
            
            # Kiểm tra cần help
            if any(q in message for q in ["giúp đỡ", "hướng dẫn", "help", "không biết dùng"]):
                return random.choice(self.bot_personality["help"])
            
            # Kiểm tra lời cảm ơn
            if any(q in message for q in ["cảm ơn", "thank", "thanks"]):
                return random.choice(self.bot_personality["user_thank"])
            
            # Kiểm tra chào buổi sáng
            if any(q in message for q in ["chào buổi sáng", "morning", "sáng"]):
                return random.choice(self.bot_personality["user_goodmorning"])
            
            # Kiểm tra chào tạm biệt/chúc ngủ ngon
            if any(q in message for q in ["tạm biệt", "bye", "ngủ ngon", "good night"]):
                return random.choice(self.bot_personality["user_goodnight"])

            # Nếu không match với bất kỳ pattern nào, trả về câu trả lời error
            return random.choice(self.bot_personality["error"])
            
        except Exception as e:
            print(f"Error: {e}")
            return random.choice(self.bot_personality["error"])

    def get_statistics(self) -> str:
        if not self.transactions:
            return self.get_random_response('no_data')
            
        total = sum(t['amount'] for t in self.transactions)
        items = [f"📝 {t['item']}: {t['amount']:,}đ" for t in self.transactions]
        
        return f"""📊 Thống kê chi tiêu của cậu:
{chr(10).join(items)}
------------------------
💰 Tổng cộng: {total:,}đ"""

    def analyze_spending_trends(self) -> str:
        """Phân tích xu hướng chi tiêu với góc nhìn cá nhân hóa"""
        if not self.transactions:
            return "Mình chưa có đủ dữ liệu để phân tích. Hãy ghi nhận thêm các khoản chi tiêu nhé!"

        # Phân tích cơ bản
        category_totals = {}
        for trans in self.transactions:
            cat_name = trans['category']['name']
            category_totals[cat_name] = category_totals.get(cat_name, 0) + trans['amount']

        sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
        
        # Tạo phân tích được cá nhân hóa
        response = f"📊 {self.bot_name} đã phân tích chi tiêu của cậu:\n\n"
        for cat_name, total in sorted_categories:
            response += f"{cat_name}: {total:,}đ\n"
        
        # Thêm nhận xét cá nhân hóa
        top_category = sorted_categories[0][0]
        if top_category in self.conversation_context["common_transactions"]:
            response += f"\n💡 Nhận xét: Như mình đã quan sát thấy, cậu thường xuyên chi tiêu cho {top_category}. "
            if len(sorted_categories) > 1:
                second_category = sorted_categories[1][0]
                response += f"Kế đến là {second_category}."
        
        return response

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

    def get_personalized_response(self, message: str) -> str:
        """Tạo câu trả lời dựa trên ngữ cảnh và tính cách"""
        message = message.lower()

        # Xử lý câu hỏi về bot
        if any(q in message for q in ["cậu là ai", "cậu tên gì", "cậu là gì"]):
            return random.choice(self.bot_personality["about_me"])

        # Xử lý câu hỏi về khả năng
        if any(q in message for q in ["biết làm gì", "có thể làm gì", "giúp được gì"]):
            return random.choice(self.bot_personality["capabilities"])

        # Xử lý dựa trên ngữ cảnh trước đó
        if self.conversation_context["last_topic"]:
            if "như vậy" in message or "thế" in message:
                return f"Dựa vào cuộc trò chuyện trước, mình hiểu là cậu đang nói về {self.conversation_context['last_topic']}"

        return None  # Trả về None nếu không có câu trả lời đặc biệt

    def get_tsundere_reaction(self, expense: dict) -> str:
        """Tạo phản ứng tsundere dựa trên loại và số tiền chi tiêu"""
        category = expense['category']['name']
        amount = expense['amount']
        item = expense['item']
        
        # Lấy reactions cho category
        reactions = self.tsundere_reactions.get(category, self.tsundere_reactions['DEFAULT'])
        
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
        
        # Lấy random một reaction và format với thông tin chi tiêu
        reaction = random.choice(reactions[level])
        return reaction.format(amount=f"{amount:,}đ", item=item)

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

# Demo usage
def main():
    bot = FinanceBot()
    
    while True:
        user_input = input("cậu: ")
        if user_input.lower() == "quit":
            break
            
        response = bot.process_message(user_input)
        print(f"Bot: {response}")

if __name__ == "__main__":
    main()