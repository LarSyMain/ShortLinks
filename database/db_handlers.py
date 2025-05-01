import sqlite3

class DBhandler():
    def __init__(self, db_name=r"database/URLs.db"):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        try:
            with sqlite3.connect(self.db_name) as conn:
                coursor = conn.cursor()
                coursor.execute(
                    """
                        CREATE TABLE IF NOT EXISTS links(
                            URL TEXT,
                            URLShort TEXT
                        )

                    """
                )
                conn.commit()
        except Exception as e:
            pass

    def add_URL(self, URLold=None, URLshort=None):
        try:
            with sqlite3.connect(self.db_name) as conn:
                coursor = conn.cursor()
                coursor.execute(
                    """
                        INSERT INTO links (URL, URLShort) VALUES(?, ?)

                    """,(URLold, URLshort)
                )
                conn.commit()
        except Exception as e:
            pass

    def chek_URL(self):
        try:
            with sqlite3.connect(self.db_name) as conn:
                coursor = conn.cursor()
                coursor.execute(
                    """
                       SELECT URL FROM links

                    """
                )
                conn.commit()
                result = coursor.fetchall()
                return [row[0] for row in result]
        except Exception as e:
            pass

    def chek_Short_URL(self):
        try:
            with sqlite3.connect(self.db_name) as conn:
                coursor = conn.cursor()
                coursor.execute(
                    """
                       SELECT URLShort FROM links

                    """
                )
                conn.commit()
                result = coursor.fetchall()
                return [row[0] for row in result]
        except Exception as e:
            pass

    def get_URL(self, URLold=None):
        try:
            with sqlite3.connect(self.db_name) as conn:
                coursor = conn.cursor()
                coursor.execute(
                    """
                       SELECT URLShort FROM links WHERE URL = (?)

                    """, (URLold)
                )
                conn.commit()
                return coursor.fetchall()
        except Exception as e:
            pass