from core.drag_model import DragCalculator
from core.effect import Effect
from core.projectile import Projectile


class DragEffect(Effect):
    def __init__(self, fluid_mass_density, drag_calculator: DragCalculator):
        self.fluid_mass_density = fluid_mass_density
        self.drag_calculator = drag_calculator

    def apply(self, projectile: Projectile, timestep_in_ms):
        seconds = timestep_in_ms / 1000.0
        if projectile.speed == 0:
            return {}
        drag_coefficient = self.drag_calculator.calculate_drag_coefficient(projectile)
        drag = self.fluid_mass_density * pow(projectile.speed, 2) * drag_coefficient * projectile.cross_section_area / 2
        drag_effect = drag * seconds
        deceleration = drag_effect / projectile.mass_in_grams / 1000.0
        deceleration_ratio = deceleration / projectile.speed
        deceleration_vector = {}
        for key, value in projectile.velocity.items():
            deceleration_vector[key] = value * -deceleration_ratio
        return deceleration_vector
