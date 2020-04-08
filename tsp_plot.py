from matplotlib import pyplot as plt


def plot_tour(tour):
    "Plot the cities as circles and the tour as lines between them."
    plot_lines(list(tour) + [tour[0]])
    plot_lines([tour[0]], 'rs')
    plt.show()


def plot_4_tours(tour1, tour2, tour3, tour4):
    fig, axs = plt.subplots(2, 2)
    axs[0][0].plot([p.x for p in (list(tour1) + [tour1[0]])],
                   [p.y for p in (list(tour1) + [tour1[0]])], '-bo')
    for (label, p) in enumerate(tour1):
        axs[0][0].text(p.x, p.y, '  '+str(label))
    axs[0][0].axis('scaled')

    axs[0][1].plot([p.x for p in (list(tour2) + [tour2[0]])],
                   [p.y for p in (list(tour2) + [tour2[0]])], '-bo')
    for (label, p) in enumerate(tour2):
        axs[0][1].text(p.x, p.y, '  '+str(label))
    axs[0][1].axis('scaled')

    axs[1][0].plot([p.x for p in (list(tour3) + [tour3[0]])],
                   [p.y for p in (list(tour3) + [tour3[0]])], '-bo')
    for (label, p) in enumerate(tour3):
        axs[1][0].text(p.x, p.y, '  '+str(label))
    axs[1][0].axis('scaled')

    axs[1][1].plot([p.x for p in (list(tour4) + [tour4[0]])],
                   [p.y for p in (list(tour4) + [tour4[0]])], '-bo')
    for (label, p) in enumerate(tour4):
        axs[1][1].text(p.x, p.y, '  '+str(label))
    axs[1][1].axis('scaled')


def plot_lines(points, style='bo-'):
    "Plot lines to connect a series of points."
    plt.plot([p.x for p in points], [p.y for p in points], style)
    plt.axis('scaled')
    # plt.axis('off')
