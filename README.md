# Urban Heatwave Prediction — Delhi

## Problem Statement

Delhi experiences extreme heat events that kill hundreds of people each year. Existing national weather forecasts operate at too coarse a resolution to be actionable — they tell a city official that "Delhi will be hot," not which neighbourhoods will hit dangerous thresholds in the next 48 hours. This project produces hyper-local, short-term heatwave predictions at the urban grid level, giving decision-makers enough lead time to deploy targeted interventions.

## Who It's For

This tool is built for **urban planners and city health officials** — not data scientists. The end users are people who need to decide where to open cooling centres, which districts to prioritise for early warnings, and how to allocate emergency health resources before a heat event peaks. The interface was designed so that someone without a machine learning background can open it, read the forecast, and act on it.

## Key Product Decisions

**Why combine Random Forest and Graph Convolutional Networks?**
A standalone Random Forest would treat each grid cell as independent — it learns from temperature, humidity, and land use features, but ignores the fact that a heat island in one block radiates into adjacent blocks. A GCN captures those spatial neighbourhood dependencies across the urban graph. The hybrid model gets the interpretability and speed of RF for feature-level signals plus the spatial propagation awareness of GCN. Keeping both models rather than choosing one was a deliberate tradeoff: RF handles feature importance cleanly for stakeholder explainability; GCN handles the urban heat island cascade that RF misses.

**Why NASA MODIS LST satellite data?**
Ground weather stations in Delhi are sparse and unevenly distributed — placing a sensor network at grid resolution would be prohibitively expensive. MODIS Land Surface Temperature is freely available at 1km resolution and updated daily, making it the only practical source for dense spatial coverage. This was a cost and feasibility decision as much as a technical one.

**Why Streamlit for the dashboard?**
The tool was not built for research publication — it was built to be opened in a browser by a non-technical official in a heat emergency. Streamlit allowed rapid iteration on the UI without a frontend engineering bottleneck, and produces a clean enough interface for stakeholder demos without custom web development.

## Tech Stack

| Layer | Technology |
|---|---|
| Prediction models | Random Forest + Graph Convolutional Network (hybrid ensemble) |
| Satellite data | NASA MODIS Land Surface Temperature (LST) |
| Data processing | Python, pandas, NumPy |
| Spatial graph | NetworkX, PyTorch Geometric |
| Dashboard | Streamlit |
| Notebooks | Jupyter |

## How To Run

```bash
# Install dependencies
pip install -r requirements.txt

# Launch the Streamlit dashboard
streamlit run app.py
```

The dashboard loads pre-trained model weights and the most recent MODIS LST tile. No retraining is required to view predictions. To retrain, run the notebooks in order inside `/notebooks`.


---

<sub>Made by [tanaytejush](https://github.com/tanaytejush)</sub>
