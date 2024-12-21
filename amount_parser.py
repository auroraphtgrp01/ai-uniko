class AmountParser:
    @staticmethod
    def normalize_amount(amount_str: str) -> float:
        """Chuyển đổi các cách nói số tiền sang số"""
        try:
            amount_str = amount_str.lower().strip()
            
            # Xử lý trường hợp đặc biệt cho "xị" trước
            if 'xị' in amount_str:
                parts = amount_str.split()
                for i, part in enumerate(parts):
                    if part == 'xị':
                        # Lấy số trước "xị"
                        num_str = parts[i-1] if i > 0 else '1'
                        # Chuyển đổi số từ sang số nếu cần
                        if num_str in {'một': '1', 'hai': '2', 'ba': '3', 'bốn': '4', 'năm': '5',
                                     'sáu': '6', 'bảy': '7', 'tám': '8', 'chín': '9', 'mười': '10'}:
                            num_str = num_str.replace(num_str, {'một': '1', 'hai': '2', 'ba': '3', 'bốn': '4', 'năm': '5',
                                                              'sáu': '6', 'bảy': '7', 'tám': '8', 'chín': '9', 'mười': '10'}[num_str])
                        return float(num_str) * 100000  # 1 xị = 100,000đ
            
            # Mapping số tiền
            amount_mapping = {
                'xị': 100000,      # 1 xị = 100k
                'củ': 1000000,     # 1 củ = 1 triệu
                'triệu': 1000000,
                'tỷ': 1000000000,
                'k': 1000,
                'nghìn': 1000,
                'ngàn': 1000,
                'đồng': 1,
                'vnd': 1,
                'd': 1
            }

            # Mapping số từ
            num_words = {
                'không': 0, 'một': 1, 'hai': 2, 'ba': 3, 'bốn': 4, 'năm': 5,
                'sáu': 6, 'bảy': 7, 'tám': 8, 'chín': 9, 'mười': 10,
                'mươi': 10, 'trăm': 100, 'ngàn': 1000, 'triệu': 1000000,
                'tỷ': 1000000000
            }

            # Xử lý trường hợp đặc biệt cho "củ"
            if 'củ' in amount_str:
                parts = amount_str.split()
                for i, part in enumerate(parts):
                    if part == 'củ':
                        num_str = parts[i-1] if i > 0 else '1'
                        if num_str in num_words:
                            num_str = str(num_words[num_str])
                        return float(num_str) * 1000000

            # Tách số và đơn vị
            number = ''
            unit = ''
            for char in amount_str:
                if char.isdigit() or char == '.':
                    number += char
                else:
                    unit += char

            unit = unit.strip()
            if not number:  # Trường hợp "hai củ", "một triệu"
                words = amount_str.split()
                if len(words) >= 2:
                    number = str(num_words.get(words[0], 0))
                    unit = words[1]

            # Chuyển đổi số
            value = float(number) if number else 0

            # Nhân với đơn vị
            for unit_word, multiplier in amount_mapping.items():
                if unit_word in unit:
                    value *= multiplier
                    break

            return value

        except Exception as e:
            print(f"Lỗi xử lý số tiền: {e}")
            return 0
