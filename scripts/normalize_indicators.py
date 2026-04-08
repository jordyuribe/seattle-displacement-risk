import pandas as pd

print("Loading raw Census data...")
df = pd.read_csv("data/raw/king_county_acs.csv")

# ── Derived Indicators ───────────────────────────────────────────────────────
# We calculate percentages here rather than using raw counts
# because tracts have different population sizes

# % of households that are renters
df["pct_renters"] = df["renter_occupied"] / df["total_housing_units"]

# % of renters who are cost-burdened (paying 30%+ of income on rent)
df["pct_cost_burdened"] = (
    df["rent_burden_30_34"] +
    df["rent_burden_35_39"] +
    df["rent_burden_40_49"] +
    df["rent_burden_50_plus"]
) / df["rent_burden_total"]

# % of population that are people of color
df["pct_poc"] = 1 - (df["white_non_hispanic"] / df["total_population"])

# Invert median income — higher income = lower vulnerability
# We invert so that all indicators point in the same direction:
# higher value = more displacement risk
df["income_inverted"] = 1 / (df["median_household_income"].replace(0, pd.NA))

# ── Drop rows with missing values ────────────────────────────────────────────
# Some tracts have missing data (hospitals, prisons, etc.)
indicators = ["pct_renters", "pct_cost_burdened", "pct_poc", "income_inverted"]
df = df.dropna(subset=indicators)
print(f"Tracts after dropping missing data: {len(df)}")

# ── Min-Max Normalization ────────────────────────────────────────────────────
# Scales each indicator to a 0-1 range
# 0 = lowest risk tract, 1 = highest risk tract
def normalize(series):
    return (series - series.min()) / (series.max() - series.min())

for col in indicators:
    df[f"{col}_norm"] = normalize(df[col])

# ── Weighted Composite Score ─────────────────────────────────────────────────
# Each weight represents how much that indicator contributes to the final score
# These are documented in the methodology writeup
WEIGHTS = {
    "pct_renters_norm":      0.25,
    "pct_cost_burdened_norm": 0.25,
    "pct_poc_norm":          0.25,
    "income_inverted_norm":  0.25,
}

df["displacement_risk_score"] = sum(
    df[col] * weight for col, weight in WEIGHTS.items()
)

# ── Preview Results ──────────────────────────────────────────────────────────
print("\nTop 5 highest risk tracts:")
print(df[["NAME", "displacement_risk_score"]].sort_values(
    "displacement_risk_score", ascending=False
).head())

print("\nTop 5 lowest risk tracts:")
print(df[["NAME", "displacement_risk_score"]].sort_values(
    "displacement_risk_score", ascending=False
).tail())

# ── Save to processed folder ─────────────────────────────────────────────────
df.to_csv("data/processed/displacement_risk_scores.csv", index=False)
print("\nSaved to data/processed/displacement_risk_scores.csv")