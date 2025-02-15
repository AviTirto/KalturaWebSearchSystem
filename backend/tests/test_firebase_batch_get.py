import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, project_root)

from backend.utils.firebase_tools.firebase_api import get_db, get_lecture_batch

db = get_db()

res = get_lecture_batch(db, [[159560715833883834], [848603976102201492, 33486559523529952]])

print('The number of lectures is: ', len(res))

print('The first lecture is: ', res[159560715833883834]['title'])

print('The second lecture is: ', res[848603976102201492]['title'])

print('The third lecture is: ', res[33486559523529952]['title'])