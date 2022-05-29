from matplotlib import pyplot as plt

def plot_array(arr, fig, ax):
    im = ax.imshow(arr, cmap="gray")
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
            rotation_mode="anchor")
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            text = ax.text(j, i, arr[i, j],
                        ha="center", va="center", color="b", fontsize = 32)