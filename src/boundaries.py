import geopandas as gpd
from pathlib import Path


def load_chile_boundary(out_path: Path) -> gpd.GeoDataFrame:
    """
    Download and return Chile national boundary (Natural Earth admin-0).
    Saves a cached GeoPackage for reproducibility.
    """
    if out_path.exists():
        return gpd.read_file(out_path, layer="chile")

    url = "https://naturalearth.s3.amazonaws.com/50m_cultural/ne_50m_admin_0_countries.zip"
    world = gpd.read_file(url)

    chile = world[world["ADM0_A3"] == "CHL"].copy()
    chile = chile.to_crs("EPSG:4326")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    chile.to_file(out_path, layer="chile", driver="GPKG")

    return chile