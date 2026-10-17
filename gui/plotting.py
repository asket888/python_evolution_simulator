import matplotlib as mpl
mpl.use('TkAgg')
from matplotlib import lines
from matplotlib import pyplot
from matplotlib.patches import Circle

from functions.name_functions import frame_img_name_template, result_img_name_template


def plot_frame(settings, predators, organisms, foods, gen, time):
    fig, ax = pyplot.subplots()
    fig.set_size_inches(9.6, 5.4)

    pyplot.xlim([settings['x_min'] + settings['x_min'] * 0.45, settings['x_max'] + settings['x_max'] * 0.45])
    pyplot.ylim([settings['y_min'] + settings['y_min'] * 0.45, settings['y_max'] + settings['y_max'] * 0.45])

    # plot predators, organisms and food
    for predator in predators:
        if predator.fitness <= 0:
            _plot_dead_predator(predator, ax)
        else:
            _plot_predator(predator, ax)

    for organism in organisms:
        if organism.eaten:
            continue
        if organism.fitness <= 0:
            _plot_dead_organism(organism, ax)
        else:
            _plot_organism(organism, ax)

    for food in foods:
        _plot_food(food, ax)

    # misc plot settings
    ax.set_aspect('equal')
    frame = pyplot.gca()
    frame.axes.get_xaxis().set_ticks([])
    frame.axes.get_yaxis().set_ticks([])

    pyplot.figtext(0.025, 0.95, r'GENERATION: ' + str(gen))
    pyplot.figtext(0.025, 0.90, r'TICK: ' + str(time))

    pyplot.savefig(frame_img_name_template(gen, time), dpi=120)
    pyplot.close(fig)


def plot_stats(settings, gen_stats):
    gens = list(range(1, len(gen_stats) + 1))
    share = lambda key, count: [100 * g[key] / g[count] for g in gen_stats]

    fig, (ax_fit, ax_life) = pyplot.subplots(2, 1, sharex=True, figsize=(8, 8))

    # herbivore fitness
    ax_fit.plot(gens, [g['BEST'] for g in gen_stats])
    ax_fit.plot(gens, [g['AVG'] for g in gen_stats])
    ax_fit.plot(gens, [g['WORST'] for g in gen_stats])
    ax_fit.legend(['Best', 'Average', 'Worst'], loc='upper left')
    ax_fit.set_ylabel('herbivore fitness score')

    # survival of both species and how many herbivores were killed by predators
    ax_life.plot(gens, share('SURVIVED', 'COUNT'), color='green', label='Herbivores survived')
    if gen_stats[0]['PRED_COUNT']:
        ax_life.plot(gens, share('PRED_SURVIVED', 'PRED_COUNT'), color='red', label='Predators survived')
        ax_life.plot(gens, share('KILLED', 'COUNT'), color='darkred', linestyle='--', label='Herbivores killed')
    ax_life.set_ylim(0, 100)
    ax_life.legend(loc='lower center', bbox_to_anchor=(0.5, 1.0), ncol=3, frameon=False)
    ax_life.set_xlabel('generation')
    ax_life.set_ylabel('% of population')

    fig.tight_layout()
    fig.savefig(result_img_name_template(settings), dpi=200)
    pyplot.close(fig)


def _plot_food(food, ax):
    circle = Circle([food.x, food.y], 0.03, edgecolor='darkslateblue', facecolor='mediumslateblue', zorder=5)
    ax.add_artist(circle)


def _plot_organism(org, ax):
    circle = Circle([org.x, org.y], 0.05, edgecolor='green', facecolor='lightgreen', zorder=8)
    ax.add_artist(circle)

    ax.add_line(lines.Line2D([org.x, org.x_tail], [org.y, org.y_tail], color='darkgreen', linewidth=1, zorder=10))


def _plot_dead_organism(org, ax):
    circle = Circle([org.x, org.y], 0.05, edgecolor='darkgoldenrod', facecolor='goldenrod', zorder=5)
    ax.add_artist(circle)


def _plot_predator(pred, ax):
    circle = Circle([pred.x, pred.y], 0.07, edgecolor='darkred', facecolor='red', zorder=8)
    ax.add_artist(circle)

    ax.add_line(lines.Line2D([pred.x, pred.x_tail], [pred.y, pred.y_tail], color='darkred', linewidth=2, zorder=10))


def _plot_dead_predator(pred, ax):
    circle = Circle([pred.x, pred.y], 0.07, edgecolor='dimgray', facecolor='darkgray', zorder=5)
    ax.add_artist(circle)
