"""
chicago_sql.py
==============
Helpers for the Chicago Public Schools SQL analysis project.

* build_database()  - CSV (URL or local path) -> SQLite tables
* run_sql_file()    - execute a .sql file and return a DataFrame
* load_verified()   - results captured from the original notebook run
* plot_*()          - charts
"""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SQL_DIR = ROOT / "sql"
DATA_DIR = ROOT / "data"
RESULTS_DIR = ROOT / "results"

BASE_URL = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/FinalModule_Coursera_V5/data/"
)
SCHOOLS_URL = BASE_URL + "ChicagoPublicSchools.csv"
CENSUS_URL = BASE_URL + "ChicagoCensusData.csv"

SCHOOLS_TABLE = "CHICAGO_PUBLIC_SCHOOLS_DATA"
CENSUS_TABLE = "CENSUS_DATA"

BLUE, RED, GREY = "#1f4e9c", "#b3261e", "#9aa0a6"


# --------------------------------------------------------------------------- #
# Database
# --------------------------------------------------------------------------- #
def build_database(db_path, schools_src=SCHOOLS_URL, census_src=CENSUS_URL) -> sqlite3.Connection:
    """Load both CSVs (URL or local path) into a SQLite file and return an open connection."""
    con = sqlite3.connect(str(db_path))
    pd.read_csv(schools_src).to_sql(SCHOOLS_TABLE, con, if_exists="replace", index=False)
    pd.read_csv(census_src).to_sql(CENSUS_TABLE, con, if_exists="replace", index=False)
    return con


def run_sql(con: sqlite3.Connection, sql: str) -> pd.DataFrame:
    return pd.read_sql_query(sql, con)


def run_sql_file(con: sqlite3.Connection, path) -> pd.DataFrame:
    return run_sql(con, Path(path).read_text())


def sql_files(kind: str) -> list[Path]:
    """kind = 'problems' or 'extended'"""
    return sorted((SQL_DIR / kind).glob("*.sql"))


def table_metadata(con: sqlite3.Connection, table: str = SCHOOLS_TABLE) -> pd.DataFrame:
    """Column name, declared type and position, straight from SQLite's catalog."""
    return run_sql(con, f"SELECT cid + 1 AS position, name AS column_name, type AS declared_type "
                        f"FROM PRAGMA_TABLE_INFO('{table}')")


# --------------------------------------------------------------------------- #
# Results captured from the original run
# --------------------------------------------------------------------------- #
def load_verified() -> dict[str, pd.DataFrame]:
    raw = json.loads((RESULTS_DIR / "verified_results.json").read_text())
    return {k: pd.DataFrame(v["rows"], columns=v["columns"]) for k, v in raw.items()}


def load_verified_meta() -> dict:
    return json.loads((RESULTS_DIR / "verified_results.json").read_text())


def load_enrollment_snapshot() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "community_area_college_enrollment.csv")


def load_schema_snapshot() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "schema_chicago_public_schools.csv")


