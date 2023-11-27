from dataclasses import dataclass
from particula import u
from particula.constants import (GAS_CONSTANT_JOULE_KELVIN_MOLE,
                                 MOLECULAR_WEIGHT_AIR_KILOGRAM_MOLE,
                                 REF_TEMPERATURE_STP_KELVIN,
                                 REF_VISCOSITY_AIR_STP_PASCAL_SECOND,
                                 SUTHERLAND_CONSTANT_KELVIN)
from particula.util.dynamic_viscosity import dyn_vis
from particula.util.mean_free_path import mfp
from particula.util.dilution_loss import drc
from particula.util.species_properties import vapor_concentration


# pylint: disable=too-many-instance-attributes
@dataclass
class Environment:
    """ Data class for storing environment properties. """
    coagulation_approximation: str = "hardsphere"
    dilution_rate_constant: float = 0.0  # s^-1
    temperature: float = 298.15  # K
    reference_viscosity: float = REF_VISCOSITY_AIR_STP_PASCAL_SECOND
    reference_temperature: float = REF_TEMPERATURE_STP_KELVIN
    pressure: float = 101325.0  # Pa
    molecular_weight: float = MOLECULAR_WEIGHT_AIR_KILOGRAM_MOLE
    sutherland_constant: float = SUTHERLAND_CONSTANT_KELVIN
    gas_constant: float = GAS_CONSTANT_JOULE_KELVIN_MOLE
    water_saturation_ratio: float = 0.0
