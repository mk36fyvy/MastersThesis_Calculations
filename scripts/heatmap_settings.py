# For configuring settings regarding heatmaps AND other plots
import os

n_enzymes = 0
nuc_num = 0

if os.path.isfile("./results/channels.txt"):
    file = "./results/channels.txt"
elif os.path.isfile("../results/channels.txt"):
    file = "../results/channels.txt"
elif os.path.isfile("../../results/channels.txt"):
    file = "../../results/channels.txt"
else:
    print("results/channel.txt could not be found anywhere from {}".format(os.getcwd))
    raise FileNotFoundError

with open(file) as f:
    for line in f:
        n_enzymes += 1


if os.path.isfile("./results/statefile"):
    file = "./results/statefile"
elif os.path.isfile("../results/statefile"):
    file = "../results/statefile"
elif os.path.isfile("../../results/statefile"):
    file = "../../results/statefile"
else:
    print("results/statefile could not be found anywhere from {}".format(os.getcwd))
    raise FileNotFoundError


with open(file) as f:
    for i, line in enumerate(f):
        if i == 1:
            # 2nd line
            nuc_num = line.count('{')
            break

font_size = 24
heatbar_shrink = 0.5

width = nuc_num/2.4
height = n_enzymes/2.66
fig_size = (width, height)

x_tick_spacing = 5
