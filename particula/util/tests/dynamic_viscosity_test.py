""" testing the dynamic viscosity function
"""

import pytest
import numpy as np
from particula import u
from particula.constants import REF_TEMPERATURE_STP as REF_TEMP
from particula.constants import REF_VISCOSITY_AIR_STP as REF_VIS_AIR
from particula.util.dynamic_viscosity import dyn_vis, dyn_vis_strict


def test_dyn_vis():
    """ Testing the dynamic viscosity calculation:
            * see if dyn_vis returns correct units of constant
            * see if defaults work properly
            * see if scaling is correct (dividing by 2)
            * see if conversion from celsius works
            * see if user-provided constants work properly
            * testing invalid inputs

    """

    assert dyn_vis().units == REF_VIS_AIR.to_base_units().units

    assert dyn_vis(temperature=REF_TEMP) == REF_VIS_AIR

    assert dyn_vis(temperature=REF_TEMP) == REF_VIS_AIR

    assert dyn_vis(temperature=REF_TEMP/2) <= REF_VIS_AIR

    assert dyn_vis(temperature=REF_TEMP*2) >= REF_VIS_AIR

    assert (
        dyn_vis(temperature=REF_TEMP.to("degC")).to_base_units()
        ==
        REF_VIS_AIR.to_base_units()
    )

    assert (
        dyn_vis(
            temperature=REF_TEMP,
            reference_viscosity=REF_VIS_AIR/2,
            reference_temperature=REF_TEMP,
        )
        ==
        REF_VIS_AIR/2
    )

    assert dyn_vis(temperature=[250, 255, 260]).m.shape == (3,)

    with pytest.raises(ValueError):
        dyn_vis(temperature=5*u.m)

    with pytest.raises(ValueError):
        dyn_vis(reference_viscosity=5*u.m)

    with pytest.raises(ValueError):
        dyn_vis(reference_temperature=5*u.m)


def test_dyn_vis_strict():
    """ Testing the dynamic viscosity strict calculation:
    for floats and np.arrays, comparing with dyn_vis
    """
    ref = dyn_vis(temperature=300.0).m
    strict_float = dyn_vis_strict(temperature_kelvin=300.0)

    assert strict_float == ref

    ref = dyn_vis(temperature=np.array([300, 310, 320])*u.K).m
    strict_array = dyn_vis_strict(temperature_kelvin=np.array([300, 310, 320]))

    assert np.all(strict_array == ref)