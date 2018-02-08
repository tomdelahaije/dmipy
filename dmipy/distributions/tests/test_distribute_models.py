from dmipy.signal_models import (
    cylinder_models, gaussian_models, sphere_models, plane_models)
from dmipy.distributions import distribute_models, distributions
from dmipy.data.saved_acquisition_schemes import wu_minn_hcp_acquisition_scheme
import numpy as np
from numpy.testing import assert_equal, assert_almost_equal


def test_all_models_dispersable():
    scheme = wu_minn_hcp_acquisition_scheme()

    dispersable_models = [
        cylinder_models.C1Stick,
        cylinder_models.C2CylinderSodermanApproximation,
        cylinder_models.C3CylinderCallaghanApproximation,
        cylinder_models.C4CylinderGaussianPhaseApproximation,
        gaussian_models.G2Zeppelin,
        gaussian_models.G3RestrictedZeppelin
    ]

    spherical_distributions = [
        distribute_models.SD1WatsonDistributed,
        distribute_models.SD2BinghamDistributed
    ]

    for model in dispersable_models:
        for distribution in spherical_distributions:
            mod = model()
            dist_mod = distribution([mod])
            params = {}
            for param, card in dist_mod.parameter_cardinality.items():
                params[param] = np.random.rand(
                    card) * dist_mod.parameter_scales[param]
            assert_equal(isinstance(
                dist_mod(scheme, **params), np.ndarray), True)


def test_gamma_pdf_unity():
    normalizations = ['standard', 'plane', 'cylinder', 'sphere']

    alpha = 1.
    beta = 3e-6

    for normalization in normalizations:
        gamma = distributions.DD1GammaDistribution(
            alpha=alpha, beta=beta, normalization=normalization)
        x, Px = gamma()
        assert_almost_equal(np.trapz(Px, x=x), 1.)


def test_all_models_distributable():
    scheme = wu_minn_hcp_acquisition_scheme()

    distributable_models = [
        plane_models.P3PlaneCallaghanApproximation,
        cylinder_models.C2CylinderSodermanApproximation,
        cylinder_models.C3CylinderCallaghanApproximation,
        cylinder_models.C4CylinderGaussianPhaseApproximation,
        sphere_models.S2SphereSodermanApproximation
    ]

    spatial_distributions = [
        distribute_models.DD1GammaDistributed
    ]

    for model in distributable_models:
        for distribution in spatial_distributions:
            mod = model()
            dist_mod = distribution([mod])
            params = {}
            for param, card in dist_mod.parameter_cardinality.items():
                params[param] = np.random.rand(
                    card) * dist_mod.parameter_scales[param]
            assert_equal(isinstance(
                dist_mod(scheme, **params), np.ndarray), True)