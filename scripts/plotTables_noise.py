import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import sys


run_number = sys.argv[1]
noise_factor = sys.argv[2]

# reading in data
df = pd.read_csv('state_counts.csv', delimiter='\t', names=['steps', 'activated', 'silenced', 'bivalent', 'total'], header=None)

steps = df['steps']
activated = df['activated']
silenced = df['silenced']
bivalent = df['bivalent']
total = df['total']

# defining pandas DataFrame for stacked bar plot
df2 = pd.DataFrame({'activated': activated, 'silenced': silenced, 'bivalent': bivalent}, index=steps)

#preparing subplot grid
# fig, axs = plt.subplots(2, 3)

print("Creating plots of run {} with factor {} noise".format(run_number, noise_factor))
fig = plt.figure()#constrained_layout=True)
# plt.ylim(top=40)
fig.suptitle('Nucleosome state amount with noise factor {}:1 (total: 40 nucleosomes)'.format(noise_factor))
# fig.suptitle('Nucleosome state amount (total: 60 nucleosomes)'.format(noise_factor))

fig.text(0.5, 0.04, 'steps', ha='center')
fig.text(0.04, 0.5, 'Nucleosome state occurrence', va='center', rotation='vertical')

plt.rc('xtick', labelsize=6) 
plt.rc('ytick', labelsize=6)

gs = fig.add_gridspec(2,3, hspace=0.4)

# gs = GridSpec(2, 3, figure=fig)

axs00 = fig.add_subplot(gs[0,0])
axs00.plot(steps, activated, color='#15b01a', linewidth=0.3)
axs00.set_title('active', fontsize=8)
# axs00.axhline(y=0.5, color='grey', linestyle='-') # draw horizontal line
axs00.set_ylim([0,60])

axs01 = fig.add_subplot(gs[0,1])
axs01.set_title('silent', fontsize=8)
axs01.set_ylim([0,60])
axs01.plot(steps, silenced, color='#e50000', linewidth=0.3)

axs02 = fig.add_subplot(gs[0,2])
axs02.set_title('bivalent', fontsize=8)
axs02.set_ylim([0,60])
axs02.plot(steps, bivalent, color='#f8d950', linewidth=0.3)


ax13 = fig.add_subplot(gs[1,:])

my_colors = ['#15b01a', '#e50000', '#f8d950']

# plot stacked bar plot
df2.plot.bar(rot=0, stacked=True, ax=ax13, color=my_colors, legend=False)
# ax13.plot(steps, activated, color='#15b01a', linewidth=0.3)
# ax13.plot(steps, silenced, color='#e50000', linewidth=0.3)
# ax13.plot(steps, bivalent, color='#f8d950', linewidth=0.3)

start, end = ax13.get_xlim()
ax13.xaxis.set_ticks(np.arange(start, end, len(steps)/10))
ax13.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
x_axis = ax13.axes.get_xaxis()
# x_axis.set_label_text('foo')
x_label = x_axis.get_label()
x_label.set_visible(False)

# # only display every n_th tick
# every_nth = int(len(steps)/10)
# for n, label in enumerate(ax13.xaxis.get_ticklabels()):
#     if n % every_nth != 0:
#         label.set_visible(False)

# for ax in axs.flat:
#     ax.set(xlabel='Modification steps')

# Hide x labels and tick labels for top plots and y ticks for right plots.
# for ax in axs.flat:
#     ax.label_outer()


fig.savefig('{}_factor{}_suboutplots.pdf'.format(run_number, noise_factor))


# plot.savefig('outplot.pdf')
