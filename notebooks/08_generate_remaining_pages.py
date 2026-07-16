"""
Generate Page 2 (Bears Deep Dive) and Page 3 (Team Explorer) using the
same visual patterns already validated against Power BI Desktop on
Page 1 (card, tableEx, clusteredBarChart all confirmed working).
"""
import json
import uuid
from pathlib import Path

REPORT_DIR = Path(
    r"C:\Users\Ryan\Desktop\nfl-win-analytics\powerbi\NFL Wins Dashboard.Report\definition"
)
PAGES_DIR = REPORT_DIR / "pages"


def guid():
    return str(uuid.uuid4())


def write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")
    print(f"wrote {path}")


def make_page(page_id, display_name):
    write_json(PAGES_DIR / page_id / "page.json", {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json",
        "name": page_id,
        "displayName": display_name,
        "displayOption": "FitToPage",
        "height": 720,
        "width": 1280,
    })


def visual_container(name, x, y, w, h, z, visual_body):
    return {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.9.0/schema.json",
        "name": name,
        "position": {"x": x, "y": y, "width": w, "height": h, "z": z, "tabOrder": z},
        "visual": visual_body,
    }


def col_projection(table, prop, is_measure=False):
    key = "Measure" if is_measure else "Column"
    return {
        "field": {
            key: {
                "Expression": {"SourceRef": {"Entity": table}},
                "Property": prop,
            }
        },
        "queryRef": f"{table}.{prop}",
        "nativeQueryRef": prop,
    }


def title_object(text):
    return {
        "title": [
            {"properties": {"text": {"expr": {"Literal": {"Value": f"'{text}'"}}}}}
        ]
    }


def make_card(page_id, name, x, y, w, h, z, table, measure):
    body = {
        "visualType": "card",
        "query": {"queryState": {"Values": {"projections": [col_projection(table, measure, is_measure=True)]}}},
        "objects": {},
        "visualContainerObjects": {},
    }
    write_json(PAGES_DIR / page_id / "visuals" / name / "visual.json", visual_container(name, x, y, w, h, z, body))


def make_table(page_id, name, x, y, w, h, z, table, columns, title=None):
    projections = [col_projection(table, c, is_measure=m) for c, m in columns]
    body = {
        "visualType": "tableEx",
        "query": {"queryState": {"Values": {"projections": projections}}},
        "objects": {},
        "visualContainerObjects": title_object(title) if title else {},
    }
    write_json(PAGES_DIR / page_id / "visuals" / name / "visual.json", visual_container(name, x, y, w, h, z, body))


def make_line_chart(page_id, name, x, y, w, h, z, table, category_col, y_cols, title=None):
    body = {
        "visualType": "lineChart",
        "query": {
            "queryState": {
                "Category": {"projections": [col_projection(table, category_col)]},
                "Y": {"projections": [col_projection(table, c) for c in y_cols]},
            }
        },
        "objects": {},
        "visualContainerObjects": title_object(title) if title else {},
    }
    write_json(PAGES_DIR / page_id / "visuals" / name / "visual.json", visual_container(name, x, y, w, h, z, body))


def make_slicer(page_id, name, x, y, w, h, z, table, column, title=None):
    body = {
        "visualType": "slicer",
        "query": {"queryState": {"Values": {"projections": [col_projection(table, column)]}}},
        "objects": {},
        "visualContainerObjects": title_object(title) if title else {},
    }
    write_json(PAGES_DIR / page_id / "visuals" / name / "visual.json", visual_container(name, x, y, w, h, z, body))


# ============================================================
# Page 2 — Bears Deep Dive
# ============================================================
page2_id = guid()
make_page(page2_id, "Bears Deep Dive")

make_line_chart(
    page2_id, guid(), 20, 20, 900, 400, 1000,
    "bears_vs_league", "season",
    ["off_epa_per_play", "off_epa_per_play_league_avg"],
    title="Bears Offensive Efficiency vs League Average",
)
make_card(page2_id, guid(), 940, 20, 300, 180, 1001, "team_season_summary", "Bears Win Pct")
make_table(
    page2_id, guid(), 20, 440, 1220, 250, 1002,
    "bears_vs_league",
    [("season", False), ("wins", False), ("losses", False), ("win_pct", False),
     ("off_epa_per_play", False), ("off_epa_per_play_league_avg", False)],
    title="Bears Season-by-Season Record",
)

# ============================================================
# Page 3 — Team Explorer
# ============================================================
page3_id = guid()
make_page(page3_id, "Team Explorer")

make_slicer(page3_id, guid(), 20, 20, 300, 100, 1000, "team_season_summary", "team", title="Team")
make_slicer(page3_id, guid(), 340, 20, 300, 100, 1001, "team_season_summary", "season", title="Season")
make_table(
    page3_id, guid(), 20, 140, 1220, 550, 1002,
    "team_season_summary",
    [("team", False), ("season", False), ("wins", False), ("losses", False), ("win_pct", False),
     ("off_epa_per_play", False), ("off_success_rate", False), ("off_third_down_pct", False),
     ("def_epa_per_play_allowed", False), ("def_success_rate_allowed", False), ("turnover_margin", False)],
    title="Team-Season Detail",
)

# ============================================================
# Update pages.json ordering
# ============================================================
pages_json_path = PAGES_DIR / "pages.json"
pages_json = json.loads(pages_json_path.read_text(encoding="utf-8"))
existing_page1_id = pages_json["pageOrder"][0]
pages_json["pageOrder"] = [existing_page1_id, page2_id, page3_id]
write_json(pages_json_path, pages_json)

print(f"\nPage 1 (existing): {existing_page1_id}")
print(f"Page 2 (Bears Deep Dive): {page2_id}")
print(f"Page 3 (Team Explorer): {page3_id}")
