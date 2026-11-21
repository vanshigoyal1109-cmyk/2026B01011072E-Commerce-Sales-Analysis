"""Small terminal-formatting helpers shared by the CLI and reports."""

import pandas as pd


def print_table(rows, include_index=False):
    """Display dictionaries or a DataFrame in a readable terminal table."""
    if isinstance(rows, pd.DataFrame):
        if rows.empty:
            print("(no records)")
        else:
            print(rows.to_string(index=include_index))
        return
    rows = list(rows)
    if not rows:
        print("(no records)")
        return
    columns = list(rows[0].keys())
    widths = {
        column: max(len(column), *(len(str(row.get(column, ""))) for row in rows))
        for column in columns
    }
    print(" | ".join(column.ljust(widths[column]) for column in columns))
    print("-+-".join("-" * widths[column] for column in columns))
    for row in rows:
        print(" | ".join(str(row.get(column, "")).ljust(widths[column]) for column in columns))
