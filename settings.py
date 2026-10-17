def settings():
    settings = {}

    # FILE DETAILS
    settings['name'] = 'universe_26'

    # EVOLUTION SETTINGS
    settings['gens'] = 100                     # number of generations
    settings['org_num'] = 30                   # number of organisms
    settings['food_num'] = 15                  # number of food particles
    settings['pred_num'] = 4                   # number of predators
    settings['elitism_org'] = 0.35             # elitism (percent of population to keep and allow to have children)
    settings['elitism_pred'] = 0.50            # elitism (percent of population to keep and allow to have children)
    settings['mutate'] = 0.1                   # mutation rate (probability to mutate each weight of a child)
    settings['mutate_sigma'] = 0.5             # mutation strength (std of gaussian noise added to a weight)

    # FOOD SETTINGS
    settings['food_energy'] = 2                # food energy

    # ORGANISM SETTINGS
    settings['org_vision_dist'] = 5            # organism vision distance
    settings['org_momentum'] = 0.90            # velocity decay factor, so the organisms have momentum
    settings['org_thrust'] = 0.2               # how much the network output changes velocity per tick (acceleration)
    settings['org_max_velocity'] = 1.0         # organism maximum speed
    settings['org_start_fitness'] = 5          # organism start energy
    settings['org_eat_dist'] = 0.15            # food to be eaten distance
    settings['org_org_dist'] = 0.10            # other organism clumping penalty distance
    settings['org_org_penalty'] = 0.06         # other organism clumping penalty value
    settings['org_hunger_penalty'] = 0.07      # end of tick hunger penalty value
    settings['org_wall_penalty'] = 0.03        # touching arena wall penalty value

    # PREDATOR SETTINGS
    settings['pred_create'] = True             # option to seed predator to pool
    settings['pred_vision_dist'] = 10          # predator vision distance
    settings['pred_momentum'] = 0.8125         # velocity decay factor: predators are slower but more agile (ambush)
    settings['pred_thrust'] = 0.3              # how much the network output changes velocity per tick (acceleration)
    settings['pred_max_velocity'] = 0.8        # predator maximum speed (herbivores: 1.0)
    settings['pred_start_fitness'] = 7         # predator start energy
    settings['pred_eat_dist'] = 0.10           # distance to kill a living organism (from the predator's path)
    settings['pred_body_eat_dist'] = 0.20      # distance to eat a dead body (from the predator's path)
    settings['pred_carrion_energy'] = 6        # energy for eating a dead organism (killed by a predator or died itself)
    settings['pred_body_priority'] = 'always'  # no hunting while a body is in sight: 'always' or 'closer' (body closer than prey)
    settings['pred_pred_dist'] = 0.20          # other predator clumping penalty distance
    settings['pred_pred_penalty'] = 0.20       # other predator clumping penalty value
    settings['pred_hunger_penalty'] = 0.07     # end of tick hunger penalty value
    settings['pred_wall_penalty'] = 0.03       # touching arena wall penalty value

    # SIMULATION SETTINGS
    settings['seed'] = 333                     # for reproducibility
    settings['ticks'] = 100                    # time steps in a generation
    settings['corpse_momentum'] = 0.7          # dead bodies drift by inertia and slow down by this factor per tick
    settings['x_min'] = -3.0                   # arena western border
    settings['x_max'] = 3.0                    # arena eastern border
    settings['y_min'] = -3.0                   # arena southern border
    settings['y_max'] = 3.0                    # arena northern border

    # NEURAL NETWORK SETTINGS
    settings['org_inodes'] = 8                 # herbivore inputs: velocity, food, neighbour, predator (x, y each)
    settings['pred_inodes'] = 8                # predator inputs: velocity, prey, neighbour, carrion (x, y each)
    settings['hnodes'] = 5                     # number of hidden nodes
    settings['onodes'] = 2                     # number of output nodes

    # GIF
    settings['plot_gens'] = [9, 49, 99]        # plot following generations (list(range(10, 100, 10)))

    return settings
