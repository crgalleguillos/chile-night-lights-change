from pathlib import Path
from typing import List

import rasterio
import rioxarray as rxr
import xarray as xr
from tqdm import tqdm


NTL_CANDIDATES = [
    "AllAngle_Composite_Snow_Free",
    "NearNadir_Composite_Snow_Free",
    "AllAngle_Composite_Snow_Covered",
]

QUALITY_CANDIDATES = [
    "AllAngle_Composite_Snow_Free_Quality",
    "NearNadir_Composite_Snow_Free_Quality",
    "AllAngle_Composite_Snow_Covered_Quality",
]


def find_subdataset(h5_path: Path, candidates: List[str]) -> str:
    """Return the first matching subdataset name inside the HDF5 file."""
    with rasterio.open(h5_path) as src:
        subdatasets = src.subdatasets

    for name in candidates:
        for s in subdatasets:
            if name in s:
                return s

    raise FileNotFoundError(
        f"No matching subdataset found in {h5_path.name}. Tried: {candidates}"
    )


def open_ntl_layer(h5_path: Path, use_quality_mask: bool = True) -> xr.DataArray:
    """
    Open a NTL (night-time lights) layer from a VNP46A3 HDF5 granule.
    Optionally apply a simple quality mask (keep q > 0).
    """
    ntl_sds = find_subdataset(h5_path, NTL_CANDIDATES)
    ntl = rxr.open_rasterio(ntl_sds).squeeze()

    if use_quality_mask:
        try:
            q_sds = find_subdataset(h5_path, QUALITY_CANDIDATES)
            q = rxr.open_rasterio(q_sds).squeeze()
            ntl = ntl.where(q > 0)
        except Exception as e:
            print(f"Warning: quality mask not applied for {h5_path.name} -> {e}")

    return ntl


def annual_mean_ntl(h5_files: List[Path], use_quality_mask: bool = True) -> xr.DataArray:
    """
    Build an annual mean composite by reading monthly granules and averaging them.
    Aligns rasters to the first valid raster via reproject_match when needed.
    """
    rasters = []
    for f in tqdm(h5_files, desc="Reading NTL granules"):
        try:
            rasters.append(open_ntl_layer(f, use_quality_mask=use_quality_mask))
        except Exception as e:
            print(f"Skipping {f.name} -> {e}")

    if not rasters:
        raise RuntimeError("No granules could be read from the provided H5 files.")

    base = rasters[0]
    aligned = []
    for r in rasters:
        if (r.rio.crs != base.rio.crs) or (r.rio.transform() != base.rio.transform()) or (r.shape != base.shape):
            r = r.rio.reproject_match(base)
        aligned.append(r)

    return xr.concat(aligned, dim="t").mean(dim="t", skipna=True)