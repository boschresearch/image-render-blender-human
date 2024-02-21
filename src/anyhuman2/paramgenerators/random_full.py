# <LICENSE id="GPL-3.0">
#
#   Image-Render Blender Human add-on module
#   Copyright (C) 2022 Robert Bosch GmbH and its subsidiaries
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#
# </LICENSE>
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# -----
# Copyright (c) 2022 Robert Bosch GmbH and its subsidiaries.
# All rights reserved.
# -----
###

import random
from ..tools import RandomUniformDiscrete

############################################################################################
def FullyRandomizeParams(params, generator_params):
    """
    Create a set of completely random parameters for human generation.
    This randomizer is intended for domain randomization purposes and tries
    to contain a large variation in the appearance of humans, which might
    result in the generation of 'funny' humans.

    The params dict can contain:
    - 'gender': either 'male' or 'female'

    If gender is not given, it will be selected randomly.


    Parameters
    ----------
    params : dict
        set of parameter controlling the randomization

    Returns
    -------
    dict
        Dictionary of parameters for human generator
    """
    gender = params.get("gender", random.choice(["male", "female"]))

    sets = ["Casual", "Summer", "Winter", "Office", "Extra Outfits Pack"]
    sets = ["Extra Outfits Pack"]

    ignore_list = ["Pirate"]
    ignore_list.extend(params.get("additional_clothes_to_ignore", []))

    outfit_set = random.choice(sets)
    outfit_list = [
        item
        for item in generator_params.dict_outfits[gender][outfit_set]
        if item not in ignore_list
    ]
    outfit = random.choice(outfit_list)
    outfit_style = "{}/{}".format(outfit_set, outfit)

    new_params = {
        "gender": gender,
        "body": random.choice(generator_params.dict_bodies[gender]),
        "muscular": RandomUniformDiscrete(0, 1, 11),
        "overweight": RandomUniformDiscrete(0, 1, 11),
        # set skinny value to 0-0.2 as  persons too skinny look odd
        "skinny": RandomUniformDiscrete(0, 0.5, 11),
        "height": random.randint(150, 190),
        "face": "random",
        "skin": {
            "tone": RandomUniformDiscrete(0.1, 1.9, 51),
            "redness": RandomUniformDiscrete(-0.2, 0.8, 51),
            "saturation": RandomUniformDiscrete(0.1, 0.9, 51),
            "normal_strength": random.randint(1, 2),
            "roughness_multiplier": RandomUniformDiscrete(1.5, 2.0, 51),
            "dark_areas": RandomUniformDiscrete(0.0, 2.0, 101),
            "light_areas": RandomUniformDiscrete(0.0, 2.0, 101),
            "freckles": RandomUniformDiscrete(0.0, 0.5, 101),
            "splotches": RandomUniformDiscrete(0.0, 0.5, 101),
            "beauty_spots_amount_": random.randint(0, 100),  # TODO clarify what this is
            "beauty_spots_amount": RandomUniformDiscrete(0.0, 1.0, 101),
            "beauty_spots_opacity": RandomUniformDiscrete(0.0, 0.5, 101),
            "sagging": RandomUniformDiscrete(0.3, 1.0, 15),
            "wrinkles": RandomUniformDiscrete(5.0, 20.0, 51),
        },
        "eyes": {
            "iris_color": [random.random(), random.random(), random.random(), 1.00],
            "eyebrows_style": "random",
            "eyebrows_length": None,  # TODO implement
            "eyelashes_lenght": None,  # TODO implement
            "hair_lightness": 0.3,
            "hair_redness": 0.9,
            "hair_roughness": 0.3,
        },
        "hair": {
            "hair_style": random.choice(
                list(generator_params.dict_hair[gender].keys())
            ),
            "length": RandomUniformDiscrete(
                0.0, 1.0, 101
            ),  # hairstyle seems not to be evaluated
            "lightness": RandomUniformDiscrete(0.1, 3.9, 39),
            "redness": RandomUniformDiscrete(0.1, 0.9, 9),
            "roughness": RandomUniformDiscrete(0.1, 0.9, 9),
            "salt_and_pepper": RandomUniformDiscrete(0.1, 0.9, 9),
            "roots": RandomUniformDiscrete(0.1, 0.9, 9),
            "hue": RandomUniformDiscrete(0.1, 1.0, 10),
        },
        "beard": {
            "beard_style": random.choice(
                list(generator_params.dict_male_face_hair.keys())
            ),
            "shadow_mustache": 0,
            "shadow_beard": RandomUniformDiscrete(0.0, 1.0, 11),
        },
        "makeup": {
            "foundation_amount": 0,
            "foundation_color": [0.655761, 0.332872, 0.191478, 1.000000],
            "blush_opacity": RandomUniformDiscrete(0.0, 1.0, 101),
            "blush_color": [0.553053, 0.138596, 0.109141, 1.000000],
            "eyeshadow_opacity": RandomUniformDiscrete(0.0, 1.0, 101),
            "eyeshadow_color": [0.239424, 0.041744, 0.013199, 1.000000],
            "lipstick_opacity": RandomUniformDiscrete(0.0, 1.0, 101),
            "lipstick_color": [0.309741, 0.091615, 0.073231, 1.000000],
            "eyeliner_opacity": RandomUniformDiscrete(0.0, 1.0, 101),
            "eyeliner_color": [0.001578, 0.010979, 0.060677, 1.000000],
        },
        "outfit": {
            "outfit_style": outfit_style,
            "outfit_pattern": [
                random.choice(["random", False]),
                random.choice(["random", False]),
                random.choice(["random", False]),
                random.choice(["random", False]),
            ],
            "outfit_palette": "RANDOM_FULL",
            "outfit_color": "random",
            "outfit_brightness": random.triangular(0.6, 1.4),
            "outfit_saturation": random.triangular(0.8, 1.7),
            "outfit_contrast": random.triangular(1.8, 2.4),
        },
        "footwear": {
            "footwear_style": "random",
            "footwear_color": "random",
        },
        "posefilename": None,
    }

    if gender == "male":
        if random.choice([True, False]):
            new_params["beard"]["beard_style"] = None

    return new_params


# enddef
