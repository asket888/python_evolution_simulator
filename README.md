# Universe 26 evolution simulator

An aquarium where herbivores and predators learn to survive. Every creature is controlled by a tiny neural network,
and the networks are improved by a genetic algorithm: nobody programs the behaviour, it evolves from generation to generation.

![Screenshot](screenshot.gif)

## How it works

The aquarium is an 8×8 square. A generation lasts 100 ticks; at the end of it the best creatures of each species become
parents of the next generation.

| On the picture | What it is |
|---|---|
| green circle with a tail | herbivore (the tail shows its last move) |
| blue dot | food |
| red circle | predator |
| yellow circle | dead herbivore (a body) |
| gray circle | dead predator |

### Herbivores
- Swim towards food, avoid walls, each other and predators.
- See (network inputs): own velocity, the closest food, the closest other herbivore and the closest predator.
  The predator is sensed as a *threat*: direction to it scaled by closeness, so a far predator does not distract
  from food and a close one dominates.
- Energy: start with 5, lose it every tick (hunger), when touching a wall or another herbivore; gain it by eating food.
  A herbivore that eats nothing during a generation dies.

### Predators
- See: own velocity, the closest living herbivore, the closest other predator and the closest dead body.
- **Kill, then eat.** Touching a living herbivore kills it but gives no energy. The body drifts by inertia and slows down;
  to eat it, a predator has to come back (from the next tick). A body gives the same energy whether it was killed
  by a predator or died by itself (hunger, walls, collisions).
- **Bodies first.** While an uneaten body is in sight a predator does not hunt.
- Predators are *ambush hunters*: slower than herbivores (max speed 0.8 vs 1.0) but more agile.
- Hunger is lethal: a predator that eats nothing during a generation dies.

### Physics
- The network output is a thrust: it changes the velocity a little every tick, and the velocity keeps momentum,
  so creatures swim in smooth arcs instead of jerking.
- Food and prey are eaten / killed if they are close to the *path* travelled during a tick, so fast creatures
  do not fly through their targets.
- Hitting a wall stops the movement into it.

### Evolution
- The brain is a neural network with one hidden layer (5 neurons, `tanh`).
- After each generation the creatures are ranked by their energy (`fitness`). The best part of the population
  (`elitism_*`) survives unchanged, the rest are children of two random parents from it.
- Crossover: every hidden neuron (with its input and output weights) is inherited whole from one of the parents.
- Mutation: every weight of a child is changed with probability `mutate` by adding gaussian noise (`mutate_sigma`).

Typical run with the default settings (100 generations): in the first generation most herbivores die,
by generation ~20 they learn to find food and avoid walls; predators start as scavengers,
go through a starvation crisis when herbivores stop dying of hunger and then learn to hunt.

## Run

Requires Python 3.12+.

1. navigate to the application directory
2. run `$ pip install -r requirements.txt` to install all necessary dependencies
3. run `$ python run.py`

The run takes 1–2 minutes. Every generation prints a line like this:

```
 > GEN-30 : HERBIVORES best  21.52 avg   4.68 worst  -6.78 survived 24/30 (killed 5, died 1) | PREDATORS survived 2/4 avg  6.17, bodies eaten 5
```

- `killed` – herbivores killed by predators, `died` – died by themselves (hunger, walls, collisions)
- `bodies eaten` – bodies eaten by predators

Results are saved to the `results` folder:
- `universe_26 <date>.jpg` – chart: herbivore fitness (best / average / worst) and survival of both species by generation
- `universe_26 gen-<N> <date>.gif` – animation of the generations listed in `plot_gens`

## Settings

All parameters are in [settings.py](settings.py). The most interesting ones:

| Parameter | Default | Meaning |
|---|---|---|
| `gens` | 100 | number of generations |
| `org_num` / `pred_num` | 30 / 4 | number of herbivores / predators |
| `pred_create` | True | `False` – herbivores only |
| `food_num` | 15 | number of food particles (eaten food reappears at a random place) |
| `food_energy` | 2 | energy for one food particle |
| `org_hunger_penalty` / `pred_hunger_penalty` | 0.07 / 0.07 | energy lost every tick |
| `org_start_fitness` / `pred_start_fitness` | 5 / 7 | start energy |
| `org_org_penalty`, `org_wall_penalty` | 0.06, 0.03 | herbivore penalty per tick for touching another herbivore / a wall |
| `org_max_velocity` / `pred_max_velocity` | 1.0 / 0.8 | max speed |
| `org_momentum`, `org_thrust` | 0.9, 0.2 | herbivore inertia and acceleration (agility) |
| `pred_momentum`, `pred_thrust` | 0.8125, 0.3 | predator inertia and acceleration |
| `org_vision_dist` / `pred_vision_dist` | 5 / 10 | vision distance |
| `org_eat_dist` | 0.15 | herbivore reach for food |
| `pred_eat_dist` / `pred_body_eat_dist` | 0.10 / 0.20 | predator reach to kill a herbivore / to eat a body |
| `pred_carrion_energy` | 6 | energy for eating a body |
| `pred_body_priority` | `'always'` | no hunting while a body is in sight; `'closer'` – only if the body is closer than any prey |
| `corpse_momentum` | 0.7 | how fast dead bodies stop drifting |
| `elitism_org` / `elitism_pred` | 0.35 / 0.5 | share of the population that survives and becomes parents |
| `mutate`, `mutate_sigma` | 0.1, 0.5 | mutation probability per weight and strength |
| `hnodes` | 5 | hidden neurons |
| `seed` | 333 | random seed: the same seed gives the same run |
| `plot_gens` | [9, 49, 99] | generations to save as gifs (0-based: 9 is generation 10) |
| `gif_fps` | 10 | gif speed, frames (ticks) per second; gifs loop forever |

## Project structure

| Path | What is there |
|---|---|
| `run.py` | entry point |
| `settings.py` | all parameters |
| `simulation.py` | generation loop: sensing, eating, hunting, moving |
| `evolution.py` | selection, crossover and mutation |
| `objects/` | `Creature` (shared body and brain), `Organism` (herbivore), `Predator`, `Food` |
| `behavior/` | what herbivores and predators do when they meet food, each other and bodies |
| `functions/` | geometry and file name helpers |
| `gui/` | console output, chart, gif frames |
