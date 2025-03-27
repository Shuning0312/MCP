from travel_mcp import TravelPlannerMCP
from llm_connector import LLMConnector
from notion_handler import NotionHandler
import os
import argparse
import re

def setup_environment():
    """设置环境变量和配置"""
    # 可以使用dotenv加载.env文件
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("提示: 安装python-dotenv可以更方便地管理环境变量")
        pass

def create_travel_plan(destination, duration, season, budget, interests, special_req=None, save_to_notion=True):
    """创建旅游计划的主函数"""
    # 初始化MCP
    travel_mcp = TravelPlannerMCP()
    travel_mcp.set_destination(destination, duration, season)
    travel_mcp.set_traveler_preferences(
        budget=budget,
        interests=interests,
        special_requirements=special_req
    )
    travel_mcp.set_notion_format()
    
    # 生成提示词
    prompt = travel_mcp.generate_prompt()
    print("已生成MCP提示词:")
    print("-" * 50)
    print(prompt)
    print("-" * 50)
    
    # 调用LLM
    try:
        
        print("正在调用大语言模型...")
        llm = LLMConnector()
        travel_plan = llm.generate_travel_plan(prompt)
        
        # 保存结果到本地文件
        with open(f"{destination}_{duration}天旅游计划.txt", "w", encoding="utf-8") as f:
            f.write(travel_plan)
        
        print(f"旅游计划已保存到 {destination}_{duration}天旅游计划.txt")
        
        # 保存到Notion (如果requested)
        if save_to_notion:
            print("正在保存到Notion...")
            notion = NotionHandler()
            response = notion.create_travel_plan_page(f"{destination}{duration}日游计划", travel_plan)
            print(f"旅游计划已成功保存到Notion! 页面ID: {response.get('id')}")
        
        return travel_plan
    
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return None
    
def test_upload_local_plan_to_notion(filepath, title):
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ 当前 Notion 数据库 ID：", os.environ.get("NOTION_DATABASE_ID"))
    """测试：直接将本地计划文件上传到 Notion"""
    from notion_handler import NotionHandler
    
    # 读取本地内容
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 上传到 Notion
    notion = NotionHandler()
    response = notion.create_travel_plan_page(title, content)
    print(f"✅ 成功上传到 Notion，页面ID: {response.get('id')}")

def main():
    """命令行入口点"""
    # 设置环境
    setup_environment()
    
    
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="旅游计划生成器")
    parser.add_argument("--destination", "-d", required=True, help="旅行目的地")
    parser.add_argument("--duration", "-l", type=int, required=True, help="旅行天数")
    parser.add_argument("--season", "-s", help="旅行季节")
    parser.add_argument("--budget", "-b", default="中等", help="预算(低/中等/高)")
    parser.add_argument("--interests", "-i", nargs="+", help="兴趣爱好列表")
    parser.add_argument("--special", help="特殊要求")
    parser.add_argument("--no-notion", action="store_true", help="不保存到Notion")
    
    args = parser.parse_args()
    
    interests = args.interests or ["文化", "美食", "观光"]
    
    create_travel_plan(
        args.destination, 
        args.duration,
        args.season,
        args.budget,
        interests,
        args.special,
        not args.no_notion
    )

if __name__ == "__main__":
    # main()
    test_upload_local_plan_to_notion("京都_5天旅游计划.markdown", "京都5日游计划new")