from functions import maths_functions


def sense_organism(closest_prey, closest_carrion, pred, org):
    # living organism is prey, dead one is a body: sense the closest of each kind separately (eaten ones are gone)
    if pred.fitness <= 0 or org.eaten:
        return closest_prey, closest_carrion

    pred_org_dist = maths_functions.dist_to_organism(pred, org)
    alive = org.fitness > 0
    if alive and pred_org_dist < closest_prey:
        closest_prey = pred_org_dist
        pred.x_distance_to_food, pred.y_distance_to_food = maths_functions.xy_dist_to_organism(pred, org)
    if not alive and pred_org_dist < closest_carrion:
        closest_carrion = pred_org_dist
        pred.x_distance_to_carrion, pred.y_distance_to_carrion = maths_functions.xy_dist_to_organism(pred, org)

    return closest_prey, closest_carrion


def touch_organism(hunting, kill_dist, eat_dist, carrion_energy, pred, org):
    # contact along the predator's path this tick: a living organism is killed only when the predator is hunting
    # (no body in sight), a dead body is eaten - the same energy whether it was killed or died by itself
    if pred.fitness <= 0 or org.eaten:
        return

    path_dist = maths_functions.path_dist(pred, org)
    if org.fitness > 0:
        if hunting and path_dist <= kill_dist:
            org.fitness = 0
            org.killed = True
    elif org.edible and path_dist <= eat_dist:
        pred.fitness += carrion_energy
        org.eaten = True


def behave_on_other_predator(closest_dist, penalty_dist, penalty_value, pred1, pred2):
    # get the closest neighbour
    if pred1 is pred2:
        return closest_dist
    pred_pred_dist = maths_functions.dist_to_neighbour(pred1, pred2)
    if pred_pred_dist < closest_dist:
        closest_dist = pred_pred_dist
        pred1.x_distance_to_neighbour, pred1.y_distance_to_neighbour = maths_functions.xy_dist_to_neighbour(pred1,
                                                                                                            pred2)

    # update organism fitness function
    if pred_pred_dist <= penalty_dist:
        pred1.fitness -= penalty_value

    return closest_dist
