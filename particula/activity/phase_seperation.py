# linting disabled until reformatting of this file
# pylint: disable=all
# flake8: noqa
# pytype: skip-file

# %% 


import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({'text.color': "#333333",
                     'axes.labelcolor': "#333333",
                     "figure.figsize": (6,4),
                     "font.size": 14,
                     "axes.edgecolor": "#333333",
                     "axes.labelcolor": "#333333",
                     "xtick.color": "#333333",
                     "ytick.color": "#333333",
                     "pdf.fonttype": 42,
                     "ps.fonttype": 42})

# Gorkowski, K., Preston, T. C., &#38; Zuend, A. (2019).
# Relative-humidity-dependent organic aerosol thermodynamics
# via an efficient reduced-complexity model.
# Atmospheric Chemistry and Physics
# https://doi.org/10.5194/acp-19-13383-2019

# %%


def organic_water_single_phase(molar_mass_ratio):
    """
    Convert the given molar mass ratio (MW water / MW organic) to a
    and O2C value were above is a single phase with water and below
    phase separation is possible.

    Parameters:
    molar_mass_ratio np.: The molar mass ratio with respect to water.

    Returns:
    float: The single phase cross point.
    """

    o2c_single_phase_cross_point = 0.205 / (
        1 + np.exp(26.6 * (molar_mass_ratio - 0.12))
        )**0.843 + 0.225
    return o2c_single_phase_cross_point

# %% Plot Example curve


organic_molecular_weight = np.linspace(50, 500, 500)

o2c_value = organic_water_single_phase(18.01528 / organic_molecular_weight)

fig, ax = plt.subplots()
ax.plot(
    organic_molecular_weight,
    o2c_value,
    label="initial",
    linestyle='dashed'
    )
ax.set_xlabel("Organic molecular weight (g/mol)")
ax.set_ylabel("O:C ratio")
ax.set_title("Organic Phase separation")
ax.legend()
fig.show

# %% activity calc

# function [ln_func1, ln_func2, ycalc1, ycalc2, activity_calc1, activity_calc2, mass_fraction1, mass_fraction2, Gibbs_RT, dGibbs_RTdx2]=BAT_properties_calculation_v1(...
#     org_mole_fraction, O2C, H2C, molarmass_ratio, BAT_functional_group, special_options, N2C_values_denistyOnly)
import numpy as np

def exp_wlimiter(x):
    # Define the limiting function for the exponent here
    return np.exp(x)

def convert_to_OH_eqivelent(O2C, molarmass_ratio, BAT_functional_group):
    # Define this function
    return O2C, molarmass_ratio

def organic_density_estimate(M, O2C, H2C=None, N2C=None):
    """
    Function to estimate the density of organic compounds based on the simple
    model by Girolami (1994). The input parameters include molar mass, O:C
    and H:C ratios. If the H:C ratio is unknown at input, enter a negative
    value. The actual H:C will then be estimated based on an initial assumption
    of H:C = 2. The model also estimates the number of carbon atoms per
    molecular structure based on molar mass, O:C, and H:C.
    The density is then approximated by the formula of Girolami.

    Reference:
    Girolami, G. S.: A Simple 'Back of the Envelope' Method for Estimating
    the Densities and Molecular Volumes of Liquids and Solids,
    J. Chem. Educ., 71(11), 962, doi:10.1021/ed071p962, 1994.

    Parameters:
        M (float): Molar mass.
        O2C (float): O:C ratio.
        H2C (float): H:C ratio. If unknown, provide a negative value.
        N2C (float, optional): N:C ratio. Defaults to None.

    Returns:
        densityEst (float): Estimated density in g/cm^3.
    """
    if N2C is None:
        N2C = M * 0
    if H2C is None:
        H2C = M * 0

    mass_C = 12.01  # the molar masses in [g/mol]
    mass_O = 16.0
    mass_H = 1.008
    mass_N = 14.0067

    # 1) Estimate the H2C value if not provided from input
    if H2C < 0.1:
        # Estimate H2C assuming an aliphatic compound with H2C = 2 in the absence of oxygen functional groups,
        # then correct for oxygen content assuming a -1 slope (Van Krevelen Diagram of typical SOA).
        H2Cest = 2.0 - O2C
    else:
        H2Cest = H2C

    # 2) Compute the approximate number of carbon atoms per organic molecule
    NC = M / (mass_C + H2Cest * mass_H + O2C * mass_O + N2C * mass_N)

    # 3) Compute density estimate based on method by Girolami (1994)
    # Here no correction is applied for rings and aromatic compounds
    # (due to limited info at input)
    rho1 = M / (5.0 * NC * (2.0 + H2Cest + O2C * 2.0 + N2C * 2.0))
    density = rho1 * (1.0 + min(NC * O2C * 0.1 + NC * N2C * 0.1, 0.3))
    # density in [g/cm^3];
    # Here it is scaled assuming that most of the oxygen atoms are able to
    # make H-bonds (donor or acceptor).

    return density


