import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import pandas as pd
import numpy as np
import sys

doLog = sys.argv[2]=="true"

if len(sys.argv) < 4:
    outfile = ""
else:
    run_number = sys.argv[3]
    outfile = "../../analysis/{}/".format(run_number)
if doLog:
    outfile += 'topEnzymes_log.pdf'
else:
    outfile += 'topEnzymes.pdf'

data = pd.read_csv(sys.argv[1], sep="\t", header=None)

heights = data[0]
bars = data[1]
fig = plt.figure(figsize=(16,12))
fig.suptitle("Enzyme activity by abs. association number", fontsize=24)
# use a gray background
ax = plt.axes(facecolor='#E6E6E6')
ax.set_axisbelow(True)

# draw solid white grid lines
plt.grid(color='w', linestyle='solid')

# hide axis spines
for spine in ax.spines.values():
    spine.set_visible(False)

# hide top and right ticks
ax.xaxis.tick_bottom()
ax.yaxis.tick_left()


# Rotation of the bars names
y_pos = range(len(bars))
plt.xticks(y_pos, bars, fontsize=12)

# lighten ticks and labels
# ax.tick_params(colors='gray', direction='out')
i = 0
for tick in ax.get_xticklabels():
    if "andom" in bars[i]:
        tick.set_color('darkred')
    else:
        tick.set_color('darkblue')
    i+=1
for tick in ax.get_yticklabels():
    tick.set_color('black')

# rotates labels and aligns them horizontally to left
plt.setp( ax.xaxis.get_majorticklabels(), rotation=-45, ha="left", rotation_mode="anchor")

plt.bar(y_pos, heights, edgecolor='#E6E6E6', color='#EE6666', width=1, log=doLog)

plt.tight_layout(pad=5)

plt.savefig(outfile)