"""Derived properties from the system properties."""

from typing import Union

from particula.sectional.system_properties import Environment
from particula import util


def dynamic_viscosity(environment: Environment):
    """ Calculate dynamic viscosity. """
    return util.dynamic_viscosity.dyn_vis(
        temperature=environment.temperature,
        reference_viscosity=environment.reference_viscosity,
        reference_temperature=environment.reference_temperature,
        sutherland_constant=environment.sutherland_constant,
    )

env = Environment()

print(dynamic_viscosity(env))


# def mean_free_path(env_props: Environment):
#     """ Calculate mean free path. """
#     return mfp(
#         temperature=env_props.temperature,
#         pressure=env_props.pressure,
#         molecular_weight=env_props.molecular_weight,
#         dynamic_viscosity=EnvCalc.dynamic_viscosity(env_props),
#         gas_constant=env_props.gas_constant,
#     )

# def water_vapor_concentration(env_props: Environment):
#     """ Calculate water vapor concentration. """
#     return vapor_concentration(
#         saturation_ratio=env_props.water_saturation_ratio,
#         temperature=env_props.temperature,
#         species="water"
#     )

# def dilution_rate_coefficient(env_props: Environment):
#     """ Calculate dilution rate coefficient. """
#     return drc(value=env_props.dilution_rate_constant)
