
class Chunk:
    def __init__(self, id: str, index: int, document: str, start_time: str, end_time: str, seconds: float, link: str):
        self.id = id
        self.index = index
        self.subtitle = document
        self.start_time = start_time
        self.end_time = end_time
        self.seconds = seconds
        self.link = link

    def get_index(self):
        return self.index

    def get_subtitle(self):
        return self.subtitle

    def get_start_time(self):
        return self.start_time

    def get_end_time(self):
        return self.end_time

    def get_seconds(self):
        return self.seconds

    def get_link(self):
        return self.link



class Lesson:
    def __init__(self, date: str, embed_link: str, title: str, link: str):
        self.date = date
        self.embed_link = embed_link
        self.title = title
        self.link = link

    def get_date(self):
        return self.date

    def get_embed_link(self):
        return self.embed_link

    def get_title(self):
        return self.title

    def get_link(self):
        return self.link


class Summary():
    def __init__(self, id, summary: str, start_time: str, end_time: str, seconds: int, link: str):
        self.id = id
        self.subtitle = summary
        self.start_time = start_time
        self.end_time = end_time
        self.seconds = seconds
        self.link = link