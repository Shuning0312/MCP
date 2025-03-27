# mcp.py

class MindContextProcedure:
    """
    MCP (Mind-Context-Procedure) 模块用于结构化大语言模型提示
    - Mind: 定义AI的角色、背景和能力
    - Context: 提供任务的上下文和约束条件
    - Procedure: 指导AI完成任务的具体步骤
    """
    
    def __init__(self, mind="", context="", procedure=""):
        self.mind = mind
        self.context = context
        self.procedure = procedure
    
    def set_mind(self, mind):
        """设置Mind组件"""
        self.mind = mind
        return self
    
    def set_context(self, context):
        """设置Context组件"""
        self.context = context
        return self
    
    def set_procedure(self, procedure):
        """设置Procedure组件"""
        self.procedure = procedure
        return self
    
    def generate_prompt(self):
        """生成完整的提示词"""
        prompt = f"""
# Mind
{self.mind}

# Context
{self.context}

# Procedure
{self.procedure}
"""
        return prompt.strip()