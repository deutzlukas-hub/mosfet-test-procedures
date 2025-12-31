from scipy.interpolate import interp1d

import matplotlib.pyplot as plt

from dirs import data_gnucap_dir, data_ngspice_dir, figures_dir
from parse import parse_gnucap, parse_ngspice
from util import calc_abs_rel_err, supported_models
import style

def load_data(test_name: str, technology: str, model: str):
    gc_filepath = data_gnucap_dir / technology / model / 'transient' / (test_name + '.gc.out')
    ngs_filepath = data_ngspice_dir / technology / model / 'transient' / (test_name + '.sp.out')
    gc_data_arr = parse_gnucap(gc_filepath, starts_with='#Time')
    ngs_data_arr = parse_ngspice(ngs_filepath)
    return gc_data_arr, ngs_data_arr

def plot_not(technology: str, model: str):

    figures_trans_dir = figures_dir / technology / model / 'transient'
    figures_trans_dir.mkdir(parents=True, exist_ok=True)

    gc_data_arr, ngs_data_arr = load_data('not', technology, model)

    gc_t_arr = gc_data_arr[:, 0] * 1e9  # Convert to nanoseconds
    gc_v_in_arr = gc_data_arr[:, 1]
    gc_v_out_arr = gc_data_arr[:, 2]

    ngs_t_arr = ngs_data_arr[:, 0] * 1e9
    ngs_v_in_arr = ngs_data_arr[:, 1]
    ngs_v_out_arr = ngs_data_arr[:, 2]

    plt.figure(figsize=style.FIGSIZE_2)
    gs = plt.GridSpec(3, 1, hspace=0.3)
    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1], sharex=ax0)
    ax2 = plt.subplot(gs[2], sharex=ax0)

    ax0.plot(gc_t_arr, gc_v_in_arr, c='r', lw=2.0, label='Input (gnucap)')
    ax0.plot(ngs_t_arr, ngs_v_in_arr, c='k', ls='--', lw=1.0, label='ngspice')

    ax1.plot(gc_t_arr, gc_v_out_arr, c='g', lw=2.0, label='Output (gnucap)')
    ax1.plot(ngs_t_arr, ngs_v_out_arr, c='k', ls='--', lw=1.0, label='Output (ngspice)')

    f = interp1d(ngs_t_arr, ngs_v_out_arr, kind='cubic', fill_value='extrapolate')
    ngs_v_out_interp = f(gc_t_arr)
    rel_err_out = calc_abs_rel_err(gc_v_out_arr, ngs_v_out_interp)
    ax2.semilogy(gc_t_arr, rel_err_out, c='k', ls='-', lw=2.0)

    ax0.set_ylabel(r'$V_{\mathrm{in}}$ [V]')
    ax1.set_ylabel(r'$V_{\mathrm{out}}$ [V]')
    ax2.set_ylabel(style.REL_ERR_LABEL)
    ax2.set_xlabel('Time [ns]')

    ax0.grid(True)
    ax1.grid(True)
    ax2.grid(True)
    ax0.legend()
    ax1.legend()

    out_path = figures_trans_dir / 'not.png'
    plt.savefig(out_path)

    return

