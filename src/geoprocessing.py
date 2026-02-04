from pathlib import Path
import rioxarray as rxr
import geopandas as gpd


def ensure_raster_crs(da, crs: str):
    """
    Ensure a DataArray has a CRS. If missing, write it.
    """
    if da.rio.crs is None:
        da = da.rio.write_crs(crs, inplace=False)
    return da


def clip_raster_to_geometry(
    in_path: Path,
    out_path: Path,
    geometry: gpd.GeoDataFrame,
    raster_crs_fallback: str = "EPSG:4326",
):
    """
    Clip a raster to the given geometry and save to disk.

    If the raster CRS is missing, a fallback CRS is written (default EPSG:4326).
    Note: This assumes the raster is already in that CRS.
    """
    da = rxr.open_rasterio(in_path)

    # Ensure CRS exists (rioxarray requires it for clip)
    da = ensure_raster_crs(da, raster_crs_fallback)

    # Make sure geometry is in the same CRS as raster
    geom = geometry.to_crs(da.rio.crs)

    clipped = da.rio.clip(
        geom.geometry,
        geom.crs,
        drop=True,
        invert=False,
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    clipped.rio.to_raster(out_path, dtype="float32")

    return out_path

import numpy as np
import rioxarray as rxr

def georef_raster_with_bbox(
    in_path: Path,
    out_path: Path,
    bbox: tuple,
    crs: str = "EPSG:4326",
):
    """
    Assign lon/lat coordinates using a bounding box and write CRS.
    This is a bbox-based georeferencing fallback.

    bbox = (min_lon, min_lat, max_lon, max_lat)
    """
    min_lon, min_lat, max_lon, max_lat = bbox

    da = rxr.open_rasterio(in_path).squeeze()  # (y, x)
    h, w = da.shape

    # pixel size in degrees
    px_w = (max_lon - min_lon) / w
    px_h = (max_lat - min_lat) / h

    # pixel center coordinates
    xs = np.linspace(min_lon + px_w / 2, max_lon - px_w / 2, w)
    ys = np.linspace(max_lat - px_h / 2, min_lat + px_h / 2, h)

    da = da.assign_coords({"x": xs, "y": ys})
    da = da.rio.write_crs(crs, inplace=False)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    da.rio.to_raster(out_path, dtype="float32")

    return out_path