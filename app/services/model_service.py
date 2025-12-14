from app.utils.qwen_client import QwenClient

class ModelService:
    def __init__(self):
        self.qwen_client = QwenClient()
    
    async def process_with_qwen_plus(self, prompt: str, **kwargs):
        """
        使用Qwen-Plus处理任务
        :param prompt: 输入提示
        :param kwargs: 其他参数
        :return: 模型响应
        """
        try:
            # 为工作流任务提供适当的系统提示
            system_prompt_path = kwargs.pop("system_prompt_path", "app/sysprompt/prompt.md")
            response = await self.qwen_client.call_qwen_plus(prompt, system_prompt_path, **kwargs)
            return {
                "success": True,
                "data": response
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

# For debugging purposes
if __name__ == "__main__":
    import asyncio
    
    async def test():
        service = ModelService()
        result = await service.process_with_qwen_plus("Hello, how are you?", max_tokens=100, temperature=0.7)
        print(result)
    
    asyncio.run(test())