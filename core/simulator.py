import math

from typing import List, Dict

from core.axis_enum import AxisEnum
from core.effect import Effect
from core.projectile import Projectile


def rotate_vector(vector, milrad):
    angle_cos = math.cos(milrad / 1000)
    angle_sin = math.sin(milrad / 1000)
    new_x = vector[0] * angle_cos - vector[1] * angle_sin
    new_y = vector[0] * angle_sin + vector[1] * angle_cos
    return [new_x, new_y]


class Simulator:
    def __init__(self, projectile: Projectile, effects: List[Effect], timestep_in_ms, log_interval):
        self.effects = effects
        self.logs = []
        self.log_interval = log_interval
        self.zero_angle = 0
        self.elevation = 0
        self.projectile = projectile
        self.timestep_in_ms = timestep_in_ms

    def simulate(self, boundaries: Dict[str, float]):
        self.projectile.coordinate = {AxisEnum.X.value: 0, AxisEnum.Y.value: -0.0416}
        self.logs = []
        timestamp = 0
        while self.projectile.is_within_boundaries(boundaries):
            if round(timestamp / self.timestep_in_ms) % self.log_interval == 0:
                self.log(timestamp)
            self.simulate_timestep()
            timestamp += self.timestep_in_ms
        self.log(timestamp)

    def log(self, timestamp):
        self.logs.append({
            "coordinate": self.projectile.coordinate.copy(),
            "velocity": self.projectile.velocity.copy(),
            "timestamp": timestamp / 1000.0,
        })

    def simulate_timestep(self):
        deltas = []
        for effect in self.effects:
            deltas.append(effect.apply(self.projectile, self.timestep_in_ms))

        for delta in deltas:
            for key, value in delta.items():
                self.projectile.velocity[key] = self.projectile.velocity.get(key, 0) + value
        self.projectile.update_speed()
        self.projectile.update_position(self.timestep_in_ms)

    def zero(self, zero_distance: float):
        self.zero_angle = 0
        self.zero_angle = self.get_adjustment(zero_distance)

    def get_adjustment(self, target_distance: float, target_height=0.0):
        is_target_hit = False
        milrad = target_distance / 1000
        adjustment = 0
        while not is_target_hit:
            self.shoot(adjustment, target_distance, max_drop=target_distance)
            closest_log = min(self.logs, key=lambda log: abs(log['coordinate']['x'] - target_distance))
            distance = closest_log['coordinate']['y'] - target_height
            if abs(distance) < 0.05:
                break
            adjustment -= distance / milrad
        return adjustment

    def shoot(self, adjustment: float, max_distance: float, max_drop=20.0):
        vector = rotate_vector([self.projectile.muzzle_velocity, 0], self.zero_angle + self.elevation + adjustment)
        self.projectile.velocity = {AxisEnum.X.value: vector[0],
                                    AxisEnum.Y.value: vector[1]}  # 2585 fps = 787.908 m/s
        self.simulate({AxisEnum.X.value: max_distance + 10, AxisEnum.Y.value: -abs(max_drop)})
