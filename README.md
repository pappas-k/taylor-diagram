# Taylor Diagram

A generic, self-contained Python implementation of the normalised Taylor diagram, a compact polar plot that summarises how well one or more model outputs reproduce a reference (observed) signal using three statistics simultaneously: the normalised standard deviation ($\sigma_N$), the Pearson correlation coefficient ($R$), and the normalised centred root-mean-square error (NRMSE).

The Taylor diagram was introduced by Taylor (2001) as a way to condense model evaluation into a single, readable figure. Each model appears as a point on a polar plot: its angular position encodes the correlation with the reference, its radial distance encodes the ratio of model-to-observed variability, and its distance from the reference point encodes the centred RMSE. A model that perfectly reproduces the observations plots exactly on the reference point.

This repository provides a ready-to-run script that generates such a diagram from synthetic sinusoidal signals and prints a companion statistics table to the terminal. It is designed to be easy to adapt to real observed and modelled time series from any domain, including oceanography, hydrology, atmospheric science, or any other field where model performance assessment is needed.

<div align="center">
  <img src="taylor_diagram.png" width="500"/>
</div>

---

## Mathematical derivation

The geometry of the Taylor diagram follows directly from the definition of the centred root-mean-square error (cRMSE) and the Pearson correlation coefficient.

**Step 1 — expand the centred RMSE.**  
For a model signal $f$ and reference signal $r$, both with their means removed, the squared centred RMSE is:

$$E'^2 = \frac{1}{N}\sum_{i=1}^{N}\bigl[(f_i - \bar{f}) - (r_i - \bar{r})\bigr]^2$$

Expanding the square:

$$E'^2 = \sigma_f^2 + \sigma_r^2 - \frac{2}{N}\sum_{i=1}^{N}(f_i - \bar{f})(r_i - \bar{r})$$

**Step 2 — introduce the Pearson correlation coefficient.**  
By definition, $R = \frac{1}{N\,\sigma_f\,\sigma_r}\sum(f_i-\bar{f})(r_i-\bar{r})$, so:

$$E'^2 = \sigma_f^2 + \sigma_r^2 - 2\,\sigma_f\,\sigma_r\,R$$

**Step 3 — normalise by $\sigma_r$.**  
Dividing through by $\sigma_r^2$ and defining $\sigma_N = \sigma_f/\sigma_r$:

$$\text{NRMSE}^2 = \sigma_N^2 + 1 - 2\,\sigma_N\,R$$

**Step 4 — recognise the law of cosines.**  
Setting $\theta = \arccos(R)$, this is identical to the law of cosines for a triangle with sides $\sigma_N$, $1$, and NRMSE:

$$\text{NRMSE}^2 = \sigma_N^2 + 1^2 - 2\,\sigma_N\cdot 1\cdot\cos\theta$$

The consequence is geometric: in polar coordinates $(\theta, r) = (\arccos R,\; \sigma_N)$, the NRMSE is exactly the Euclidean distance from each model point to the **reference point** $(R=1,\; \sigma_N=1)$. Constant-NRMSE contours are therefore circles centred on the reference point.

---

## Practical application

This implementation was used in the following peer-reviewed study:

> Pappas, K., Nguyen, Q. C., Zilakos, I., Beevers, L., & Angeloudis, A. (2025). On the economic feasibility of tidal range power plants. *Proceedings of the Royal Society A: Mathematical, Physical and Engineering Sciences*, 481(2305), 20230867. https://doi.org/10.1098/rspa.2023.0867

In that paper, Taylor diagrams were used to evaluate and compare hydrodynamic model outputs against observational reference data as part of an integrated framework for assessing tidal range power plants. The framework combined operation strategy optimisation, hydrodynamic impact modelling, and techno-economic analysis (CAPEX and LCOE). The study redesigned 18 tidal range installations across UK sites and demonstrated that equivalent or lower levelised costs of energy can be achieved at substantially reduced capital expenditure, strengthening the economic case for tidal range energy.

---

## Citation

If you use this code, please cite:

1. **The paper above** (practical application and context):
   > Pappas, K., Nguyen, Q. C., Zilakos, I., Beevers, L., & Angeloudis, A. (2025). On the economic feasibility of tidal range power plants. *Proceedings of the Royal Society A*, 481(2305), 20230867. https://doi.org/10.1098/rspa.2023.0867

2. **The original Taylor diagram paper**:
   > Taylor, K. E. (2001). Summarizing model performance in a single diagram. *Journal of Geophysical Research: Atmospheres*, 106(D7), 7183-7192. https://doi.org/10.1029/2000JD900719

---

## Features

- **Normalised Standard Deviation ($\sigma_N$)** on the radial axis
- **Pearson correlation coefficient ($R$)** on the angular axis
- **Normalised centred RMSE (NRMSE)** as dashed contours centred on the reference point
- **Summary statistics table** printed to the terminal before plotting: $\sigma_N$, $R$, $R^2$, NRMSE for every model
- **Synthetic test signals**: sinusoids with configurable amplitude, frequency, phase, and noise level
- Up to **8 labelled model signals** out of the box, trivially extensible
- Optional **figure export** to PNG (or any matplotlib-supported format)

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
Angular axis (top arc)  ->  R   (0 = uncorrelated, 1 = perfect correlation)
Radial axis             ->  σ_N = σ_model / σ_obs
Dashed contours         ->  NRMSE = sqrt(1 + σ_N² - 2·σ_N·R)
Reference point (X)     ->  (R=1, σ_N=1) — perfect model
```

A model that agrees well with observations plots close to the reference point: $\sigma_N \approx 1$, $R \approx 1$, NRMSE $\approx 0$.

---

## Requirements

- Python 3.8+
- numpy
- matplotlib

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## References
- Pappas, K. et al. (2025). On the economic feasibility of tidal range power plants. *Proceedings of the Royal Society A*, 481(2305), 20230867. https://doi.org/10.1098/rspa.2023.0867

- Taylor, K. E. (2001). Summarising model performance in a single diagram. *Journal of Geophysical Research: Atmospheres*, 106(D7), 7183-7192. https://doi.org/10.1029/2000JD900719

- [Pearson correlation coefficient - Wikipedia](https://en.wikipedia.org/wiki/Pearson_correlation_coefficient)
- [Root mean square deviation - Wikipedia](https://en.wikipedia.org/wiki/Root_mean_square_deviation)
- [Coefficient of determination - Wikipedia](https://en.wikipedia.org/wiki/Coefficient_of_determination)
