"""UNICEF SR4S - SQLite ETL Loader. Run: python src/etl/load_to_sqlite.py"""
import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = Path('data/processed/sr4s_ahmedabad.db')
RAW = Path('data/raw')
TABLES = {
    'schools_dim': ('schools_dim.csv', []),
    'irap_audit_logs': ('irap_audit_logs.csv', ['audit_date', 'sync_date']),
    'sky_satellite_metrics': ('sky_satellite_metrics.csv', []),
    'countermeasure_costs': ('countermeasure_costs.csv', []),
}

def load():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    for table, (file, dates) in TABLES.items():
        df = pd.read_csv(RAW / file, parse_dates=dates or None)
        df.to_sql(table, conn, if_exists='replace', index=False)
        print(f'  Loaded {table}: {len(df)} rows')
    conn.commit()
    conn.close()
    print('\n✅ SR4S SQLite warehouse ready at', DB_PATH)

if __name__ == '__main__':
    load()
