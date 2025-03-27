# llm_connector.py
import requests
import json
import os

class LLMConnector:
    """连接大语言模型的接口 - DeepSeek版本"""
    
    def __init__(self, api_key=None, api_base=None):
        self.api_key = api_key or os.environ.get("DEEPSEEK_API_KEY")
        self.api_base = api_base or os.environ.get("DEEPSEEK_API_BASE", "https://api.deepseek.com")
        
        if not self.api_key:
            raise ValueError("需要提供DeepSeek API密钥")
    
    def generate_travel_plan(self, mcp_prompt):
        """调用DeepSeek LLM生成旅游计划"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        print()
        
        # DeepSeek API接口参数
        payload = {
            "model": "deepseek-chat",  # 或使用其他可用的DeepSeek模型
            "messages": [
                {"role": "system", "content": "你是一个旅游规划助手，按照用户的MCP框架提供旅游计划。"},
                {"role": "user", "content": mcp_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 4000
        }
        
        # 构建完整的API URL
        api_url = f"{self.api_base}/v1/chat/completions"
        
        response = requests.post(
            api_url,
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            error_msg = f"DeepSeek API调用失败: {response.status_code}"
            try:
                error_detail = response.json()
                error_msg += f", {error_detail.get('error', {}).get('message', response.text)}"
            except:
                error_msg += f", {response.text}"
            raise Exception(error_msg)