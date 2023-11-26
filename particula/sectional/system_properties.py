from dataclasses import dataclass
from particula import u
from particula.constants import (GAS_CONSTANT, MOLECULAR_WEIGHT_AIR,
                                 REF_TEMPERATURE_STP, REF_VISCOSITY_AIR_STP,
                                 SUTHERLAND_CONSTANT)
from particula.util.dynamic_viscosity import dyn_vis
from particula.util.input_handling import (in_gas_constant, in_handling,
                                           in_molecular_weight, in_pressure,
                                           in_temperature, in_viscosity,
                                           in_scalar)
from particula.util.mean_free_path import mfp
from particula.util.dilution_loss import drc
from particula.util.species_properties import vapor_concentration


@dataclass
class Environment:
    """ Data class for storing environment properties. """
    coagulation_approximation: str = "hardsphere"
    dilution_rate_constant: float = in_handling(0.0, u.s**-1)
    temperature: float = in_temperature(298.15)
    reference_viscosity: float = REF_VISCOSITY_AIR_STP
    reference_temperature: float = REF_TEMPERATURE_STP
    pressure: float = in_pressure(101325.0)
    molecular_weight: float = MOLECULAR_WEIGHT_AIR
    sutherland_constant: float = SUTHERLAND_CONSTANT
    gas_constant: float = GAS_CONSTANT
    water_saturation_ratio: float = 0.0
