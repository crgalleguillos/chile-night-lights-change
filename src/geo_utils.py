from pathlib import Path
import numpy as np
import rioxarray as rxr


def minmax_normalize(in_path: Path, out_path: Path) -> Path:
    """
    Min-Max normalize raster values to [0, 1] using only finite pixels.
    Writes float32 output GeoTIFF.
    """
    da = rxr.open_rasterio(in_path).squeeze()

    arr = da.values
    mask = np.isfinite(arr)

    if mask.sum() == 0:
        raise ValueError(f"No valid pixels found in {in_path.name}")

    vmin = float(np.nanmin(arr[mask]))
    vmax = float(np.nanmax(arr[mask]))

    if vmax == vmin:
        # Avoid division by zero
        norm = da.copy(data=np.zeros_like(arr, dtype="float32"))
    else:
        norm = (da - vmin) / (vmax - vmin)

    norm = norm.astype("float32")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    norm.rio.to_raster(out_path, dtype="float32")

    return out_path