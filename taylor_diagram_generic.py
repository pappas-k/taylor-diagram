# -*- coding: utf-8 -*-
"""
taylor_diagram_generic.py
-------------------------
Generic Taylor diagram comparing multiple model signals against a baseline.
Signals are synthetic sinusoids. Statistics (NSD, R, R², NRMSE) are computed
and printed as a summary table before plotting.

Taylor diagram axes:
  - Radial   : Normalised Standard Deviation  NSD = σ_model / σ_obs
  - Angular  : R² coefficient of determination
  - Contours : Normalised centred RMSE  NRMSE = cRMSE / σ_obs
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.projections import PolarAxes
import mpl_toolkits.axisartist.grid_finder as gf
import mpl_toolkits.axisartist.floating_axes as fa
from matplotlib import rc
from matplotlib.lines import Line2D

rc('font', **{'family': 'serif', 'size': 15})
rc('text', usetex=True)          # comment out if LaTeX is not installed


# ══════════════════════════════════════════════════════════════════════════════
#  CONFIG  —  edit this block
# ══════════════════════════════════════════════════════════════════════════════

t = np.linspace(0, 10, 2000)    # time vector

# Baseline (observed reference):  A * sin(2π f t + φ)
BASELINE = dict(A=1.00, f=1.00, phi=0.00, noise=0.00)

# Model signals — adjust A (amplitude), f (frequency), phi (phase), noise
MODELS = [
    dict(A=0.95, f=1.00, phi=0.15, noise=0.05, label=r'Model 1', color='steelblue'),
    dict(A=1.20, f=1.00, phi=0.40, noise=0.10, label=r'Model 2', color='darkorange'),
    dict(A=0.80, f=1.01, phi=0.60, noise=0.12, label=r'Model 3', color='mediumseagreen'),
    dict(A=1.10, f=0.99, phi=0.20, noise=0.08, label=r'Model 4', color='crimson'),
    dict(A=0.85, f=1.00, phi=0.70, noise=0.15, label=r'Model 5', color='mediumpurple'),
    dict(A=1.05, f=1.02, phi=0.30, noise=0.18, label=r'Model 6', color='saddlebrown'),
    dict(A=0.90, f=0.98, phi=0.50, noise=0.07, label=r'Model 7', color='deeppink'),
    dict(A=1.15, f=1.01, phi=0.45, noise=0.20, label=r'Model 8', color='teal'),
]

OUTPUT_FILE = 'taylor_diagram.png'

# ══════════════════════════════════════════════════════════════════════════════


def make_signal(t, A, f, phi, noise, seed=0):
    """Return  A·sin(2π f t + φ)  plus optional white noise."""
    rng = np.random.default_rng(seed)
    return A * np.sin(2 * np.pi * f * t + phi) + rng.normal(0.0, noise, t.size)


def compute_statistics(obs, mod):
    """
    Return NSD, Pearson R, R², and NRMSE for a model against observations.

    NSD   = σ_mod / σ_obs
    R     = Pearson correlation coefficient
    R²    = coefficient of determination  (1 − SS_res / SS_tot)
    NRMSE = √(1 + NSD² − 2·NSD·R)   (centred RMSE normalised by σ_obs)
    """
    std_obs = np.std(obs)
    nsd     = np.std(mod) / std_obs
    r       = float(np.corrcoef(obs, mod)[0, 1])
    r2      = 1.0 - np.sum((obs - mod) ** 2) / np.sum((obs - np.mean(obs)) ** 2)
    nrmse   = np.sqrt(1.0 + nsd**2 - 2.0 * nsd * r)
    return nsd, r, r2, nrmse


def setup_taylor_axes(fig, rect=111, smax=1.5):
    """
    Build the quarter-circle polar axes for the Taylor diagram.
    Returns the auxiliary axes used for all subsequent plotting.
    """
    tr = PolarAxes.PolarTransform()

    # R² ticks on the arc
    r2_ticks = np.concatenate((np.arange(11.0) / 10.0, [0.95, 0.99]))
    t_ticks  = np.arccos(r2_ticks)
    gh = fa.GridHelperCurveLinear(
        tr,
        extremes=(0, np.pi / 2, 0, smax),
        grid_locator1=gf.FixedLocator(t_ticks),
        tick_formatter1=gf.DictFormatter(dict(zip(t_ticks, map(str, r2_ticks)))),
    )

    ax = fa.FloatingSubplot(fig, rect, grid_helper=gh)
    fig.add_subplot(ax)

    # Configure the three visible axes: top (R²), left and right (σ_N)
    axis_config = {
        'top':   dict(axis_dir='bottom', tick_dir='top',   label_dir='top',   text='$R^2$'),
        'left':  dict(axis_dir='bottom', tick_dir='bottom', label_dir='bottom', text=r'$\sigma_N$'),
        'right': dict(axis_dir='top',    tick_dir='left',   label_dir='top',   text=r'$\sigma_N$'),
    }
    for side, cfg in axis_config.items():
        ax.axis[side].set_axis_direction(cfg['axis_dir'])
        ax.axis[side].toggle(ticklabels=True, label=True)
        ax.axis[side].major_ticklabels.set_axis_direction(cfg['tick_dir'])
        ax.axis[side].label.set_axis_direction(cfg['label_dir'])
        ax.axis[side].label.set_text(cfg['text'])
        ax.axis[side].label.set_fontsize(22)
    ax.axis['bottom'].set_visible(False)
    ax.grid()

    aux_ax = ax.get_aux_axes(tr)
    aux_ax.plot([0], [1.0], 'kX', ms=8, zorder=5)
    aux_ax.plot(np.linspace(0, np.pi / 2), np.ones(50), 'k--', lw=0.8)

    return aux_ax


def add_nrmse_contours(aux_ax, smax=1.5, levels=None):
    """
    Draw NRMSE contours on the Taylor diagram.
    Contours are circles centred at the reference point (R²=1, NSD=1).
    NRMSE = √(1 + NSD² − 2·NSD·cos(θ))
    """
    if levels is None:
        levels = [0.25, 0.50, 0.75, 1.00]

    rs, ts = np.meshgrid(
        np.linspace(0, smax, 300),
        np.linspace(0, np.pi / 2, 300),
    )
    NRMSE = np.sqrt(1.0 + rs**2 - 2.0 * rs * np.cos(ts))
    cs = aux_ax.contour(ts, rs, NRMSE, levels=levels,
                        colors='navy', linestyles='--', linewidths=0.8)
    plt.clabel(cs, fmt='%.2f', fontsize=14, inline=True)


def plot_taylor(stats, model_defs, output_file=None):
    """
    Plot the Taylor diagram.

    Parameters
    ----------
    stats      : list of (nsd, r, r2, nrmse) — one tuple per model
    model_defs : list of model dicts with keys 'label' and 'color'
    """
    fig    = plt.figure(figsize=(8, 8))
    aux_ax = setup_taylor_axes(fig, rect=111, smax=1.5)
    add_nrmse_contours(aux_ax)

    for (nsd, r, r2, nrmse), m in zip(stats, model_defs):
        aux_ax.plot(
            np.arccos(r2), nsd,
            marker='o', color=m['color'],
            markeredgecolor='black', markeredgewidth=0.5,
            ms=8, zorder=5, ls='',
        )

    # Legend
    handles = [
        Line2D([0], [0], marker='X', color='k', linestyle='None',
               markersize=8, label='Baseline'),
    ] + [
        Line2D([0], [0], marker='o', color=m['color'], linestyle='None',
               markeredgecolor='black', markeredgewidth=0.5,
               markersize=9, label=m['label'])
        for m in model_defs
    ]
    fig.legend(handles=handles, loc='upper left',
               bbox_to_anchor=(0.78, 0.95), frameon=False, fontsize=14)

    fig.text(0.40, 0.62, 'NRMSE', rotation=18, color='navy', fontsize=14)

    if output_file:
        plt.savefig(output_file, dpi=600, bbox_inches='tight')
        print(f'Saved: {output_file}')
    plt.show()
    plt.close(fig)


# ── Run ───────────────────────────────────────────────────────────────────────

if __name__ == '__main__':

    # Build signals
    obs    = make_signal(t, **BASELINE, seed=0)
    models = [make_signal(t, **{k: v for k, v in m.items()
                                if k not in ('label', 'color')}, seed=i + 1)
              for i, m in enumerate(MODELS)]

    # Compute statistics
    stats = [compute_statistics(obs, mod) for mod in models]

    # Print summary table
    header = f"{'Model':<12}  {'NSD':>8}  {'R':>8}  {'R2':>8}  {'NRMSE':>8}"
    sep    = '─' * len(header)
    print(f'\n{sep}\n{header}\n{sep}')
    for m, (nsd, r, r2, nrmse) in zip(MODELS, stats):
        print(f"{m['label']:<12}  {nsd:>8.4f}  {r:>8.4f}  {r2:>8.4f}  {nrmse:>8.4f}")
    print(sep + '\n')

    # Plot
    plot_taylor(stats, MODELS, output_file=OUTPUT_FILE)
