# travel_mcp.py
from mcp import MindContextProcedure

class TravelPlannerMCP(MindContextProcedure):
    """旅游计划专用的MCP实现"""
    
    def __init__(self):
        # 设置默认的旅游规划师角色定义
        default_mind = """你是一名专业的旅游规划师，擅长创建详细的旅行计划。
你了解世界各地的旅游景点、文化习俗、美食和交通信息。
你会考虑旅行者的预算、偏好和时间安排，提供个性化的旅游建议。"""
        
        super().__init__(mind=default_mind)
    
    def set_destination(self, destination, duration, season=None):
        """设置旅行目的地信息"""
        destination_context = f"目的地: {destination}\n旅行天数: {duration}天"
        if season:
            destination_context += f"\n季节: {season}"
            
        # 更新现有的context而不是替换
        self.context = self.context + "\n" + destination_context if self.context else destination_context
        return self
    
    def set_traveler_preferences(self, budget, interests, special_requirements=None):
        """设置旅行者偏好"""
        prefs = f"预算: {budget}\n兴趣偏好: {', '.join(interests)}"
        if special_requirements:
            prefs += f"\n特殊要求: {special_requirements}"
            
        # 更新现有的context
        self.context = self.context + "\n" + prefs if self.context else prefs
        return self
    
    def set_notion_format(self):
        """设置Notion格式的输出要求"""
        notion_procedure = """请按以下格式生成适合Notion的旅游计划:
1. 创建一个总览页面，包含旅行概要和每日行程链接
2. 为每天创建单独的页面，使用日期作为标题
3. 每天的行程使用时间表格式，包含以下列:
   - 时间
   - 活动/景点
   - 描述
   - 预算
4. 为每个景点添加简短描述和参观建议
5. 包含餐厅推荐，注明菜系和价格范围
6. 添加交通建议部分
7. 创建一个打包清单数据库
8. 添加当地紧急联系信息"""
        
        self.procedure = notion_procedure
        return self