"""UNICEF SR4S - Deficiency-Driven Fund Allocation Model (v2)"""
import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = 'data/processed/sr4s_ahmedabad.db'
OUT = Path('outputs/tables')

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    ranking = pd.read_sql('SELECT * FROM v_school_safety_ranking ORDER BY ahmedabad_safety_rank', conn)
    gaps = pd.read_sql('SELECT * FROM v_infrastructure_gaps', conn)
    rx = pd.read_sql('SELECT * FROM v_prescribed_interventions', conn)
    conn.close()

    rx['students_protected_per_1k_inr'] = ((rx['projected_star_rating_increase'] * rx['student_population']) / (rx['estimated_cost_inr'] / 1000.0)).round(2)

    # Primary prescription per school = most severely failing component
    primary = rx.loc[rx.groupby('school_name')['component_score'].idxmin()].copy()
    primary = primary.sort_values('students_protected_per_1k_inr', ascending=False)

    # City-wide treatment portfolio
    portfolio = rx.groupby('measure_name').agg(
        prescribed_schools=('school_id', 'count'),
        avg_students_protected_per_1k_inr=('students_protected_per_1k_inr', 'mean'),
        total_estimated_cost_inr=('estimated_cost_inr', 'sum'),
    ).round(2).reset_index().sort_values('prescribed_schools', ascending=False)

    print('=' * 80)
    print('🚨 UNICEF SR4S: AHMEDABAD PRIORITY INTERVENTION REPORT (v2)')
    print('=' * 80)
    print('\n🏆 TOP 5 HIGHEST-RISK SCHOOLS + PRESCRIBED TREATMENT:')
    top5 = ranking.head(5).merge(primary[['school_name', 'measure_name', 'diagnosed_component', 'component_score']], on='school_name', how='left')
    top5['measure_name'] = top5['measure_name'].fillna('Monitor only (already >=4 stars)')
    top5['diagnosed_component'] = top5['diagnosed_component'].fillna('-')
    for _, r in top5.iterrows():
        print(f"  {int(r['ahmedabad_safety_rank'])}. {r['school_name']} ({r['zone']})")
        print(f"     └─ Risk {r['risk_index']} | {r['star_rating']} stars | Dx: {r['diagnosed_component']} ({r['component_score']}/100)")
        print(f"     └─ Rx: {r['measure_name']}")
    print('\n🏗️ CITY-WIDE TREATMENT PORTFOLIO:')
    print(portfolio.to_string(index=False))

    ranking.to_csv(OUT / 'school_ranking.csv', index=False)
    primary.to_csv(OUT / 'top_interventions.csv', index=False)
    portfolio.to_csv(OUT / 'treatment_portfolio.csv', index=False)
    gaps.to_csv(OUT / 'infrastructure_gaps.csv', index=False)
    print('\n✅ Exports refreshed in outputs/tables/')

if __name__ == '__main__':
    main()