def plot_logic_gate(technology: str, model: str, test_name: str):

    figures_trans_dir = figures_dir / technology / model / 'transient'
    figures_trans_dir.mkdir(parents=True, exist_ok=True)

    gc_data_arr, ngs_data_arr = load_data(test_name, technology, model)

    gc_t_arr = gc_data_arr[:, 0] * 1e9  # Convert to nanoseconds
    gc_v_in1_arr = gc_data_arr[:, 1]
    gc_v_in2_arr = gc_data_arr[:, 2]
    gc_v_out_arr = gc_data_arr[:, 3]

    ngs_t_arr = ngs_data_arr[:, 0] * 1e9  # Convert to nanoseconds
    ngs_v_in1_arr = ngs_data_arr[:, 1]
    ngs_v_out_arr = ngs_data_arr[:, 3]

    # Interpolate ngspice data to gnucap time points
    f = interp1d(ngs_t_arr, ngs_v_out_arr, kind='cubic', fill_value='extrapolate')
    ngs_v_out_interp = f(gc_t_arr)
    rel_err_out = calc_abs_rel_err(gc_v_out_arr, ngs_v_out_interp)

    plt.figure(figsize=style.FIGSIZE_2)
    gs = plt.GridSpec(3, 1, hspace=0.3)
    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1], sharex=ax0)
    ax2 = plt.subplot(gs[2], sharex=ax0)

    ax0.plot(gc_t_arr, gc_v_in1_arr, c='r', lw=2.0, label='Input 1 (gnucap)')
    ax0.plot(gc_t_arr, gc_v_in2_arr, c='b', lw=2.0, label='Input 2 (gnucap)')

    ax0.plot(ngs_t_arr, ngs_v_in1_arr, c='k', ls='--', lw=1.0, label='ngspice')

    ax1.plot(gc_t_arr, gc_v_out_arr, c='g', lw=2.0, label='Output (gnucap)')
    ax1.plot(ngs_t_arr, ngs_v_out_arr, c='k', lw=1.0, ls='--', label='Output (ngspice)')

    ax2.semilogy(gc_t_arr, rel_err_out, c='k', ls='-', lw=2.0)

    ax0.set_ylabel(r'$V_{\mathrm{in}}$ [V]')
    ax1.set_ylabel(r'$V_{\mathrm{out}}$ [V]')
    ax2.set_ylabel(style.REL_ERR_LABEL)
    ax2.set_xlabel('Time [ns]')

    ax0.legend()
    ax1.legend()

    out_path = figures_trans_dir / (test_name + '.png')
    plt.savefig(out_path)
    return


def plot_inv_chain(technology: str, model: str):
    figures_trans_dir = figures_dir / technology / model / 'transient'
    figures_trans_dir.mkdir(parents=True, exist_ok=True)
    gc_data_arr, ngs_data_arr = load_data('inv_chain', technology, model)

    gc_t_arr = gc_data_arr[:, 0] * 1e9  # Convert to nanoseconds
    gc_v_in_arr = gc_data_arr[:, 1]
    gc_v_out_arr = gc_data_arr[:, 2]

    ngs_t_arr = ngs_data_arr[:, 0] * 1e9
    ngs_v_in_arr = ngs_data_arr[:, 1]
    ngs_v_out_arr = ngs_data_arr[:, 2]

    plt.figure(figsize=style.FIGSIZE_2)
    gs = plt.GridSpec(3, 1, hspace=0.3)
    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1], sharex=ax0)
    ax2 = plt.subplot(gs[2], sharex=ax0)

    ax0.plot(gc_t_arr, gc_v_in_arr, c='r', lw=2.0, label='Input (gnucap)')
    ax0.plot(ngs_t_arr, ngs_v_in_arr, c='k', ls='--', lw=1.0, label='ngspice')

    ax1.plot(gc_t_arr, gc_v_out_arr, c='g', lw=2.0, label='Output (gnucap)')
    ax1.plot(ngs_t_arr, ngs_v_out_arr, c='k', ls='--', lw=1.0, label='Output (ngspice)')

    # Interpolate ngspice data to gnucap time points
    f = interp1d(ngs_t_arr, ngs_v_out_arr, kind='cubic', fill_value='extrapolate')
    ngs_v_out_interp = f(gc_t_arr)
    rel_err_out = calc_abs_rel_err(gc_v_out_arr, ngs_v_out_interp)
    ax2.semilogy(gc_t_arr, rel_err_out, c='k', ls='-', lw=2.0)

    ax0.set_ylabel(r'$V_{\mathrm{in}}$ [V]')
    ax1.set_ylabel(r'$V_{\mathrm{out}}$ [V]')
    ax2.set_ylabel(style.REL_ERR_LABEL)
    ax2.set_xlabel('Time [ns]')

    ax0.legend()
    ax1.legend()

    out_path = figures_trans_dir / 'inv_chain.png'
    plt.savefig(out_path)

    return out_path