# --------------------------------------------------------------------------- #
# Insights that need nothing but the captured results
# --------------------------------------------------------------------------- #
def enrollment_concentration(enroll: pd.DataFrame) -> dict:
    s = enroll["total_college_enrollment"].sort_values(ascending=False)
    total = s.sum()
    return {
        "community_areas": len(s),
        "total_enrollment": int(total),
        "mean": float(s.mean()),
        "median": float(s.median()),
        "largest_area": enroll.loc[s.index[0], "community_area_name"],
        "largest_total": int(s.iloc[0]),
        "smallest_area": enroll.loc[s.index[-1], "community_area_name"],
        "smallest_total": int(s.iloc[-1]),
        "largest_to_smallest_ratio": float(s.iloc[0] / s.iloc[-1]),
        "top5_share": float(s.head(5).sum() / total),
        "top10_share": float(s.head(10).sum() / total),
        "top20_share_of_areas": float(s.head(int(np.ceil(0.2 * len(s)))).sum() / total),
        "bottom_half_share": float(s.tail(len(s) // 2).sum() / total),
    }


def schema_summary(schema: pd.DataFrame) -> pd.Series:
    counts = schema["declared_type"].value_counts()
    return counts.rename("columns")


# --------------------------------------------------------------------------- #
# Charts
# --------------------------------------------------------------------------- #
def _style(ax):
    ax.grid(True, axis="x", color="#e6e6e6", lw=0.8)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def _save(fig, path):
    if path:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, dpi=160, bbox_inches="tight", facecolor="white")
        plt.close(fig)
        return path
    return fig


def plot_enrollment_extremes(enroll: pd.DataFrame, n: int = 10, path=None):
    """Top-n and bottom-n community areas by total college enrollment."""
    s = enroll.sort_values("total_college_enrollment", ascending=False)
    top = s.head(n).iloc[::-1]          # largest drawn at the top
    bottom = s.tail(n)                  # smallest drawn at the bottom
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2))
    for ax, d, color, title in ((axes[0], top, BLUE, f"Top {n} community areas"),
                                (axes[1], bottom, RED, f"Bottom {n} community areas")):
        ax.barh(d["community_area_name"].str.title(), d["total_college_enrollment"], color=color)
        for y, v in enumerate(d["total_college_enrollment"]):
            ax.text(v, y, f" {v:,.0f}", va="center", fontsize=9)
        _style(ax)
        ax.set_title(title, loc="left", fontweight="bold")
        ax.set_xlabel("Total college enrollment")
        ax.set_xlim(0, d["total_college_enrollment"].max() * 1.15)
    fig.suptitle("Total college enrollment by Chicago community area (2011-12)", x=0.01, ha="left", fontsize=13, fontweight="bold")
    fig.tight_layout()
    return _save(fig, path)


def plot_enrollment_distribution(enroll: pd.DataFrame, path=None):
    """Sorted bar profile of all areas + cumulative share line."""
    s = enroll.sort_values("total_college_enrollment", ascending=False).reset_index(drop=True)
    cum = s["total_college_enrollment"].cumsum() / s["total_college_enrollment"].sum() * 100
    fig, ax = plt.subplots(figsize=(11, 4.8))
    ax.bar(s.index + 1, s["total_college_enrollment"], color=BLUE, alpha=0.85)
    ax.set_xlabel("Community areas, ranked by enrollment")
    ax.set_ylabel("Total college enrollment")
    ax2 = ax.twinx()
    ax2.plot(s.index + 1, cum, color=RED, lw=2)
    ax2.set_ylabel("Cumulative share of citywide total (%)")
    ax2.set_ylim(0, 105)
    for k, (tx, ty) in ((10, (44, 36)), (20, (44, 50))):
        ax2.annotate(f"top {k} areas = {cum.iloc[k - 1]:.0f}% of total", (k, cum.iloc[k - 1]), xytext=(tx, ty),
                     textcoords="data", color=RED, fontsize=9.5, fontweight="bold",
                     bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=RED, lw=0.8),
                     arrowprops=dict(arrowstyle="->", color=RED))
    for s_ in ("top",):
        ax.spines[s_].set_visible(False); ax2.spines[s_].set_visible(False)
    ax.set_title("How concentrated is college enrollment across the 77 community areas?", loc="left", fontweight="bold")
    fig.tight_layout()
    return _save(fig, path)


