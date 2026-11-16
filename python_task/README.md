# Dormitory Data Processing CLI Tool

A Python-based command-line interface (CLI) data pipeline that processes dormitory room and student records using raw PostgreSQL queries (`psycopg2`), without using an Object-Relational Mapper (ORM). The application extracts data from raw JSON datasets into a PostgreSQL database, executes complex analytical queries, and serializes the resulting reports into formatted JSON or XML files.

---

## Database Configuration

Database configuration is managed via a `.env` file to prevent hardcoding credentials in the code[cite: 1]. Create a `.env` file in the root directory with the following variables:

```env
DB_HOST=localhost
DB_PORT=5332
DB_NAME=dormitory_db
DB_USER=postgres
DB_PASSWORD=postgres
```

---

## What Was Done (Project Highlights)

1. **ETL Pipeline Implementation**: Built an end-to-end Extract, Transform, Load (ETL) workflow that reads input datasets (`rooms.json`, `students.json`), creates necessary relational schema constraints, and batch-inserts records into PostgreSQL.
2. **Raw SQL Analytics**: Written raw SQL queries using `GROUP BY`, `HAVING`, `JOIN`, and date arithmetic (`AGE()`) to compute statistical aggregations directly inside the database engine.
3. **Design Patterns**: Applied the **Factory Pattern** (`ExportFormatSelector`) to dynamically instantiate JSON or XML exporters at runtime.
4. **Performance & Optimization**: Created composite index (`idx_students_room_sex`) on (`(room, sex)`) to optimize JOINs by room and the 4th query. Created composite index (`idx_students_room_birthday`) on (`(room, birthday)`) to optimize date of birth aggregations per room in the 2nd and 3rd queries.
5. **Quality Assurance**: Created comprehensive unit tests using Python's `unittest` framework to validate parser outputs, export serializers, and factory exception handling.

---

## Project Structure

```text
.
├── dormitory/
│   ├── db.py               # Database connection & raw SQL execution manager[cite: 1]
│   ├── parsers.py          # Input JSON parsers (Rooms and Students)
│   ├── exporters.py        # JSON & XML output exporters with Factory pattern
│   └── queries.py          # SQL queries repository
├── sql/
│   ├── schema.sql          # DDL script creating 'rooms' and 'students' tables
│   └── indexes.sql         # SQL script creating database performance indexes
├── tests/
│   ├── test_parsers.py     # Unit tests for parsers[cite: 1]
│   └── test_exporters.py   # Unit tests for exporters and factory[cite: 1]
├── main.py                 # Main CLI entry point orchestrating the pipeline
├── .env                    # Environment variables configuration file
├── requirements.txt        # Project dependencies
├── rooms.json              # Input JSON file containing room records[cite: 3]
└── students.json           # Input JSON file containing student records[cite: 3]
```

---

## CLI Usage Example

```bash
# Export reports to JSON (default format)
python main.py data/students.json data/rooms.json

# Export reports to XML format
python main.py data/students.json data/rooms.json -f xml
```

---

### 4. Файл `sql/indexes.sql`
Added a second index to optimize operations with the `birthday` field, and added a required newline at the end of the file.

```sql
-- Composite index on (room, sex) to optimize room JOINs and the 4th query (with DISTINCT sex)[cite: 1, 2].
CREATE INDEX IF NOT EXISTS idx_students_room_sex ON students(room, sex);

-- Composite index on (room, birthday) for the 2nd and 3rd queries (birthday aggregations per room)[cite: 1, 2].
CREATE INDEX IF NOT EXISTS idx_students_room_birthday ON students(room, birthday);