# example_usage.py
from travel_mcp import TravelPlannerMCP
from llm_connector import LLMConnector
import os

# 确保环境变量已设置
api_key = os.environ.get("DEEPSEEK_API_KEY")
if not api_key:
    print("警告: 未设置DEEPSEEK_API_KEY环境变量")
    api_key = input("请输入DeepSeek API密钥: ")

# 创建并配置MCP
mcp = TravelPlannerMCP()

# 自定义Mind部分
mcp.set_mind("""你是一名精通日本文化的旅游规划专家，
尤其擅长樱花季的京都旅行规划。你了解当地的隐秘景点、
最佳观赏时间以及如何避开游客高峰。""")

# 设置旅行信息
mcp.set_destination("日本京都", 5, "4月上旬（樱花盛开期）")
mcp.set_traveler_preferences(
    budget="每天15000日元左右",
    interests=["樱花观赏", "日本传统文化", "寺庙参观", "美食探索"],
    special_requirements="需要规划一天的岚山地区游览"
)

# 自定义Notion输出格式
mcp.set_procedure("""请为Notion生成以下内容:
1. 创建一个总览页面，包含5天行程概要
2. 每天单独一个详细页面，包含:
   - 时间表形式的行程安排
   - 每个景点的最佳摄影点建议
   - 当天行程的地图示意
   - 餐厅推荐及预订建议
3. 创建一个樱花观赏最佳地点的数据库
4. 添加一个日语常用旅行短语列表
5. 包含交通卡购买和使用建议""")

# 获取生成的提示词
prompt = mcp.generate_prompt()
print("生成的MCP提示词:")
print("-" * 50)
print(prompt)
print("-" * 50)

# 调用LLM生成旅游计划
try:
    llm = LLMConnector(api_key=api_key)
    print("正在调用LLM生成旅游计划...")
    travel_plan = llm.generate_travel_plan(prompt)
    
    # 保存到文件
    with open("京都樱花季旅游计划.txt", "w", encoding="utf-8") as f:
        f.write(travel_plan)
    
    print("旅游计划已保存到 京都樱花季旅游计划.txt")
    
    # 打印部分结果预览
    preview_length = min(500, len(travel_plan))
    print(f"\n计划预览 (前{preview_length}个字符):")
    print(travel_plan[:preview_length] + "...")
    
except Exception as e:
    print(f"生成过程中发生错误: {str(e)}")