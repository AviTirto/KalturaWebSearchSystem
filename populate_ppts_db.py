# from app.services.PPT_manager import PPTManager
# from app.models.ChromaModel.records import PPTcdb
# import time

# cdb = PPTcdb()
# cdb.db.delete_collection('ppts')
# ppt_manager = PPTManager()


# # ppt_manager.pdf_files = ['./Econ_301_PPT/Chapter 12 PPT.pdf', './Econ_301_PPT/Chapter 2 PPT.pdf', './Econ_301_PPT/Chapter 5 PPT.pdf', './Econ_301_PPT/Chapter 14 PPT.pdf', './Econ_301_PPT/Chapter 15 PPT.pdf', './Econ_301_PPT/Chapter 6 PPT.pdf', './Econ_301_PPT/Chapter 7 PPT.pdf']


# start = time.time()
# ppt_manager.populate_ppts()
# end = time.time()
# print(end - start)

# metas = ppt_manager.cdb.ppts.get()['metadatas']
# docs = ppt_manager.cdb.ppts.get()['documents']
# print(ppt_manager.cdb.db.get_collection('ppts').count())

import os
from backend.utils.cloudfareR2_tools.cloudfareR2_api import *

econ_dir_path = r"./Econ_301_PPT"
r2_client = get_cloudfareR2()

if os.path.exists(econ_dir_path):
    for path in os.listdir(econ_dir_path):
        file_path = os.path.join(econ_dir_path, path)
        with open(file_path, 'rb') as file:
            data = file.read()
            object_key = "Econ-301/" + path.replace(" ", "-") # Making format compatible with what R2 wants
            upload_file(r2_client, data, object_key)


