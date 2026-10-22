# Dormitory Data Processing CLI Tool

A Python-based command-line interface (CLI) data pipeline that processes dormitory room and student records using raw PostgreSQL queries (`psycopg2`), without using an Object-Relational Mapper (ORM). The application extracts data from raw JSON datasets into a PostgreSQL database, executes complex analytical queries, and serializes the resulting reports into formatted JSON or XML files.

---

## What Was Done (Project Highlights)

1. **ETL Pipeline Implementation**: Built an end-to-end Extract, Transform, Load (ETL) workflow that reads input datasets (`rooms.json`, `students.json`), creates necessary relational schema constraints, and batch-inserts records into PostgreSQL.
2. **Raw SQL Analytics**: Written raw SQL queries using `GROUP BY`, `HAVING`, `JOIN`, and date arithmetic (`AGE()`) to compute statistical aggregations directly inside the database engine.
3. **Design Patterns**: Applied the **Strategy Pattern** for configurable file parsers and the **Factory Pattern** (`ExportFormatSelector`) to dynamically instantiate JSON or XML exporters at runtime.
4. **Performance & Optimization**: Created foreign key indexes on foreign key relationships to accelerate database join and grouping operations.
5. **Quality Assurance**: Created comprehensive unit tests using Python's `unittest` framework to validate parser outputs, export serializers, and factory exception handling.

---

## Project Structure

```text
.
├── db_manager.py       # Database connection & raw SQL execution manager
├── parsers.py          # Input JSON parsers (Rooms and Students)
├── exporters.py        # JSON & XML output exporters with Factory pattern
├── schema.sql          # DDL script creating 'rooms' and 'students' tables
├── indexes.sql         # SQL script creating database performance indexes
├── main.py             # Main CLI entry point orchestrating the pipeline
├── test1.py            # Unit test suite for parsers, exporters, and factory
├── rooms.json          # Input JSON file containing room records
└── students.json       # Input JSON file containing student records