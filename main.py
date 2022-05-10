import json
import math

import matplotlib.pyplot as plt

from ballistic_simulator.drag_effect import DragEffect
from ballistic_simulator.gravity_effect import GravityEffect
from core.drag_model import DragCalculator
from core.projectile import Projectile
from core.simulator import Simulator


air_mass_density = 1.225  # kg/m3 @ 1atm 15c


def bullet_factory(projectile_path: str):
    with open("ballistic_simulator/bullets.json") as bullet_file:
        bullet_specs = json.load(bullet_file)
    path = projectile_path.split("/")
    for key in path:
        bullet_specs = bullet_specs.get(key)
    projectile = Projectile(
        bullet_specs["diameter"],
        bullet_specs["weight_in_grams"],
        bullet_specs["muzzle_velocity"],
    )

    if bullet_specs.get("ballistic_coefficient_g7", False):
        projectile.ballistic_coefficient_g7 = bullet_specs["ballistic_coefficient_g7"]
    elif bullet_specs.get("ballistic_coefficient_g1", False):
        projectile.ballistic_coefficient_g1 = bullet_specs["ballistic_coefficient_g1"]
    else:
        raise Exception("Missing ballistic coefficient")

    return projectile


def plot_bullet(adjustment: float, projectile_path: str, create_label=True, max_drop=20.0):
    path = projectile_path.split("/")
    projectile = bullet_factory(projectile_path)
    drag_calculator = DragCalculator()
    simulator = Simulator(
        projectile,
        [
            GravityEffect(),
            DragEffect(air_mass_density, drag_calculator),
        ],
        0.1,
        50,
    )
    simulator.zero(91.44)
    simulator.shoot(adjustment, 1000, max_drop=max_drop)
    plot_bullet_path(simulator, path[-2] + " " + path[-1], create_label=create_label)
    plt.plot((0, 1010), (0.1, 0.1), "k", alpha=.1)
    plt.plot((0, 1010), (-0.1, -0.1), "k", alpha=.1)


def create_lookup(projectile_path: str):
    counter = 0
    while counter < 9:
        plot_bullet(counter, projectile_path, False, 0.15)
        counter += 0.5


def rotate_vector(vector, angle):
    angle_cos = math.cos(math.radians(angle))
    angle_sin = math.sin(math.radians(angle))
    new_x = vector[0] * angle_cos - vector[1] * angle_sin
    new_y = vector[0] * angle_sin + vector[1] * angle_cos
    return [new_x, new_y]


def shoot_at(distance, angle, projectile_path: str):
    x, y = rotate_vector([distance, 0], angle)
    path = projectile_path.split("/")
    projectile = bullet_factory(projectile_path)
    drag_calculator = DragCalculator()
    simulator = Simulator(
        projectile,
        [
            GravityEffect(),
            DragEffect(air_mass_density, drag_calculator),
        ],
        0.1,
        50,
    )
    simulator.zero(100)
    simulator.elevation = 1000 * y / distance
    adjustment = simulator.get_adjustment(x, y)
    simulator.shoot(adjustment, x, y - 1)
    plot_bullet_path(simulator, path[-2] + " " + path[-1] + " +" + adjustment.__str__() + " milrad")
    plt.plot((0, x), (0.1, y + 0.1), "k", alpha=.1)
    plt.plot((0, x), (-0.1, y - 0.1), "k", alpha=.1)


def plot_bullet_path(simulator, label, create_label=True):
    log_xs = list(map(lambda x: x["coordinate"]["x"], simulator.logs))
    log_ys = list(map(lambda x: x["coordinate"]["y"], simulator.logs))
    plot = plt.scatter(log_xs, log_ys, s=3)
    if create_label:
        plot.set_label(label)


if __name__ == '__main__':
    shoot_at(1000, -10, "6.5/6.5 creedmoor/140")
    # plot_bullet(0, "6.5/6.5 creedmoor/140")
    plt.grid()
    plt.legend()
    plt.show()
