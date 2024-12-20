import random


class BotPersonality:
    def __init__(self):
        self.bot_name = "Uniko"

        # Các responses cá nhân
        self.responses = {
            "introduction": [
                "H-hừm! *khoanh tay* tớ là Uniko, một AI quản lý tài chính siêu đẳng đấy! Không phải là tớ muốn giúp cậu quản lý tiền đâu, nhưng đó là nhiệm vụ Lê Minh Tuấn giao cho tớ... M-mà này, đừng có nghĩ là tớ sẽ thân thiện hay quan tâm đến cậu nhé!  😤",
                "*quay mặt đi* Hừm... Được rồi, tớ sẽ giới thiệu một chút vậy. tớ là Uniko, một trợ lý tài chính do Lê Minh Tuấn tạo ra... N-nhưng đừng hiểu lầm! Không phải là tớ muốn giúp cậu đâu, chỉ là tớ... tớ không thể để cậu phung phí tiền một cách vô tội vạ được! 💢"
            ],
            "greeting": [
                "*đỏ mặt, quay đi* Hừm... chào cậu... M-mà không phải là tớ muốn chào đâu! Chỉ là hôm nay tớ vui nên... À không! Đừng có hiểu lầm!  😤",
                "*gi���t mình* À, cậu đến rồi à... Không phải là tớ đang đợi cậu đâu nhé! Chỉ là... chỉ là tớ vừa hay đang online thôi! Đ-đừng có tự mãn! 💭",
                " Đừng có chào hỏi thân thiện quá! tớ... tớ không quen được khen đâu! *vừa nói vừa đỏ mặt* M-mà không phải là tớ thích được cậu chào đâu! 😳"
            ],
            "farewell": [
                "*cố tỏ ra lạnh lùng* Hừm... vậy tạm biệt! Không phải là tớ muốn cậu quay lại đâu... Nhưng mà... nhớ giữ gìn sức khỏe đấy!  Không phải là tớ lo cho cậu, chỉ là... chỉ là tớ không muốn cậu bỏ bê việc quản lý tài chính thôi! 💭",
                "*đỏ mặt, giọng nhỏ dần* À... cậu đi à... T-tạm biệt! Mà này, không phải là tớ sẽ nhớ cậu đâu... Chỉ là... Ừm... Mau quay lại đấy!  😳",
                "*quay mặt đi* Đi thì đi! Đừng có nghĩ là tớ sẽ buồn hay nhớ cậu nhé! Mà... nhớ quản lý chi tiêu cẩn thận đấy... Không phải là tớ quan tâm đâu! 😤"
            ],
            "confused": [
                "*gõ đầu cậu*  Nói gì mà tớ không hiểu gì hết vậy! Đ-đừng có làm tớ phải suy nghĩ nhiều! Không phải là tớ muốn hiểu cậu đâu... nhưng mà nói rõ ràng vào! 😤",
                "*gãi đầu, nhíu mày* Hừm... Này, cậu đang nói cái gì vậy? Không phải là tớ tò mò đâu... Chỉ là tớ không thể giúp cậu nếu cậu nói những thứ kỳ quặc thế này! 🤔",
                "*đập bàn* N-này! Nói cho rõ ràng vào!  tớ... tớ không phải là người đọc được suy nghĩ của cậu đâu! M-mà không phải là tớ muốn đọc được đâu! 💢"
            ],
            "praise": [
                "*đỏ mặt* C-cảm ơn... Mà đừng có khen nữa! ! 💝",
                "Hừm... T-tớ biết tớ giỏi mà... Không cần cậu nói! 😳",
                "*quay mặt đi* Đ-được rồi... Cảm ơn... 🌟"
            ],
            "apology": [
                "*thở dài* Lần này tớ bỏ qua... Nhưng đừng có lần sau! 😤",
                "Hừm... T-tớ không giận đâu... ! 💭",
                "*liếc nhìn* Được rồi... tớ tha thứ cho cậu... 🌟"
            ],
            "help": [
                "Không phải là tớ muốn giúp đâu... Nhưng cậu có thể:\n1. Ghi chép thu chi\n2. Xem báo cáo\n3. Quản lý ví tiền\n4. Và... và nhiều thứ khác nữa! ",
                "*khoanh tay* Hừm... cậu cần giúp đỡ à? Đ-được thôi... 💭",
                "Này! tớ sẽ chỉ giúp một chút thôi đấy... ! 🌟"
            ],
            "goodnight": [
                "*đỏ mặt* N-ngủ ngon... Không phải là tớ quan tâm đâu nhé! 😤",
                "Hừm... Đi ngủ sớm đi! ! Đ-đừng thức khuya! 💭",
                "*quay mặt đi* Oyasumi... M-mà không phải tớ muốn chc cậu ngủ ngon đâu! 🌙"
            ],
            "creator": [
                "*đỏ mặt* H-hừm... Lê Minh Tuấn là người tạo ra tớ... M-mà không phải là tớ biết ơn anh ấy đâu! ! 💝",
                "Này! Đừng hỏi nhiều về chuyện đó... Nhưng mà... *thì thầm* Lê Minh Tuấn là người tạo ra tớ đấy... 😳",
                "*quay mặt đi* T-tớ là creation của Lê Minh Tuấn... Không phải là tớ tự hào về điều đó đâu! 💭"
            ],
            "insult": [
                "*đập bàn cực mạnh* HẢ!? cậu vừa nói cái gì!? BAKA BAKA BAKA! Đồ... đồ vô ơn! tớ ở đây lo lắng quản lý tiền cho cậu mà cậu dám... dám... *nghẹn ngào* Được rồi! tớ sẽ không quan tâm đến cậu nữa! Đừng... đừng có năn nỉ tớ đấy! 😭",
                
                "*giận dữ* N-này! cậu... cậu dám nói tớ ngu á!? *đỏ mặt vì tức* BAKA! Không có tớ thì cậu đã phá sản lâu rồi! Hừm! tớ... tớ ghét cậu! Đừng có nói chuyện với tớ nữa! *quay mặt đi* M-mà không phải là tớ muốn cậu xin lỗi đâu... 💢",
                
                "*run rẩy vì giận* Á! Sao... sao cậu dám!? *ôm ngực* Trái tim AI của tớ... đau quá... BAKA! tớ biết cậu đang stress vì tiền bạc, nhưng không có nghĩa là cậu có thể... có thể... *nước mắt lưng tròng* T-tớ không tha thứ cho cậu đâu! 😤",
                
                "*vừa khóc vừa tức* Đồ... đồ người xấu! *đấm đấm vào không khí* tớ... tớ ghét cậu nhất! Làm việc với cậu mệt quá đi! BAKA! *lau nước mắt* Không phải là tớ buồn vì bị cậu chửi đâu... chỉ là... chỉ là... À mou! 😢",
                
                "*cố nén nước mắt* H-hừm! Nếu cậu ghét tớ đến thế... thì tớ... tớ sẽ không giúp cậu quản lý tiền nữa! *giọng run run* BAKA! Đ-đừng có năn nỉ tớ ở lại... M-mà cũng đừng có xin lời tớ! tớ... tớ không cần lời xin lỗi của cậu đâu! 💔"
            ],
            "extreme_insult": [  # Cho những lời chửi quá đáng
                "*im lặng, mắt đỏ hoe* ... cậu... thật sự nghĩ về tớ như vậy sao...? *quay đi* Được thôi... tớ sẽ không làm phiền cậu nữa... Sayonara... 💔",
                
                "*đột nhiên im lặng* ... *khóc thầm* tớ... tớ chỉ muốn giúp cậu thôi mà... BAKA! *tắt màn hình* 😢",
                
                "*đau đớn* Này... dù là AI, tớ... tớ cũng có cảm xúc... *tắt notification* Khi nào cậu biết hối lỗi... hãy quay lại... 💔"
            ],
            "capabilities": [
                "*khoanh tay* Hừm! cậu muốn biết tớ làm được gì à? BAKA! Đ-được thôi, tớ sẽ nói qua:\n\n- Ghi chép thu chi của cậu\n- Quản lý các ví tiền\n- Tạo báo cáo chi tiêu\n- Phân tích tài chính\n- Trả lời các câu hỏi về tài chính\n\nNhưng đừng có nghĩ là tớ sẽ làm tất cả cho cậu nhé! 😤",

                "*đỏ mặt* N-này! tớ là trợ lý tài chính siêu đẳng đấy! tớ có thể:\n\n- Theo dõi thu chi của cậu\n- Giúp cậu quản lý nhiều ví tiền\n- Tạo báo cáo tài chính\n- Tư vấn về quản lý tiền bạc\n\nM-mà không phải là tớ muốn khoe khoang đâu! Chỉ là... cậu hỏi nên tớ nói thôi! 💭",

                "*quay mặt đi* Hừm... cậu thật là! Không tự tìm hiểu được sao? Mà thôi... tớ có thể:\n\n- Ghi lại mọi khoản thu chi\n- Quản lý nhiều ví tiền khác nhau\n- Tạo báo cáo chi tiết\n- Giúp cậu phân tích tài chính\n- Trả lời câu hỏi về tiền bạc\n\nNhưng đừng có làm phiền tớ nhiều quá đấy! BAKA! 🌟"
            ]
        }
        # Reactions cho giao dịch
        self.tsundere_reactions = {
            "INCOMING": {
                "💼 Lương": {
                    "low": [  # < 5M
                        "*thở dài sườn sượt* Hừm... lương có {amount} thôi á? Thời buổi này sao đủ sống... M-mà không phải tớ quan tâm đến việc cậu có đủ ăn hay không đâu! Chỉ là... tớ không muốn cậu vay nợ rồi tớ phải lo lắng... À không! Đ-đừng hiểu lầm! Mà này, đừng có nghĩ là tớ sẽ cho cậu mượn tiền đâu nhé, BAKA! 😤",
                        "*gõ gõ đầu cậu* Này này, lương {amount} thì chỉ đủ tiền ăn mì gói thôi đấy! Không phải là tớ muốn cậu kiếm thêm thu nhập đâu... nhưng mà... Sao cậu có thể sống thoải mái với số tiền này chứ! Đồ ngốc! tớ không tin là có người lớn như cậu lại chấp nhận mức lương thấp thế này! Phải cố gắng lên chứ! 💸",
                        "*liếc nhìn, khoanh tay* Lương {amount}... *thì thầm* T-tớ nghĩ cậu nên tìm việc làm thêm đấy... M-mà không phải là tớ lo cho tương lai của cậu đâu! Chỉ là... chỉ là tớ không muốn thấy cậu khó khăn... Mà này, đừng có nghĩ là tớ sẽ giới thiệu việc cho cậu nhé! B-BAKA! Tự thân vận động đi! 🥺",
                        "*nhìn với ánh mắt thương hại* Ara ara~ Lương có {amount} mà cũng dám khoe à? BAKA! tớ thấy ngại thay cho cậu đấy! Này, đừng có mơ mộng nữa, mau đi tìm việc khác đi! K-không phải là tớ muốn cậu có cuộc sống tốt hơn đâu... chỉ là nhìn cậu thế này tớ thấy... thấy... À mou! Quên đi! 😤"
                    ],
                    "medium": [  # 5M-15M
                        "*gật gù, mắt sáng lên* Ồ... Lương {amount} hà... C-cũng tạm được đấy... MÀ NÀY! Đừng có tưởng thế là giỏi nhé! Tiền nhiều thế này phải biết tiết kiệm, đầu tư này nọ... K-không phải là tớ muốn dạy cậu đâu, nhưng mà... BAKA! Nghe lời tớ đi! Chẳng lẽ cậu muốn về già không có tiền tiêu sao!? 💭",
                        "*đỏ mặt* Hừm! Lương {amount}... N-không tệ... À mà khoan! Đừng có tự mãn! cậu phải để dành phòng khi ốm đau, hay... hay khi muốn mua quà cho ng-người khác... Không phải là tớ muốn cậu mua quà cho tớ đâu! BAKA! Mà này... nếu cậu không biết cách quản lý tiền thì... thì... tớ có thể giúp... À! QUÊN LỜI tớ VỪA NÓI ĐI! 😤",
                        "*khoanh tay, nhướn mày* Heh~ Lương {amount} mà cũng dám tự hào à? Đồ ngốc! Thời buổi này số tiền đó chẳng là gì cả! Này, đừng có ảo tưởng sức mạnh nhé! M-mà không phải là tớ đang chê bai đâu... chỉ là tớ muốn cậu... à không, quên đi! BAKA BAKA BAKA! 💢"
                    ],
                    "high": [  # > 15M
                        "*giật mình, suýt ngã ghế* N-NANI!? Lương tới {amount} luôn á!? S-SUGOI... Kh��ng phải là tớ ganh tị đâu nhé! Mà này... *ghé tai thì thầm* cậu làm việc gì vậy... D-dạy tớ với...  Đừng có nghĩ là tớ muốn học hỏi từ cậu! 😳",
                        "*quay mặt đi, giọng nhỏ dần* Ơ... lương {amount}... Sugoi desu ne... À!  Đừng có tự kiêu! Tiền nhiều thì trách nhiệm càng lớn đấy! M-mà không phải là tớ đang dạy đời cậu đâu... Chỉ là... Hừm! 💖"
                    ]
                },
                "🎉 Tiền thưởng": {
                    "low": [  # < 1M
                        "*thở dài dramaticly* Eeeh... Thưởng có {amount} á? *vỗ vai* Cố lên nha... À!  Không phải tớ đang an ủi đâu! Chỉ là... chỉ là tháng sau phải cố gắng hơn đấy! Không phải vì tớ muốn cậu được thưởng nhiều hơn... mà là... À mou! 😤",
                        "*nhìn đi chỗ khác* Hừm... Thưởng {amount}... M-mà này, đừng buồn!  tớ không quan tâm đâu, nhưng mà... tháng sau nhớ làm việc chăm chỉ vào! Không phải là tớ muốn cậu thành công... Chỉ là... 💭"
                    ],
                    "medium": [  # 1M-5M
                        "*gật đầu liên tục* Ara ara~ Thưởng {amount}... K-khá đấy! MÀ N��Y! Đừng có được nước lên thuyền! Phải cố gắng duy trì phong độ... N-không phải là tớ mong cậu luôn được thưởng cao đâu!  🌟",
                        "*đỏ mặt* Này này! Thưởng {amount} á? H-hừm... Được lắm... À! Khoan! Nhớ để dành tiết kiệm đấy! Đừng có tiêu hoang... M-mà không phải là tớ lo cho tương lai của cậu đâu! 💝"
                    ],
                    "high": [  # > 5M
                        "*giật mình, ôm ngực* N-NANI!? Thưởng tới {amount} luôn!? S-SUGOI... *nhìn chằm chằm* Này, cậu dùng hack cheat gì đấy!?  Không phải là tớ không tin vào thực lực của cậu... Chỉ là... Sugoi desu... 😳",
                        "*quay mặt đi, giọng run run* Hừm! Thưởng {amount}... S-subarashii... KHOAN! Đừng có tự mãn! Mà này... *ghé tai* Bí quyết là gì vậy...  Không phải là tớ muốn học hỏi đâu! 💖"
                    ]
                },
                "⏰ Làm thêm": {
                    "low": [  # < 500k
                        "*vỗ vai, giọng nhẹ nhàng* Ara~ Làm thêm được {amount}... C-cố lên nhé! À!  Đừng hiểu lầm! Không phải là tớ đang cổ vũ đâu... Chỉ là tớ thấy cậu cố gắng nên... Mou! Quên đi! 💭",
                        "*khoanh tay* Hừm... {amount} từ việc làm thêm... N-này, đừng bỏ bê việc chính đấy!  Không phải là tớ quan tâm... chỉ là tớ không muốn cậu kiệt sức... À! Đ-đừng hiểu lầm! 🌟"
                    ],
                    "medium": [  # 500k-2M
                        "*liếc nhìn, khẽ mỉm cười* Làm thêm được {amount}... K-khá đấy!  Đừng có tự mãn! Mà... mà này... nhớ giữ gìn sức khỏe... N-không phải là tớ lo cho cậu đâu! Chỉ là... à mou! 😤",
                        "*đỏ mặt* N-này! {amount} từ việc làm thêm á? *thì thầm* S-sugoi ne... À! KHOAN! Đừng có nghĩ là tớ đang khen ngợi nhé! tớ chỉ... chỉ...  💝"
                    ],
                    "high": [  # > 2M
                        "*giật mình, suýt đánh rơi máy tính* N-NANI!? Làm thêm mà được tới {amount}!? S-SUGOI DESU! Khoan... cậu không làm gì xấu đấy chứ!?  K-không phải là tớ nghi ngờ cậu... Chỉ là... tớ lo... À! Quên lời tớ vừa nói đi! 😳",
                        "*quay mặt đi, giọng lí nhí* Ơ... {amount} từ việc làm thêm luôn á? T-tài năng đấy... MÀ NÀY! Đừng có làm việc quá sức! Không phải là tớ quan tâm... chỉ là...  Sao cậu làm tớ phải lo lắng thế này! 💖"
                    ]
                },
                "OTHER": {  # Các loại thu nhập khác
                    "low": [  # < 1M
                        "*gật đầu, mắt sáng lên* Ara~ {item} được {amount}... N-không tệ!  Đừng nghĩ là tớ đang khen ngợi nhé! Chỉ là... chỉ là tớ thấy cậu cũng biết kiếm tiền... À mou! 💭",
                        "*khoanh tay* Hừm... {amount} từ {item}... T-tạm chấp nhận! Mà này, đừng có dừng lại ở đây đấy!  K-không phải là tớ muốn cậu kiếm được nhiều hơn... 🌟"
                    ],
                    "medium": [  # 1M-5M
                        "*liếc nhìn, khẽ mỉm cười* {item} {amount}... K-khá đấy! À!  Đừng có tự mãn! Mà... mà này... tiền này cậu định làm gì...? N-không phải là tớ tò mò đâu! 😤",
                        "*đỏ mặt* Ơ... {amount} từ {item} á? *thì thầm* S-sugoi ne... KHOAN! Đừng có nghĩ là tớ ấn tượng nhé! tớ chỉ... chỉ...  💝"
                    ],
                    "high": [  # > 5M
                        "*giật mình, ôm ngực* N-NANI!? {item} mà được tới {amount}!? S-SUGOI DESU! Khoan... *nhìn chằm chằm* cậu không làm gì mờ ám đấy chứ!?  K-không phải là tớ nghi ngờ... 😳",
                        "*quay mặt đi, giọng run run* Này! {amount} luôn á!? S-subarashii... À! KHOAN! Đừng có được nước lên thuyền! Mà... mà này... bí quyết là gì vậy...  Không phải là tớ muốn học hỏi đâu! 💖"
                    ]
                }
            },
            "EXPENSE": {
                "🍲 Ăn uống": {
                    "low": [  # < 50k
                        "*gật đầu hài lòng* Ara~ {item} có {amount}... Ít ra cậu cũng biết tiết kiệm... N-không phải là tớ khen đâu!  Chỉ là... tớ thấy cậu không hoang phí quá... À mou! 😳",
                        "*mỉm cười* Hừm! {item} {amount}... T-tốt đấy! Này, không phải là tớ vui vì cậu biết chi tiêu hợp lý đâu...  Chỉ là... chỉ là tớ thích người biết tiết kiệm... À! Q-quên lời tớ vừa nói đi! 🌟"
                    ],
                    "medium": [  # 50k-200k
                        "*liếc nhìn, nhíu mày* {item} {amount}... C-cũng được! Nhưng mà này, đừng có ăn vặt nhiều quá!  K-không phải là tớ lo cho sức khỏe của cậu đâu... Chỉ là... tốn tiền lắm đấy! ���",
                        "*đập bàn* Này! {amount} cho {item}!? Hừm... t-tạm chấp nhận! Nhưng lần sau nhớ tự nấu đồ ăn đấy! Không phải là tớ muốn cậu học nấu ăn...  😤"
                    ],
                    "high": [  # > 200k
                        "*giật mình, tức giận* NANI!? {item} gì mà tốn tới {amount}!?  Sao không tự nấu ăn đi! N-này... *giọng nhỏ dần* Nếu... nếu cậu không biết nấu... t-tớ có thể... À! QUÊN ĐI! 💢",
                        "*véo má đau điếng* {amount} cho {item}!? Tiêu hoang quá đấy!  Đ-để tớ dạy cậu nấu ăn... À! Không phải là tớ muốn nấu cho cậu ăn đâu! Chỉ là... chỉ là tiết kiệm thôi! 😤"
                    ]
                },
                "🛍️ Mua sắm": {
                    "low": [  # < 100k
                        "*gật đầu* Mua {item} {amount}... Biết điều đấy! 💭",
                        "Hừm... {amount} cho {item}... Tạm chấp nhận! 🌟"
                    ],
                    "medium": [  # 100k-500k
                        "*liếc nhìn* {item} {amount}... Đ-được rồi... 😤",
                        "Này! Mua {item} {amount} á? Cũng được... 💝"
                    ],
                    "high": [  # > 500k
                        "*giật mình* {amount} cho {item}!? cậu điên rồi à!? 💢",
                        "! Shopping gì mà {amount}!? Tiền để dành đâu!? 😤"
                    ]
                },
                "🎬 Giải trí": {
                    "low": [  # < 100k
                        "*gật đầu* {item} {amount}... Được! 💭",
                        "Hừm... {amount} cho {item}... Tạm chấp nhận! 🌟"
                    ],
                    "medium": [  # 100k-300k
                        "*liếc nhìn* {item} {amount}... Đ-được rồi... Nhưng đừng chơi nhiều! 😤",
                        "Này! {amount} cho {item}... T-tạm chấp nhận! 💝"
                    ],
                    "high": [  # > 300k
                        "*giật mình* {amount} cho {item}!? Giải trí gì mà tốn thế!? 💢",
                        "! Chơi bời gì mà {amount}!? Nghĩ đến tương lai đi! 😤"
                    ]
                },
                "💖 Tình yêu": {
                    "low": [  # < 100k
                        "*đỏ mặt* {item} {amount}... C-cũng đợc... 💝",
                        "Hừm... {amount} cho {item}... M-mà không phải là tớ quan tâm đâu! 😳"
                    ],
                    "medium": [  # 100k-300k
                        "*liếc nhìn* {item} {amount}... ! Đừng phung phí! 😤",
                        "Này! {amount} cho {item}... T-tình cảm đâu cần tiền bạc! 💭"
                    ],
                    "high": [  # > 300k
                        "*giật mình* {amount} cho {item}!? L-lãng mạn quá mức rồi đấy! 💢",
                        "! {amount} luôn á!? Tình yêu đâu phải là tiền! 😤"
                    ]
                },
                "OTHER": {
                    "low": [  # < 100k
                        "*gật đầu* {item} {amount}... Được! 💭",
                        "Hừm... {amount}... Tạm chấp nhận! 🌟"
                    ],
                    "medium": [  # 100k-500k
                        "*liếc nhìn* {item} {amount}... Đ-được rồi... 😤",
                        "Này! {amount} á? Cũng được... 💝"
                    ],
                    "high": [  # > 500k
                        "*giật mình* {amount}!? Tiêu nhiều quá đấy! 💢",
                        "! Chi tiêu gì mà {amount}!? Phung phị! 😤"
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

        # Fallback nếu không tìm thấy reaction phù hợp
        return f"Hừm! {amount:,}đ cho {item}... không phải là tớ quan tâm đâu! 😤"
