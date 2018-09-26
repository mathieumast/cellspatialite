import os
import database
import pandas as pd

class Treatment:
    def __init__(self, input, output):
        self.input = input
        self.db = database.Database(output)

    def start(self):
        self.db.remove_file()
        self.db.connect()
        self.db.define()
        self.import_all()
        self.db.disconnect()

    def import_all(self):
        df =pd.read_csv(self.input, names = ['date','x','y','z','val'], sep=',', header=0)
        print(df.head(1))
        for row in df.itertuples():
            self.import_row(row)

    def import_row(self, row):
        self.db.insert_into_data(row)
        for level in range(1, 12):
            self.db.upsert_into_cell_level(level, row)