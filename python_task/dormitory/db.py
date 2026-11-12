import psycopg2
from psycopg2.extras import RealDictCursor, execute_values


class DatabaseManager:
    """
    Low-level database manager for executing raw PostgreSQL scripts.
    """
    def __init__(self, config: dict):
        self.config = config
        self.connection = None

    def connect(self):
        """Establishes an active connection to PostgreSQL."""
        self.connection = psycopg2.connect(**self.config)

    def close(self):
        """Safely closes the active database connection if it is open."""
        if self.connection and not self.connection.closed:
            self.connection.close()

    def execute_script(self, script_path: str):
        """Reads an external SQL script file and executes it on the database."""
        with self.connection.cursor() as cursor:
            with open(script_path, "r", encoding="utf-8") as file:
                sql_script = file.read()
                cursor.execute(sql_script)
        self.connection.commit()

    def insert_bulk(self, query: str, data: list):
        """Performs a fast batch insert of multiple rows into a table."""
        with self.connection.cursor() as cursor:
            execute_values(cursor, query, data)
        self.connection.commit()

    def fetch_all(self, query: str) -> list[dict]:
        """Executes a SELECT query and returns rows as a list of dictionaries."""
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]