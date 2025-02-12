from app.services.PPT_manager import PPTManager
from app.models.ChromaModel.records import PPTcdb
import time

cdb = PPTcdb()
cdb.db.delete_collection('ppts')
ppt_manager = PPTManager()


# ppt_manager.pdf_files = ['./Econ_301_PPT/Chapter 12 PPT.pdf', './Econ_301_PPT/Chapter 2 PPT.pdf', './Econ_301_PPT/Chapter 5 PPT.pdf', './Econ_301_PPT/Chapter 14 PPT.pdf', './Econ_301_PPT/Chapter 15 PPT.pdf', './Econ_301_PPT/Chapter 6 PPT.pdf', './Econ_301_PPT/Chapter 7 PPT.pdf']


start = time.time()
ppt_manager.populate_ppts()
end = time.time()
print(end - start)

metas = ppt_manager.cdb.ppts.get()['metadatas']
docs = ppt_manager.cdb.ppts.get()['documents']
print(ppt_manager.cdb.db.get_collection('ppts').count())