def plot_inv_ring(technology: str, model: str):
    figures_trans_dir = figures_dir / technology / model / 'transient'
    figures_trans_dir.mkdir(parents=True, exist_ok=True)

    gc_data_arr, ngs_data_arr = load_data('inv_ring', technology, model)

    gc_t_arr = gc_data_arr[:, 0] * 1e9  # Convert to nanoseconds
    gc_v_in_arr = gc_data_arr[:, 1]
    gc_v_out_arr = gc_data_arr[:, 2]

    ngs_t_arr = ngs_data_arr[:, 0] * 1e9
    ngs_v_in_arr = ngs_data_arr[:, 1]
    ngs_v_out_arr = ngs_data_arr[:, 2]

    plt.figure(figsize=style.FIGSIZE_2)
    gs = plt.GridSpec(3, 1, hspace=0.3)
    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1], sharex=ax0)
    ax2 = plt.subplot(gs[2], sharex=ax0)

    ax0.plot(gc_t_arr, gc_v_in_arr, c='r', lw=2.0, label='Input (gnucap)')
    ax0.plot(ngs_t_arr, ngs_v_in_arr, c='k', ls='--', lw=1.0, label='ngspice')

    ax1.plot(gc_t_arr, gc_v_out_arr, c='g', lw=2.0, label='Output (gnucap)')
    ax1.plot(ngs_t_arr, ngs_v_out_arr, c='k', ls='--', lw=1.0, label='ngspice')

    f = interp1d(ngs_t_arr, ngs_v_out_arr, kind='linear', fill_value='extrapolate')
    ngs_v_out_interp = f(gc_t_arr)
    rel_err_out = calc_abs_rel_err(gc_v_out_arr, ngs_v_out_interp)
    ax2.semilogy(gc_t_arr, rel_err_out, c='k', ls='-', lw=2.0)

    ax0.set_ylabel(r'$V_{\mathrm{in}}$ [V]')
    ax1.set_ylabel(r'$V_{\mathrm{out}}$ [V]')
    ax2.set_ylabel(style.REL_ERR_LABEL)
    ax2.set_xlabel('Time [ns]')

    ax0.legend()
    ax1.legend()

    out_path = figures_trans_dir / 'inv_ring.png'
    plt.savefig(out_path)
    return out_path


