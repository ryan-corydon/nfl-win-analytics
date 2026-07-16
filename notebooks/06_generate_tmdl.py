"""
Generate TMDL table definitions for the Power BI semantic model directly
from the export CSVs, so column names/types always match the actual data
and every lineageTag GUID is valid and unique.
"""
import uuid
import pandas as pd
from pathlib import Path

EXPORTS_DIR = r"C:\Users\Ryan\Desktop\nfl-win-analytics\exports"
TABLES_DIR = Path(
    r"C:\Users\Ryan\Desktop\nfl-win-analytics\powerbi\NFL Wins Dashboard.SemanticModel\definition\tables"
)
TABLES_DIR.mkdir(parents=True, exist_ok=True)


def guid():
    return str(uuid.uuid4())


def dtype_map(pandas_dtype):
    if pandas_dtype == "int64":
        return "int64", "Int64.Type", "sum", "0"
    if pandas_dtype == "float64":
        return "double", "type number", "sum", None
    return "string", "type text", "none", None


TABLES = [
    "team_season_summary",
    "teams",
    "feature_importance",
    "correlation_with_wins",
    "linear_coefficients",
    "bears_vs_league",
]

# Measures to attach to team_season_summary, from POWERBI_GUIDE.md
MEASURES = [
    ("Avg Win Pct", "AVERAGE(team_season_summary[win_pct])", "0.0%"),
    ("Avg Off EPA per Play", "AVERAGE(team_season_summary[off_epa_per_play])", "0.000"),
    ("Avg Def EPA Allowed", "AVERAGE(team_season_summary[def_epa_per_play_allowed])", "0.000"),
    ("Total Wins", "SUM(team_season_summary[wins])", "0"),
    ("Bears Win Pct", 'CALCULATE([Avg Win Pct], team_season_summary[team] = "CHI")', "0.0%"),
    ("League Avg Off EPA", "CALCULATE([Avg Off EPA per Play], ALL(team_season_summary[team]))", "0.000"),
]

for table_name in TABLES:
    csv_path = f"{EXPORTS_DIR}\\{table_name}.csv"
    df = pd.read_csv(csv_path)
    n_cols = len(df.columns)

    lines = [f"table {table_name}", f"\tlineageTag: {guid()}", ""]

    col_type_exprs = []
    for col in df.columns:
        tmdl_type, m_type, summarize_by, format_string = dtype_map(str(df[col].dtype))
        lines.append(f"\tcolumn {col}")
        lines.append(f"\t\tdataType: {tmdl_type}")
        if format_string:
            lines.append(f"\t\tformatString: {format_string}")
        lines.append(f"\t\tlineageTag: {guid()}")
        lines.append(f"\t\tsummarizeBy: {summarize_by}")
        lines.append(f"\t\tsourceColumn: {col}")
        lines.append("")
        lines.append("\t\tannotation SummarizationSetBy = Automatic")
        lines.append("")
        col_type_exprs.append(f'{{"{col}", {m_type}}}')

    if table_name == "team_season_summary":
        for name, expr, fmt in MEASURES:
            lines.append(f"\tmeasure '{name}' = {expr}")
            lines.append(f"\t\tformatString: {fmt}")
            lines.append(f"\t\tlineageTag: {guid()}")
            lines.append("")

    type_list = ", ".join(col_type_exprs)
    # M string literals don't use backslash-escaping (only "" escapes a
    # literal quote) — a single backslash is the correct, valid form here.
    escaped_path = csv_path
    lines.append(f"\tpartition {table_name} = m")
    lines.append("\t\tmode: import")
    lines.append("\t\tsource =")
    lines.append("\t\t\t\tlet")
    lines.append(
        f'\t\t\t\t    Source = Csv.Document(File.Contents("{escaped_path}"),'
        f'[Delimiter=",", Columns={n_cols}, Encoding=65001, QuoteStyle=QuoteStyle.None]),'
    )
    lines.append(
        '\t\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),'
    )
    lines.append(
        f'\t\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{{type_list}}})'
    )
    lines.append("\t\t\t\tin")
    lines.append('\t\t\t\t    #"Changed Type"')
    lines.append("")
    lines.append("\tannotation PBI_ResultType = Table")
    lines.append("")

    out_path = TABLES_DIR / f"{table_name}.tmdl"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out_path}")

print("\nDone.")
