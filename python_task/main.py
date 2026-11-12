import argparse
from pathlib import Path
from dormitory.db import DatabaseManager
from dormitory.parsers import JSONFileParser
from dormitory.exporters import ExportFormatSelector
from dormitory.queries import (
    QUERY_ROOMS_WITH_STUDENT_COUNT,
    QUERY_TOP5_ROOMS_LOWEST_AVG_AGE,
    QUERY_TOP5_ROOMS_HIGHEST_AGE_DIFF,
    QUERY_ROOMS_WITH_MIXED_SEXES
)


# Base directory resolution for absolute paths to SQL scripts
BASE_DIR = Path(__file__).resolve().parent


def setup_argparser() -> argparse.ArgumentParser:
    """Configures comman-line interface arguments for the program."""
    parser = argparse.ArgumentParser(
        description="Dormitory Data Processing CLI Tool"
    )

    # Add required positional argument for students JSON input path
    parser.add_argument(
        "students_path", type=str, help="Path to students JSON file"
    )

    # Add required positional argument for rooms JSON input path
    parser.add_argument(
        "rooms_path", type=str, help="Path to rooms JSON file"
    )

    # Add optional argument for export format choice defaulting to json
    parser.add_argument(
        "-f",
        "--format",
        choices=["json", "xml"],
        default="json",
        help="Export format choice: json or xml (default: json)",
    )

    # Add optional database server hostname flag
    parser.add_argument(
        "--db-host",
        type=str,
        default="localhost",
        help="Database server host address",
    )

    # Add optional database server port flag
    parser.add_argument(
        "--db-port", type=int, default=5332, help="Database server port number"
    )

    # Add optional target database name flag
    parser.add_argument(
        "--db-name",
        type=str,
        default="dormitory_db",
        help="Target database name",
    )

    # Add optional database username flag
    parser.add_argument(
        "--db-user", type=str, default="postgres", help="Database username"
    )

    # Add optional database user password flag
    parser.add_argument(
        "--db-password",
        type=str,
        default="postgres",
        help="Database user password",
    )

    # Return the configured argument parser instance
    return parser


def main():
    """Main execution function coordinating database setup, parsing, query execution, and export."""
    parser = setup_argparser()
    args = parser.parse_args()

    db_config = {
        "dbname": args.db_name,
        "user": args.db_user,
        "password": args.db_password,
        "host": args.db_host,
        "port": args.db_port,
    }

    db = DatabaseManager(db_config)
    db.connect()

    try:
        print("Initializing database schema and indexes...")
        db.execute_script(BASE_DIR / "sql" / "schema.sql")
        db.execute_script(BASE_DIR / "sql" / "indexes.sql")

        print("Parsing input JSON data files...")
        rooms_data = JSONFileParser.parse(args.rooms_path)
        students_data = JSONFileParser.parse(args.students_path)

        # Extract values by explicit keys to guarantee exact column order for SQL INSERT
        rooms_tuples = [
            (item["id"], item["name"]) for item in rooms_data
        ]
        students_tuples = [
            (item["id"], item["name"], item["birthday"], item["sex"], item["room"]) for item in students_data
        ]

        print("Inserting records into PostgreSQL database...")
        # ON CONFLICT DO NOTHING ensures the script remains idempotent
        # and can be safely re-run without duplicate key errors
        db.insert_bulk(
            "INSERT INTO rooms (id, name) VALUES %s ON CONFLICT (id) DO NOTHING;",
            rooms_tuples,
        )
        db.insert_bulk(
            "INSERT INTO students (id, name, birthday, sex, room) VALUES %s ON CONFLICT (id) DO NOTHING;",
            students_tuples,
        )

        print("Executing analytical queries...")
        query_results = {
            "rooms_with_student_count": db.fetch_all(
                QUERY_ROOMS_WITH_STUDENT_COUNT
            ),
            "top5_rooms_lowest_avg_age": db.fetch_all(
                QUERY_TOP5_ROOMS_LOWEST_AVG_AGE
            ),
            "top5_rooms_highest_age_diff": db.fetch_all(
                QUERY_TOP5_ROOMS_HIGHEST_AGE_DIFF
            ),
            "rooms_with_mixed_sexes": db.fetch_all(
                QUERY_ROOMS_WITH_MIXED_SEXES
            ),
        }

        exporter = ExportFormatSelector.get_exporter(args.format)

        print(f"Exporting query results in '{args.format.upper()}' format...")
        for query_name, result_data in query_results.items():
            output_filename = f"{query_name}.{args.format}"
            exporter.export(result_data, output_filename)
            print(f"Saved output file: {output_filename}")

    finally:
        db.close()

    print("Data processing pipeline completed successfully!")


if __name__ == "__main__":
    main()