def plot_comprt(technology: str, model: str):
    figures_trans_dir = figures_dir / technology / model / 'transient'
    figures_trans_dir.mkdir(parents=True, exist_ok=True)

    gc_data_arr, ngs_data_arr = load_data('comprt', technology, model)

    gc_t_arr = gc_data_arr[:, 0] * 1e9  # Convert to nanoseconds
    gc_v_a_arr = gc_data_arr[:, 1]
    gc_v_b_arr = gc_data_arr[:, 2]
    gc_v_gt_arr = gc_data_arr[:, 3]
    gc_v_lt_arr = gc_data_arr[:, 4]
    gc_v_eq_arr = gc_data_arr[:, 5]

    ngs_t_arr = ngs_data_arr[:, 0] * 1e9
    ngs_v_a_arr = ngs_data_arr[:, 1]
    ngs_v_b_arr = ngs_data_arr[:, 2]
    ngs_v_gt_arr = ngs_data_arr[:, 3]
    ngs_v_lt_arr = ngs_data_arr[:, 4]
    ngs_v_eq_arr = ngs_data_arr[:, 5]

    plt.figure(figsize=style.FIGSIZE_2)
    gs = plt.GridSpec(4, 2, hspace=0.3, wspace=0.3)
    ax00 = plt.subplot(gs[0, 0])
    ax01 = plt.subplot(gs[0, 1], sharex=ax00)
    ax10 = plt.subplot(gs[1, 0], sharex=ax00)
    ax11 = plt.subplot(gs[1, 1], sharex=ax00)
    ax20 = plt.subplot(gs[2, 0], sharex=ax00)
    ax21 = plt.subplot(gs[2, 1], sharex=ax00)
    ax30 = plt.subplot(gs[3, 0], sharex=ax00)
    ax31 = plt.subplot(gs[3, 1], sharex=ax00)

    # Plot input signals
    ax00.plot(gc_t_arr, gc_v_a_arr, c='r', lw=2.0, label='A (gnucap)')
    ax00.plot(ngs_t_arr, ngs_v_a_arr, c='k', ls='--', lw=1.0, label='A (ngspice)')
    ax00.plot(gc_t_arr, gc_v_b_arr, c='b', lw=2.0, label='B (gnucap)')
    ax00.plot(ngs_t_arr, ngs_v_b_arr, c='k', ls='--', lw=1.0, label='B (ngspice)')

    # Plot outputs
    ax10.plot(gc_t_arr, gc_v_gt_arr, c='r', lw=2.0, label='gnucap')
    ax10.plot(ngs_t_arr, ngs_v_gt_arr, c='k', ls='--', lw=1.0, label='ngspice')

    ax20.plot(gc_t_arr, gc_v_lt_arr, c='r', lw=2.0, label='gnucap')
    ax20.plot(ngs_t_arr, ngs_v_lt_arr, c='k', ls='--', lw=1.0, label='ngspice')

    ax30.plot(gc_t_arr, gc_v_eq_arr, c='r', lw=2.0, label='gnucap')
    ax30.plot(ngs_t_arr, ngs_v_eq_arr, c='k', ls='--', lw=1.0, label='ngspice')

    # Calculate and plot errors
    f = interp1d(ngs_t_arr, ngs_v_gt_arr, kind='linear', fill_value='extrapolate')
    ngs_v_gt_interp = f(gc_t_arr)
    rel_err_gt = calc_abs_rel_err(gc_v_gt_arr, ngs_v_gt_interp)
    ax11.semilogy(gc_t_arr, rel_err_gt, c='k', ls='-', lw=2.0)

    f = interp1d(ngs_t_arr, ngs_v_lt_arr, kind='linear', fill_value='extrapolate')
    ngs_v_lt_interp = f(gc_t_arr)
    rel_err_lt = calc_abs_rel_err(gc_v_lt_arr, ngs_v_lt_interp)
    ax21.semilogy(gc_t_arr, rel_err_lt, c='k', ls='-', lw=2.0)

    f = interp1d(ngs_t_arr, ngs_v_eq_arr, kind='linear', fill_value='extrapolate')
    ngs_v_eq_interp = f(gc_t_arr)
    rel_err_eq = calc_abs_rel_err(gc_v_eq_arr, ngs_v_eq_interp)
    ax31.semilogy(gc_t_arr, rel_err_eq, c='k', ls='-', lw=2.0)

    ax00.set_ylabel('Input [V]')
    ax10.set_ylabel('A > B [V]')
    ax20.set_ylabel('A < B [V]')
    ax30.set_ylabel('A = B [V]')
    ax30.set_xlabel('Time [ns]')
    ax31.set_xlabel('Time [ns]')

    for ax in [ax01, ax11, ax21, ax31]:
        ax.set_ylabel(style.REL_ERR_LABEL)

    for ax in [ax00, ax01, ax10, ax11, ax20, ax21, ax30, ax31]:
        ax.grid(True)

    ax00.legend()
    ax10.legend()

    out_path = figures_trans_dir / 'comprt.png'
    plt.savefig(out_path)
    return out_path


def plot_input_switch(model: str):
    figures_trans_dir = figures_dir / model / 'transient'
    figures_trans_dir.mkdir(parents=True, exist_ok=True)

    gc_data_arr, ngs_data_arr = load_data(model, 'input_switch')

    gc_t_arr = gc_data_arr[:, 0] * 1e9  # Convert to nanoseconds
    gc_vg_arr = gc_data_arr[:, 1]
    gc_vd_arr = gc_data_arr[:, 2]

    ngs_t_arr = ngs_data_arr[:, 0] * 1e9
    ngs_vg_arr = ngs_data_arr[:, 1]
    ngs_vd_arr = ngs_data_arr[:, 2]

    plt.figure(figsize=style.FIGSIZE_2)
    gs = plt.GridSpec(3, 1, hspace=0.3)
    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1], sharex=ax0)
    ax2 = plt.subplot(gs[2], sharex=ax0)

    ax0.plot(gc_t_arr, gc_vg_arr, c='r', lw=2.0, label='Gate (gnucap)')
    ax0.plot(ngs_t_arr, ngs_vg_arr, c='k', ls='--', lw=1.0, label='Gate (ngspice)')

    ax1.plot(gc_t_arr, gc_vd_arr, c='r', lw=2.0, label='Drain (gnucap)')
    ax1.plot(ngs_t_arr, ngs_vd_arr, c='k', ls='--', lw=1.0, label='Drain (ngspice)')

    f = interp1d(ngs_t_arr, ngs_vd_arr, kind='linear', fill_value='extrapolate')
    ngs_vd_interp = f(gc_t_arr)
    rel_err = calc_abs_rel_err(gc_vd_arr, ngs_vd_interp)
    ax2.semilogy(gc_t_arr, rel_err, c='k', ls='-', lw=2.0)

    ax0.set_ylabel('Gate Voltage [V]')
    ax1.set_ylabel('Drain Voltage [V]')
    ax2.set_ylabel(style.REL_ERR_LABEL)
    ax2.set_xlabel('Time [ns]')

    ax0.grid(True)
    ax1.grid(True)
    ax2.grid(True)
    ax0.legend()
    ax1.legend()

    out_path = figures_trans_dir / 'input_switch.png'
    plt.savefig(out_path)
    return out_path

