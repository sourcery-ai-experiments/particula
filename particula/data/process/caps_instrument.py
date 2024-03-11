"""Data corrections for CAPS instrument data"""

from numpy.typing import NDArray
import numpy as np
from scipy.interpolate import interp1d
from particula.data.process import kappa_via_extinction, scattering_truncation
from particula.data.stream import Stream
from particula.data.lake import Lake
from particula.util import convert, time_manage, size_distribution_convert


def correction(
        stream_caps: Stream,
        header_wet: str = 'Bsca_wet_CAPS_450nm[1/Mm]',
        calibration_wet: float = 1,
        header_dry: str = 'Bsca_dry_CAPS_450nm[1/Mm]',
        calibration_dry: float = 1,
):
    """
    Applies calibration corrections to the CAPS data. Operates on the stream
    object. No returns.

    Args
    ----------
    - stream_caps (object): Stream object with the CAPS data.
    - header_wet (str, optional): The header for the wet data. The default is
    'Bsca_wet_CAPS_450nm[1/Mm]'.
    - calibration_wet (float, optional): The calibration factor for the wet
    data. The default is 1.
    - calibration_dry (float, optional): The calibration factor for the dry
    data. The default is 1.
    - header_dry (str, optional): The header for the dry data. The default is
    'Bsca_dry_CAPS_450nm[1/Mm]'.
    """

    # copy the data to raw_
    stream_caps['raw_' + header_wet] = stream_caps[header_wet]
    stream_caps['raw_' + header_dry] = stream_caps[header_dry]

    # apply the calibration
    stream_caps[header_wet] = stream_caps['raw_' + header_wet] * calibration_wet
    stream_caps[header_dry] = stream_caps['raw_' + header_dry] * calibration_dry


def kappa_hgf_fit(
        stream_sizer: Stream,
        stream_caps: Stream,
        humidity_sizer: NDArray[np.float64],
        refractive_index_dry: float = 1.45,
):
    """
    Function to process the CAPS data, and smps for kappa fitting, and then add
    it to the datalake. Also applies truncation corrections to the CAPS data.

    Args
    ----

    """

    sizer_cs = size_distribution_convert.get_conversion_strategy(
        'dn/dlogdp', 'pms')

    number_per_cm3 = sizer_cs.convert(
        diameters=stream_sizer.header_float,
        concentration=stream_sizer.data,
    )

    # do the kappa fitting
    kappa_matrix = kappa_via_extinction.kappa_from_extinction_looped(
        extinction_dry=stream_caps['Bext_dry_CAPS_450nm[1/Mm]'],
        extinction_wet=stream_caps['Bext_wet_CAPS_450nm[1/Mm]'],
        number_per_cm3=number_per_cm3,
        diameter=stream_sizer.header_float,
        water_activity_sizer=humidity_sizer/100,
        water_activity_sample_dry=stream_caps['dualCAPS_inlet_RH[%]']/100,
        water_activity_sample_wet=stream_caps['Wet_RH_preCAPS[%]']/100,
        refractive_index_dry=refractive_index_dry,
        wavelength=450,
        discretize=True)

    # add the kappa matrix to the stream
    stream_caps['kappaHGF_fit'] = kappa_matrix[:, 0]
    stream_caps['kappaHGF_fit_lower'] = kappa_matrix[:, 1]
    stream_caps['kappaHGF_fit_upper'] = kappa_matrix[:, 2]


def truncation(
        stream_sizer: Stream,
        stream_caps: Stream,
        humidity_sizer: NDArray[np.float64],
        refractive_index_dry: float = 1.45,
):
    """
    Function to apply truncation corrections to the CAPS data.
    """

    sizer_cs = size_distribution_convert.get_conversion_strategy(
        'dn/dlogdp', 'pms')

    number_per_cm3 = sizer_cs.convert(
        diameters=stream_sizer.header_float,
        concentration=stream_sizer.data,
    )

    trunc_dry = scattering_truncation.correction_for_humidified_looped(
        kappa=stream_caps['kappaHGF_fit'],
        number_per_cm3=number_per_cm3,
        diameter=stream_sizer.header_float,
        water_activity_sizer=humidity_sizer/100,
        water_activity_sample=stream_caps['dualCAPS_inlet_RH[%]']/100,
        refractive_index_dry=refractive_index_dry,
        wavelength=450,
        discretize=True)

    trunc_wet = scattering_truncation.correction_for_humidified_looped(
        kappa=stream_caps['kappaHGF_fit'],
        number_per_cm3=number_per_cm3,
        diameter=stream_sizer.header_float,
        water_activity_sizer=humidity_sizer/100,
        water_activity_sample=stream_caps['Wet_RH_preCAPS[%]']/100,
        refractive_index_dry=refractive_index_dry,
        wavelength=450,
        discretize=True)

    stream_caps['truncation_wet'] = trunc_wet
    stream_caps['truncation_dry'] = trunc_dry

    # copy uncorrected data to not_trunc_
    stream_caps['not_trunc_Bsca_wet_CAPS_450nm[1/Mm]'] = \
        stream_caps['Bsca_wet_CAPS_450nm[1/Mm]']
    stream_caps['not_trunc_Bsca_dry_CAPS_450nm[1/Mm]'] = \
        stream_caps['Bsca_dry_CAPS_450nm[1/Mm]']
    # apply the truncation corrections
    stream_caps['Bsca_wet_CAPS_450nm[1/Mm]'] = \
        stream_caps['Bsca_wet_CAPS_450nm[1/Mm]'] * trunc_wet
    stream_caps['Bsca_dry_CAPS_450nm[1/Mm]'] = \
        stream_caps['Bsca_dry_CAPS_450nm[1/Mm]'] * trunc_dry