def single_phase_O2C_point_KGv3(Mr):
    # Define this function
    return Onephase_O2C

def replace_data_A_to_B_KGv1(x2, A, B):
    return np.where(x2 == A, B, x2)

# %%

org_mole_fraction = np.linspace(0, 1, 100)
molarmass_ratio = 18.016/250
O2C = 0.2
H2C = 0
N2C = 0


O2C, molarmass_ratio = convert_to_OH_eqivelent(
        O2C,
        molarmass_ratio,
        BAT_functional_group=None
    )

# check the limits of possible mole fractions
org_mole_fraction = np.where(org_mole_fraction>1, 1, org_mole_fraction)
org_mole_fraction = np.where(org_mole_fraction<=0, 10**-20, org_mole_fraction)

density = organic_density_estimate(18.016/molarmass_ratio, O2C, H2C, N2C)


#%%

def bat_blending_weights(molarmass_ratio, O2C):
    """
    Function to estimate the blending weights for the BAT model.

    Parameters:
    -----------
    molarmass_ratio (float): Molar mass ratio of the organic compound.

    Returns:
    --------
    blending_weights (array): List of blending weights for the BAT model
        in the low, mid, and high O2C regions.
    """

    Onephase_O2C = organic_water_single_phase(molarmass_ratio)
    mid_transition = Onephase_O2C * 0.75

    blending_weights = np.zeros(3)  # [low, mid, high] O2C regions

    if O2C <= mid_transition:  # lower to mid O2C region
        tran_lowO2C_fractionOne_phase = 0.189974476118418
        tran_lowO2C_sigmoid_bend = 79.2606902175984
        tran_lowO2C_sigmoid_shift = 0.0604293454322489

        O2C_1phase_delta = O2C - Onephase_O2C * tran_lowO2C_fractionOne_phase
        weight_1phase = 1 / (1 + np.exp(
            -tran_lowO2C_sigmoid_bend
            *(O2C_1phase_delta - tran_lowO2C_sigmoid_shift)
        ))  # logistic transfer function

        O2C_1phase_delta_norm = O2C - (
                mid_transition * tran_lowO2C_fractionOne_phase
            )
        weight_1phase_norm = 1 / (1 + np.exp(
            -tran_lowO2C_sigmoid_bend
            *(O2C_1phase_delta_norm - tran_lowO2C_sigmoid_shift)
        ))

        blending_weights[1] = weight_1phase / weight_1phase_norm
        blending_weights[0] = 1 - weight_1phase

    elif O2C <= Onephase_O2C * 2:  # mid to high O2C region
        tran_midO2C_sigmoid_bend = 75.0159268221068
        tran_midO2C_sigmoid_shift = 0.000947111285750515

        O2C_1phase_delta = O2C - Onephase_O2C
        blending_weights[1] = 1 / (1 + np.exp(
            -tran_midO2C_sigmoid_bend
            *(O2C_1phase_delta - tran_midO2C_sigmoid_shift)
        ))  # logistic transfer function

        blending_weights[2] = 1 - blending_weights[1]

    else:  # high only region
        blending_weights[2] = 1

    return blending_weights

