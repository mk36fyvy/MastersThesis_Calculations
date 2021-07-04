import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
import heatmap_settings as pref


dfs = {}
path = "./analysis/"

file = "./results/channels.txt"
# Generate enzyme name dict from channels.txt in order to translate the reaction channels later
enzyme_name_dict = {}
with open(file) as f:
    for line in f:
        key, value = line.split(": ")
        enzyme_name_dict[key] = value.strip("\n")

plt.rcParams.update({'font.size': pref.font_size})
plt.rcParams["font.family"] = "serif"
for x in next(os.walk(path))[1]:

    # reading in files that hold, one by one, the type and duration of enzymes that were associated to this specific nucl
    df = pd.read_csv(
        path + "{}/bindingTimes/bindingTimesOn1.txt".format(x), sep=" ")
    for i in range(2, pref.nuc_num+1):
        data_file = path + "{}/bindingTimes/bindingTimesOn{}.txt".format(x, i)
        new_df = pd.read_csv(data_file, sep=" ")
        df = pd.concat([df, new_df], axis=1)

    df = df.fillna(0)
    dfs[x] = df

    fig, ax = plt.subplots(
        figsize=pref.fig_size,
    )

    # plot heatmap for single run
    ax = sns.heatmap(df, cmap='rocket', vmin=0, vmax=df.values.max(), cbar_kws={"shrink": pref.heatbar_shrink},
                     xticklabels=3)

    # turn the axis label
    new_yticklabels = []
    i = 1
    for item in ax.get_yticklabels():
        if (i < 10):
            new_yticklabels.append('[ {}]'.format(i))
        else:
            new_yticklabels.append('[{}]'.format(i))
        i += 1
        # new_yticklabels.append(enzyme_name_dict[item.get_text()])
        item.set_rotation(0)
    ax.set_yticklabels(new_yticklabels)

    for item in ax.get_xticklabels():
        item.set_rotation(90)

    ax.set(xlabel="Nucleosome position", ylabel="Enzyme identifier")
    # save figure
    plt.savefig(
        './analysis/{}/{}_bindingTimeDuration_numberAnnot.pdf'.format(x, x), dpi=200, bbox_inches='tight')
    # plt.show()

# Getting number of runs that were done
n_runs = len([f.path for f in os.scandir("./analysis") if f.is_dir()])

# summing up and averaging all data frames of all the runs


def sum_up(s1, s2): return s1+s2


df = list(dfs.values())[0]
for frame in list(dfs.values())[1:]:

    df = df.combine(frame, sum_up, fill_value=0)
df = df/n_runs

# plot heatmap for whole run
fig, ax = plt.subplots(
    figsize=pref.fig_size,
)


# plot heatmap for single run
ax = sns.heatmap(df, cmap='rocket', vmin=0, vmax=df.values.max(), cbar_kws={"shrink": pref.heatbar_shrink},
                 xticklabels=3)

# translate reaction_channel into enzyme name
new_yticklabels = []
i = 1
for item in ax.get_yticklabels():
    if (i < 10):
        new_yticklabels.append('[ {}]'.format(i))
    else:
        new_yticklabels.append('[{}]'.format(i))
    i += 1
    # new_yticklabels.append(enzyme_name_dict[item.get_text()])
    item.set_rotation(0)
ax.set_yticklabels(new_yticklabels)


# turn the axis label
for item in ax.get_xticklabels():
    item.set_rotation(90)

ax.set(xlabel="Nucleosome position", ylabel="Enzyme name")
# save figure
df.to_csv('./analysis/bindingDuration_{}runs_dataTable.csv'.format(n_runs), sep=' ')

plt.savefig(
    './analysis/bindingTimeDuration_{}runs_numberAnnot.pdf'.format(n_runs), dpi=200, bbox_inches='tight')
