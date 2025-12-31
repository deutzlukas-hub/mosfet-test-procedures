import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

from dirs import data_gnucap_dir, data_ngspice_dir, figures_dir
from parse import parse_gnucap, parse_ngspice, split_nested_sweep
from python.util import supported_models
from util import calc_abs_rel_err
import style

VIN = {
    'cs_amp': np.array([0.4, 0.5, 0.6]),
    'cd_amp': np.array([0.4, 0.5, 0.6]),
    'cg_amp': np.array([-0.3, -0.4, -0.5]),
}

ac_test_tiles = {
    'cs_amp': 'Common Source Amplifier',
    'cd_amp': 'Common Drain Amplifier',
    'cg_amp': 'Common Gain Amplifier',
}

def get_input_output_voltage(technology: str, model: str, test: str):

    result_gnucap_ac_dir = data_gnucap_dir / technology / model / 'ac'
    result_ngspice_ac_dir = data_ngspice_dir / technology /model / 'ac'

    gc_filepath = result_gnucap_ac_dir / (test + '.gc.out')
    ngs_filepath = result_ngspice_ac_dir / (test + '.sp.out')

    gc_data_arr = parse_gnucap(gc_filepath, starts_with='#Freq')
    ngs_data_arr = parse_ngspice(ngs_filepath)

    gc_f_arr = gc_data_arr[:, 0]
    ngs_f_arr = ngs_data_arr[:, 0]
    assert np.allclose(gc_f_arr, ngs_f_arr)
    f_arr = gc_f_arr

    gc_v_in_arr = gc_data_arr[:, 1]
    gc_v_out_arr = gc_data_arr[:, 2]

    ngs_v_in_arr = ngs_data_arr[:, 1]
    ngs_v_out_arr = ngs_data_arr[:, 2]

    # Dbs into volt
    gc_v_in_arr = 10**(gc_v_in_arr/20)
    gc_v_out_arr = 10**(gc_v_out_arr/20)
    ngs_v_in_arr = 10**(ngs_v_in_arr/20)
    ngs_v_out_arr = 10**(ngs_v_out_arr/20)

    return f_arr, gc_v_in_arr, gc_v_out_arr, ngs_v_in_arr, ngs_v_out_arr

def plot_amplifier(technology: str, model: str, test_name: str = 'cs_amp', VNOM=1.2):
    figures_ac_dir = figures_dir / technology / model / 'ac'
    figures_ac_dir.mkdir(parents=True, exist_ok=True)

    tests = [f'{test_name}_1', f'{test_name}_2', f'{test_name}_3']

    Vin_arr = VIN[test_name] * VNOM

    fig = plt.figure(figsize=style.FIGSIZE)
    gs = plt.GridSpec(2, 1,
                      bottom=style.BOTTOM, left=style.LEFT, right=style.RIGHT, hspace=style.HSPACE)
    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1], sharex=ax0)
    ax0.text(-0.2, 1.05, 'A', transform=ax0.transAxes, fontsize=style.FS['panel'])
    ax1.text(-0.2, 1.05, 'B', transform=ax1.transAxes, fontsize=style.FS['panel'])

    cmap = plt.get_cmap('spring')
    norm = Normalize(vmin=min(Vin_arr), vmax=max(Vin_arr))

    for i, (test, vin) in enumerate(zip(tests, Vin_arr)):
        f_arr, gc_v_in, gc_v_out, ngs_v_in, ngs_v_out = get_input_output_voltage(technology, model, test)
        Av_gc = gc_v_out / gc_v_in
        Av_ngs = ngs_v_out / ngs_v_in
        rel_err = calc_abs_rel_err(Av_gc, Av_ngs)

        color = cmap(norm(vin))

        ax0.semilogx(f_arr, Av_gc, c=color, ls='-', label=f'{vin:.2f}V')
        ax0.semilogx(f_arr, Av_ngs, c='k', ls='--', label='Ngspice' if i == 2 else '')
        ax1.loglog(f_arr, rel_err, c=color)

    ax0.set_title(model + " " + ac_test_tiles[test_name])
    ax0.set_ylabel(r'$A_v$')

    ax1.set_ylabel(style.REL_ERR_LABEL, fontsize=style.FS['math'])
    ax1.set_xlabel('frequency [Hz]')

    fig.legend(title=r'$V_{\mathrm{in}}$', ncol=1, bbox_to_anchor=(0.8, 0.5), loc='center left')
    fig.align_ylabels()
    plt.savefig(figures_ac_dir / (test_name + '.png'))
    plt.close(fig)

    return
