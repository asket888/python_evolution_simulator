import operator

from numpy import floor
from numpy import where

from numpy.random import random
from numpy.random import choice
from numpy.random import normal

from functions.name_functions import next_gen_org_name_template
from objects.organism import Organism
from objects.predator import Predator


def evolve_organisms(settings, old_generation, gen):
    ancestors_num = int(floor(settings['elitism_org'] * settings['org_num']))
    descendants_num = settings['org_num'] - ancestors_num

    new_generation = _calculate_new_org_generation(settings, gen, old_generation, ancestors_num, descendants_num)

    return new_generation


def evolve_predators(settings, old_generation, gen):
    ancestors_num = int(floor(settings['elitism_pred'] * settings['pred_num']))
    descendants_num = settings['pred_num'] - ancestors_num

    new_generation = _calculate_new_pred_generation(settings, gen, old_generation, ancestors_num, descendants_num)

    return new_generation


def _calculate_new_org_generation(settings, gen, old_generation, ancestors_num, descendants_num):
    sorted_old_generation = sorted(old_generation, key=operator.attrgetter('fitness'), reverse=True)

    # keep best organisms from previous generation
    new_generation = []
    for org in range(0, ancestors_num):
        best_candidate = sorted_old_generation[org]
        new_generation.append(Organism(settings,
                                       wih=best_candidate.wih,
                                       who=best_candidate.who,
                                       name=best_candidate.name))

    # generate children of best organisms from previous generation
    for org in range(0, descendants_num):
        all_parents_candidates = range(0, ancestors_num)
        random_parents_indexes = choice(a=all_parents_candidates, size=2, replace=False)
        org_1 = sorted_old_generation[random_parents_indexes[0]]
        org_2 = sorted_old_generation[random_parents_indexes[1]]

        wih_new, who_new = _calculate_child_mutations(settings, org_1, org_2)

        new_generation.append(Organism(settings,
                                       wih=wih_new,
                                       who=who_new,
                                       name=next_gen_org_name_template(gen, org)))

    return new_generation


def _calculate_new_pred_generation(settings, gen, old_generation, ancestors_num, descendants_num):
    sorted_old_generation = sorted(old_generation, key=operator.attrgetter('fitness'), reverse=True)

    # keep best organisms from previous generation
    new_generation = []
    for pred in range(0, ancestors_num):
        best_candidate = sorted_old_generation[pred]
        new_generation.append(Predator(settings,
                                       wih=best_candidate.wih,
                                       who=best_candidate.who,
                                       name=best_candidate.name))

    # generate children of best organisms from previous generation
    for pred in range(0, descendants_num):
        all_parents_candidates = range(0, ancestors_num)
        random_parents_indexes = choice(a=all_parents_candidates, size=2, replace=True)
        pred_1 = sorted_old_generation[random_parents_indexes[0]]
        pred_2 = sorted_old_generation[random_parents_indexes[1]]

        wih_new, who_new = _calculate_child_mutations(settings, pred_1, pred_2)

        new_generation.append(Predator(settings,
                                       wih=wih_new,
                                       who=who_new,
                                       name=next_gen_org_name_template(gen, pred)))

    return new_generation


def _calculate_child_mutations(settings, org_1, org_2):
    # crossover: each hidden neuron is inherited as a whole (its input and output weights) from one of the parents
    from_org_1 = random(settings['hnodes']) < 0.5
    wih_new = where(from_org_1[:, None], org_1.wih, org_2.wih)  # rows of wih are hidden neurons
    who_new = where(from_org_1[None, :], org_1.who, org_2.who)  # columns of who are hidden neurons

    # mutation: each weight is mutated with 'mutate' probability by adding gaussian noise
    wih_new = wih_new + (random(wih_new.shape) < settings['mutate']) * normal(0, settings['mutate_sigma'], wih_new.shape)
    who_new = who_new + (random(who_new.shape) < settings['mutate']) * normal(0, settings['mutate_sigma'], who_new.shape)

    return wih_new, who_new
