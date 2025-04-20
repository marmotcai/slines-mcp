from praisonaiagents import Agent, MCP
import gradio as gr
import litellm
import os

# from litellm import completion
# response = completion(model="ollama/deepseek-r1:14b", messages=[{ "content": "respond in 20 words. who are you?","role": "user"}], api_base=os.environ.get("OLLAMA_HOST"))
# print(response)

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

instructions = "你是一个助手,请使用工具完成用户的请求"
def search_mongo(query):
    print(f"Current working directory: {os.getcwd()}")
    agent = Agent(
        instructions=instructions,
        llm="ollama/deepseek-r1:14b",
        tools=MCP("/opt/miniconda3/envs/dev/bin/python /Users/andrewcai/devspaces/slines-mcp/src/mcpserver_ops/main.py", debug=True)
    )

    result = agent.start(query)
    return f"## Search Results\n\n{result}"

demo = gr.Interface(
    fn=search_mongo,
    inputs=gr.Textbox(placeholder="查询服务器100.126.229.5上运行的容器..."),
    outputs=gr.Markdown(value="## 欢迎使用远程服务器管理工具\n\n你好我是来帮你管理服务器的。请输入一个类似于“查询服务器100.126.229.5上运行的容器”的查询即可开始。"),
    title="远程服务器管理工具",
    description="在下面输入您的查询："
)

if __name__ == "__main__":
    demo.launch()
