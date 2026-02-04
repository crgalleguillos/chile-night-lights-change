from pathlib import Path

# --- Repository paths ---
REPO_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = REPO_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROC_DIR = DATA_DIR / "processed"

REPORTS_DIR = REPO_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
RESULTS_DIR = REPORTS_DIR / "results"

# --- Create directories (safe) ---
for p in [RAW_DIR, INTERIM_DIR, PROC_DIR, FIGURES_DIR, RESULTS_DIR]:
    p.mkdir(parents=True, exist_ok=True)

# --- Study area / analysis parameters ---
YEARS = [2014, 2019, 2024]

# Chile bounding box (min_lon, min_lat, max_lon, max_lat)
BBOX_CHILE = (-75.0, -56.0, -66.0, -17.0)

CRS_WGS84 = "EPSG:4326"

# Threshold for categorical change (normalized delta)
CHANGE_THRESHOLD = 0.03