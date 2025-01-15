import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_name="taif.db"):
        self.db_path = os.path.join("database", db_name)
        self.ensure_database_directory_exists()
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def ensure_database_directory_exists(self):
        if not os.path.exists("database"):
            os.makedirs("database")

    def create_tables(self):
        tables = {
            "Passports": """
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                booking_date TEXT,
                type TEXT,
                booking_price REAL,
                purchase_price REAL,
                net_amount REAL,
                paid_amount REAL,
                remaining_amount REAL,
                status TEXT,
                receipt_date TEXT,
                receiver_name TEXT
            """,
            "Umrah": """
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                passport_number TEXT,
                phone_number TEXT,
                sponsor_name TEXT,
                sponsor_number TEXT,
                cost REAL,
                paid REAL,
                remaining_amount REAL,
                entry_date TEXT,
                exit_date TEXT,
                status TEXT
            """,
            "Trips": """
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                passport_number TEXT,
                from_place TEXT,
                to_place TEXT,
                booking_company TEXT,
                amount REAL,
                agent TEXT,
                net_amount REAL,
                trip_date TEXT,
                office_name TEXT
            """
        }
        for table_name, columns in tables.items():
            self.create_table(table_name, columns)

    def create_table(self, table_name, columns):
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        self.execute_query(query)

    def execute_query(self, query, params=()):
        self.cursor.execute(query, params)
        self.connection.commit()

    def insert(self, table_name, **kwargs):
        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join(['?'] * len(kwargs))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.execute_query(query, tuple(kwargs.values()))

    def select(self, table_name, **filters):
        query = f"SELECT * FROM {table_name}"
        if filters:
            conditions = ' AND '.join([f"{key} = ?" for key in filters])
            query += f" WHERE {conditions}"
            return self.execute_read_query(query, tuple(filters.values()))
        return self.execute_read_query(query)

    def update(self, table_name, identifier, **kwargs):
        set_clause = ', '.join([f"{key} = ?" for key in kwargs])
        query = f"UPDATE {table_name} SET {set_clause} WHERE id = ?"
        self.execute_query(query, tuple(kwargs.values()) + (identifier,))

    def delete(self, table_name, **kwargs):
        query = f"DELETE FROM {table_name} WHERE "
        conditions = ' AND '.join([f"{key} = ?" for key in kwargs])
        query += conditions
        self.execute_query(query, tuple(kwargs.values()))

    def exists(self, table_name, **kwargs):
        query = f"SELECT COUNT(*) FROM {table_name} WHERE "
        conditions = ' AND '.join([f"{key} = ?" for key in kwargs])
        query += conditions
        result = self.execute_read_query(query, tuple(kwargs.values()))
        return result[0][0] > 0

    def execute_read_query(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()