def plot_attendance_extremes(top10: pd.DataFrame, below70: pd.DataFrame, path=None):
    """Best-10 vs worst-8 attendance, coloured by whether the school name says 'High School'."""
    def clean(df):
        d = df.copy()
        d["pct"] = d["average_student_attendance"].str.replace("%", "").astype(float)
        d["is_hs"] = d["name_of_school"].str.contains("High School")
        return d
    best, worst = clean(top10).iloc[::-1], clean(below70).iloc[::-1]
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.4), sharex=False)
    for ax, d, title in ((axes[0], best, "10 highest attendance"), (axes[1], worst, "Every school below 70% attendance")):
        colors = [RED if h else BLUE for h in d["is_hs"]]
        ax.barh(d["name_of_school"].str.replace(" School", "", regex=False), d["pct"], color=colors)
        for y, v in enumerate(d["pct"]):
            ax.text(v, y, f" {v:.1f}%", va="center", fontsize=9)
        _style(ax)
        ax.set_title(title, loc="left", fontweight="bold")
        ax.set_xlabel("Average student attendance (%)")
        ax.tick_params(axis="y", labelsize=8.5)
    axes[0].set_xlim(90, 100.2)
    axes[1].set_xlim(50, 76)
    from matplotlib.patches import Patch
    axes[1].legend(handles=[Patch(color=RED, label="Name contains 'High School'"),
                            Patch(color=BLUE, label="Other (elementary / magnet / early childhood)")],
                   frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.16), fontsize=9)
    fig.suptitle("Attendance extremes: top-10 vs. below-70% schools", x=0.01, ha="left", fontsize=13, fontweight="bold")
    fig.tight_layout()
    return _save(fig, path)


def plot_safety_extremes(highest: pd.DataFrame, lowest: pd.DataFrame, path=None):
    """Counts of schools tied at the top safety score vs. the five lowest scores."""
    fig, axes = plt.subplots(1, 2, figsize=(13, 5), gridspec_kw={"width_ratios": [1, 1.3]})
    t = highest.copy()
    t["is_hs"] = t["name_of_school"].str.contains("High School")
    counts = pd.Series({"Elementary-level": int((~t["is_hs"]).sum()), "High school": int(t["is_hs"].sum())})
    axes[0].bar(counts.index, counts.values, color=[BLUE, RED])
    for x, v in enumerate(counts.values):
        axes[0].text(x, v + 0.2, str(v), ha="center", fontweight="bold")
    axes[0].set_ylabel("Schools")
    axes[0].set_title(f"{len(t)} schools tie at the top score (99)", loc="left", fontweight="bold")
    for s_ in ("top", "right"):
        axes[0].spines[s_].set_visible(False)
    l = lowest.iloc[::-1]
    axes[1].barh(l["name_of_school"].str.replace(" School", "", regex=False), l["safety_score"], color=RED)
    for y, v in enumerate(l["safety_score"]):
        axes[1].text(v, y, f" {v:.0f}", va="center")
    axes[1].set_xlim(0, 100)
    _style(axes[1])
    axes[1].set_title("Five lowest safety scores (0-99 scale)", loc="left", fontweight="bold")
    axes[1].set_xlabel("Safety score")
    fig.tight_layout()
    return _save(fig, path)


def plot_correlation_scatter(df: pd.DataFrame, x: str, y: str, xlabel: str, ylabel: str, path=None, color_by=None):
    """Generic scatter + OLS line + Pearson r for the extended (full-data) analysis."""
    d = df[[x, y] + ([color_by] if color_by else [])].dropna()
    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    if color_by:
        for k, g in d.groupby(color_by):
            ax.scatter(g[x], g[y], s=22, alpha=0.7, label=k)
        ax.legend(frameon=False, title=color_by)
    else:
        ax.scatter(d[x], d[y], s=22, alpha=0.7, color=BLUE)
    if len(d) >= 3 and d[x].nunique() > 1:
        m, b = np.polyfit(d[x], d[y], 1)
        xs = np.linspace(d[x].min(), d[x].max(), 50)
        ax.plot(xs, m * xs + b, color="#333", ls="--", lw=1.2)
        r = d[x].corr(d[y])
        ax.set_title(f"{ylabel} vs {xlabel}  (r = {r:.2f}, n = {len(d)})", loc="left", fontweight="bold")
    ax.set_xlabel(xlabel); ax.set_ylabel(ylabel)
    ax.grid(True, color="#e6e6e6"); ax.set_axisbelow(True)
    for s_ in ("top", "right"):
        ax.spines[s_].set_visible(False)
    fig.tight_layout()
    return _save(fig, path)
