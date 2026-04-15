# Urban Microclimate Digital Twin
### Hyper-Local Short-Term Heatwave Prediction for Delhi
**Major Project Review II — March 2026**

---

## The Problem, In Plain English

Imagine it's a scorching June afternoon in Delhi. The official weather forecast says 42°C. But if you're standing in Okhla's industrial area, it feels closer to 48°C. Walk five minutes to the Yamuna floodplain, and it drops back to 40°C. The city is not one temperature — it's a patchwork of microclimates.

The tragedy is that our warning systems don't know this. A single weather station in Safdarjung covers an area of hundreds of square kilometres. The hospital in Shahdara has no idea it's about to get hit harder than the hospital in Lodhi Garden. Nobody warned the construction workers in Naraina that their patch of the city would be 5 degrees hotter than everywhere else.

**People die because our prediction tools are too coarse.**

In 2022, India recorded its hottest March since 1901. In 2024, over 40,000 heat-related deaths were reported across South Asia. Heatwaves are no longer rare events — they are a new normal. And cities, with their concrete, asphalt, and density, are the most dangerous places to be.

This project builds a system that actually understands how a city heats up — zone by zone, hour by hour.

---

## What We Built

We built a **Digital Twin of Delhi's urban climate** — a live, interactive replica of how heat moves through the city. It combines three layers of intelligence:

1. **Weather data** — real hourly readings from Delhi (temperature, humidity, wind speed)
2. **Satellite imagery** — NASA's MODIS satellite measures how hot the ground surface actually is, not just the air
3. **A city graph** — we model Delhi as a network of 600 connected zones, because heat doesn't respect borders, it spreads from neighbourhood to neighbourhood

Feed it current conditions, and it tells you: which zones will cross dangerous thresholds in the next 6 hours, and which specific neighbourhoods need to act now.

---

## How the City is Divided

Think of Delhi as a 25×24 chessboard. Each square on the board is a 2×2 km zone — 600 zones in total, covering the entire city from Narela in the north to Okhla in the south.

Every zone has:
- A unique ID and name (A1, B7, R24, etc.)
- Its geographic centre (latitude and longitude)
- Its neighbours — the zones directly to its north, south, east, and west

This grid is the backbone of everything. It lets us say "Zone M14 is going to hit 43°C in 3 hours" instead of just "Delhi will be hot."

---

## The Two Brains of the System

### Brain 1 — Random Forest (The Time Machine)

The Random Forest model is trained on a full year of Delhi weather data — 8,760 hours of real readings. It learns patterns like:

- When humidity is high and wind drops in the afternoon, temperature spikes in the next hour
- May afternoons follow a consistent heating curve
- Night-time cools at a predictable rate after 11 PM

Given the current reading, it predicts the city-wide temperature for the **next 6 hours**, one hour at a time.

Think of it as a very experienced weather analyst who has seen every season Delhi has to offer and can say with confidence: "given where we are right now, here is where we're heading."

**Performance on test data (data it had never seen):**
- Average error: 0.54°C
- R² score: 0.9836 (98.4% of temperature variation explained)

That is genuinely excellent for short-term forecasting.

---

### Brain 2 — Graph Convolutional Network (The Spatial Awareness)

Here's the problem with Brain 1: it thinks of Delhi as a single point. It predicts one temperature for the whole city. But we know Okhla runs hotter than Lodhi Garden. The industrial north-east bakes differently than the ridge forests.

This is where the Graph Convolutional Network (GCN) comes in.

A GCN treats the city as what it actually is — a connected graph. Each of the 600 zones is a node. Each pair of neighbouring zones is an edge. The network learns how heat propagates through these connections.

To understand why this matters, think about how a rumour spreads. It doesn't jump randomly across the city — it moves through connections, neighbour to neighbour. Heat behaves the same way. An industrial zone baking at 46°C slowly pushes that heat into the residential zone next door.

The GCN takes the Random Forest's city-wide prediction and asks: "given where each zone is, what its neighbours look like, and the physical geography, what is the *actual* temperature in this specific zone?"

**It refines a blunt city-wide forecast into a surgical neighbourhood-level prediction.**

**Performance improvement over RF alone:**
- RF spatial error: 0.80°C average
- RF + GCN error: 0.55°C average
- **The GCN cuts spatial error by 31%**
- Combined R² score: 0.9936

---

## The Urban Heat Island Effect

Not all parts of a city heat equally, even under the same sun. This is called the Urban Heat Island (UHI) effect, and it is one of the most well-documented phenomena in climate science.

In Delhi, we've modelled five major heat sources and three cooling zones:

**Hot zones:**
- **Connaught Place / Central Delhi** — dense concrete, minimal vegetation, intense human activity (+4°C above average)
- **Shahdara / Trans-Yamuna** — industrial area, dark rooftops, poor air circulation (+3.5°C)
- **Okhla Industrial Area** — manufacturing, large impervious surfaces (+3°C)
- **Naraina** — industrial estate in west Delhi (+2.5°C)
- **North Delhi residential** — high-density housing, limited green cover (+2°C)

**Cooling zones:**
- **Delhi Ridge (Aravalli)** — the city's green lungs, forest cover keeps it 2.5°C cooler
- **Yamuna Floodplain** — water presence and riparian vegetation (-2°C)
- **Lodhi Garden** — one of Delhi's largest green spaces (-1.5°C)

The system uses Gaussian kernels — mathematical "heat clouds" — to model how these hot and cool zones influence the temperature of every surrounding neighbourhood.

---

## What the Satellite Sees

