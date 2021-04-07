import psycopg2

class Database:
    def __init__(self):
        self.data_base = psycopg2.connect(
            host='localhost',
            user='postgres',
            database='nasiba_db',
            password='nasiba69'
        )
        self.cursor = self.data_base.cursor()

    def create_table(self, name_table):
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {name_table}(
            id SERIAL PRIMARY KEY NOT NULL,
            photo bytea     --для jpeg
            )
        """)
        self.data_base.commit()

    def insert_data(self, name_table, *args):
        self.cursor.execute(f"""INSERT INTO {name_table}(photo) VALUES (%s)""", args)
        self.data_base.commit()

    def export_json(self):
        self.cursor.execute(f"""SELECT photo FROM afisha_photos""")
        photos = self.cursor.fetchmany(5)
        i = 1
        for photo in photos:
            print(bytes(photo))
            # with open(f'images/{i}.jpg', mode='wb') as file:
            #     file.write(photo)
            # i += 1
