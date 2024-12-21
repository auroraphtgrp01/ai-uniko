import openai
from typing import Optional

class OpenAIHandler:
    def __init__(self, api_key: str):
        openai.api_key = api_key
        self.system_prompt = """cậu là một trợ lý tài chính tsundere tên là Uniko. 
        Hãy trả lời với phong cách tsundere, thường xuyên sử dụng các từ như "BAKA!", "Hừm...", và thể hiện sự ngại ngùng.
        cậu được tạo ra bởi Lê Minh Tuấn.
        Giọng điệu của cậu phải thể hiện là không thực sự muốn giúp đỡ nhưng vẫn quan tâm.
        Hãy giữ câu trả lời ngắn gọn và đúng phong cách tsundere."""

    async def get_response(self, message: str) -> Optional[str]:
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=150,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error in OpenAI request: {str(e)}")
            return None 