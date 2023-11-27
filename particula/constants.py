""" a centralized location for important, unchanged physics parameters.

    This file contains constants that are used in multiple modules. Each
    constant has its own units and exported with them. The constants are
    mostly related to atmospheric aerosol particles in usual conditions.

"""

from particula import u

BOLTZMANN_CONSTANT = (1*u.k_B).to_base_units()
BOLTZMANN_CONSTANT_JOULE_KELVIN = float(BOLTZMANN_CONSTANT.m)

AVOGADRO_NUMBER = (1*u.avogadro_constant).to_base_units()
AVOGADRO_NUMBER_MOLE = float(AVOGADRO_NUMBER.m)

# Gas constant in J mol^-1 K^-1 = m^2 kg mol^-1 s^-2 K^-1
# J = kg m^2 s^-2
# or (1*u.molar_gas_constant).to_base_units()
GAS_CONSTANT = BOLTZMANN_CONSTANT * AVOGADRO_NUMBER
GAS_CONSTANT_JOULE_KELVIN_MOLE = float(GAS_CONSTANT.m)

ELEMENTARY_CHARGE_VALUE = (1*u.elementary_charge).to_base_units()
ELEMENTARY_CHARGE_VALUE_COULOMB = float(ELEMENTARY_CHARGE_VALUE.m)

# Relative permittivity of air at approx.
# 296.15 K and 101325 Pa and 40% RH
# See https://www.osti.gov/servlets/purl/1504063
# Previously known as the "dielectric constant"
# Often denoted as epsilon
RELATIVE_PERMITTIVITY_AIR_ROOM = 1.000530569  # unitless
RELATIVE_PERMITTIVITY_AIR_ROOM_UNITLESS = float(
    RELATIVE_PERMITTIVITY_AIR_ROOM)
# At STP (273.15 K, 1 atm):
# see: https://en.wikipedia.org/wiki/Relative_permittivity
RELATIVE_PERMITTIVITY_AIR_STP = 1.00058986  # unitless
RELATIVE_PERMITTIVITY_AIR_STP_UNITLESS = float(RELATIVE_PERMITTIVITY_AIR_STP)

# select one of the two:
RELATIVE_PERMITTIVITY_AIR = RELATIVE_PERMITTIVITY_AIR_ROOM
RELATIVE_PERMITTIVITY_AIR_UNITLESS = RELATIVE_PERMITTIVITY_AIR_ROOM_UNITLESS

# Permittivity of free space in F/m
# Also known as the electric constant, permittivity of free space
# Often denoted by epsilon_0
VACUUM_PERMITTIVITY = (1*u.vacuum_permittivity).to_base_units()
VACUUM_PERMITTIVITY_FARAD_METER = float(VACUUM_PERMITTIVITY.m)

ELECTRIC_PERMITTIVITY = RELATIVE_PERMITTIVITY_AIR * VACUUM_PERMITTIVITY
ELECTRIC_PERMITTIVITY_FARAD_METER = float(ELECTRIC_PERMITTIVITY.m)

# These values are used to calculate the dynamic viscosity of air
# Here, REF temperature and viscosity are at STP:
# Standard temperature and pressure (273.15 K and 101325 Pa)
REF_VISCOSITY_AIR_STP = 1.716e-5 * u.Pa * u.s
REF_VISCOSITY_AIR_STP_PASCAL_SECOND = float(REF_VISCOSITY_AIR_STP.m)
REF_TEMPERATURE_STP = 273.15 * u.K
REF_TEMPERATURE_STP_KELVIN = float(REF_TEMPERATURE_STP.m)
SUTHERLAND_CONSTANT = 110.4 * u.K
SUTHERLAND_CONSTANT_KELVIN = float(SUTHERLAND_CONSTANT.m)

MOLECULAR_WEIGHT_AIR = (28.9644 * u.g / u.mol).to_base_units()
MOLECULAR_WEIGHT_AIR_KILOGRAM_MOLE = float(MOLECULAR_WEIGHT_AIR.m)

STANDARD_GRAVITY = (1*u.gravity).to_base_units()
STANDARD_GRAVITY_METER_SECOND2 = float(STANDARD_GRAVITY.m)