#%%

O2C_array = np.linspace(0, 0.6, 100)
weights_matrix = np.zeros((100, 3))

for index, O2C in enumerate(O2C_array):
    weights_matrix[index, :] = bat_blending_weights(molarmass_ratio, O2C)

fig, ax = plt.subplots()
ax.plot(
    O2C_array,
    weights_matrix,
    )

ax.set_xlabel("O:C")
ax.set_ylabel("weights")
ax.legend()
fig.show


#%%
FIT_lowO2C = {'a1':[7.089476E+00, -7.711860E+00, -3.885941E+01, -1.000000E+02],
              'a2':[-6.226781E-01, -1.000000E+02, 3.081244E-09, 6.188812E+01],
              's':[-5.988895E+00, 6.940689E+00]}
FIT_midO2C = {'a1':[5.872214E+00, -4.535007E+00, -5.129327E+00, -2.809232E+01],
              'a2':[-9.740486E-01, -1.000000E+02, 2.109751E+00, -2.367683E+01,],
              's':[-1.219164E+00, 4.742729E+00]}
FIT_highO2C = {'a1':[5.921550E+00, -2.528295E+00, -3.883017E+00, -7.898128E+00,],
               'a2':[-1.000000E+02, -1.000000E+02, 1.353916E+00, -1.160145E+01,],
               's':[-7.868187E-02, 3.650860E+00]}

def coefficents_c(
        molarmass_ratio,
        fit_values
    ):

    """
    Coefficents for activity model, see Gorkowski (2019). equation S1 S2.

    Paramters:
    ---------
        molar mass ratio (float): water MW / orgniac MW
        fit_values (list): a_n1, a_n2, a_n3, a_n4
    """
    c = (fit_values[0] * np.exp(fit_values[1] * O2C)
        + fit_values[2] * np.exp(fit_values[3] * molarmass_ratio))
    return c


# %%

def gibbs_of_mixing(
        molarmass_ratio,
        org_mole_fraction,
        O2C,
        density,
        fit_dict
    ):
    """
    Gibbs free energy of mixing, see Gorkowski (2019). equation S4.

    Paramters:
    ---------
        molar mass ratio (float): water MW / orgniac MW
        org mole fraction (float): fraction of organic matter
        O2C (float): oxygen to carbon ratio
        density (float): density of mixture
        fit_coefficent (dict): dictionary of fit values for low O2C region
    """
    c1 = coefficents_c(molarmass_ratio, fit_dict['a1'])
    c2 = coefficents_c(molarmass_ratio, fit_dict['a2'])

    rhor = 0.997 / density  # assumes water is the other fluid

    # equation S3
    scaledMr = molarmass_ratio * fit_dict['s'][1] * (1.0 + O2C) ** fit_dict['s'][0]  # scaledMr is the scaled molar mass ratio of this mixture's components.
    phi2 = org_mole_fraction / (org_mole_fraction + (1.0 - org_mole_fraction) * scaledMr / rhor)  # phi2 is a scaled volume fraction

    # equation S4
    sum1 = c1 + c2*(1-2*phi2)
    gibbs_mix = phi2 * (1.0 - phi2) * sum1

    # equation s6 the derivative of phi2 with respect to orgnaic x2
    dphi2dx2 = (scaledMr / rhor) * (phi2 / org_mole_fraction) ** 2

    # equation S7
    dervative_gibbs_mix = (
        (1.0 - 2.0 * phi2) * sum1 - 2*c2*phi2 * (1.0 - phi2)
        ) * dphi2dx2

    return gibbs_mix, dervative_gibbs_mix

