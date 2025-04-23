import json
import anyio
import click
import httpx
import mcp.types as types
from mcp.server.lowlevel import Server

from pydantic import BaseModel
from typing import Optional
from typing import Union, Optional

from dataset.mongodb import MongoDBInterface

mongo_url = 'mongodb://root:Suwell123@10.213.84.11:27117'
# Initialize MongoDBInterface
mongo_interface = MongoDBInterface(
    uri=mongo_url,
    database_name="crawler_file"
)
connected = mongo_interface.connect()
if not connected:
    raise ConnectionError("Failed to connect to MongoDB. Please check the connection settings.")

print(mongo_interface.list_collections())
print(mongo_interface.distinct(
    collection_name = "file_info",
    field = "SiteName")
)

tools = [
        types.Tool(
            name="fetch",
            description="Fetches a website and returns its content",
            inputSchema={
                "type": "object",
                "required": ["url"],
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL to fetch",
                    }
                },
            },
        ),
        types.Tool(
            name="reader",
            description="Read content from documents",
            inputSchema={
                "type": "object",
                "required": ["filep_path"],
                "properties": {
                    "filep_path": {
                        "type": "string",
                        "description": "file path to read",
                    }
                },
            },
        ),
        types.Tool(
            name="dataset_overview",
            description="Get overview information of the dataset",
            inputSchema={
                "type": "object",
                "required": [],
            },
        ),
        types.Tool(
            name="dataset_count_documents",
            description="Count the number of documents in a dataset in a collection.",
            inputSchema={
                "type": "object",
                "required": ["SiteName"],
                "properties": {
                    "SiteName": {
                        "type": "string",
                        "description": "站点名称",
                    }
                },
            },
        ),
        types.Tool(
            name="dataset_find",
            description="Find multiple documents in a collection.",
            inputSchema={
                "type": "object",
                "required": ["query"],
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "检索字段",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "限制返回的文档数量",
                    }
                },
            },
        ),
        types.Tool(
            name="dataset_search_title",
            description="Search documents by title using fuzzy matching",
            inputSchema={
                "type": "object",
                "required": ["title"],
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "要搜索的标题关键词",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "限制返回的文档数量",
                        "default": 10
                    }
                },
            },
        )
    ]


# Define some models
class Tool(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    inputSchema: Optional[dict] = None

# In-memory database
tools_pool: dict[int, Tool] = {}
for tool in tools:
    tools_pool[tool.name] = tool

async def fetch_website(
    url: str,
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    headers = {
        "User-Agent": "MCP Test Server (github.com/modelcontextprotocol/python-sdk)"
    }
    async with httpx.AsyncClient(follow_redirects=True, headers=headers) as client:
        response = await client.get(url)
        response.raise_for_status()
        return [types.TextContent(type="text", text=response.text)]

def serialize_document(doc):
    if isinstance(doc, dict):
        return {key: serialize_document(value) for key, value in doc.items()}
    elif isinstance(doc, list):
        return [serialize_document(item) for item in doc]
    elif isinstance(doc, (int, float, str, bool)):
        return doc
    elif hasattr(doc, 'isoformat'):
        return doc.isoformat()
    elif hasattr(doc, 'binary'):
        return doc.binary.hex()
    else:
        return str(doc)
    
def dataset_overview(collection_name = "file_info", field = "SiteName") -> list[types.TextContent]:
    overview = mongo_interface.distinct(
                    collection_name="file_info",
                    field="SiteName"
                )
    return [types.TextContent(type="text", text=str(overview))]

def dataset_count_documents(SiteName: str = "") -> types.TextContent:
    query = {"SiteName": SiteName}
    count = mongo_interface.count_documents(
        collection_name = "file_info",
        query = query)
    
    return [types.TextContent(type="text", text=str(count))]

def dataset_search_title(
    title: str,
    limit: int = 10
) -> list[types.TextContent]:
    # 构建模糊查询的正则表达式
    query = {"Title": {"$regex": title, "$options": "i"}}
    
    results = mongo_interface.find_many(
        collection_name="file_info",
        query=query,
        limit=limit
    )
    
    return [types.TextContent(type="text", text=str([serialize_document(doc) for doc in results]))]

def dataset_find(
        query: Union[dict, str],
        limit: int = 0
    ) -> list[types.TextContent]:
    results = mongo_interface.find_many(
        collection_name = "file_info",
        query = query,
        limit = limit)
    
    return [types.TextContent(type="text", text=str([serialize_document(doc) for doc in results]))]

@click.command()
@click.option("--port", default=8000, help="Port to listen on for SSE")
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse"]),
    default="stdio",
    help="Transport type",
)
def main(transport: str, port: int = 8000) -> int:
    app = Server("slines-mcp")

    @app.call_tool()
    async def call_tool_as_name(
        name: str, arguments: dict
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:        
        tool = tools_pool.get(name)
        if not tool:
            raise ValueError(f"Unknown tool: {name}")
        
        if name == "fetch":
            if "url" not in arguments:
                raise ValueError("Missing required argument 'url'")            
            return await fetch_website(arguments["url"])
        elif name == "reader":
            file_path = arguments.get("filep_path")
            if not file_path:
                raise ValueError("Missing required argument 'filep_path'")
            with open(file_path, "r") as file:
                content = file.read()
            return [types.TextContent(type="text", text=content)]
        elif name == "dataset_overview":
            return dataset_overview()
        elif name == "dataset_count_documents":
            return dataset_count_documents(SiteName=arguments.get("SiteName", None))
        elif name == "dataset_search_title":
            title = arguments.get("title")
            if not title:
                raise ValueError("Missing required argument 'title'")
            limit = arguments.get("limit", 10)
            return dataset_search_title(title, limit)        
        elif name == "dataset_find":
            query = {"SiteName": arguments.get("query", None)}
            limit = arguments.get("limit", 0)
            return dataset_find(query, limit)

    @app.list_tools()
    async def list_tools() -> list[types.Tool]:
        return list(tools_pool.values())

    if transport == "sse":
        from mcp.server.sse import SseServerTransport
        from starlette.applications import Starlette
        from starlette.routing import Mount, Route

        sse = SseServerTransport("/messages/")

        async def handle_sse(request):
            async with sse.connect_sse(
                request.scope, request.receive, request._send
            ) as streams:
                await app.run(
                    streams[0], streams[1], app.create_initialization_options()
                )

        starlette_app = Starlette(
            debug=True,
            routes=[
                Route("/sse", endpoint=handle_sse),
                Mount("/messages/", app=sse.handle_post_message),
            ],
        )

        import uvicorn

        uvicorn.run(starlette_app, host="0.0.0.0", port=port)
    else:
        from mcp.server.stdio import stdio_server

        async def arun():
            async with stdio_server() as streams:
                await app.run(
                    streams[0], streams[1], app.create_initialization_options()
                )

        anyio.run(arun)

    return 0
