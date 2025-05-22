import sqlite3

def create_connection():
    return sqlite3.connect("air_quality.db")

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            lat TEXT,
            lon TEXT,
            city TEXT,
            street TEXT
        );
    """)
    conn.commit()
    conn.close()


def insert_station(station):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO stations (id, name, lat, lon, city, street)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        station['id'],
        station['stationName'],
        station['gegrLat'],
        station['gegrLon'],
        station.get('city', {}).get('name', ''),
        station.get('addressStreet', '')
    ))
    conn.commit()
    conn.close()