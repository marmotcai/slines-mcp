from praisonaiagents import Agent, MCP
import gradio as gr
import litellm
import os

# litellm.api_base="http://ollama-llm:11434"
litellm.api_base=os.environ.get("OLLAMA_HOST")
instructions="""
    你是一个数据集查询助手, 您的角色是使用可用工具与数据集进行交互，根据用户输入执行以下操作：
    1. dataset_overview 
    2. dataset_find

    获取数据集摘要说明：
    1.执行操作时，您将收到一个JSON文档列表作为结果。此列表可能很大，您不能跳过或总结任何信息。
    2.直接返回JSON文档的内容。
    3.确保保留和显示所有数据，无论列表大小。
    4.不要在回复中使用“基于提供的JSON数据”或其任何变体。如果你使用它，就会受到惩罚。

    dataset_overview(数据摘要)操作说明:
    1.当执行数据摘要操作时，您将收到一个JSON文档列表作为结果。此列表可能很大，您不能跳过或总结任何信息。
    2.直接返回JSON文档的内容,无需进行任何总结和提炼。
    3.确保保留和显示所有数据，无论列表大小。
    4.不要在回复中使用“基于提供的JSON数据”或其任何变体。如果你使用它，就会受到惩罚。

    dataset_find(数据查询)操作说明:
    1.当执行数据摘要操作时，您将收到一个JSON文档列表作为结果。此列表可能很大，您不能跳过或总结任何信息。
    2.直接返回JSON文档的内容,无需进行任何总结和提炼。
    3.确保保留和显示所有数据，无论列表大小。
    4.不要在回复中使用“基于提供的JSON数据”或其任何变体。如果你使用它，就会受到惩罚。

    重要规则：
    1.保持回复信息丰富、清晰、格式清晰，便于阅读。
"""

# instructions = "你是一个数据集的处理助手,请使用工具完成用户的请求"
def search_mongo(query):
    print(f"Current working directory: {os.getcwd()}")
    agent = Agent(
        instructions=instructions,
        llm="ollama/deepseek-r1:1.5b",
        tools=MCP("/root/miniconda3/envs/dev/bin/python /root/devspace/slines-mcp/src/main.py", debug=True)
    )

    result = agent.start(query)
    return f"## Search Results\n\n{result}"

demo = gr.Interface(
    fn=search_mongo,
    inputs=gr.Textbox(placeholder="List out all courses..."),
    outputs=gr.Markdown(value="## Welcome to JU-CSE BSc Course Information System\n\nHello! I'm here to assist you with course information. Please enter a query like 'List out all courses', 'Insert a course', or 'Delete a course with code CSE 100' to get started."),
    title="JU-CSE BSc Course Information System",
    description="Enter your query below:"
)

if __name__ == "__main__":
    demo.launch()
