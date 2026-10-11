from functions import maths_functions


def behave_on_food(closest_dist, eat_dist, org, food):
    # get the closest food
    food_org_dist = maths_functions.dist_to_food(org, food)
    if food_org_dist < closest_dist:
        closest_dist = food_org_dist
        org.x_distance_to_food, org.y_distance_to_food = maths_functions.xy_dist_to_food(org, food)

    # update organism fitness function and food status (food within eat distance of the path travelled this tick)
    if maths_functions.path_dist_to_food(org, food) <= eat_dist:
        org.fitness += food.energy
        food.energy = 0

    return closest_dist


def behave_on_other_organism(closest_dist, penalty_dist, penalty_value, org1, org2):
    # get the closest neighbour
    if org1 is org2:
        return closest_dist
    org_org_dist = maths_functions.dist_to_neighbour(org1, org2)
    if org_org_dist < closest_dist:
        closest_dist = org_org_dist
        org1.x_distance_to_neighbour, org1.y_distance_to_neighbour = maths_functions.xy_dist_to_neighbour(org1, org2)

    # update organism fitness function
    if org_org_dist <= penalty_dist:
        org1.fitness -= penalty_value

    return closest_dist


def behave_on_predator(closest_dist, penalty_dist, org, pred):
    # get the closest neighbour
    if org is pred:
        pass
    org_pred_dist = maths_functions.dist_to_predator(org, pred)
    if org_pred_dist < closest_dist:
        closest_dist = org_pred_dist
        org.x_distance_to_predator, org.y_distance_to_predator = maths_functions.xy_dist_to_predator(org, pred)

    # update organism fitness function
    if org_pred_dist <= penalty_dist:
        org.fitness = 0

    return closest_dist