gibbs_mix, dervative_gibbs = gibbs_of_mixing(
    molarmass_ratio,
    org_mole_fraction,
    O2C,
    density,
    FIT_lowO2C
)


# %%

def gibbs_mix_weight(
        molarmass_ratio,
        org_mole_fraction,
        O2C,
        density,
        BAT_functional_group=None,
    ):
    """
    Gibbs free energy of mixing, see Gorkowski (2019), with weighted
    O2C regions

    Paramters:
    ---------
        molar mass ratio (float): water MW / orgniac MW
        org mole fraction (float): fraction of organic matter
        O2C (float): oxygen to carbon ratio
        density (float): density of mixture
        fit_coefficent (dict): dictionary of fit values for low O2C region

    Returns:
    -------
        gibbs_mix (float): Gibbs energy of mixing (including 1/RT)
        dervative_gibbs (float): dervative of Gibbs energy with respect to 
        mole fraction of orgnaics (includes 1/RT)
    """
    O2C, molarmass_ratio = convert_to_OH_eqivelent(
        O2C,
        molarmass_ratio,
        BAT_functional_group=None
    )

    weights = bat_blending_weights(molarmass_ratio, O2C)

    if weights[1]>0:  # if mid region is used
        gibbs_mix_mid, dervative_gibbs_mid = gibbs_of_mixing(
            molarmass_ratio,
            org_mole_fraction,
            O2C,
            density,
            FIT_midO2C
        )

        if weights[0]>0: # if paired with low O2C region
            gibbs_mix_low, dervative_gibbs_low = gibbs_of_mixing(
                molarmass_ratio,
                org_mole_fraction,
                O2C,
                density,
                FIT_lowO2C
            )
            gibbs_mix = weights[0]*gibbs_mix_low + weights[1]*gibbs_mix_mid
            dervative_gibbs = weights[0]*dervative_gibbs_low \
            + weights[1]*dervative_gibbs_mid
        
        else:  #else paired with high O2C region
            gibbs_mix_high, dervative_gibbs_high = gibbs_of_mixing(
                molarmass_ratio,
                org_mole_fraction,
                O2C,
                density,
                FIT_highO2C
            )
            gibbs_mix = weights[2]*gibbs_mix_high + weights[1]*gibbs_mix_mid
            dervative_gibbs = weights[2]*dervative_gibbs_high \
                + weights[1]*dervative_gibbs_mid
    else:  # when only high 2OC region is used
        gibbs_mix, dervative_gibbs = gibbs_of_mixing(
            molarmass_ratio,
            org_mole_fraction,
            O2C,
            density,
            FIT_highO2C
        )
    return gibbs_mix, dervative_gibbs


# %%
O2C=0.225
molarmass_ratio = 18.016/100
density = organic_density_estimate(18.016/molarmass_ratio, O2C)

gibbs_mix, dervative_gibbs= gibbs_mix_weight(
        molarmass_ratio,
        org_mole_fraction,
        O2C,
        density,
    )

# equations S8 S10
ln_gamma_water = gibbs_mix - org_mole_fraction * dervative_gibbs  # the func value for component 1 = LOG(activity coeff. water)
ln_gamma_org = gibbs_mix + (1.0 - org_mole_fraction) * dervative_gibbs  # the func value of the component 2 = LOG(activity coeff. of the organic)

gamma_water = np.exp(np.where(ln_gamma_water>690, 690, ln_gamma_water))
gamma_org = np.exp(np.where(ln_gamma_org>690, 690, ln_gamma_org))

activity_water = gamma_org * (1.0 - org_mole_fraction)
activity_organic = gamma_water * org_mole_fraction

mass_water = (1.0 - org_mole_fraction) * molarmass_ratio / (
        (1.0 - org_mole_fraction) * (molarmass_ratio - 1) + 1
    )
