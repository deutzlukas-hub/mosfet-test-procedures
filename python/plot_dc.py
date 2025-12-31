import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import get_cmap

from dirs import data_gnucap_dir, data_ngspice_dir, figures_dir
from parse import parse_gnucap, parse_ngspice, split_nested_sweep
from util import supported_models, calc_abs_rel_err
import style

dc_tests_dict = {
    'id_vd_nmos_1': {'xlabel': 'V(d)', 'ylabel': 'I(d)', 'legend_title': 'V(g)', 'title': 'NMOS'},
    'id_vd_nmos_2': {'xlabel': 'V(d)', 'ylabel': 'I(d)', 'legend_title': 'V(g)', 'title': 'NMOS'},
    'id_vd_nmos_3': {'xlabel': 'V(d)', 'ylabel': 'I(d)', 'legend_title': 'V(g)', 'title': 'NMOS'},
    'id_vg_nmos_1': {'xlabel': 'V(d)', 'ylabel': 'I(d)', 'legend_title': 'V(g)', 'title': 'NMOS'},
    'id_vg_nmos_2': {'xlabel': 'V(d)', 'ylabel': 'I(d)', 'legend_title': 'V(g)', 'title': 'NMOS'},
    'id_vg_nmos_3': {'xlabel': 'V(d)', 'ylabel': 'I(d)', 'legend_title': 'V(g)', 'title': 'NMOS'},
    'id_vg_nmos_4': {'xlabel': 'V(d)', 'ylabel': 'I(d)', 'legend_title': 'V(g)', 'title': 'NMOS'},
    'id_vd_pmos_1': {'xlabel': 'V(d)', 'ylabel': 'I(d)', 'legend_title': 'V(g)', 'title': 'PMOS'},
    'id_vd_pmos_2': {'xlabel': 'V(d)', 'ylabel': 'I(d)', 'legend_title': 'V(g)', 'title': 'PMOS'},
    'id_vd_pmos_3': {'xlabel': 'V(d)', 'ylabel': 'I(d)', 'legend_title': 'V(g)', 'title': 'PMOS'},
    'id_vg_pmos_1': {'xlabel': 'V(d)', 'ylabel': 'I(d)', 'legend_title': 'V(g)', 'title': 'PMOS'},
    'id_vg_pmos_2': {'xlabel': 'V(d)', 'ylabel': 'I(d)', 'legend_title': 'V(g)', 'title': 'PMOS'},
    'id_vg_pmos_3': {'xlabel': 'V(d)', 'ylabel': 'I(d)', 'legend_title': 'V(g)', 'title': 'PMOS'},
    'id_vg_pmos_4': {'xlabel': 'V(d)', 'ylabel': 'I(d)', 'legend_title': 'V(g)', 'title': 'PMOS'},
}

def plot_dc_sweeps(technology: str, model, test_name: str):

    result_gnucap_dc_dir = data_gnucap_dir / technology / model / 'dc'
    result_ngspice_dc_dir = data_ngspice_dir / technology / model / 'dc'
    figures_dc_dir = figures_dir / technology / model / 'dc'

    figures_dc_dir.mkdir(parents=True, exist_ok=True)

    gc_filepath = result_gnucap_dc_dir / (test_name + '.gc.out')
    ngs_filepath = result_ngspice_dc_dir / (test_name + '.sp.out')

    gc_data_arr = parse_gnucap(gc_filepath)
    ng_data_arr = parse_ngspice(ngs_filepath)

    gc_split_data_list, gc_inner_sweep_arr, gc_outer_sweep_arr = split_nested_sweep(gc_data_arr, [2])
    ng_split_data_list, ng_inner_sweep_arr, ng_outer_sweep_arr = split_nested_sweep(ng_data_arr, [2])

    assert np.allclose(gc_outer_sweep_arr, ng_outer_sweep_arr)
    outer_sweep_arr = gc_outer_sweep_arr
    assert np.allclose(gc_inner_sweep_arr, ng_inner_sweep_arr)
    inner_sweep_arr = gc_inner_sweep_arr

    fig = plt.figure(figsize=style.FIGSIZE)
    gs = plt.GridSpec(2, 1,
        bottom=style.BOTTOM, left=style.LEFT, right=style.RIGHT, hspace=style.HSPACE)
    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1], sharex=ax0)
    ax0.text(-0.2, 1.05, 'A', transform=ax0.transAxes, fontsize=style.FS['panel'])
    ax1.text(-0.2, 1.05, 'B', transform=ax1.transAxes, fontsize=style.FS['panel'])


    cmap = get_cmap("spring")
    norm = Normalize(vmin=outer_sweep_arr.min(), vmax=outer_sweep_arr.max())

    colors = cmap(norm(outer_sweep_arr))

    for i, (gc_sweep_arr, ng_sweep_arr, val) in enumerate(zip(gc_split_data_list, ng_split_data_list, outer_sweep_arr)):

        ax0.plot(inner_sweep_arr, gc_sweep_arr, c=colors[i], ls='-', label = f'{val}')
        ax0.plot(inner_sweep_arr, ng_sweep_arr, c='k', ls='--',
                 label = f'ngspice' if i == len(outer_sweep_arr)-1 else None)

        rel_abs_err_arr = calc_abs_rel_err(ng_sweep_arr, gc_sweep_arr)
        ax1.semilogy(inner_sweep_arr, rel_abs_err_arr, c=colors[i], ls='-')

    fig.legend(title=dc_tests_dict[test_name]['legend_title'],
               ncol=1, bbox_to_anchor=(0.8, 0.5), loc='center left')

    ax0.set_title(model + " " + dc_tests_dict[test_name]['title'])
    ax0.set_ylabel(dc_tests_dict[test_name]['ylabel'])
    ax1.set_ylabel(style.REL_ERR_LABEL, fontsize=style.FS['math'])
    ax1.set_xlabel(dc_tests_dict[test_name]['xlabel'])

    ax0.grid(True)
    ax1.grid(True)

    fig.align_ylabels()
    plt.savefig(figures_dc_dir / (test_name + '.png'))
    plt.close(fig)

    return

if __name__ == '__main__':

    for technology in ['cmos90']:
        for model in supported_models:
            print(f'plot dc sweeps for {model}...')
            for test_name in dc_tests_dict.keys():
                print(f'plot test {test_name}...')
                plot_dc_sweeps(technology, model, test_name)


