# Urban Heatwave Prediction

**Hyper-local short-term heatwave prediction for Delhi using a hybrid Random Forest + Graph Convolutional Network (GCN), fused with MODIS satellite Land Surface Temperature.**

> Author: **Tanay Tejush** · GitHub: [@tanaytejush](https://github.com/tanaytejush)
> License: MIT

---

## Overview

An urban microclimate digital twin that forecasts zone-level temperature across a 25×24 grid over Delhi (600 zones, ~2 km resolution) up to 6 hours ahead and surfaces heatwave alerts.

- **Temporal model** — Random Forest regressor on hourly weather (temperature, humidity, wind).
- **Spatial model** — 2-layer GCN that refines RF predictions using a 4-neighbour zone graph and Urban Heat Island (UHI) offsets.
- **Satellite layer** — MODIS MOD11A1 Land Surface Temperature integration (HDF parsing + physically-calibrated Delhi LST generation).
- **Dashboard** — Streamlit app with forecast, animated spatial map, RF vs RF+GCN comparison, satellite LST, and alert tabs.

## Project structure

```
urban-heatwave-prediction/
├── src/                          # Source code
│   ├── app.py                    # Streamlit dashboard
│   ├── model.py                  # Random Forest temporal model
│   ├── gcn_model.py              # Graph Convolutional Network
│   ├── train_hybrid.py           # Hybrid RF+GCN training pipeline
│   ├── modis_processor.py        # MODIS LST integration
│   └── fetch_historical_data.py  # Open-Meteo data fetcher
├── data/                         # Input datasets (CSV, GeoJSON, HDF*)
├── models/                       # Trained model weights & scalers
├── notebooks/                    # Jupyter exploration
├── docs/                         # Project explanation
├── requirements.txt
├── LICENSE
└── README.md
```
*The raw MODIS `.hdf` tile is gitignored (regenerate via the link in `docs/`).*

## Quick start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. (Optional) Fetch a fresh year of weather data
python src/fetch_historical_data.py

# 3. Train the hybrid RF+GCN model
python src/train_hybrid.py

# 4. Launch the dashboard
streamlit run src/app.py
```

## Tech stack

Python · scikit-learn · PyTorch · GeoPandas · Streamlit · Plotly · pyhdf

## License

MIT © 2026 Tanay Tejush — see [LICENSE](LICENSE).
