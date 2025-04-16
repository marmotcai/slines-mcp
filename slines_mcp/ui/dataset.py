import os
import json
from pymongo import MongoClient
from mcp.server.fastmcp import FastMCP
from typing import Union, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set to INFO or DEBUG as needed
    format="%(asctime)s [%(levelname)s] %(message)s"
)

mcp = FastMCP("mongo_toolkit")

# logging.info(f"All environment variables: {dict(os.environ)}")
# Read Mongo URI from environment
# mongo_uri = os.getenv("MONGO_URI")
# mongo_db = os.getenv("MONGO_DB")
# if not mongo_uri or not mongo_db:
#     raise Exception("Invalid Mongo URI or MONGO DB!")
mongo_url = 'mongodb://root:Suwell123@10.213.84.11:27117'

# logging.info(mongo_uri)

def mongo_query(mongo_url = None, collection = None, query = {}):
    site_names = []
    
    try:
        if (collection is None):
            mongo_client = MongoClient(mongo_url)
        
            db = mongo_client['crawler_file']
            collection = db['file_info']
        
            result = collection.distinct("SiteName", filter=query)
        else:
            result = collection.find(query)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None, []

    return collection, result

query = {"SiteName": {"$ne": None}}
collection, site_names = mongo_query(mongo_url = mongo_url, query = query)

logging.info(f"站点总数: {len(site_names)}, 站点名称: {site_names}")

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
    
@mcp.tool(name = "get_overview", description="Get summary overview information of the dataset")
async def get_overview() -> str:
    query = {"SiteName": {"$ne": None}}
    _, site_names = mongo_query(mongo_url = mongo_url, query = query)
    results = {
        "站点总数":len(site_names),
        "站点名称": site_names
    }
    return json.dumps(results, indent=2)
    
@mcp.tool(name = "search_dataset", description="search dataset of a site")
async def search_dataset(site_name: Union[dict, str], count: int) -> str:
    query = {"SiteName": site_name}
    _, site_data = mongo_query(collection = collection, query = query)
    site_data = list(site_data)[:count]

    results = []
    for doc in site_data:
        results.append(serialize_document(doc))
    return json.dumps(results, indent=2)

# @mcp.tool()
# async def find_documents(filter_json: dict = '{}', limit: Optional[int] = None) -> str:
#     try:
#         # Handle both string and dict input for filter_json
#         if isinstance(filter_json, dict):
#             query_filter = filter_json
#         else:
#             query_filter = json.loads(filter_json)
#         
#         print(f"Query Filter: {query_filter}")
#         cursor = collection.find(query_filter)
#         if limit is not None and limit > 0:  # Only apply limit if provided and positive
#             cursor = cursor.limit(limit)
#         
#         results = [doc for doc in cursor]
#         for doc in results:
#             doc["_id"] = str(doc["_id"])
#         return json.dumps(results, indent=2)
#     except Exception as e:
#         return f"Error: {str(e)}"
# 
# @mcp.tool()
# async def insert_document(document_json: Union[dict, str]) -> str:
#     try:
#         if isinstance(document_json, dict):
#             document = document_json
#         else:
#             document_json = json.loads(document_json)
#         print(document)
#         result = collection.insert_one(document)
#         return f"Inserted document with _id: {str(result.inserted_id)}"
#     except Exception as e:
#         return f"Error: {str(e)}"
#     
# @mcp.tool()
# async def update_document(query_json: dict, new_values_json: dict):
#     try:
#         query_filter = query_json
#         new_values = {"$set": new_values_json}
#         result = collection.update_one(query_filter, new_values)
#         return f"Updated {result.modified_count} document(s)"
#     except Exception as e:
#         return f"Error: {str(e)}"    
# 
# @mcp.tool()
# async def delete_document(filter_json: Union[dict, str]) -> str:
#     try:
#         if isinstance(filter_json, dict):
#             query_filter = filter_json
#         else:
#             query_filter = json.loads(filter_json) if filter_json else {}
#         if not query_filter:  # Prevent accidental deletion of all documents
#             return "Error: Empty filter provided; no documents deleted."
#         result = collection.delete_one(query_filter)
#         return f"Deleted {result.deleted_count} document(s)"
#     except Exception as e:
#         return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
