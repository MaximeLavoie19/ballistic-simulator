import math
from typing import Dict


class Projectile:
    velocity: Dict
    coordinate: Dict
    weight: float
    speed: float
    cross_section_area: float
    drag_coefficient: float
    mass_in_grams: float
    muzzle_velocity: float
    ballistic_coefficient_g1: float
    ballistic_coefficient_g7: float

    def __init__(
            self, diameter_in_mm: float, mass_in_grams: float, muzzle_velocity: float
    ):
        self.velocity = {"x": 0, "y": 0}
        self.coordinate = {"x": 0, "y": 0}
        self.speed = 0
        self.muzzle_velocity = muzzle_velocity
        self.mass_in_grams = mass_in_grams
        self.diameter_in_mm = diameter_in_mm
        self.cross_section_area = math.pi * pow(diameter_in_mm / 2.0, 2)

    def calculate_drag(self):
        raise Exception("Method calculate_drag not implemented")

    def calculate_speed(self):
        total = 0
        for axis in self.velocity.values():
            total += pow(axis, 2)
        speed = math.sqrt(total)
        return speed

    def update_speed(self):
        self.speed = self.calculate_speed()

    def update_position(self, time_interval_in_ms):
        for key, value in self.velocity.items():
            self.coordinate[key] += value * time_interval_in_ms / 1000

    def is_within_boundaries(self, boundaries: Dict[str, float]):
        is_within_boundaries = True
        for key, value in boundaries.items():
            if value > 0:
                is_within_boundaries &= value > self.coordinate[key]
            else:
                is_within_boundaries &= value < self.coordinate[key]
        return is_within_boundaries
