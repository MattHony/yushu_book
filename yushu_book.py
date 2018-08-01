from app.libs.httper import Http
from flask import current_app


class YuShuBook:
    # per_page = 15
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&start={}&count={}'

    def __init__(self):
        self.total = 0
        self.books = []

    def search_by_isbn(self, isbn):
        url = self.isbn_url.format(isbn)
        result = Http.get(url)
        # 返回result为json格式的dict
        # book = query_from_mysql(isbn)
        # if book:
        #     return book
        # else:
        #     save(result)
        self.__fill_single(result)

    def __fill_single(self, data):
        if data:
            self.total = 1
            self.books.append(data)

    def __fill_collection(self, data):
        self.total = data['total']
        self.books = data['books']

    def search_by_keyword(self, keyword, page=1):
        # url = cls.isbn_url.format(keyword, cls.per_page, (page-1)*cls.per_page)
        url = self.isbn_url.format(keyword, current_app.config['PER_PAGE'], self.calculate_start(page))
        result = Http.get(url)
        self.__fill_collection(result)

    @classmethod
    def calculate_start(cls, page):
        return (page-1) * current_app.config['PER_PAGE']
