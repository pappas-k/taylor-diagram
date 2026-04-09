# Normalised Taylor Diagram

A generic, self-contained Python implementation of the normalised Taylor diagram, a compact polar plot that summarises how well one or more model outputs reproduce a reference (observed) signal using three statistics simultaneously: the normalised standard deviation ($\sigma_N$), the Pearson correlation coefficient ($R$), and the normalised centred root-mean-square error (NRMSE).

The Taylor diagram was introduced by Taylor (2001) as a way to condense model evaluation into a single, readable figure. Each model appears as a point on a polar plot: its angular position encodes the correlation with the reference, its radial distance encodes the ratio of model-to-observed variability, and its distance from the reference point encodes the centred RMSE. A model that perfectly reproduces the observations plots exactly on the reference point.

This repository provides a ready-to-run script that generates such a diagram from synthetic sinusoidal signals and prints a companion statistics table to the terminal. It is designed to be easy to adapt to real observed and modelled time series from any domain, including oceanography, hydrology, atmospheric science, or any other field where model performance assessment is needed.

<div align="center">
  <img src="taylor_diagram.png" width="500"/>
</div>



## Features

- **Normalised Standard Deviation (NSD)** on the radial axis
- **Pearson correlation coefficient ($R$)** on the angular axis
- **Normalised centred RMSE (NRMSE)** as dashed contours centred on the reference point
- **Summary statistics table** printed to the terminal before plotting: NSD, $R$, NRMSE for every model
- **Synthetic test signals**: sinusoids with configurable amplitude, frequency, phase, and noise level
- Up to **8 labelled model signals** out of the box, trivially extensible
- Optional **figure export** to PNG (or any matplotlib-supported format)

---

## How to run

```bash
# Install dependencies
pip install numpy matplotlib

# Run (opens interactive window and prints statistics)
python3 taylor_diagram_norm.py
```

To save a figure, set `OUTPUT_FILE = 'taylor_diagram.png'` in the CONFIG block before running.

---

## Diagram layout

```
Angular axis (top arc)  ->  R    (0 = uncorrelated, 1 = perfect correlation)
Radial axis             ->  NSD  = σ_model / σ_obs
Dashed contours         ->  NRMSE = sqrt(1 + NSD² - 2·NSD·R)
Reference point (X)     ->  (R=1, NSD=1) — perfect model
```

A model that agrees well with observations plots close to the reference point: NSD $\approx 1$, $R \approx 1$, NRMSE $\approx 0$.

---

## Requirements

- Python 3.8+
- numpy
- matplotlib
- LaTeX (optional, for rendered math labels; to disable, comment out `rc('text', usetex=True)` in the script)

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## References
<!-- - Pappas, K. et al. (2025). On the economic feasibility of tidal range power plants. *Proceedings of the Royal Society A*, 481(2305), 20230867. https://doi.org/10.1098/rspa.2023.0867 -->

- Taylor, K. E. (2001). Summarising model performance in a single diagram. *Journal of Geophysical Research: Atmospheres*, 106(D7), 7183-7192. https://doi.org/10.1029/2000JD900719

- [Pearson correlation coefficient - Wikipedia](https://en.wikipedia.org/wiki/Pearson_correlation_coefficient)
- [Root mean square deviation - Wikipedia](https://en.wikipedia.org/wiki/Root_mean_square_deviation)
