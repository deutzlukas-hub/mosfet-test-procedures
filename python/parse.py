from pathlib import Path
from typing import List

import numpy as np

def parse_gnucap(filepath: Path, skip: int =0, starts_with='# '):

    with open(filepath, "r") as file:

        for line in file:
            if line.startswith(starts_with):
                break

        for _ in range(skip):
            next(file)

        v_table = []

        for line in file:
            if line.startswith('open circuit'):
                continue
            elif line.startswith('did not converge'):
                continue
            elif line.startswith('zero'):
                continue
            elif line.startswith('newtime'):
                continue
            elif line.startswith('#Freq'):
                continue

            v_list = line.split()
            if v_list[0] == 'Gnucap':
                break
            v_list = [float(s) for s in v_list]

            v_table.append(v_list)

        return np.array(v_table)

def parse_gnucap_chained(filepath: Path, skip: int = 0, starts_with: str = '#'):
    """
    Parse a Gnucap output file containing multiple simulations chained together.

    Returns:
        List of np.array: each array corresponds to one simulation block.
    """
    simulations = []

    with open(filepath, "r") as file:
        lines = file.readlines()

    i = 0

    while i < len(lines):
        line = lines[i]
        if line.startswith(starts_with): # Found start of a simulation block
            i += 1  # move past header
            for _ in range(skip): # skip
                i += 1

            v_table = []
            while i < len(lines):
                line = lines[i].strip()

                if line.startswith(starts_with):
                    # Next simulation block starts
                    break

                i += 1

                if line.startswith(('open circuit', 'did not converge', 'zero', 'newtime', '#Freq')):
                    continue

                v_list = line.split()
                if v_list[0] == 'Gnucap':
                    break
                try:
                    v_list = [float(s) for s in v_list]
                    v_table.append(v_list)
                except ValueError:
                    continue  # skip lines that cannot be converted

            if v_table:
                simulations.append(np.array(v_table))
        else:
            i += 1  # skip lines until next header

    return simulations

def split_nested_sweep(
    data_arr: np.ndarray,
    data_col_idx_list: List[int],
    inner_sweep_col_idx: int = 0,
    outer_sweep_col_idx: int = 1,
    ):

    inner_sweep_arr = data_arr[:, inner_sweep_col_idx]
    inner_sweep_arr, idx = np.unique(inner_sweep_arr, return_index=True)
    inner_sweep_arr = inner_sweep_arr[np.argsort(idx)]
    outer_sweep_arr, idx = np.unique(np.round(data_arr[:, outer_sweep_col_idx], 10), return_index=True)
    outer_sweep_arr = outer_sweep_arr[np.argsort(idx)]

    split_data_list = []

    for v in outer_sweep_arr:
        idx_arr = np.round(data_arr[:, outer_sweep_col_idx], 10) == v
        sweep_data_list = []
        for cold_idx in data_col_idx_list:
            sweep_data_list.append(data_arr[idx_arr, cold_idx])

        split_data_list.append(np.squeeze(np.array(sweep_data_list)))

    return split_data_list, inner_sweep_arr, outer_sweep_arr

def parse_spice(filepath: Path):

    with open(filepath, "r") as file:

        data_table = []

        idx = 0

        for line in file:
            if line.startswith(str(idx)):
                data_table.append([float(v.rstrip(',')) for v in line.split()[1:]])
                idx += 1
        return np.array(data_table)


def parse_ngspice(filepath: Path):

    with open(filepath, "r") as file:
        # Skip header
        file.__next__()

        data_table = []

        for line in file:
            data_table.append([float(v.rstrip(',')) for v in line.split()[:]])

        return np.array(data_table)

def parse_ngspice_chained_AC(filepath: Path):

    with open(filepath, "r") as file:
        lines = file.readlines()

    i = 0

    simulations = []

    while i < len(lines):
        line = lines[i].strip()

        if line.startswith('frequency'):  # Found start of a simulation block
            i += 1  # move past header
            v_table = []

            while i < len(lines):
                line = lines[i].strip()
                if line.startswith('frequency'):
                    break

                v_table.append([float(s) for s in line.split()])
                i += 1

            if v_table:
                simulations.append(np.array(v_table))
        else:
            i += 1

    return simulations

def split_nested_sweep_spice(
        data_arr: np.ndarray,
        inner_sweep_col_idx: int = 0,
        data_col_idx_list: List[int] = [1]):

    inner_sweep_arr = data_arr[:, inner_sweep_col_idx]
    inner_sweep_arr, idx = np.unique(np.round(inner_sweep_arr, 10), return_index=True)
    inner_sweep_arr = inner_sweep_arr[np.argsort(idx)]
    len_inner_sweep = len(inner_sweep_arr)
    len_data = data_arr.shape[0]
    num_sweeps = int(len_data / len_inner_sweep)

    split_data_list = []

    for i in range(num_sweeps):
        sweep_data_list = []
        start = i*len_inner_sweep
        end = (i+1)*len_inner_sweep
        for cold_idx in data_col_idx_list:
            sweep_data_list.append(data_arr[start:end, cold_idx])

        split_data_list.append(np.squeeze(np.array(sweep_data_list)))

    return split_data_list, inner_sweep_arr























