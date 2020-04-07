from matplotlib import pyplot as plt


def plot_tour(tour):
    "Plot the cities as circles and the tour as lines between them."
    plot_lines(list(tour) + [tour[0]])
    plot_lines([tour[0]], 'rs')
    plt.show()


def plot_lines(points, style='bo-'):
    "Plot lines to connect a series of points."
    plt.plot([p.x for p in points], [p.y for p in points], style)
    plt.axis('scaled')
    # plt.axis('off')
