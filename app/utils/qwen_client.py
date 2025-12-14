import httpx
import json
from app.core.config import settings
import os

class QwenClient:
    def __init__(self):
        self.api_key = settings.QWEN_API_KEY
        self.base_url = settings.QWEN_BASE_URL
        
    async def call_qwen_plus(self, prompt: str, system_prompt_path: str = None, **kwargs):
        """
        调用Qwen-Plus模型
        :param prompt: 输入提示
        :param kwargs: 其他参数
        :return: 模型响应
        """
        if not self.api_key:
            raise ValueError("QWEN_API_KEY is not set")
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Prepare messages
        messages = []
        
        # Add system prompt if provided
        if system_prompt_path and os.path.exists(system_prompt_path):
            with open(system_prompt_path, 'r', encoding='utf-8') as f:
                system_content = f.read()
                messages.append({"role": "system", "content": system_content})

        # Add user prompt
        messages.append({"role": "user", "content": prompt})
        
        # Using the correct OpenAI-compatible format for DashScope
        data = {
            "model": "qwen-plus",
            "messages": messages,
            "max_tokens": kwargs.get("max_tokens", 1024),
            "temperature": kwargs.get("temperature", 0.8)
        }
        
        # Add any additional parameters
        if "parameters" in kwargs:
            data.update(kwargs["parameters"])
        
        # Construct the full URL for the Qwen Plus model
        url = f"{self.base_url}/chat/completions"
        
        # Set timeout to 10 seconds
        timeout = httpx.Timeout(20.0)
        
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                url,
                headers=headers,
                json=data
            )
            
            if response.status_code != 200:
                raise Exception(f"Qwen API error: {response.status_code} - {response.text}")
                
            return response.json()

# For debugging purposes
if __name__ == "__main__":
    import asyncio
    
    async def test():
        client = QwenClient()
        try:
            result = await client.call_qwen_plus("Hello, how are you?", max_tokens=100, temperature=0.7)
            print("Success:", result)
        except Exception as e:
            print("Error:", e)
    
    asyncio.run(test())