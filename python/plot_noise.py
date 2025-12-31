import numpy as np
import matplotlib.pyplot as plt

from dirs import data_gnucap_dir, data_ngspice_dir, figures_dir
from parse import parse_gnucap, parse_ngspice
from util import calc_abs_rel_err, supported_models
import style


def load_noise_analysis(technology: str, test_name: str, model: str):

    gc_filepath = data_gnucap_dir / technology / model / 'noise' / f'{test_name}.gc.out'
    ngs_filepath = data_ngspice_dir / technology /model / 'noise' / f'{test_name}.sp.out'

    ng_data = parse_ngspice(ngs_filepath)
    gc_data = parse_gnucap(gc_filepath, starts_with='#Freq')

    return gc_data, ng_data

def plot_resistor_noise(model: str, test_name: str = 'resistor'):

    figures_out_dir = figures_dir / model / 'noise'
    figures_out_dir.mkdir(parents=True, exist_ok=True)

    T_list = [-40., 27., 125.]

    R = 1000.0
    k = 1.380649*10**(-23)

    fig = plt.figure(figsize=(8, 6))
    gs = plt.GridSpec(1, 2, wspace=0.4, left=0.2)
    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1])

    S_gc_list, S_ns_list, S_theo_list = [], [], []

    for i, (test_name, T) in enumerate(zip(['resistor_1', 'resistor_2', 'resistor_3'], T_list)):

        # Load data
        gc_data, ng_data = load_noise_analysis(test_name, model)
        f_ng_arr = ng_data[:, 0]
        f_gc_arr = gc_data[:, 0]
        assert np.allclose(f_ng_arr, f_gc_arr)
        f_arr = f_gc_arr

        onoise_gc = gc_data[:, 1]
        onoise_ng = ng_data[:, 2]**2

        S_gc_list.append(onoise_gc.mean())
        S_ns_list.append(onoise_ng.mean())

        # Theory
        T = T + 273.15
        S = 4.0 * k * T * R
        S_theo_list.append(S)

        if i == 1:
            # Output noise
            ax0.hlines(S, f_arr[0], f_arr[-1], colors='k', ls='-', lw=2.0, label='theory')
            ax0.loglog(f_arr, onoise_gc, c='r', lw=2.0, label='gnucap')
            ax0.loglog(f_arr, onoise_ng, c='b', ls='--', lw=2.0, label='ngspice')
            ax0.set_ylim(S * 0.9, S * 1.1)

    ax1.plot(T_list, S_theo_list, '-', c='k', label = 'theory')
    ax1.plot(T_list, S_gc_list, 'o', c='r',  label = 'gnucap')
    ax1.plot(T_list, S_ns_list, 'x', c='b', label = 'ngspice')

    ax0.set_ylabel(r'PSD [$V^2$/Hz]', fontsize=14)
    ax0.set_xlabel('Frequency [Hz]', fontsize=14)
    ax0.grid(True, which='both')
    ax0.legend()

    ax1.set_xlabel('Temperature [°C]', fontsize=14)
    ax1.set_ylabel(r'PSD [$V^2$/Hz]', fontsize=14)
    ax0.grid(True, which='both')

    plt.suptitle('Resistor thermal noise')

    # Save
    # out_path = figures_out_dir / f'{test_name}.png'
    # plt.savefig(out_path, dpi=150)
    # plt.close(fig)

    plt.show()

# --- plotting ----------------------------------------------------------------

def plot_nmos(technology: str, model: str):
    test_names, temperatures = ['nmos_1', 'nmos_2', 'nmos_3'], [-40, 27, 125]
    colors = ['red', 'green', 'blue']

    figures_out_dir = figures_dir / technology / model / 'noise'
    figures_out_dir.mkdir(parents=True, exist_ok=True)

    # Create figure with consistent style
    fig = plt.figure(figsize=style.FIGSIZE)
    gs = plt.GridSpec(2, 1,
                      bottom=style.BOTTOM, left=style.LEFT, right=style.RIGHT, hspace=style.HSPACE)
    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1], sharex=ax0)

    # Add panel labels
    ax0.text(-0.2, 1.05, 'A', transform=ax0.transAxes, fontsize=style.FS['panel'])
    ax1.text(-0.2, 1.05, 'B', transform=ax1.transAxes, fontsize=style.FS['panel'])

    for test_name, temp, color in zip(test_names, temperatures, colors):
        gc_data, ng_data = load_noise_analysis(technology, test_name, model)

        f_gc = gc_data[:, 0]
        onoise_gc = gc_data[:, 1]

        f_ng = ng_data[:, 0]
        onoise_ng = ng_data[:, 2] ** 2

        assert np.allclose(f_ng, f_gc)
        f_arr = f_gc

        err_onoise = calc_abs_rel_err(onoise_gc, onoise_ng)

        ax0.loglog(f_arr, onoise_gc, c=color, ls='-', label=f'{temp}°C')
        ax0.loglog(f_arr, onoise_ng, c='black', ls='--', lw=2.0,
                   label='ngspice' if temp == 125 else '')

        # Relative error
        ax1.loglog(f_arr, err_onoise, c=color, lw=1.6)

    # Use consistent styling for labels and title
    ax0.set_title(f'{model}: NMOS + resistor noise')
    ax0.set_ylabel(r'PSD [$V^2$/Hz]', fontsize=style.FS['math'])
    ax1.set_ylabel(style.REL_ERR_LABEL, fontsize=style.FS['math'])
    ax1.set_xlabel(r'Frequency [Hz]')

    # Add grids
    ax0.grid(True)
    ax1.grid(True)

    # Place legend in consistent location
    fig.legend(title=r'Temperature', ncol=1,
               bbox_to_anchor=(0.8, 0.5), loc='center left')

    # Align ylabels
    fig.align_ylabels()

    # Save figure
    save_path = figures_out_dir / f'nmos.png'
    plt.savefig(save_path)
    plt.close(fig)
if __name__ == '__main__':

    for technology in ['cmos90']:
        for model in supported_models:
            print(f'Plotting nmos noise for {technology} {model}...')
            plot_nmos(technology, model)




