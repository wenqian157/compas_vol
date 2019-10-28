import numpy as np
import sys, os
import random

import compas_vol
from compas_vol.primitives import *
from compas_vol.combinations import *
from compas_vol.modifications import *
from compas_vol.microstructures import *

from skimage.measure import marching_cubes_lewiner

from compas.datastructures import Mesh
from compas.geometry import Box, Frame, Point, Plane, Cylinder, Circle, Sphere, Torus

from compas_vol.pandaRenderer.pandaRenderer import PandaRenderer
from compas_vol.raymarching.rayMarchingFactory import RayMarchingFactory
from compas_vol.raymarching.translator import Translator

from compas_vol.raymarching.remapping_functions import remap


## window size
from panda3d.core import loadPrcFileData     
loadPrcFileData('', """ # win-size 1900 200
                          window-title Raymarching example 
                          sync-video 0 """) 

main_path = os.path.abspath(os.path.dirname(__file__))

sqrt2 = 1.41421

if __name__ == "__main__":
    ## --------------------------- Geometry
    # torus = VolTorus(Torus(Plane((3, 3, 3), (1., 0., 1.)), 2.0, 1.0))
    # boxb = VolBox(Box(Frame(Point(0., 0., 0.), [3., 3.5, 0.1], [2.5, 1., 2.1]), 10, 8, 9), 1)

    ## box
    box_dim_w = 3.5
    box_dim_h = 12.
    box = VolBox(Box(Frame(Point(0., 0., 0.), [1, 0, 0], [0, 1., 0]), box_dim_w, box_dim_w, box_dim_h), 0.3)
    b = box_dim_w/2
    box_corners = [[b , -b], [-b, -b], [-b, b], [b, b]]

    spheres_list = []

    height_num = 4
    for i in range(height_num): #height
        for corner in box_corners: # corner
            height = i * box_dim_h/(height_num-1) - box_dim_h/2
            radius = 1.2 + i * 0.25
            sphere = VolSphere(Sphere(Point(corner[0], corner[1], height),  radius ))
            spheres_list.append(sphere)

        if i < height_num -1:
            radius = 1.65 - i * 0.25
            height_center_sphere = height + 0.45 * box_dim_h/(height_num-1)
            center_sphere = VolSphere(Sphere(Point(0, 0, height_center_sphere), radius))
            spheres_list.append(center_sphere)

    spheres = Union(spheres_list)

    total_geom = Subtraction(box, spheres)

    ## --------------------------- Visualization
    renderer = PandaRenderer()
    # renderer.display_axes_xyz(3)  

    translator = Translator(total_geom)
    rayMarcher = RayMarchingFactory(main_path, renderer, translator, bounding_sphere = [0, 0, 0, 8.])
    rayMarcher.post_processing_ray_marching_filter()
    # rayMarcher.ray_marching_shader()
    rayMarcher.show_csg_tree_GUI()

    rayMarcher.create_slicer(range_a = -7, range_b = 12 , start_value = 12, axis = 'y', screen_position = -0.75)
    rayMarcher.create_slicer(range_a = -7, range_b = 12 , start_value = 12, axis = 'z', screen_position = -0.85)

    renderer.show()
