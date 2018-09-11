import os
import sqlite3

class Database:
    def __init__(self, name):
        self.name = name

    def remove_file(self):
        if os.path.exists(self.name):
            # remove file
            os.remove(self.name)

    def connect(self):
        with sqlite3.connect(self.name) as conn:
            # Active Spatialite extension
            conn.enable_load_extension(True)
            conn.load_extension('/usr/lib64/mod_spatialite.so')
            self.conn = conn

    def insert(self, data):
         # Execute sql
        self.conn.execute('''INSERT INTO data
                    (date, val, geometry)
                    VALUES (?,?, GeomFromText(?, 3857))''',
                    (data.date, data.val, 'POINTZ({} {} {})'.format(data.x, data.y, data.z)))

    def define(self):
        # Initialize spatial cartridge  
        self.conn.execute('SELECT InitSpatialMetaData(1)')
        # Create table
        self.conn.execute('''CREATE TABLE data
                    (date TEXT, val REAL)''')
        self.conn.execute('''SELECT AddGeometryColumn('data', 'geometry', 3857, 'POINT', 'XYZ', 1)''')       
        # Commit
        self.conn.commit()

    def disconnect(self):
        # Commit
        self.conn.commit()
        # Close
        self.conn.close()
