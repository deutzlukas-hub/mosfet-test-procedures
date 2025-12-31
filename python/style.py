import matplotlib.pyplot as plt
from matplotlib import rcParams

FIGSIZE = (6.0, 3.0)
FIGSIZE_2 = (6.0, 4.5)
REL_ERR_LABEL = r'$\varepsilon_{\mathrm{rel}}$'
BOTTOM = 0.15
LEFT = 0.2
RIGHT = 0.8
HSPACE = 0.3


FS = {
    "title": 10,
    "label": 8,
    "math": 10,
    "ticks": 8,
    "legend": 8,
    "legend_title": 10,
    'panel': 12
}

rcParams["axes.titlesize"] = FS['title']
rcParams["axes.labelsize"] = FS['label']
rcParams["xtick.labelsize"] = FS['ticks']
rcParams["ytick.labelsize"] = FS['ticks']
rcParams["legend.fontsize"] = FS['legend']
plt.rcParams["legend.title_fontsize"] = FS['legend_title']
rcParams["figure.dpi"] = 600
rcParams["savefig.dpi"] = 100
rcParams["axes.grid"] = True


