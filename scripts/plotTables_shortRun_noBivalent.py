import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import sys
import heatmap_settings as pref


plt.rcParams["font.family"] = "serif"
run_number = sys.argv[1]

input_file = "../../analysis/{}/state_counts.csv".format(run_number)
output_file = "../../analysis/{}/{}_runHistoryPlot.pdf".format(
    run_number, run_number)

# reading in data
df = pd.read_csv(input_file, delimiter='\t', names=[
                 'steps', 'activated', 'silenced', 'bivalent', 'total'], header=None)

steps = df['steps']
activated = df['activated']
silenced = df['silenced']
bivalent = df['bivalent']
total = df['total']

# defining pandas DataFrame for stacked bar plot
df2 = pd.DataFrame({'activated': activated,
                    'silenced': silenced, 'bivalent': bivalent}, index=steps)

# preparing subplot grid
# fig, axs = plt.subplots(2, 3)

print("Creating plots of run {}".format(run_number))
fig = plt.figure()  # constrained_layout=True)

# fig.suptitle('Nucleosome state amount (total: pref.nuc_num nucleosomes)')

fig.text(0.5, 0.04, 'Time', ha='center')
fig.text(0.04, 0.5, 'Nucleosome state occurrence',
         va='center', rotation='vertical')

plt.rc('xtick', labelsize=6)
plt.rc('ytick', labelsize=6)

# gs = fig.add_gridspec(2,6, width_ratios=[3,1,3,1,3,1], hspace=0.4)
# using nested Girdspecs in order to individually adjust spacing between line plots and histograms
outer_gs = fig.add_gridspec(2, 2)
activated_gs = gridspec.GridSpecFromSubplotSpec(
    1, 2, subplot_spec=outer_gs[0, 0], width_ratios=[2, 1], wspace=0.02)
silenced_gs = gridspec.GridSpecFromSubplotSpec(
    1, 2, subplot_spec=outer_gs[0, 1], width_ratios=[2, 1], wspace=0.02)
# bivalent_gs = gridspec.GridSpecFromSubplotSpec(1, 2, subplot_spec = outer_gs[0,2], width_ratios=[3,1], wspace=0.02)


# activated line plot
axs00 = fig.add_subplot(activated_gs[0])
axs00.set_title('active', fontsize=8)
axs00.set_ylim([0, pref.nuc_num])
axs00.plot(steps, activated, color='#15b01a', linewidth=0.3)

# activated histogram
axs01_hist = fig.add_subplot(activated_gs[1])
axs01_hist.set_ylim([0, pref.nuc_num])
axs01_hist.axis('off')  # disable axis annotation
axs01_hist.set_frame_on(False)  # disable black frame around histogram
axs01_hist.hist(activated, color='#15b01a', bins=100, orientation='horizontal')

# silenced line plot
axs02 = fig.add_subplot(silenced_gs[0])
axs02.set_title('silent', fontsize=8)
axs02.set_ylim([0, pref.nuc_num])
axs02.plot(steps, silenced, color='#e50000', linewidth=0.3)

# silenced histogram
axs03_hist = fig.add_subplot(silenced_gs[1])
axs03_hist.set_ylim([0, pref.nuc_num])
axs03_hist.axis('off')  # disable axis annotation
axs03_hist.set_frame_on(False)  # disable black frame around histogram
axs03_hist.hist(silenced, color='#e50000', bins=100, orientation='horizontal')

# # bivalent line plot
# axs04 = fig.add_subplot(bivalent_gs[0])
# axs04.set_title('bivalent', fontsize=8)
# axs04.set_ylim([0,pref.nuc_num])
# axs04.plot(steps, bivalent, color='#f8d950', linewidth=0.3)

# # bivalent_histogram
# axs05_hist = fig.add_subplot(bivalent_gs[1])
# axs05_hist.set_ylim([0,pref.nuc_num])
# axs05_hist.axis('off') #disable axis annotation
# axs05_hist.set_frame_on(False) # disable black frame around histogram
# axs05_hist.hist(bivalent, color='#f8d950', bins=100, orientation='horizontal')


ax13 = fig.add_subplot(outer_gs[1, :])
ax13.set_ylim([0, pref.nuc_num])

my_colors = ['#15b01a', '#e50000', '#f8d950']

# plot three lines in one plot
ax13.plot(steps, activated, color='#15b01a', linewidth=0.3)
ax13.plot(steps, silenced, color='#e50000', linewidth=0.3)
# ax13.plot(steps, bivalent, color='#f8d950', linewidth=0.3)

# set reasonable ticks
start, end = ax13.get_xlim()
# ax13.xaxis.set_ticks(np.arange(0, end, len(steps)/10))
# ax13.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
x_axis = ax13.axes.get_xaxis()
# x_axis.set_label_text('foo')
x_label = x_axis.get_label()
x_label.set_visible(False)


fig.savefig(output_file,
            dpi=200, bbox_inches='tight')


# plot.savefig('outplot.pdf')
