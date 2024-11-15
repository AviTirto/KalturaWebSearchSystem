from db import Storage
from lecture_manager import generate_unique_id

class QueryManager():
    def __init__(self):
        self.db = Storage()

    def retrieve_chunks(self, question: str):
        return self.db.query(question)

    def remove_duplicate_chunks(self, metadatas, documents, ids):
        
        uuids = set()
        unique_metadatas = []
        unique_documents = []
        unique_ids = []
        for i in range(len(ids)):
            if ids[i] in uuids:
                continue

            uuids.add(ids[i])
            unique_metadatas += [metadatas[i]]
            unique_documents += [documents[i]]
            unique_ids += [ids[i]]

        return (unique_ids, unique_metadatas, unique_documents)


    def get_neighbors(self, lect_info):
        index = lect_info['index']
        link = lect_info['link']

        n_chunks = len(
            self.db.get_lectures(
                where = {
                    'link' : link
                }
            )['metadatas']
        )

        ids = [generate_unique_id(link, i) for i in range(max(index - 2, 0), min(index + 3, n_chunks))]
        
        neighbors = self.db.get_lectures(
            ids = ids
        )

        n_lect_infos = neighbors['metadatas']
        n_docs = neighbors['documents']

        return {
            'lect_info': n_lect_infos,
            'docs': n_docs
        }
        


    def query(input: str):
        pass