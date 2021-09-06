from fury import actor, material, window
from fury.io import load_image
from fury.optpkg import optional_package
from scipy.spatial import Delaunay
from tempfile import TemporaryDirectory


import math
import numpy as np
import numpy.testing as npt
import os
import random
import pytest


dipy, have_dipy, _ = optional_package('dipy')
VTK_9_PLUS = window.vtk.vtkVersion.GetVTKMajorVersion() >= 9


@pytest.mark.skipif(VTK_9_PLUS, reason="Requires VTK < 9.0.0")
def test_manifest_pbr_vtk_less_than_9():
    center = np.array([[0, 0, 0]])

    # Test non-supported material
    test_actor = actor.square(center, directions=(1, 1, 1), colors=(0, 0, 1))
    npt.assert_warns(UserWarning, material.manifest_pbr, test_actor)


@pytest.mark.skipif(not VTK_9_PLUS, reason="Requires VTK >= 9.0.0")
def test_manifest_pbr_vtk_great_than_9():
    scene = window.Scene()  # Setup scene

    # Contour from roi setup
    data = np.zeros((50, 50, 50))
    data[20:30, 25, 25] = 1.
    data[25, 20:30, 25] = 1.
    affine = np.eye(4)
    surface = actor.contour_from_roi(data, affine, color=np.array([1, 0, 1]))
    material.manifest_pbr(surface)
    scene.add(surface)
    scene.reset_camera()
    scene.reset_clipping_range()
    arr = window.snapshot(scene)
    report = window.analyze_snapshot(arr)
    npt.assert_equal(report.objects, 1)

    scene.clear()  # Reset scene

    # Sphere setup
    xyzr = np.array([[0, 0, 0, 10], [100, 0, 0, 25], [200, 0, 0, 50]])
    colors = np.array([[1, 0, 0, 0.3], [0, 1, 0, 0.4], [0, 0, 1., 0.99]])
    opacity = 0.5
    sphere_actor = actor.sphere(centers=xyzr[:, :3], colors=colors[:],
                                radii=xyzr[:, 3], opacity=opacity)
    material.manifest_pbr(sphere_actor)
    scene.add(sphere_actor)
    scene.reset_camera()
    scene.reset_clipping_range()
    arr = window.snapshot(scene)
    report = window.analyze_snapshot(arr)
    npt.assert_equal(report.objects, 3)

    scene.clear()  # Reset scene

    # Basic geometry actors (Box, cube, frustum, octagonalprism, rectangle,
    # square)
    centers = np.array([[4, 0, 0], [0, 4, 0], [0, 0, 0]])
    colors = np.array([[1, 0, 0, 0.4], [0, 1, 0, 0.8], [0, 0, 1, 0.5]])
    directions = np.array([[1, 1, 0]])
    scale_list = [1, 2, (1, 1, 1), [3, 2, 1], np.array([1, 2, 3]),
                  np.array([[1, 2, 3], [1, 3, 2], [3, 1, 2]])]
    actor_list = [[actor.box, {}], [actor.cube, {}], [actor.frustum, {}],
                  [actor.octagonalprism, {}], [actor.rectangle, {}],
                  [actor.square, {}]]
    for act_func, extra_args in actor_list:
        for scale in scale_list:
            scene = window.Scene()
            bga_actor = act_func(centers=centers, directions=directions,
                                 colors=colors, scales=scale, **extra_args)
            material.manifest_pbr(bga_actor)
            scene.add(bga_actor)
            arr = window.snapshot(scene)
            report = window.analyze_snapshot(arr)
            msg = 'Failed with {}, scale={}'.format(act_func.__name__, scale)
            npt.assert_equal(report.objects, 3, err_msg=msg)
            scene.clear()

    #window.show(scene)

    # NOTE: For these last set of actors, there is not support for PBR
    # interpolation at all.

    """
    # Setup slicer
    data = (255 * np.random.rand(50, 50, 50))
    affine = np.eye(4)
    slicer = actor.slicer(data, affine, value_range=[data.min(), data.max()])
    slicer.display(None, None, 25)
    material.manifest_pbr(slicer)
    scene.add(slicer)
    """

    """
    # Contour from label setup
    data = np.zeros((50, 50, 50))
    data[5:15, 1:10, 25] = 1.
    data[25:35, 1:10, 25] = 2.
    data[40:49, 1:10, 25] = 3.
    color = np.array([[255, 0, 0, 0.6],
                      [0, 255, 0, 0.5],
                      [0, 0, 255, 1.0]])
    surface = actor.contour_from_label(data, color=color)
    material.manifest_pbr(surface)
    scene.add(surface)
    """

    """
    # Scalar bar setup
    lut = actor.colormap_lookup_table(
        scale_range=(0., 100.), hue_range=(0., 0.1), saturation_range=(1, 1),
        value_range=(1., 1))
    sb_actor = actor.scalar_bar(lut, ' ')
    material.manifest_pbr(sb_actor)
    scene.add(sb_actor)
    """

    """
    # Billboard setup
    centers = np.array([[0, 0, 0], [5, -5, 5], [-7, 7, -7], [10, 10, 10],
                        [10.5, 11.5, 11.5], [12, -12, -12], [-17, 17, 17],
                        [-22, -22, 22]])
    colors = np.array([[1, 1, 0], [0, 0, 0], [1, 0, 1], [0, 0, 1], [1, 1, 1],
                       [1, 0, 0], [0, 1, 0], [0, 1, 1]])
    scales = [6, .4, 1.2, 1, .2, .7, 3, 2]
    """
    fake_sphere = \
        """
        float len = length(point);
        float radius = 1.;
        if(len > radius)
            discard;
        vec3 normalizedPoint = normalize(vec3(point.xy, sqrt(1. - len)));
        vec3 direction = normalize(vec3(1., 1., 1.));
        float df_1 = max(0, dot(direction, normalizedPoint));
        float sf_1 = pow(df_1, 24);
        fragOutput0 = vec4(max(df_1 * color, sf_1 * vec3(1)), 1);
        """
    """
    billboard_actor = actor.billboard(centers, colors=colors, scales=scales,
                                      fs_impl=fake_sphere)
    material.manifest_pbr(billboard_actor)
    scene.add(billboard_actor)
    """

    """
    # Text3D setup
    msg = 'I \nlove\n FURY'
    txt_actor = actor.text_3d(msg)
    material.manifest_pbr(txt_actor)
    scene.add(txt_actor)
    """

    """
    # Figure setup
    arr = (255 * np.ones((512, 212, 4))).astype('uint8')
    arr[20:40, 20:40, 3] = 0
    tp = actor.figure(arr)
    material.manifest_pbr(tp)
    scene.add(tp)
    """


