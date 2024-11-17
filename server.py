import fastapi
from query_manager import QueryManager

app = fastapi()
process_query = QueryManager()


@app.get("/")
def get_lecture_snippets(query : str):
    x = process_query.query(query) 

    