mass_organic = 1 - mass_water

gibbs_ideal = (1-org_mole_fraction) * np.log(1-org_mole_fraction) \
    +org_mole_fraction * np.log(org_mole_fraction)
gibbs_real = gibbs_ideal + gibbs_mix

fig, ax = plt.subplots()
ax.plot(
    1-org_mole_fraction,
    gibbs_real,
    label="gibbs",
    linestyle='dashed'
    )
# ax.plot(
#     1-org_mole_fraction,
#     activity_water,
#     label="water",
#     linestyle='dashed'
#     )

# ax.plot(
#     1-org_mole_fraction,
#     activity_organic,
#     label="organic",
#     )
# ax.set_ylim((0,2))
ax.set_xlabel("water mole fraction")
ax.set_ylabel("activity")
ax.legend()
fig.show


#%%

# gemix=gemix(:,1).*weight_1phase+gemix(:,2).*weight_2phase;
# dgemix2dx=dgemix2dx(:,1).*weight_1phase+dgemix2dx(:,2).*weight_2phase;


# %calculate the function value funcx1 (= y1(x2)) at point with w2:
# ln_func1 = gemix -x2.*dgemix2dx; %the func value for component 1 = LOG(activity coeff. water)
# ln_func2 = gemix +(1.0D0-x2).*dgemix2dx; %the func value of the component 2 = LOG(activity coeff. of the organic)


# ycalc1 = exp_wlimiter(ln_func1); % exp with limiter for numerical overflow
# ycalc2 = exp_wlimiter(ln_func2);

# activity_calc1=ycalc1.*(1.0D0-x2);
# activity_calc2=ycalc2.*(x2);

# mass_fraction1=(1.0D0-x2).*Mr_massfrac_final./((1.0D0-x2).*(Mr_massfrac_final-1)+1);
# mass_fraction2=1-mass_fraction1;
# Gibbs_RT=gemix;
# dGibbs_RTdx2=dgemix2dx;






# %%

def q_alpha_transfer_vs_aw_calc_v1(a_w_sep, aw_series, VBSBAT_options):
    """
    This function makes a squeezed logistic function to transfer for q_alpha ~0 to q_alpha ~1, 
    described in VBSBAT_options.q_alpha.

    Parameters:
    a_w_sep (np.array): A numpy array of values.
    aw_series (np.array): A numpy array of values.
    VBSBAT_options (dict): A dictionary of options.

    Returns:
    np.array: The q_alpha value.
    """
    
    mask_of_miscible_points = a_w_sep == 0  # values held for correction at the end

    # spread in transfer from 50/50 point
    delta_a_w_sep = 1 - a_w_sep

    # check min value allowed
    above_min_delta_a_w_sep_value = delta_a_w_sep > VBSBAT_options['q_alpha']['min_spread_in_aw']
    delta_a_w_sep = delta_a_w_sep * above_min_delta_a_w_sep_value + \
        ~above_min_delta_a_w_sep_value * VBSBAT_options['q_alpha']['min_spread_in_aw']

    # calculate curve parameter of sigmoid
    sigmoid_curve_parameter = ln_zeropass(1. / (1 - VBSBAT_options['q_alpha']['q_alpha_at_1phase_aw']) - 1) / delta_a_w_sep

    # calculate q_alpha value
    q_alpha_value = 1 - 1. / (1 + exp_wlimiter(sigmoid_curve_parameter * (aw_series - a_w_sep + delta_a_w_sep)))

    # apply mask for complete miscibility, turns miscible organics to q_alpha=1 for all a_w
    q_alpha_value = q_alpha_value * ~mask_of_miscible_points + mask_of_miscible_points

    return q_alpha_value



