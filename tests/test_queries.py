"""
Smoke tests: every SQL file must run against the real schema.

The schools table here is the 8 real rows captured from the original notebook run.
The census table is a tiny hand-made stand-in (3 columns) used only so the join queries can execute;
its North Center row mirrors the hardship index (6) reported in the original run.
Run:  python -m pytest tests -q      (or)   python tests/test_queries.py
"""
import sqlite3
import sys
import tempfile
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from src import chicago_sql as cs  # noqa: E402
import run_pipeline  # noqa: E402


def make_fixture(tmp: Path):
    schools = pd.read_csv(ROOT / "data" / "sample_8_schools.csv")
    schools.to_csv(tmp / "schools.csv", index=False)
    pd.DataFrame({
        "COMMUNITY_AREA_NUMBER": [5, 7, 43, 66, 1],
        "COMMUNITY_AREA_NAME": ["North Center", "Lincoln Park", "South Shore", "Chicago Lawn", "Rogers Park"],
        "HARDSHIP_INDEX": [6, 1, 73, 80, 39],
    }).to_csv(tmp / "census.csv", index=False)
    return tmp / "schools.csv", tmp / "census.csv"


def test_every_sql_file_executes_and_basic_answers():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        s, c = make_fixture(tmp)
        report, metrics = run_pipeline.run(s, c, tmp / "t.db", tmp / "res", tmp / "figs")
        assert len(report) == 12
        con = sqlite3.connect(tmp / "t.db")
        try:
            # 5 of the 8 real sample schools are 'ES'
            assert cs.run_sql_file(con, cs.sql_files("problems")[0]).iloc[0, 0] == 5
            # Lane Tech (college enrollment 4368) sits in North Center -> hardship 6
            p11 = cs.run_sql_file(con, [f for f in cs.sql_files("problems") if f.name.startswith("11")][0])
            assert p11.iloc[0, 0] == 6
            # metadata query returns all 78 columns
            assert len(cs.table_metadata(con)) == 78
        finally:
            con.close()


if __name__ == "__main__":
    test_every_sql_file_executes_and_basic_answers()
    print("OK")
