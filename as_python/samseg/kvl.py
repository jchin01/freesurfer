import math

import GEMS2Python
import numpy as np


def transform_product(a, b):
    aa = a.as_numpy_array
    bb = b.as_numpy_array
    ab = np.dot(aa, bb)
    ab_f = np.asfortranarray(ab)
    return GEMS2Python.KvlTransform(ab_f)


def voxel_spacing_of_transform(t):
    m = t.as_numpy_array
    mm = m[0:3, 0:3]
    mm2 = mm * mm
    ss = mm2.sum()
    return math.sqrt(ss)


def calculate_down_sampling_factors(transform, target_voxel_spacing):
    # % Figure out how much to downsample (depends on voxel size)
    # voxelSpacing = sum( imageToWorldTransformMatrix( 1 : 3, 1 : 3 ).^2 ).^( 1/2 );
    # downSamplingFactors = max( round( targetDownsampledVoxelSpacing ./ voxelSpacing ), [ 1 1 1 ] )
    voxel_spacing = voxel_spacing_of_transform(transform)
    tentative_spacing = round(target_voxel_spacing / voxel_spacing)
    limited_spacing = max(1, tentative_spacing)
    return [limited_spacing, limited_spacing, limited_spacing]


def create_transform_from_2d_list(list_2d):
    return GEMS2Python.KvlTransform(np.array(list_2d, dtype=np.double, order='F'))


def create_translation_transform(offsets):
    return create_transform_from_2d_list([
        [1, 0, 0, offsets[0]],
        [0, 1, 0, offsets[1]],
        [0, 0, 1, offsets[2]],
        [0, 0, 0, 1],
    ])