def finds_phase_sep_w_and_org(activity_water, activity_org):
    """
    This function checks for phase separation in each activity curve.

    Parameters:
    activity_water (np.array): A numpy array of water activity values.
    activity_org (np.array): A numpy array of organic activity values.

    Returns:
    tuple: The phase separation check, lower a_w separation index, upper a_w separation index, matching upper a_w separation index.
    """

    # check for phase separation in each activity curve
    _, phase_sep_via_activity_curvature_w, index_phase_sep_starts_w, index_phase_sep_end_w = \
        finds_phase_sep_and_activity_curve_dips_v2(activity_water)
    _, phase_sep_via_activity_curvature_org, index_phase_sep_starts_org, index_phase_sep_end_org = \
        finds_phase_sep_and_activity_curve_dips_v2(activity_org)

    indexes = [index_phase_sep_starts_w, index_phase_sep_end_w, index_phase_sep_starts_org, index_phase_sep_end_org]

    if phase_sep_via_activity_curvature_w == 1:
        phase_sep_check = 1
        if activity_water[0] < activity_water[-1]:  # increasing a_w with index
            lower_a_w_sep_index = min(indexes)
            upper_a_w_sep_index = max(indexes)

            mid_sep_index = (lower_a_w_sep_index + upper_a_w_sep_index) // 2
            activity_water_beta = activity_water[:mid_sep_index]
            match_a_w = activity_water[upper_a_w_sep_index]
            match_index_prime = np.where((activity_water_beta - match_a_w) > 0)

            if len(match_index_prime[0]) == 0:
                match_index_prime = np.argmax(activity_water_beta - match_a_w)
            matching_Upper_a_w_sep_index = match_index_prime[0][0] - 1

        else:
            lower_a_w_sep_index = max(indexes)  # decreasing a_w with index
            upper_a_w_sep_index = min(indexes)

            mid_sep_index = (lower_a_w_sep_index + upper_a_w_sep_index) // 2
            activity_water_beta = activity_water[mid_sep_index:]
            match_a_w = activity_water[upper_a_w_sep_index]
            match_index_prime = np.where(activity_water_beta <= match_a_w)
            matching_Upper_a_w_sep_index = mid_sep_index + match_index_prime[0][0] - 1

    else:
        lower_a_w_sep_index = 1  # no phase sep
        upper_a_w_sep_index = 2
        matching_Upper_a_w_sep_index = 2
        phase_sep_check = 0  # no phase sep

    return phase_sep_check, lower_a_w_sep_index, upper_a_w_sep_index, matching_Upper_a_w_sep_index


def finds_phase_sep_and_activity_curve_dips_v2(activity_data):
    """
    This function finds phase separation and activity curve dips.

    Parameters:
    activity_data (np.array): A numpy array of activity data.

    Returns:
    tuple: The phase separation via activity, phase separation via activity curvature, index phase separation starts, index phase separation end.
    """

    activity_diff = np.diff(activity_data)
    L_m = len(activity_data)

    if L_m > 3:
        min_value = np.min(activity_diff)
        max_value = np.max(activity_diff)
        mean_sign = np.sign(np.mean(activity_diff))

        if np.sign(min_value) == np.sign(max_value):
            phase_sep_via_activity_curvature = 0
            index_phase_sep_starts = np.nan
            index_phase_sep_end = np.nan

        elif np.sign(min_value) != np.sign(max_value):
            phase_sep_via_activity_curvature = 1

            activity_calc1_diff_sign_change = np.sign(np.concatenate(([activity_diff[0]], activity_diff))) != np.sign(activity_diff[0])

            index_start = np.where(activity_calc1_diff_sign_change)[0][0]
            back_index = index_start - 1 + np.where(~activity_calc1_diff_sign_change[index_start:])[0][0]

            if back_index < L_m:
                activity_data_gap = np.argmin(np.abs(activity_data[back_index:] - activity_data[index_start]))
                restart_match_index = activity_data_gap + back_index - 1
            else:
                restart_match_index = L_m

            if sum(activity_data > 1):
                min_value_Idilute = np.min(activity_data[index_start:])
                min_index_Idilute = np.argmin(activity_data[index_start:]) + index_start - 1
                activity_data_gap_start = np.argmin(np.abs(activity_data[:index_start] - activity_data[min_index_Idilute]))

                if activity_data_gap_start < index_start:
                    index_phase_sep_starts = activity_data_gap_start
                else:
                    index_phase_sep_starts = index_start

                if min_index_Idilute < restart_match_index:
                    index_phase_sep_end = min_index_Idilute
                else:
                    index_phase_sep_end = restart_match_index

            else:
                index_phase_sep_starts = index_start
                index_phase_sep_end = restart_match_index

    else:
        phase_sep_via_activity = activity_data
        phase_sep_via_activity_curvature = 0
        index_phase_sep_starts = np.nan
        index_phase_sep_end = np.nan

    if sum(activity_data > 1):
        phase_sep_via_activity = 1
    else:
        phase_sep_via_activity = 0

    return phase_sep_via_activity, phase_sep_via_activity_curvature, index_phase_sep_starts, index_phase_sep_end


