import argparse
from pathlib import Path
import sys

try:
    import duckdb
except ImportError as exc:
    raise SystemExit(
        "duckdb is not installed. Run `pip install duckdb` or use the provided virtual environment."
    ) from exc


def format_rows(column_names, rows):
    if not rows:
        return "(no rows returned)"

    widths = [len(name) for name in column_names]
    for row in rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(str(value)))

    sep = "+" + "+".join("-" * (w + 2) for w in widths) + "+"
    header = "| " + " | ".join(name.ljust(widths[idx]) for idx, name in enumerate(column_names)) + " |"

    lines = [sep, header, sep]
    for row in rows:
        lines.append(
            "| " + " | ".join(str(value).ljust(widths[idx]) for idx, value in enumerate(row)) + " |"
        )
    lines.append(sep)
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run a DuckDB query against the Northwind DuckDB database.",
        epilog="Example: python query_duckdb.py --sql \"SELECT * FROM customer LIMIT 5\"",
    )
    default_db = Path("northwind_dw_duckdb") / "dev.duckdb"
    parser.add_argument(
        "--db",
        default=str(default_db),
        help="Path to the DuckDB database file (default: northwind_dw_duckdb/dev.duckdb)",
    )
    parser.add_argument(
        "--sql",
        default=None,
        help="SQL query to execute. If omitted, the script lists available tables.",
    )
    parser.add_argument(
        "--table",
        default=None,
        help="Table name to query. If --sql is omitted, the script selects from this table.",
    )
    args = parser.parse_args()

    db_path = Path(args.db)
    if not db_path.exists():
        print(f"DuckDB file not found: {db_path}")
        print("Please run dbt from northwind_dw_duckdb first, or update --db to a valid DuckDB file.")
        return 1

    conn = duckdb.connect(str(db_path))

    if args.sql is None:
        if args.table:
            args.sql = f"SELECT * FROM {args.table} LIMIT 50"
            print(f"Querying table: {args.table}\n")
        else:
            args.sql = (
                "SELECT table_schema, table_name "
                "FROM information_schema.tables "
                "WHERE table_type = 'BASE TABLE' "
                "ORDER BY table_schema, table_name"
            )
            print(f"Listing tables in {db_path}\n")

    try:
        result = conn.execute(args.sql)
        rows = result.fetchall()
        column_names = [desc[0] for desc in result.description]
        print(format_rows(column_names, rows))
    except Exception as exc:
        print(f"Error executing SQL: {exc}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
