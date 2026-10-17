import numpy as np


class Creature:
    """Body and brain shared by herbivores and predators. Settings are read with the subclass prefix ('org' / 'pred')."""
    prefix = None

    def __init__(self, settings, wih=None, who=None, name=None):
        p = self.prefix

        self.fitness = settings[p + '_start_fitness']  # fitness (creature energy)

        self.max_velocity = settings[p + '_max_velocity']
        self.velocity_decay_factor = settings[p + '_momentum']
        self.thrust = settings[p + '_thrust']

        self.x_max = settings['x_max'] + 1
        self.x_min = settings['x_min'] - 1
        self.y_max = settings['y_max'] + 1
        self.y_min = settings['y_min'] - 1

        self.x = np.random.uniform(settings['x_min'] - 1, settings['x_max'] + 1)
        self.y = np.random.uniform(settings['y_min'] - 1, settings['y_max'] + 1)

        self.x_tail = self.x
        self.y_tail = self.y

        self.x_velocity = 0  # velocity in the x direction
        self.y_velocity = 0  # velocity in the y direction

        self.x_distance_to_food = 0  # food for herbivores, prey for predators
        self.y_distance_to_food = 0

        self.x_distance_to_neighbour = 0  # closest creature of the same kind
        self.y_distance_to_neighbour = 0

        self.wih = wih  # weights from input to hidden layer
        self.who = who  # weights from hidden layer to output

        self.name = name

    def inputs(self):
        return [
            self.x_velocity,
            self.y_velocity,
            self.x_distance_to_food,
            self.y_distance_to_food,
            self.x_distance_to_neighbour,
            self.y_distance_to_neighbour
        ]

    # NEURAL NETWORK
    def think(self, settings):

        # SIMPLE MLP
        def af(x):
            return np.tanh(x)

        h1 = af(np.dot(self.wih, self.inputs()))  # hidden layer
        out = np.multiply(af(np.dot(self.who, h1)), 0.5)  # output layer

        # UPDATE FITNESS
        self.fitness -= settings[self.prefix + '_hunger_penalty']

        # UPDATE TAIL
        self.x_tail = self.x
        self.y_tail = self.y

        # DEAD CREATURE: no thrust, the body drifts by inertia and slows down
        if self.fitness <= 0:
            self.x_velocity *= settings['corpse_momentum']
            self.y_velocity *= settings['corpse_momentum']
            self._move()
        else:
            # UPDATE VELOCITIES (network output is a thrust, velocity keeps momentum)
            self.x_velocity = float(np.clip(float(out[0]) * self.thrust + self.x_velocity * self.velocity_decay_factor,
                                            -self.max_velocity, self.max_velocity))
            self.y_velocity = float(np.clip(float(out[1]) * self.thrust + self.y_velocity * self.velocity_decay_factor,
                                            -self.max_velocity, self.max_velocity))
            self._move()

            # WALL PENALTY
            if abs(self.x) >= self.x_max or abs(self.y) >= self.y_max:
                self.fitness -= settings[self.prefix + '_wall_penalty']

    def _move(self):
        # UPDATE POSITION (hitting a wall stops the movement into it, so the creature does not stay pressed to it)
        self.x += self.x_velocity
        if abs(self.x) > self.x_max:
            self.x, self.x_velocity = float(np.sign(self.x)) * self.x_max, 0
        self.y += self.y_velocity
        if abs(self.y) > self.y_max:
            self.y, self.y_velocity = float(np.sign(self.y)) * self.y_max, 0