def check_bat_functional_group_inputs_v1(O2C, shift_method):
    """
    This function checks the inputs of the BAT functional group.

    Parameters:
    O2C (np.array): A numpy array representing O2C values.
    shift_method (str/list): A string or list representing the shift method.

    Returns:
    list: The shift method with size equal to O2C.
    """

    max_dim = max(len(O2C), len(shift_method))
    
    if isinstance(shift_method, str):
        shift_method = [shift_method for _ in range(max_dim)]
    elif isinstance(shift_method, list):
        if len(shift_method) == 1:
            shift_method = [shift_method[0] for _ in range(max_dim)]
        elif len(shift_method) < max_dim:
            raise ValueError(f"shift_method has less points than O2C: {len(shift_method)} vs {max_dim}")
            
    return shift_method


def biphasic_to_single_phase_RH_master_v4(O2C, H2C, Mratio, BAT_functional_group):
    """
    This function computes the biphasic to single phase RH.

    Parameters:
    O2C (np.array): An array representing O2C values.
    H2C (np.array): An array representing H2C values.
    Mratio (np.array): An array representing molar mass ratio values.
    BAT_functional_group (str/list): The BAT functional group(s).

    Returns:
    np.array: The RH cross point array.
    """

    RH_cross_point = np.zeros_like(O2C)

    interpolate_step_numb = 500  # interpolation points
    mole_frac = np.linspace(0, 1, interpolate_step_numb + 1)

    for i in range(len(O2C)):  # loops through one compound at a time
        func1, func2, ycal_water, ycalc_org, activity_water, activity_org, mass_fraction1, mass_fraction2, Gibbs_RT, dGibbs_RTdx2 \
            = bat_properties_calculation_v1(mole_frac, O2C[i], H2C[i], Mratio[i], BAT_functional_group[i], [])

        if np.isnan(activity_water):
            raise ValueError('water activity is NaN, check inputs')

        phase_sep_check, _, upper_a_w_sep_index, _ = finds_phase_sep_w_and_org(activity_water, activity_org)  # finds a_w sep. point

        if phase_sep_check == 1:  # checks if there is phase separation.
            RH_cross_point[i] = activity_water[upper_a_w_sep_index]  # save phase sep RH
        else:
            RH_cross_point[i] = 0  # no phase separation

    # Checks outputs with in physical limits 
    #round to zero
    RH_cross_point[RH_cross_point < 0] = 0
    # round max to 1
    RH_cross_point[RH_cross_point > 1] = 1

    return RH_cross_point


def mapminmax_apply(x, settings):
    return (x - settings['xoffset']) * settings['gain'] + settings['ymin']

def tansig_apply(n):
    return 2 / (1 + np.exp(-2*n)) - 1

