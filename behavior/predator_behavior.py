from functions import maths_functions


def behave_on_organism(closest_dist, eat_dist, pred, org):
    # get the closest org
    pred_org_dist = maths_functions.dist_to_organism(pred, org)
    if org.fitness > 0:
        if pred_org_dist < closest_dist:
            closest_dist = pred_org_dist
            pred.x_distance_to_food, pred.y_distance_to_food = maths_functions.xy_dist_to_organism(pred, org)

        # update organism fitness function and food status
        if pred_org_dist <= eat_dist:
            pred.fitness += 1
            org.fitness = 0

    else:
        pass

    return closest_dist


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