# def albedo_processing(
#     datalake,
#     keys: list = None
# ):
#     """
#     Calculates the albedo from the CAPS data and updates the datastream.

#     Args
#     ----------
#     datalake : object
#         DataLake object with the processed data added.

#     Returns
#     -------
#     datalake : object
#         DataLake object with the processed data added.
#     """

#     ssa_wet = datalake.datastreams['CAPS_data'].return_data(
#         keys=['b_sca_wet_CAPS_450nm[1/Mm]'])[0] \
#         / datalake.datastreams['CAPS_data'].return_data(
#         keys=['b_ext_wet_CAPS_450nm[1/Mm]'])[0]
#     ssa_dry = datalake.datastreams['CAPS_data'].return_data(
#         keys=['b_sca_dry_CAPS_450nm[1/Mm]'])[0] \
#         / datalake.datastreams['CAPS_data'].return_data(
#         keys=['b_ext_dry_CAPS_450nm[1/Mm]'])[0]
#     ssa_wet = datalake.datastreams['CAPS_data'].return_data(
#         keys=['b_sca_wet_CAPS_450nm[1/Mm]'])[0] \
#         / datalake.datastreams['CAPS_data'].return_data(
#         keys=['b_ext_wet_CAPS_450nm[1/Mm]'])[0]
#     ssa_dry = datalake.datastreams['CAPS_data'].return_data(
#         keys=['b_sca_dry_CAPS_450nm[1/Mm]'])[0] \
#         / datalake.datastreams['CAPS_data'].return_data(
#         keys=['b_ext_dry_CAPS_450nm[1/Mm]'])[0]

#     babs_wet = datalake.datastreams['CAPS_data'].return_data(
#         keys=['b_ext_wet_CAPS_450nm[1/Mm]'])[0] \
#         - datalake.datastreams['CAPS_data'].return_data(
#         keys=['b_sca_wet_CAPS_450nm[1/Mm]'])[0]
#     babs_dry = datalake.datastreams['CAPS_data'].return_data(
#         keys=['b_ext_dry_CAPS_450nm[1/Mm]'])[0] \
#         - datalake.datastreams['CAPS_data'].return_data(
#         keys=['b_sca_dry_CAPS_450nm[1/Mm]'])[0]
#     babs_wet = datalake.datastreams['CAPS_data'].return_data(
#         keys=['b_ext_wet_CAPS_450nm[1/Mm]'])[0] \
#         - datalake.datastreams['CAPS_data'].return_data(
#         keys=['b_sca_wet_CAPS_450nm[1/Mm]'])[0]
#     babs_dry = datalake.datastreams['CAPS_data'].return_data(
#         keys=['b_ext_dry_CAPS_450nm[1/Mm]'])[0] \
#         - datalake.datastreams['CAPS_data'].return_data(
#         keys=['b_sca_dry_CAPS_450nm[1/Mm]'])[0]

#     time = datalake.datastreams['CAPS_data'].return_time(datetime64=False)
#     time = datalake.datastreams['CAPS_data'].return_time(datetime64=False)

#     datalake.datastreams['CAPS_data'].add_processed_data(
#         data_new=ssa_wet,
#         time_new=time,
#         header_new=['SSA_wet_CAPS_450nm[1/Mm]'],
#     )
#     datalake.datastreams['CAPS_data'].add_processed_data(
#         data_new=ssa_dry,
#         time_new=time,
#         header_new=['SSA_dry_CAPS_450nm[1/Mm]'],
#     )
#     datalake.datastreams['CAPS_data'].add_processed_data(
#         data_new=babs_wet,
#         time_new=time,
#         header_new=['b_abs_wet_CAPS_450nm[1/Mm]'],
#     )
#     datalake.datastreams['CAPS_data'].add_processed_data(
#         data_new=babs_dry,
#         time_new=time,
#         header_new=['b_abs_dry_CAPS_450nm[1/Mm]'],
#     )
#     return datalake
