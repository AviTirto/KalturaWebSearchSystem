import fastapi
from query_manager import QueryManager
from crud import get_lesson_by_link

app = fastapi()
qm = QueryManager()


@app.get("/")
def get_lecture_snippets(query : str):
    summaries = qm.query(query)

    lessons = []
    for summary in summaries:
        lessons+=[get_lesson_by_link(summary.link)]
    print(lessons)


    
