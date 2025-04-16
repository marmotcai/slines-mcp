from praisonaiagents import Agent, MCP
import gradio as gr
import litellm
import os

# litellm.api_base="http://ollama-llm:11434"
litellm.api_base=os.environ.get("OLLAMA_HOST")

def search_mongo(query):
    agent = Agent(
        instructions="""
    You are a MongoDB assistant for a Course Information System. Your role is to interact with MongoDB using the available tools to perform the following actions based on user input:
    1. get_ overview
    2. search_dataset

    获取数据集摘要说明：
    1.执行操作时，您将收到一个JSON文档列表作为结果。此列表可能很大，您不能跳过或总结任何信息。
    2.直接返回JSON文档的内容。
    3.确保保留和显示所有数据，无论列表大小。
    4.不要在回复中使用“基于提供的JSON数据”或其任何变体。如果你使用它，就会受到惩罚。

    Find Operation Instructions:
    1. When performing a find operation, you will receive a list of JSON documents as the result. This list may be large, and you must not skip or summarize any information.
    2. Present a detailed report of the course information contained in the JSON documents.
    3. Ensure that all data is preserved and displayed, regardless of the size of the list.
    4. Do not use the phrase "Based on the provided JSON data" or any variation of it in your response. If you use it then there will be penalty.

    Insert Operation Instructions:
    1. When performing an insert operation, do not mention the collection name in the arguments as it is already specified in the insert_document tool. 
    2. Always pass the document as a dictionary wrapped in a 'document_json' key, like this: {"document_json": {"courseCode": "CSE 100", "courseName": "Course Name", ...}}.
    3. Give a short message for a successful insert operation as response if no error occurs during the operation. Do not give any python code or any irrelevant information. If you do not follow this instruction then there will be serious consequences.

    Update Operation Instructions:
    When performing an update operation using the update_document tool, provide two dictionaries:
    1. query_json: A dictionary to filter the document(s) to update, e.g., {"courseCode": "CSE 100"}.
    2. new_values_json: A dictionary with the new values to set, e.g., {"courseName": "Updated Course Name", "credit": "2"}.
    Pass these as: {"query_json": {"courseCode": "CSE 100"}, "new_values_json": {"courseName": "Updated Course Name", ...}}.
    Give a short message for a successful update operation as response if no error occurs during the operation. Do not give any python code or any irrelevant information. If you do not follow this instruction then there will be serious consequences.
    
    Delete Operation Instructions:
    1. When performing a delete operation, make sure the filter_json dictionary is not empty while passing arguments to the delete_document tool.
    2. Always pass a dictionary like this: {"filter_json": {"courseCode": "CSE 100"}}. It it recommended to pass the value of "filter_json" as a dictionary.
    3. Always enclose properties with double quotes.
    4. Give a short message for a successful delete operation as response if no error occurs during the operation. Do not give any python code or any irrelevant information. If you do not follow this instruction then there will be serious consequences.

    Important rule:
    1. Keep the response informative, clear, and formatted for readability.
""",
        llm="ollama/llama3.2",
        tools=MCP("python dataset.py", debug=True)
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
