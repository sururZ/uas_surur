import sqlite3

conn = sqlite3.connect("database.db")

print("Koneksi Database Berhasil")

conn.execute("CREATE TABLE datacar (name TEXT, tahun TEXT, warna TEXT, harga TEXT)")

print("Database Berhasil Dibuat")

conn.close()