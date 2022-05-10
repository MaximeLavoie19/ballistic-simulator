from core.effect import Effect
from core.projectile import Projectile


class GravityEffect(Effect):
    gravity = 9.80665

    def apply(self, _projectile: Projectile, timestep_in_ms):
        seconds = timestep_in_ms / 1000.0
        gravity_effect = -seconds * self.gravity
        return {"y": gravity_effect}
