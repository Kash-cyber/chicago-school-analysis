"""
End-to-end pipeline for the Chicago Public Schools SQL project.

    python run_pipeline.py                         # downloads both CSVs, builds RealWorldData.db
    python run_pipeline.py --schools-csv a.csv --census-csv b.csv   # use local copies

Steps
  1. CSV -> SQLite (two tables)
  2. run the 12 lab problems (sql/problems) and CHECK them against the results captured in the original notebook
  3. run the extended analysis queries (sql/extended)
  4. compute correlations and write charts + CSVs to results/ and figures/
"""
import argparse
import json
from pathlib import Path

import pandas as pd

from src import chicago_sql as cs

ROOT = Path(__file__).resolve().parent


def _norm(df: pd.DataFrame):
    """Comparable representation: rows as tuples of rounded values, order-insensitive."""
    def cell(v):
        if v is None or (isinstance(v, float) and pd.isna(v)):
            return "NULL"
        if isinstance(v, (int, float)):
            return f"{float(v):.4f}"
        return str(v)
    return sorted(tuple(cell(v) for v in row) for row in df.itertuples(index=False, name=None))


def run(schools_src, census_src, db_path, out_dir, fig_dir=None):
    out_dir = Path(out_dir)
    (out_dir / "live_problems").mkdir(parents=True, exist_ok=True)
    (out_dir / "extended").mkdir(parents=True, exist_ok=True)
    fig_dir = Path(fig_dir) if fig_dir else ROOT / "figures"

    con = cs.build_database(db_path, schools_src, census_src)
    n_schools = con.execute(f"SELECT COUNT(*) FROM {cs.SCHOOLS_TABLE}").fetchone()[0]
    n_cols = len(cs.table_metadata(con))
    print(f"Loaded {n_schools} schools, {n_cols} columns")

    # ---- 2. lab problems + reproduction check ------------------------------
    verified = cs.load_verified()
    report = []
    for f in cs.sql_files("problems"):
        pid = f.stem.split("_")[0]
        df = cs.run_sql_file(con, f)
        df.to_csv(out_dir / "live_problems" / f"{f.stem}.csv", index=False)
        same = _norm(df) == _norm(verified[pid])
        report.append({"problem": int(pid), "file": f.name, "rows": len(df), "matches_original_run": same})
        print(f"  problem {pid}: {len(df):>3} rows  {'MATCH' if same else 'DIFFERS from original run'}")
    pd.DataFrame(report).to_csv(out_dir / "reproduction_check.csv", index=False)

    # ---- 3. extended queries ------------------------------------------------
    ext = {}
    for f in cs.sql_files("extended"):
        df = cs.run_sql_file(con, f)
        ext[f.stem.split("_")[0]] = df
        df.to_csv(out_dir / "extended" / f"{f.stem}.csv", index=False)
        print(f"  {f.stem}: {len(df)} rows")

    # ---- 4. correlations + charts ------------------------------------------
    metrics = {}
    scores = ext["E03"].dropna(subset=["safety_score"])
    for a, b, label in (("safety_score", "attendance_pct", "safety_vs_attendance"),
                        ("safety_score", "misconducts_per_100", "safety_vs_misconducts")):
        d = scores[[a, b]].dropna()
        metrics[label] = {"pearson_r": float(d[a].corr(d[b])) if len(d) > 2 else None, "n": int(len(d))}
    areas = ext["E02"].dropna(subset=["avg_safety_score", "hardship_index"])
    metrics["area_safety_vs_hardship"] = {
        "pearson_r": float(areas["avg_safety_score"].corr(areas["hardship_index"])) if len(areas) > 2 else None,
        "n": int(len(areas)),
    }
    (out_dir / "extended_metrics.json").write_text(json.dumps(metrics, indent=2))
    print("  correlations:", json.dumps(metrics))

    if len(scores) > 2:
        cs.plot_correlation_scatter(scores, "attendance_pct", "safety_score", "Average student attendance (%)",
                                    "Safety score", fig_dir / "10_safety_vs_attendance.png", color_by="school_type")
        cs.plot_correlation_scatter(areas, "hardship_index", "avg_safety_score", "Community hardship index",
                                    "Avg school safety score", fig_dir / "11_safety_vs_hardship.png")

    enroll = cs.run_sql(con, f"SELECT Community_Area_Name AS community_area_name, "
                                           f"SUM(College_Enrollment) AS total_college_enrollment "
                                           f"FROM {cs.SCHOOLS_TABLE} GROUP BY Community_Area_Name")
    cs.plot_enrollment_extremes(enroll, path=fig_dir / "01_enrollment_top_bottom_areas.png")
    con.close()
    return report, metrics


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--schools-csv", default=cs.SCHOOLS_URL)
    ap.add_argument("--census-csv", default=cs.CENSUS_URL)
    ap.add_argument("--db", default=str(ROOT / "RealWorldData.db"))
    ap.add_argument("--out-dir", default=str(ROOT / "results"))
    ap.add_argument("--fig-dir", default=str(ROOT / "figures"))
    a = ap.parse_args()
    run(a.schools_csv, a.census_csv, a.db, a.out_dir, a.fig_dir)