def mapminmax_reverse(y, settings):
    return (y - settings['ymin']) / settings['gain'] + settings['xoffset']

def biphasic_to_single_phase_molfrac_org_NN_v5(x1):
    # Neural Network Constants

    # Input 1
    x1_step1 = {'xoffset': np.array([0, 0.03]), 
                'gain': np.array([4.85105461413554, 6.06060606060606]), 
                'ymin': -1}

    # Layer 1
    b1 = np.array([5.8514275487869635839, 5.7010903702309043695, -4.223155231828595646, 3.8774900021515046333, -1.325265064433274409, 1.7576973644493769644,
    -0.88991761674608715893, 3.1279829884292338349, 0.78794652837451617522, 0.43896968097298133538, 0.57708117017809135163, -3.0787608017900915947,
    -0.40581098864752368494, 0.64373309554603275195, 1.7016326841051676588, 1.4946559455903600799, -1.9151891347855638514, -0.36222536287456474913,
    1.7997779117047685293, 2.1894391519933469326, -4.8365290076330538227, -4.2267640672562194482, 11.037306029484762249, -12.465284279233749487])
    IW1_1 = np.array([
        [-2.9652369062270196309, 3.5456936036245476629],
        [-5.3003896191163066831, 1.6107048934053527223],
        [1.4490960942847532777, -4.4905963483778252865],
        [-5.3604492963083165691, -1.9038162660993562803],
        [3.5615591287827941258, -0.9760690759109916792],
        [-7.4323704665484466858, 3.9952918221278448385],
        [5.2436980487815443297, 0.26336330948747371794],
        [-9.7224092904321945952, -3.3963153832437282809],
        [-6.5939564893121698219, -0.86743278765059372848],
        [-3.9566478027540843421, 6.2043545317513464354],
        [-2.6933489710522580118, -5.3296776285599456457],
        [15.078615754750318345, 7.5357195857930081573],
        [8.5837138409899615965, 2.1781365767882316931],
        [4.2753681534309269097, -1.2376866082237749644],
        [-4.3694881192877721432, -4.1504032312908245572],
        [-5.1076333577305517153, -4.2573773952093914019],
        [3.9331831538436010653, 4.2383815452477779928],
        [-3.3051366335726815038, -2.1527745655619221488],
        [5.5102707313508449971, 0.6090289580711970574],
        [4.0590106228932549826, -1.4537733443192657479],
        [1.1330332610381823599, 7.987215295423046868],
        [-1.4690914445681406697, 3.46783846307828858],
        [1.7834488065629925391, 8.9409991055225059853],
        [-2.3985373019045113097, -10.018658523996098353]
    ])

    # Layer 2
    b2 = -0.23364831139900205104
    LW2_1 = np.array([0.61668049433913207924, -0.3593912575055407399, -0.3266392699738256411, -1.6045946666158248384, -1.1739361061623092564, 0.087334561642434180295,
    2.9371817317733741604, -0.38368295323950185605, 2.3343874738168426397, 0.031130301801809163315, -0.055017015768111438012, -0.2379118380584248349,
    0.51580586145584794711, -0.35767521938020213623, -7.6921394249634440499, 3.3355022461024885772, -4.3095896749403888037, 0.29571381132244778378,
    0.30910107924737867391, -0.25489989065848722705, 0.080905914998754310807, -0.17070806216025710689, 4.7037417262526615147, 3.0438085224819206864])

    # Output 1
    y1_step1 = {'ymin': -1, 'gain': 2.02204023860075, 'xoffset': 0.0109}

    # Simulation
    Q = x1.shape[1] # samples
    xp1 = mapminmax_apply(x1, x1_step1)
    a1 = tansig_apply(b1.reshape(-1, 1) + np.dot(IW1_1, xp1))
    a2 = b2 + np.dot(LW2_1, a1)
    y1 = mapminmax_reverse(a2, y1_step1)

    return y1

# %%