def test_manifest_standard():
    # Test non-supported property
    data = np.zeros((50, 50, 50))
    data[5:15, 1:10, 25] = 1.
    data[25:35, 1:10, 25] = 2.
    data[40:49, 1:10, 25] = 3.
    color = np.array([[255, 0, 0], [0, 255, 0], [0, 0, 255]])
    test_actor = actor.contour_from_label(data, color=color)
    npt.assert_warns(UserWarning, material.manifest_standard, test_actor)

    center = np.array([[0, 0, 0]])

    # Test non-supported interpolation method
    test_actor = actor.square(center, directions=(1, 1, 1), colors=(0, 0, 1))
    npt.assert_warns(UserWarning, material.manifest_standard, test_actor,
                     interpolation='test')

    # Create tmp dir to save and query images
    with TemporaryDirectory() as out_dir:
        tmp_fname = os.path.join(out_dir, 'tmp_img.png')  # Tmp image to test

        scene = window.Scene()  # Setup scene

        test_actor = actor.box(center, directions=(1, 1, 1), colors=(0, 0, 1),
                               scales=1)
        scene.add(test_actor)

        # Test basic actor
        window.record(scene, out_path=tmp_fname, size=(200, 200),
                      reset_camera=True)
        npt.assert_equal(os.path.exists(tmp_fname), True)
        ss = load_image(tmp_fname)
        actual = ss[75, 100, :] / 1000
        desired = np.array([0, 0, 170]) / 1000
        npt.assert_array_almost_equal(actual, desired, decimal=2)
        actual = ss[125, 125, :] / 1000
        npt.assert_array_almost_equal(actual, desired, decimal=2)
        actual = ss[125, 75, :] / 1000
        desired = np.array([0, 0, 85]) / 1000
        npt.assert_array_almost_equal(actual, desired, decimal=2)

        # Test ambient level
        material.manifest_standard(test_actor, ambient_level=1)
        window.record(scene, out_path=tmp_fname, size=(200, 200),
                      reset_camera=True)
        npt.assert_equal(os.path.exists(tmp_fname), True)
        ss = load_image(tmp_fname)
        actual = ss[75, 100, :] / 1000
        desired = np.array([0, 0, 255]) / 1000
        npt.assert_array_almost_equal(actual, desired, decimal=2)
        actual = ss[125, 125, :] / 1000
        npt.assert_array_almost_equal(actual, desired, decimal=2)
        actual = ss[125, 75, :] / 1000
        npt.assert_array_almost_equal(actual, desired, decimal=2)

        # Test ambient color
        material.manifest_standard(test_actor, ambient_level=.5,
                                   ambient_color=(1, 0, 0))
        window.record(scene, out_path=tmp_fname, size=(200, 200),
                      reset_camera=True)
        npt.assert_equal(os.path.exists(tmp_fname), True)
        ss = load_image(tmp_fname)
        actual = ss[75, 100, :] / 1000
        npt.assert_array_almost_equal(actual, desired, decimal=2)
        actual = ss[125, 125, :] / 1000
        npt.assert_array_almost_equal(actual, desired, decimal=2)
        actual = ss[125, 75, :] / 1000
        desired = np.array([0, 0, 212]) / 1000
        npt.assert_array_almost_equal(actual, desired, decimal=2)

        # Test diffuse level
        material.manifest_standard(test_actor, diffuse_level=.75)
        window.record(scene, out_path=tmp_fname, size=(200, 200),
                      reset_camera=True)
        npt.assert_equal(os.path.exists(tmp_fname), True)
        ss = load_image(tmp_fname)
        actual = ss[75, 100, :] / 1000
        desired = np.array([0, 0, 127]) / 1000
        npt.assert_array_almost_equal(actual, desired, decimal=2)
        actual = ss[125, 125, :] / 1000
        desired = np.array([0, 0, 128]) / 1000
        npt.assert_array_almost_equal(actual, desired, decimal=2)
        actual = ss[125, 75, :] / 1000
        desired = np.array([0, 0, 64]) / 1000
        npt.assert_array_almost_equal(actual, desired, decimal=2)

        # Test diffuse color
        material.manifest_standard(test_actor, diffuse_level=.5,
                                   diffuse_color=(1, 0, 0))
        window.record(scene, out_path=tmp_fname, size=(200, 200),
                      reset_camera=True)
        npt.assert_equal(os.path.exists(tmp_fname), True)
        ss = load_image(tmp_fname)
        actual = ss[75, 100, :] / 1000
        desired = np.array([0, 0, 85]) / 1000
        npt.assert_array_almost_equal(actual, desired, decimal=2)
        actual = ss[125, 125, :] / 1000
        npt.assert_array_almost_equal(actual, desired, decimal=2)
        actual = ss[125, 75, :] / 1000
        desired = np.array([0, 0, 42]) / 1000
        npt.assert_array_almost_equal(actual, desired, decimal=2)

        # Test specular level
        material.manifest_standard(test_actor, specular_level=1)
        window.record(scene, out_path=tmp_fname, size=(200, 200),
                      reset_camera=True)
        npt.assert_equal(os.path.exists(tmp_fname), True)
        ss = load_image(tmp_fname)
        actual = ss[75, 100, :] / 1000
        desired = np.array([170, 170, 255]) / 1000
        npt.assert_array_almost_equal(actual, desired, decimal=2)
        actual = ss[125, 125, :] / 1000
        npt.assert_array_almost_equal(actual, desired, decimal=2)
        actual = ss[125, 75, :] / 1000
        desired = np.array([85, 85, 170]) / 1000
        npt.assert_array_almost_equal(actual, desired, decimal=2)

        # Test specular power
        material.manifest_standard(test_actor, specular_level=1,
                                   specular_power=5)
        window.record(scene, out_path=tmp_fname, size=(200, 200),
                      reset_camera=True)
        npt.assert_equal(os.path.exists(tmp_fname), True)
        ss = load_image(tmp_fname)
        actual = ss[75, 100, :] / 1000
        desired = np.array([34, 34, 204]) / 1000
        npt.assert_array_almost_equal(actual, desired, decimal=2)
        actual = ss[125, 125, :] / 1000
        npt.assert_array_almost_equal(actual, desired, decimal=2)
        actual = ss[125, 75, :] / 1000
        desired = np.array([1, 1, 86]) / 1000
        npt.assert_array_almost_equal(actual, desired, decimal=2)

        # Test specular color
        material.manifest_standard(test_actor, specular_level=1,
                                   specular_color=(1, 0, 0), specular_power=5)
        window.record(scene, out_path=tmp_fname, size=(200, 200),
                      reset_camera=True)
        npt.assert_equal(os.path.exists(tmp_fname), True)
        ss = load_image(tmp_fname)
        actual = ss[75, 100, :] / 1000
        desired = np.array([34, 0, 170]) / 1000
        npt.assert_array_almost_equal(actual, desired, decimal=2)
        actual = ss[125, 125, :] / 1000
        npt.assert_array_almost_equal(actual, desired, decimal=2)
        actual = ss[125, 75, :] / 1000
        desired = np.array([1, 0, 85]) / 1000
        npt.assert_array_almost_equal(actual, desired, decimal=2)

        scene.clear()  # Reset scene

        # Special case: Contour from roi
        data = np.zeros((50, 50, 50))
        data[20:30, 25, 25] = 1.
        data[25, 20:30, 25] = 1.
        test_actor = actor.contour_from_roi(data, color=np.array([1, 0, 1]))
        scene.add(test_actor)

        window.record(scene, out_path=tmp_fname, size=(200, 200),
                      reset_camera=True)
        npt.assert_equal(os.path.exists(tmp_fname), True)
        ss = load_image(tmp_fname)
        actual = ss[90, 110, :] / 1000
        desired = np.array([253, 0, 253]) / 1000
        npt.assert_array_almost_equal(actual, desired, decimal=2)
        actual = ss[90, 60, :] / 1000
        desired = np.array([180, 0, 180]) / 1000
        npt.assert_array_almost_equal(actual, desired, decimal=2)

        material.manifest_standard(test_actor)
        window.record(scene, out_path=tmp_fname, size=(200, 200),
                      reset_camera=True)
        npt.assert_equal(os.path.exists(tmp_fname), True)
        ss = load_image(tmp_fname)
        actual = ss[90, 110, :] / 1000
        desired = np.array([253, 253, 253]) / 1000
        npt.assert_array_almost_equal(actual, desired, decimal=2)
        actual = ss[90, 60, :] / 1000
        desired = np.array([180, 180, 180]) / 1000
        npt.assert_array_almost_equal(actual, desired, decimal=2)

        material.manifest_standard(test_actor, diffuse_color=(1, 0, 1))
        window.record(scene, out_path=tmp_fname, size=(200, 200),
                      reset_camera=True)
        npt.assert_equal(os.path.exists(tmp_fname), True)
        ss = load_image(tmp_fname)
        actual = ss[90, 110, :] / 1000
        desired = np.array([253, 0, 253]) / 1000
        npt.assert_array_almost_equal(actual, desired, decimal=2)
        actual = ss[90, 60, :] / 1000
        desired = np.array([180, 0, 180]) / 1000
        npt.assert_array_almost_equal(actual, desired, decimal=2)
