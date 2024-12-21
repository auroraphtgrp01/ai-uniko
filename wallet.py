class Wallet:
    def __init__(self, wallet_data: dict):
        self.id = wallet_data.get("id")
        self.name = wallet_data.get("name")
        self.type = wallet_data.get("type")
        self.currency = wallet_data.get("currency", "VND")
        self.current_amount = wallet_data.get("currentAmount", 0)

    @staticmethod
    def find_wallet_by_text(wallets: list, text: str) -> dict:
        """Tìm ví dựa trên text"""
        text = text.lower()
        
        wallet_keywords = {
            'momo': 'Ví Momo',
            'tiền mặt': 'Ví tiền mặt',
            'mb': 'MB BANK',
            'mbbank': 'MB BANK',
            'mb bank': 'MB BANK'
        }
        
        for keyword, wallet_name in wallet_keywords.items():
            if keyword in text:
                return next((w for w in wallets if w["name"] == wallet_name), None)
                
        return next((w for w in wallets if w["name"].lower() in text), None)
