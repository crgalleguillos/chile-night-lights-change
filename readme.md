# Chile Night Lights Change (2014–2019–2024) — VIIRS Black Marble (VNP46A3)

## General description
This project analyzes **changes in nighttime light intensity across Chile** using NASA’s **VIIRS Black Marble** monthly product (**VNP46A3**).  
The workflow builds **annual mean composites** for **2014, 2019, and 2024**, standardizes them for comparability, computes **pixel-wise changes (deltas)** between periods, and summarizes results at the **regional (Admin-1) level**.

## Project access

- **Jupyter Notebook:** `notebooks/01_chile_night_lights_change.ipynb`
- **Web report (HTML):** https://crgalleguillos.github.io/chile-night-lights-change/

The HTML version provides comfortable reading and full navigation, and is recommended for a general overview of the project and results.

## Objective
- Produce annual nighttime-lights composites for **2014, 2019, 2024**
- Detect spatial change using:
  - **Δ(2019–2014)** and **Δ(2024–2019)** (continuous deltas)
  - **categorical change maps** (increase / decrease / stable)
- Rank Chilean regions by:
  - **mean delta**
  - **% pixels increasing / decreasing / stable**

## Methodological workflow
1. **Data download**
   - Download monthly VNP46A3 granules for each study year using a Chile bounding box.
2. **Annual compositing**
   - Aggregate monthly granules into **annual mean** rasters (pixel-wise mean; nodata handled; optional quality mask).
3. **Georeferencing strategy**
   - Apply a **BBox-based fallback georeferencing** (WGS84 / EPSG:4326) when needed and validate visually.
4. **Clipping**
   - Clip rasters to Chile’s national boundary to remove ocean/irrelevant areas.
5. **Normalization**
   - Apply **Min–Max normalization (0–1) per year** to support visual comparability.
6. **Change detection**
   - Compute **deltas**:
     - Δ(2019–2014)
     - Δ(2024–2019)
   - Use robust visualization scaling (e.g., 99th percentile of |Δ|).
7. **Categorical change maps**
   - Convert deltas into:
     - **Increase** (Δ > +0.03)
     - **Decrease** (Δ < −0.03)
     - **Stable** (|Δ| ≤ 0.03)
8. **Regional aggregation**
   - Compute per-region metrics (mean/median/std of Δ and % increase/decrease/stable) and export CSV tables.

## Main results (summary)
- **Net change is small at the national scale**, with distributions centered near zero, indicating that most pixels exhibit minor variations.
- **Localized hotspots** of increase/decrease exist and drive the tails of the delta distributions.
- **Regional metrics** reveal heterogeneous behavior across Chile, with northern regions often ranking among the strongest mean increases, while central macrozones show important signals in the later period.

> Note: Because normalization is performed **per year**, delta values represent change in **normalized units** rather than absolute radiance units.

## Data sources
- **Nighttime lights:** NASA VIIRS Black Marble **VNP46A3** (monthly)
- **Administrative boundaries (regions):** **GADM v4.1** (Chile Admin-1)

## Technologies used
- **Language:** Python
- **Geospatial:** GeoPandas, Rasterio, RioXarray, Fiona
- **Scientific computing:** NumPy, Pandas, Xarray
- **Visualization:** Matplotlib
- **Environment:** Conda, Jupyter Notebook
- **Version control:** Git & GitHub

## Author
**Cristián Andrés Galleguillos Vega**  
Data Scientist | Biologist | MSc in Data Science & Big Data | MSc in Natural Resources Engineering

## Conclusion
This project demonstrates an end-to-end, reproducible geospatial pipeline to quantify and communicate **nighttime-light change** across Chile.  
By combining pixel-level deltas, categorical interpretation, and region-level aggregation, the notebook provides an interpretable baseline for future extensions such as city-level analysis, cross-year scaling strategies, and integration with socioeconomic or infrastructure datasets.