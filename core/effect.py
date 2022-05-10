from typing import Dict

from core.projectile import Projectile


class Effect:
    def apply(self, projectile: Projectile, timestep_in_ms: float) -> Dict[str, float]:
        raise Exception("Method Apply not implemented")
