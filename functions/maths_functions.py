from numpy import sqrt


def dist(x2, x1, y2, y1):
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def xy_dist(x2, x1, y2, y1):
    return [x2 - x1, y2 - y1]


# organism math
def dist_to_food(org, food):
    return dist(food.x, org.x, food.y, org.y)


def xy_dist_to_food(org, food):
    return xy_dist(food.x, org.x, food.y, org.y)


def path_dist_to_food(org, food):
    # closest distance from food to the path travelled during the last tick (tail -> current position)
    path_x, path_y = org.x - org.x_tail, org.y - org.y_tail
    path_len_sq = path_x ** 2 + path_y ** 2
    if path_len_sq == 0:
        return dist_to_food(org, food)
    t = ((food.x - org.x_tail) * path_x + (food.y - org.y_tail) * path_y) / path_len_sq
    t = min(max(t, 0), 1)
    return dist(food.x, org.x_tail + t * path_x, food.y, org.y_tail + t * path_y)


def dist_to_neighbour(org1, org2):
    return dist(org2.x, org1.x, org2.y, org1.y)


def xy_dist_to_neighbour(org1, org2):
    return xy_dist(org2.x, org1.x, org2.y, org1.y)


def dist_to_predator(org, pred):
    return dist(pred.x_tail, org.x, pred.y_tail, org.y)


def xy_dist_to_predator(org, pred):
    return xy_dist(pred.x_tail, org.x, pred.y_tail, org.y)


# predator math
def dist_to_organism(pred, org):
    return dist(org.x, pred.x, org.y, pred.y)


def xy_dist_to_organism(pred, org):
    return xy_dist(org.x, pred.x, org.y, pred.y)
