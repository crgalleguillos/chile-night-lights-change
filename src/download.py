from pathlib import Path
import earthaccess as ea


def login_earthaccess():
    """
    Login to NASA Earthdata via earthaccess.
    The first time, select 'Save credentials'.
    """
    return ea.login()


def search_vnp46a3(year: int, bbox: tuple):
    """
    Search VIIRS Black Marble monthly product (VNP46A3) for a given year and bbox.
    """
    results = ea.search_data(
        short_name="VNP46A3",
        temporal=(f"{year}-01-01", f"{year}-12-31"),
        bounding_box=bbox,
    )
    return results


def download_granules(results, out_dir: Path):
    """
    Download search results to output directory.
    If the folder already contains .h5 files, skip download.
    """
    out_dir.mkdir(parents=True, exist_ok=True)

    existing = list(out_dir.glob("*.h5"))
    if existing:
        print(f"Already downloaded: {len(existing)} files in {out_dir}")
        return existing

    downloaded = ea.download(results, out_dir)
    return downloaded


def download_year_vnp46a3(year: int, bbox: tuple, raw_dir: Path):
    """
    Full pipeline: search + download for one year.
    """
    out_dir = raw_dir / "blackmarble" / str(year)
    results = search_vnp46a3(year, bbox)

    print(f"{year}: {len(results)} granules found")

    files = download_granules(results, out_dir)
    print(f"{year}: {len(files)} files downloaded")

    return files