# Sales Record Manager

A terminal-based sales record manager and data-analysis project. The project creates a deterministic CSV dataset with 100 transactions on first run and keeps subsequent additions, edits, and deletions in `data/sales_data.csv`.

## Setup

From this folder, install the dependencies and start the interactive application:

```powershell
python -m pip install -r requirements.txt
python main.py
```

Select menu options to add, display, search, update, or delete transactions, or generate the summary report. To print the report and exit without opening the menu:

```powershell
python main.py --report
```

The report demonstrates CSV input, Pandas DataFrames, row/column selection, filtering, sorting, GroupBy aggregation, missing-region handling, descriptive statistics, and NumPy 1D/2D array indexing, slicing, and calculations.

## Project files

- `main.py` — interactive menu and command-line entry point
- `data_manager.py` — sample dataset creation and CSV-backed record operations
- `analysis.py` — Pandas and NumPy reporting
- `formatter.py` — terminal table presentation
- `data/sales_data.csv` — generated project dataset (100 initial records)
