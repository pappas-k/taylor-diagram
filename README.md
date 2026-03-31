# Taylor Diagram

A generic Python implementation of the Taylor diagram for comparing multiple model signals against a baseline reference.

---

## Features

- **Normalised Standard Deviation (NSD)** on the radial axis — σ\_model / σ\_obs
- **R² (coefficient of determination)** on the angular axis
- **Normalised centred RMSE (NRMSE)** as dashed contours centred on the reference point
- **Summary statistics table** printed to the terminal before plotting: NSD, R, R², NRMSE for every model
- **Synthetic test signals** — sinusoids with configurable amplitude, frequency, phase, and noise level
- Up to **8 labelled model signals** out of the box, trivially extensible
- Optional **figure export** to PNG (or any matplotlib-supported format)

---

## Known simplifications

| What is omitted | Why it matters |
|---|---|
| Angular axis uses R² (not R) | The original Taylor (2001) diagram uses R; here R² is used on the arc for readability |
| Signals are synthetic sinusoids | Real applications would supply observed and modelled time series directly |
| Only centred RMSE is normalised | Total RMSE includes bias; the centred form used here removes the mean difference |

---

## How to run

```bash
# Install dependencies
pip install numpy matplotlib

# Run (opens interactive window and prints statistics)
python3 taylor_diagram_generic.py
```

To save a figure, set `OUTPUT_FILE = 'taylor_diagram.png'` in the CONFIG block before running.

---

## Diagram layout

```
Angular axis (top arc)  →  R²  (0 = orthogonal, 1 = perfect correlation)
Radial axis             →  NSD = σ_model / σ_obs
Dashed contours         →  NRMSE = √(1 + NSD² − 2·NSD·R)
Reference point (✕)     →  (R²=1, NSD=1) — perfect model
```

A model that agrees well with observations plots close to the reference point: NSD ≈ 1, R² ≈ 1, NRMSE ≈ 0.

---

## Requirements

- Python 3.8+
- numpy
- matplotlib

---

## References

- Taylor, K. E. (2001). Summarizing model performance in a single diagram. *Journal of Geophysical Research: Atmospheres*, 106(D7), 7183–7192. https://doi.org/10.1029/2000JD900719
- [Pearson correlation coefficient — Wikipedia](https://en.wikipedia.org/wiki/Pearson_correlation_coefficient)
- [Root mean square deviation — Wikipedia](https://en.wikipedia.org/wiki/Root_mean_square_deviation)
- [Coefficient of determination — Wikipedia](https://en.wikipedia.org/wiki/Coefficient_of_determination)
