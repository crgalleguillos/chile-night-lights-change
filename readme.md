# Chile Night Lights Change (2014–2019–2024)

Spatial change analysis of night-time lights in Chile using VIIRS Black Marble (VNP46A3). The workflow downloads monthly granules, builds annual composites, clips to Chile, normalizes, computes deltas, and summarizes change by region.

## Project status
Work in progress.

## Structure
- `notebooks/`: main analysis notebook
- `src/`: reusable code (config, download, preprocessing, viz)
- `data/`: local data (ignored by git)
- `reports/figures/`: exported maps and charts
- `reports/results/`: exported tables (regional metrics)

## Data
- VIIRS Black Marble monthly product: VNP46A3 (NASA)
- Natural Earth boundaries (admin-0 and admin-1)