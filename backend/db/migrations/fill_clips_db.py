from ....backend.utils.scraper_tools.kaltura_scraper import *
from ....backend.utils.parsing_tools.srt_parser import *
from ....backend.utils.zilliz_tools.zilliz_api import *
from ....backend.utils.encoders import *

PLAYLIST_LINK = 'https://mediaspace.wisc.edu/playlist/dedicated/1_pdlead8k/1_krmy057m'

lecture_links = get_lessons(PLAYLIST_LINK)

for lecture in lecture_links:
    link = lecture['lecture_link']
    title = lecture['title']

    lecture_id = generate_unique_int64(link)

    page_info = scrape_lecture_page(link)
    
    if not page_info:
        continue

    date = page_info['date']
    embed_link = page_info['embed_link']
    chunks = parse_chunks(page_info['file_name'])



