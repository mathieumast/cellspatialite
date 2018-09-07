import sqlite3
import cell

with sqlite3.connect(":memory:") as conn:
    conn.enable_load_extension(True)
    conn.load_extension("/usr/lib64/mod_spatialite.so")
    print(conn.execute('SELECT spatialite_version()').fetchone()[0])

    cell.Cell(0, 0, 1)

