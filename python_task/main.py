# Import argparse module from standard library to parse CLI arguments
import argparse
import sys
from db_manager import DatabaseManager
from exporters import ExportFormatSelector
from parsers import RoomsJSONParser, StudentsJSONParser

def setup_argparser() -> argparse.ArgumentParser:
    """Configures comman-line interface arguments for the program."""
    # Instantiate ArgumentParser with application description
    parser = argparse.ArgumentParser(
        description="Dormitory Data Processing CLI Tool"
    )

    # Add required positional argument for rooms JSON input path
    parser.add_argument(
        "rooms_path", type=str, help="Path to rooms JSON file"
    )

    # Add required positional argument for students JSON input path
    parser.add_argument(
        "students_path", type=str, help="Path to students JSON file"
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

# Query 1: Returns a list of rooms and the total count of students in each room
QUERY_ROOMS_WITH_STUDENT_COUNT = """
    SELECT 
        r.id AS room_id,
        r.name AS room_name,
        COUNT(s.id) AS student_count
    FROM rooms r
    LEFT JOIN students s ON r.id = s.room
    GROUP BY r.id, r.name
    ORDER BY r.id;
"""

# Query 2: Returns top 5 rooms with the lowest average student age
QUERY_TOP5_ROOMS_LOWEST_AVG_AGE = """
    SELECT 
        r.id AS room_id,
        r.name AS room_name,
        AVG(EXTRACT(YEAR FROM AGE(CURRENT_DATE, s.birthday))) AS avg_age
    FROM rooms r
    JOIN students s ON r.id = s.room
    GROUP BY r.id, r.name
    ORDER BY avg_age ASC
    LIMIT 5;
"""

# Query 3: Returns top 5 rooms with the highest age difference among resident students
QUERY_TOP5_ROOMS_HIGHEST_AGE_DIFF = """
    SELECT 
        r.id AS room_id,
        r.name AS room_name,
        MAX(EXTRACT(YEAR FROM AGE(CURRENT_DATE, s.birthday))) - 
        MIN(EXTRACT(YEAR FROM AGE(CURRENT_DATE, s.birthday))) AS age_difference
    FROM rooms r
    JOIN students s ON r.id = s.room
    GROUP BY r.id, r.name
    ORDER BY age_difference DESC
    LIMIT 5;
"""

# Query 4: Returns a list of rooms inhabited by students of mixed sexes
QUERY_ROOMS_WITH_MIXED_SEXES = """
    SELECT 
        r.id AS room_id,
        r.name AS room_name
    FROM rooms r
    JOIN students s ON r.id = s.room
    GROUP BY r.id, r.name
    HAVING COUNT(DISTINCT s.sex) > 1
    ORDER BY r.id;
"""

def main():
    """Main execution function coordinating database setup, parsing, query execution, and export."""
    # Instantiate argument parser and parse command line parameters
    parser = setup_argparser()
    args = parser.parse_args()

    # Build database configuration dictionary from parsed CLI arguments
    db_config = {
        "dbname": args.db_name,
        "user": args.db_user,
        "password": args.db_password,
        "host": args.db_host,
        "port": args.db_port,
    }

    # Instantiate DatabaseManager using the configuration dictionary
    db = DatabaseManager(db_config)

    # Establish connection to PostgreSQL database server
    db.connect()

    # Wrap operations in try-finally block to guarantee connection cleanup
    try:
        # Execute DDL SQL files to build tables and performance indexes
        print("Initializing database schema and indexes...")
        db.execute_script("schema.sql")
        db.execute_script("indexes.sql")

        # Parse input JSON files into lists of database tuple records
        print("Parsing input JSON data files...")
        rooms_tuples = RoomsJSONParser().parse(args.rooms_path)
        students_tuples = StudentsJSONParser().parse(args.students_path)

        # Perform batch insertion using original insert_bulk method
        print("Inserting records into PostgreSQL database...")
        db.insert_bulk(
            "INSERT INTO rooms (id, name) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING;",
            rooms_tuples,
        )
        db.insert_bulk(
            "INSERT INTO students (id, name, birthday, sex, room) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING;",
            students_tuples,
        )

        # Execute analytical SQL queries and collect dictionary results
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

        # Obtain the appropriate exporter instance using ExportFormatSelector
        exporter = ExportFormatSelector.get_exporter(args.format)

        # Iterate through query dictionary results and export each to an output file
        print(f"Exporting query results in '{args.format.upper()}' format...")
        for query_name, result_data in query_results.items():
            output_filename = f"{query_name}.{args.format}"
            exporter.export(result_data, output_filename)
            print(f"Saved output file: {output_filename}")

        # Ensure database connection is closed regardless of success or failure
    finally:
        db.close()

        # Print success message upon pipeline completion
    print("Data processing pipeline completed successfully!")

# Standard Python conditional check ensuring script executes directly
if __name__ == "__main__":
    main()