if __name__ == '__main__':

    for technology in ['cmos90']:
        for model in supported_models:
            print(f'Plotting AC results for {technology} {model}...')
            plot_amplifier('cmos90', model, 'cs_amp')
            plot_amplifier('cmos90', model, 'cd_amp')
            plot_amplifier('cmos90', model, 'cg_amp')

# def plot_voltage_gain(model: str, name: str):
#
#     f_arr, gc_v_in_arr, gc_v_out_arr, ngs_v_in_arr, ngs_v_out_arr = get_input_output_voltage(model, name)
#
#     fig = plt.figure(figsize=(6, 6))
#     gs = plt.GridSpec(2, 1, hspace=0.4)
#     ax0 = plt.subplot(gs[0])
#     ax1 = plt.subplot(gs[1], sharex=ax0)
#
#     gc_A_v = gc_v_out_arr / gc_v_in_arr
#     ngs_A_v = ngs_v_out_arr / ngs_v_in_arr
#
#     plt.margins(0.03)
#     ax0.tick_params(axis='both', which='major', labelsize=12)
#     ax0.tick_params(axis='both', which='major', labelsize=12)
#
#     ax0.set_title('B', loc='left', fontsize = 18)
#     ax0.semilogx(f_arr, gc_A_v, c='k', label = 'Gnucap')
#     ax0.semilogx(f_arr, ngs_A_v, c='r', ls = '--', label = 'Ngspice')
#     ax0.set_ylabel(r'$A_v$', fontsize=14)
#
#     ax0.legend()
#
#     ax0.grid(True)
#     ax0.set_xlabel('frequency [Hz]', fontsize=14)
#
#     rel_err = calc_abs_rel_err(gc_A_v, ngs_A_v)
#
#     ax1.set_title('B', loc='left', fontsize = 18)
#     ax1.loglog(f_arr, rel_err, c='k')
#     ax1.grid(True)
#
#     ax1.set_ylabel(r'$V_\mathrm{out}/V_\mathrm{in}$', fontsize=14)
#     ax1.set_xlabel('frequency [Hz]', fontsize=14)
#
#     plt.show()
#
#
# def plot_cascode():
#
#     result_gnucap_ac_dir = data_gnucap_dir / 'psp104' / 'ac'
#     result_ngspice_ac_dir = data_ngspice_dir / 'psp104' / 'ac'
#     figures_dc_dir = figures_dir / 'psp104' / 'ac'
#
#     gc_filepath = result_gnucap_ac_dir / ('cascode' + '.gc.out')
#     ngs_filepath = result_ngspice_ac_dir / ('cascode' + '.sp.out')
#
#     gc_data_arr = parse_gnucap(gc_filepath, starts_with='#Freq')
#     ngs_data_arr = parse_ngspice(ngs_filepath)
#
#     fig = plt.figure(figsize=(6, 6))
#     gs = plt.GridSpec(2, 1, hspace=0.4)
#     ax0 = plt.subplot(gs[0])
#     ax1 = plt.subplot(gs[1], sharex=ax0)
#
#     gc_f_arr = gc_data_arr[:, 0]
#     ngs_f_arr = ngs_data_arr[:, 0]
#     assert np.allclose(gc_f_arr, ngs_f_arr)
#     f_arr = gc_f_arr
#
#     # Convert into linear
#     gc_v_in_arr = 10 ** (gc_data_arr[:, 1] / 20)
#     gc_v_out_arr = 10 ** (gc_data_arr[:, 2] / 20)
#     ngs_v_in_arr = 10 ** (ngs_data_arr[:, 1] / 20)
#     ngs_v_out_arr = 10 ** (ngs_data_arr[:, 2] / 20)
#
#     gc_A_v = gc_v_out_arr / gc_v_in_arr
#     ngs_A_v = ngs_v_out_arr / ngs_v_in_arr
#
#     plt.margins(0.03)
#
#     ax0.set_title('B', loc='left', fontsize=18)
#     ax0.semilogx(f_arr, gc_A_v, c='k', label='Gnucap')
#     ax0.semilogx(f_arr, ngs_A_v, c='r', ls='--', label='Ngspice')
#     ax0.set_ylabel(r'$A_v$', fontsize=14)
#
#     ax0.legend()
#
#     ax0.grid(True)
#     ax0.set_xlabel('frequency [Hz]', fontsize=14)
#
#     rel_err = calc_abs_rel_err(gc_A_v, ngs_A_v)
#
#     ax1.set_title('B', loc='left', fontsize=18)
#     ax1.loglog(f_arr, rel_err, c='k')
#     ax1.grid(True)
#
#     ax1.set_ylabel(r'$V_\mathrm{out}/V_\mathrm{in}$', fontsize=14)
#     ax1.set_xlabel('frequency [Hz]', fontsize=14)
#
#     plt.show()
#
#     return



