from typing import List, Dict

class ResponseFormatter:
    @staticmethod
    def format_transactions_markdown(transactions: list) -> str:
        """Format transactions với markdown chuẩn"""
        if not transactions:
            return "Không có giao dịch nào gần đây."
        
        md = "### 📝 Giao dịch gần đây\n\n"
        for trans in transactions:
            wallet_name = trans["wallet"]["name"]
            amount = ResponseFormatter.format_currency(trans["amount"])
            item = trans["item"]
            md += f"- {item}: `{amount}` từ {wallet_name}\n"
        
        return md

    @staticmethod
    def format_stats_markdown(stats: dict) -> str:
        """Format statistics với markdown chuẩn"""
        if not stats:
            return ""
        
        md = "### 📊 Thống kê chi tiêu\n\n"
        
        # Format số tiền đơn giản
        expense = ResponseFormatter.format_currency(stats["total_expense"])
        income = ResponseFormatter.format_currency(stats["total_income"])
        
        md += f"* 💸 **Chi tiêu:** `{expense}`\n"
        md += f"* 💰 **Thu nhập:** `{income}`\n"
        
        return md

    @staticmethod
    def format_currency(amount: int) -> str:
        """Format số tiền thành dạng đẹp với dấu chấm phân cách"""
        return f"{amount:,}đ".replace(",", ".")

    @staticmethod
    def create_full_response(response: str, transactions: List[Dict], stats: Dict, recent_transaction: str) -> Dict:
        """Tạo response với messages gốc và recent dạng markdown"""
        # Chỉ format phần statistics thành markdown
        stats_md = ResponseFormatter.format_stats_markdown(stats)
        
        # Format transactions thành markdown
        transactions_md = ResponseFormatter.format_transactions_markdown(transactions)
        
        # Kết hợp thống kê và giao dịch vào recent
        recent_md = f"{stats_md}\n{transactions_md}\n{recent_transaction}" if transactions else stats_md
        
        return {
            "messages": response,  # Chỉ chứa phản hồi từ bot
            "recent": recent_md,   # Chèn markdown vào recent
            "transactions": transactions,
            "statistics": stats
        }
