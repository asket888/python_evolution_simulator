from objects.creature import Creature


class Predator(Creature):
    """Predator: hunts herbivores, eats carrion (dead herbivores), avoids other predators and walls."""
    prefix = 'pred'

    def __init__(self, settings, wih=None, who=None, name=None):
        super().__init__(settings, wih, who, name)

        self.x_distance_to_carrion = 0  # closest dead (not eaten) herbivore, 0 when none is visible
        self.y_distance_to_carrion = 0

    def inputs(self):
        return super().inputs() + [self.x_distance_to_carrion, self.y_distance_to_carrion]