def plot_oneshot(model: str):
    pass
    # figures_dc_dir = figures_dir / model / 'transient'
    # figures_dc_dir.mkdir(parents=True, exist_ok=True)
    #
    # gc_data_arr, ngs_data_arr = load_data('oneshot', model)
    #
    # gc_t_arr = gc_data_arr[:, 0] * 1e9  # Convert to nanoseconds
    # gc_v_in_arr = gc_data_arr[:, 1]
    # gc_v_out_arr = gc_data_arr[:, 2]
    #
    # ngs_t_arr = ngs_data_arr[:, 0] * 1e9
    # ngs_v_in_arr = ngs_data_arr[:, 1]
    # ngs_v_out_arr = ngs_data_arr[:, 2]
    #
    # plt.figure(figsize=(8, 6))
    # gs = plt.GridSpec(3, 1, hspace=0.3)
    # ax0 = plt.subplot(gs[0])
    # ax1 = plt.subplot(gs[1], sharex=ax0)
    # ax2 = plt.subplot(gs[2], sharex=ax0)
    #
    # ax0.plot(gc_t_arr, gc_v_in_arr, c='k', lw=2.0, label='Input (Gnucap)')
    # ax0.plot(ngs_t_arr, ngs_v_in_arr, c='r', ls='--', lw=2.0, label='Input (Ngspice) ')
    #
    # ax1.plot(gc_t_arr, gc_v_out_arr, c='k', lw=2.0, label='Output (Gnucap)')
    # ax1.plot(ngs_t_arr, ngs_v_out_arr, c='r', ls='--', lw=2.0, label='Output (Ngspice)')
    #
    # f = interp1d(ngs_t_arr, ngs_v_out_arr, kind='cubic', fill_value='extrapolate')
    # ngs_v_out_interp = f(gc_t_arr)
    # rel_err_out = calc_abs_rel_err(gc_v_out_arr, ngs_v_out_interp)
    # ax2.semilogy(gc_t_arr, rel_err_out, c='k', ls='-', lw=2.0)
    #
    # ax0.set_ylabel('Input Voltage [V]', fontsize=14)
    # ax1.set_ylabel('Output Voltage [V]', fontsize=14)
    # ax2.set_ylabel(r'$\varepsilon_{\mathrm{rel}}$', fontsize=14)
    # ax2.set_xlabel('Time [ns]', fontsize=14)
    #
    # ax0.grid(True)
    # ax1.grid(True)
    # ax2.grid(True)
    # ax0.legend()
    # ax1.legend()
    #
    # plt.show()
    #
    # return

if __name__ == "__main__":

    for technology in ['cmos90']:
        for model in supported_models:
            print(f'Plotting transient test cases for {model} model...')
            plot_not(technology, model)
            plot_logic_gate(technology, model, 'nor2')
            plot_logic_gate(technology, model, 'nand2')
            plot_logic_gate(technology, model, 'and2')
            plot_logic_gate(technology, model, 'or2')
            plot_inv_ring(technology, model)
            plot_comprt(technology, model)


