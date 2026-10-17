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


def path_dist(mover, target):
    # closest distance from target (food or prey) to the path travelled by mover during the last tick (tail -> position)
    path_x, path_y = mover.x - mover.x_tail, mover.y - mover.y_tail
    path_len_sq = path_x ** 2 + path_y ** 2
    if path_len_sq == 0:
        return dist(target.x, mover.x, target.y, mover.y)
    t = ((target.x - mover.x_tail) * path_x + (target.y - mover.y_tail) * path_y) / path_len_sq
    t = min(max(t, 0), 1)
    return dist(target.x, mover.x_tail + t * path_x, target.y, mover.y_tail + t * path_y)


def dist_to_neighbour(org1, org2):
    return dist(org2.x, org1.x, org2.y, org1.y)


def xy_dist_to_neighbour(org1, org2):
    return xy_dist(org2.x, org1.x, org2.y, org1.y)


def dist_to_predator(org, pred):
    return dist(pred.x, org.x, pred.y, org.y)


def xy_dist_to_predator(org, pred):
    return xy_dist(pred.x, org.x, pred.y, org.y)


# predator math
def dist_to_organism(pred, org):
    return dist(org.x, pred.x, org.y, pred.y)


def xy_dist_to_organism(pred, org):
    return xy_dist(org.x, pred.x, org.y, pred.y)