Human beings measure air temperature — the temperature two metres above the ground. But the satellite sees something different: **Land Surface Temperature (LST)**, the actual heat radiating off the ground.

These two numbers can be dramatically different:
- A park: surface temperature ≈ air temperature + 2°C
- A residential area: +9°C above air temperature
- An industrial rooftop: +12–14°C above air temperature
- Bare asphalt in direct sun: up to +18°C above air temperature

We use NASA's MODIS MOD11A1 satellite product — a sensor that passes over Delhi twice daily and records the surface temperature of every square kilometre. By mapping these readings onto our 600-zone grid, we can see the exact thermal fingerprint of the city from space.

This is important because surface temperature predicts air temperature. A concrete plaza that has been absorbing heat all day at 52°C will radiate that heat back into the air at night, keeping certain zones dangerously hot even after sunset.

---

## The Alert System

All of this prediction feeds into a practical, actionable alert system with four levels:

| Level | Heat Stress Index | What It Means |
|-------|------------------|---------------|
| **Normal** | Below 33°C | Standard conditions, monitor forecast |
| **Watch** | 33–36°C | Elevated risk. Alert hospitals, open cooling centres |
| **Warning** | 36–40°C | High risk. Restrict outdoor work 12–4 PM. Issue public advisory |
| **Emergency** | Above 40°C | Severe. Full emergency protocol. Close schools. Mandatory shelters |

The Heat Stress Index (HSI) is not just temperature — it combines temperature, humidity, and wind speed into a single number that reflects what the human body actually experiences.

Every one of the 600 Delhi zones gets its own alert level. The dashboard shows exactly which neighbourhoods are at Warning or Emergency, updated every hour.

---

## The Dashboard

Everything comes together in a live, interactive web dashboard with six sections:

**1. Forecast Tab**
The 6-hour temperature forecast for the city, plotted as a line chart. Shows the observed temperature history and the predicted trajectory. Includes model accuracy metrics.

**2. Spatial Map Tab**
An animated heatmap of Delhi, showing how temperatures evolve zone by zone over the next 6 hours. Also shows: which zones are escalating fastest, and which are forming dangerous heat clusters.

**3. GCN Comparison Tab**
Side-by-side maps: what the Random Forest predicted vs what the RF+GCN hybrid predicted. A third map shows the correction — where the GCN raised or lowered the RF's estimate and by how much. This visualises exactly where the graph network adds value.

**4. Satellite LST Tab**
The MODIS satellite view — surface temperature across all 600 zones. Shown alongside the air temperature prediction so you can see exactly how much hotter the ground is than the air in each neighbourhood.

**5. Alert System Tab**
The city-wide alert banner, zone-level alert map, and a ranked table of zones that need immediate attention. Actionable recommendations for each alert level.

**6. Model Info Tab**
The technical architecture explained with equations, diagrams, and data source references — for those who want to understand what's running under the hood.

---

## The Technical Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| Weather forecasting | Random Forest (200 trees) | Robust, handles non-linear patterns, no overfitting with depth=10 |
| Spatial refinement | 2-layer GCN (pure PyTorch) | Models heat propagation through city graph, no heavy dependencies |
| Satellite data | MODIS MOD11A1 (NASA) | Daily 1km resolution LST, free and globally available |
| Dashboard | Streamlit + Plotly | Interactive maps and charts, runs locally, no cloud needed |
| City grid | 600 zones, 25×24, 2km spacing | Balances spatial detail with computational tractability |
| Graph topology | 4-neighbour adjacency | Captures direct spatial influence without over-connection |

---

## Why This Is Different From What Exists Today

**Existing systems** use one or two weather stations to forecast for an entire city. They produce a single number: "Delhi will be 43°C tomorrow." That's it.

**Our system** produces 600 numbers — one per zone — updated every hour, 6 hours into the future, with zone-level alert classification.

That difference is not incremental. It's the difference between knowing "there's a fire somewhere in the building" and knowing "there's a fire in Room 412."

---

## Real World Impact

If this system were deployed at scale:

- **Emergency services** could pre-position ambulances near high-risk zones before a heatwave peaks
- **Municipal hospitals** in Warning zones could activate heat emergency protocols hours in advance
- **Construction site managers** could get automatic alerts to halt outdoor work in their specific area
- **City planners** could use the UHI maps to prioritise where to plant trees, install reflective pavements, or build water features
- **Vulnerable populations** — the elderly, those without air conditioning — could be identified by zone and reached proactively

---

## Results Summary

| Model | MAE (°C) | RMSE (°C) | R² |
|-------|----------|-----------|-----|
| Random Forest — Temporal | 0.543 | 0.747 | 0.9836 |
| Random Forest — Spatial | 0.800 | 1.035 | 0.9874 |
| RF + GCN Hybrid | 0.548 | 0.737 | **0.9936** |

The hybrid model achieves **31% lower spatial error** than RF alone, and a near-perfect R² of 0.9936 — meaning it explains 99.36% of all temperature variation across the city grid.

---

## How to Run It

```
Step 1 — (Optional) Fetch a full year of Delhi weather data
         python fetch_historical_data.py

Step 2 — Train the RF + GCN models
         python train_hybrid.py

Step 3 — Launch the dashboard
         streamlit run app.py

Step 4 — Open your browser at:
         http://localhost:8501
```

The dashboard auto-loads the local weather CSV. No manual file upload needed.

---

*Built for Major Project Review II, March 2026.*
*Urban Microclimate Digital Twin — Hyper-Local Short-Term Heatwave Prediction.*
