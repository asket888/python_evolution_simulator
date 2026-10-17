from termcolor import colored

from gui.make_gif import make_gif


def get_generation_stats(organisms, predators):
    fitness = [org.fitness for org in organisms]
    dead = sum(f <= 0 for f in fitness)
    killed = sum(org.killed for org in organisms)
    stats = {
        'BEST': max(fitness),
        'AVG': sum(fitness) / len(fitness),
        'WORST': min(fitness),
        'SURVIVED': len(fitness) - dead,
        'COUNT': len(fitness),
        'KILLED': killed,                                    # killed by predators
        'DIED': dead - killed,                               # starved or lost energy on walls / collisions
        'BODIES_EATEN': sum(org.eaten for org in organisms),
        'PRED_COUNT': len(predators),
        'PRED_SURVIVED': sum(pred.fitness > 0 for pred in predators),
        'PRED_AVG': sum(pred.fitness for pred in predators) / len(predators) if predators else 0,
    }

    return stats


def print_generation_stats(gen, stats):
    line = ' > GEN-{:<3}: '.format(gen + 1) + colored('HERBIVORES best {:6.2f} avg {:6.2f} worst {:6.2f}'.format(
        stats['BEST'], stats['AVG'], stats['WORST']), 'green') + colored(
        ' survived {}/{} (killed {}, died {})'.format(
            stats['SURVIVED'], stats['COUNT'], stats['KILLED'], stats['DIED']), 'yellow')
    if stats['PRED_COUNT']:
        line += colored(' | PREDATORS survived {}/{} avg {:5.2f}, bodies eaten {}'.format(
            stats['PRED_SURVIVED'], stats['PRED_COUNT'], stats['PRED_AVG'], stats['BODIES_EATEN']), 'red')
    print(line)


def build_generation_gif(settings, gen):
    print(' > GEN-' + str(gen + 1), '.gif file is building...\n')
    make_gif(settings, gen)
