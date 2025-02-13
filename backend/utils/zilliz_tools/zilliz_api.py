import http.client
import json
import os
from dotenv import load_dotenv

load_dotenv()

def get_conn():
    conn = http.client.HTTPSConnection("in05-b060be9f89d5787.serverless.gcp-us-west1.cloud.zilliz.com")
    return

def upload_clips(conn, lecture_id, chunk_ids, embeddings):
    conn = http.client.HTTPSConnection("in05-b060be9f89d5787.serverless.gcp-us-west1.cloud.zilliz.com")

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