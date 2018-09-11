import os
import database
import pandas as pd

class Treatment:
    def __init__(self, name):
        self.db = database.Database(name)

    def start(self):
        self.db.remove_file()
        self.db.connect()
        self.db.define()
        self.import_data()
        self.db.disconnect()

    def import_data(self):
        df =pd.read_csv('data.csv', names = ['date','x','y','z','val'], sep=',', header=0)
        print(df.head(1))
        for row in df.itertuples():
            self.db.insert(row)