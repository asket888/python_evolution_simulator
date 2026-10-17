from objects.creature import Creature


class Organism(Creature):
    """Herbivore: looks for food, avoids other herbivores, walls and predators."""
    prefix = 'org'

    def __init__(self, settings, wih=None, who=None, name=None):
        super().__init__(settings, wih, who, name)

        self.vision = settings['org_vision_dist']
        self.edible = False  # dead body that predators can eat (from the tick after death)
        self.killed = False  # killed by a predator
        self.eaten = False  # eaten by a predator: the body is gone

        self.x_distance_to_predator = 0  # closest visible predator, 0 when none is visible
        self.y_distance_to_predator = 0

    def inputs(self):
        # predator is sensed as a threat: direction to it scaled by closeness (0 at the edge of vision, 1 at contact),
        # so a far predator does not distract from food and a close one dominates
        threat_x, threat_y = 0, 0
        dist = (self.x_distance_to_predator ** 2 + self.y_distance_to_predator ** 2) ** 0.5
        if dist > 0:
            closeness = (1 - dist / self.vision) / dist
            threat_x, threat_y = self.x_distance_to_predator * closeness, self.y_distance_to_predator * closeness

        return super().inputs() + [threat_x, threat_y]

    def think(self, settings):
        super().think(settings)
        # a body becomes edible on the tick after death: a predator that killed it has to come back to eat
        self.edible = self.fitness <= 0 and not self.eaten
