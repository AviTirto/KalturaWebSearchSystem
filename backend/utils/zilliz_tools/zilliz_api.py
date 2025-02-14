import http.client
import json
import os
from dotenv import load_dotenv
import asyncio
from typing import List

import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, project_root)

from backend.utils.embedder import embed_text

load_dotenv()

def get_conn():
    conn = http.client.HTTPSConnection("in05-b060be9f89d5787.serverless.gcp-us-west1.cloud.zilliz.com")
    return conn

def upload_clips(conn, lecture_id, chunk_ids, embeddings):

    data = [{"chunk_id": chunk_id, "lecture_id": lecture_id, "embedding": embedding}
            for chunk_id, embedding in zip(chunk_ids, embeddings)]

    payload = json.dumps({
        "collectionName": "clips",
        "data": data
    })

    headers = {
        'Authorization': os.getenv("ZILLIZ_AUTH_TOKEN"),
        'Accept': "application/json",
        'Content-Type': "application/json"
    }

    conn.request("POST", "/v2/vectordb/entities/insert", body=payload, headers=headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))

async def batch_clip_query(conn, queries: List[str]):
    data = [embed_text(query) for query in queries]

    payload = json.dumps({
        "collectionName": "clips",
        "data": data,
        "annsField": "embedding",
        "limit": 10
    })

    headers = {
        'Authorization': os.getenv("ZILLIZ_AUTH_TOKEN"),
        'Accept': "application/json",
        'Content-Type': "application/json"
    }

    conn.request("POST", "/v2/vectordb/entities/search", body=payload, headers=headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))