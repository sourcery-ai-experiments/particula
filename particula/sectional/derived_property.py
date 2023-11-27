"""Derived properties from the system properties."""

from typing import Union, Optional
from numpy import ndarray
from particula.sectional.system_properties import Environment


# def water_vapor_concentration(env_props: Environment):
#     """ Calculate water vapor concentration. """
#     return vapor_concentration(
#         saturation_ratio=env_props.water_saturation_ratio,
#         temperature=env_props.temperature,
#         species="water"
#     )
