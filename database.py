import os
import sqlite3
import cluster

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

    def insert_into_data(self, data):
        c = self.conn.cursor()
        # Execute sql 
        c.execute('''INSERT INTO data (date, val, geometry)
            VALUES (?, ?, GeomFromText(?, 3857))''',
            (data.date, data.val, 'POINTZ(%s %s %s)' % (data.x, data.y, data.z)))
    
    def upsert_into_cell_level(self, level, data):
        pos = cluster.Pos(data.x, data.y)
        cell = pos.cell(level)
        c = self.conn.cursor()
        id = 'cluster.%s.%s.%s' % (cell.level, cell.q, cell.r)
        c.execute('''SELECT count, sum FROM cell%s WHERE id = ?''' % (level), (id,))
        row = c.fetchone()
        if row is None:
            c.execute('''INSERT INTO cell%s (id, count, sum, average, geometry)
                VALUES (?, ?, ?, ?, GeomFromText(?, 3857))
                ''' % (level),
                (id, 1, data.val, data.val, cell.wkt()))
        else:
            count = row[0] + 1
            sum = row[1] + data.val
            average = float(sum) / float(count)
            c.execute('''UPDATE cell%s
                SET count = ?, sum = ?, average = ?
                WHERE id = ?''' % (level),
                (count, sum, average, id))

    def define(self):
        c = self.conn.cursor()
        # Initialize spatial cartridge  
        c.execute('SELECT InitSpatialMetaData(1)')
        # Create tables
        # Table data
        c.execute('''CREATE TABLE data
            (date TEXT, val REAL)''')
        c.execute('''SELECT AddGeometryColumn('data', 'geometry', 3857, 'POINT', 'XYZ', 1)''')
        for level in range(1, 12):
            # Table cellx
            c.execute('''CREATE TABLE cell%s
                (id TEXT NOT NULL PRIMARY KEY, count INTEGER, sum REAL, average REAL)''' % (level))
            c.execute('''SELECT AddGeometryColumn('cell%s', 'geometry', 3857, 'POLYGON', 'XY', 1)''' % (level))

    def commit(self):
        # Commit
        self.conn.commit()

    def disconnect(self):
        # Commit
        self.conn.commit()
        # Close
        self.conn.close()
