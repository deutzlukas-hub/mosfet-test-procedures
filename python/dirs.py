from pathlib import Path

project_dir = Path('../').resolve()
assert project_dir.is_dir()

results_dir = project_dir / 'results'
data_dir = results_dir / 'data'
data_gnucap_dir = data_dir / 'gnucap'
data_ngspice_dir = data_dir / 'ngspice'
figures_dir = results_dir / 'figures'


# bsim_dir = project_dir / 'bsim'
# assert bsim_dir.is_dir()
#
# psp_dir = project_dir / 'psp'
# assert psp_dir.is_dir()
#
# bsim481_dir = bsim_dir / 'BSIM481'
# assert bsim481_dir.is_dir()
#
# bsim483_dir = bsim_dir / 'BSIM483'
# assert bsim483_dir.is_dir()
#
# bsim4_ngspice_dir = bsim_dir / 'tests_spice'
# assert bsim4_ngspice_dir.is_dir()
#
# psp104_dir = psp_dir / 'psp104'
# assert psp104_dir.is_dir()







