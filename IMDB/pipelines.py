# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
#from itemadapter import ItemAdapter
import sqlite3

class SQLlitePipeline(object):

    def open_spider(self, spider):
        self.connection = sqlite3.connect("imdb.db")
        self.c = self.connection.cursor()
        try:
            self.c.execute('''
                CREATE TABLE best_movies(
                    title TEXT,
                    duration TEXT,
                    genre TEXT,
                    year TEXT,
                    rating TEXT
                )
            
            ''')
            self.connection.commit()
        except sqlite3.OperationalError:
            pass

    def close_spider(self, spider):
        self.connection.close()


    def process_item(self, item, spider):
        data=[item.get('title'),
            item.get('duration'),
            item.get('genre')[0],
            item.get('year'),
            item.get('rating')]
        self.c.execute('''
            INSERT INTO best_movies (title,duration,genre,year,rating) VALUES(?,?,?,?,?)
        ''', tuple(data))
        self.connection.commit()
        return item

    