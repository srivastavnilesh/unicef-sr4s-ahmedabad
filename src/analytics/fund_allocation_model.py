"""UNICEF SR4S - Fund Allocation Model. Run: python src/analytics/fund_allocation_model.py"""
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
    cb = pd.read_sql('SELECT * FROM v_cost_benefit_optimization', conn)
    conn.close()

    best = cb.loc[cb.groupby('school_name')['students_protected_per_1k_inr'].idxmax()]
    best = best.sort_values('students_protected_per_1k_inr', ascending=False)

    print('=' * 80)
    print('🚨 UNICEF SR4S: AHMEDABAD PRIORITY INTERVENTION REPORT')
    print('=' * 80)
    print('\n🏆 TOP 5 HIGHEST-RISK SCHOOLS:')
    for _, r in ranking.head(5).iterrows():
        print(f"  {int(r['ahmedabad_safety_rank'])}. {r['school_name']} ({r['zone']})")
        print(f"     └─ Risk Index: {r['risk_index']} | Students: {r['student_population']} | Rating: {r['star_rating']}★")
    print('\n📉 CITY-WIDE INFRASTRUCTURE GAPS:')
    print(gaps.to_string(index=False))
    print('\n💡 TOP 5 COST-EFFECTIVE COUNTERMEASURES:')
    for _, r in best.head(5).iterrows():
        print(f"  • {r['school_name']} → {r['measure_name']}")
        print(f"    └─ Cost: ₹{int(r['estimated_cost_inr']):,} | Gain: +{r['projected_star_rating_increase']}★ | {r['students_protected_per_1k_inr']} students/₹1k")

    ranking.to_csv(OUT / 'school_ranking.csv', index=False)
    best.head(15).to_csv(OUT / 'top_interventions.csv', index=False)
    gaps.to_csv(OUT / 'infrastructure_gaps.csv', index=False)
    print('\n✅ CSV exports saved to outputs/tables/ (ready for Tableau)')

if __name__ == '__main__':
    main()
