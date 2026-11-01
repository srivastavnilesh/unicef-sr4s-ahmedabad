# UNICEF SR4S: Ahmedabad Road Safety & Fund Optimization Engine

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/SQL-Advanced%20(CTEs,%20Window%20Functions)-orange?logo=sqlite&logoColor=white" alt="SQL">
  <img src="https://img.shields.io/badge/Tableau-Public-e97627?logo=tableau&logoColor=white" alt="Tableau">
  <img src="https://img.shields.io/badge/Domain-iRAP%20Certified%20%7C%20SR4S-0072CE?logo=unicef&logoColor=white" alt="Domain">
</p>

<p align="center">
  <strong>From Offline Field Audits to Government Fund Allocation: An End-to-End Data Engineering Pipeline</strong>
</p>

<p align="center">
  <a href="https://public.tableau.com/app/profile/srivastav.n/viz/UNICEFSR4SAhmedabadRoadSafetyStrategy/GujaratGovermentSR4SFundAllocationStrategyAhmedabad" target="_blank">
    <img src="https://img.shields.io/badge/View_Live_Interactive_Dashboard-Click_Here-0077B5?style=for-the-badge&logo=tableau&logoColor=white" alt="Live Dashboard">
  </a>
</p>

---

## Dashboard Preview
*(Click the image or link above to interact with the live, filterable dashboard)*
![Dashboard Preview](dashboard_preview.png)

---

## Executive Summary
This project simulates a real-world UNICEF/iRAP data contract to optimize road safety infrastructure spending for the Gujarat Government. By engineering a robust pipeline around 50 Ahmedabad schools, integrating synthetic offline SR4S audit logs with satellite-derived ("Sky") traffic metrics, the model identifies critical safety gaps and prescribes diagnosis-driven countermeasures to maximize "students protected per 1,000 INR spent."

---

## Key Business & Engineering Insights
| Metric | Insight | Strategic Action |
| :--- | :--- | :--- |
| **Spatial Risk** | 1-star and 2-star schools cluster in high-traffic zones (e.g., Maninagar, Naranpura) with risk indices >150. | Prioritize immediate structural interventions (refuge islands, sidewalks) for these blackspots. |
| **City-Wide Gaps** | 29 schools scored <50/100 on Pedestrian Crossings, the highest failure rate across all 4 audited components. | Allocate Q1 procurement budget heavily toward raised zebra crossings. |
| **Cost-Benefit ROI** | Speed Limit Signage protects ~25 students per 1,000 INR, making it the ultimate "quick win" for 3-star schools. | Deploy signage city-wide immediately, while reserving heavy capital for 1-star structural upgrades. |
| **Data Integrity** | Simulated 30% offline audit sync delays without data loss, validating field collection resilience. | Implement automated post-sync validation scripts to flag GPS drift or missing fields instantly. |

---

## System Architecture

This project follows a modern, modular data pipeline designed for real-world field conditions:

```mermaid
graph LR
    A[Offline iRAP App Logs] -->|Pandas ETL and Validation| B[SQLite Warehouse]
    C[Sky Satellite Metrics] --> B
    B -->|Advanced SQL Analytics| D[Prescription Model]
    D -->|CSV Exports| E[Tableau Public Dashboard]
    
    style A fill:#f9f9f9,stroke:#333,stroke-width:2px
    style B fill:#e1f5fe,stroke:#0288d1,stroke-width:2px
    style C fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    style D fill:#e8f5e9,stroke:#388e3c,stroke-width:2px
    style E fill:#fce4ec,stroke:#c2185b,stroke-width:2px
```