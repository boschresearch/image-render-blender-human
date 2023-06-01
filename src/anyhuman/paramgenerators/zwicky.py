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

######################################################################
def ZwickyParams(zwicky_params, generator_params):
    """ """

    def _get_param(key, defaults):
        if key in zwicky_params:
            if isinstance(zwicky_params[key], list):
                # if the parameter is given by a list, choose a value from the list
                return random.choice(zwicky_params[key])
            else:
                return zwicky_params[key]

        return random.choice(defaults)

    ##################################################################
    def _get_type_param(bodytype, gender):
        bodytypes = [
            bodyfile
            for bodyfile in generator_params.dict_bodies[gender]
            if bodytype.capitalize() in bodyfile
        ]
        return random.choice(bodytypes)

    # enddef

    ##################################################################
    def _get_body_type_params(bodytype, gender):
        if bodytype == "thin":
            muscular = random.triangular(0.2, 0.4)
            overweight = random.triangular(0.0, 0.5)
            skinny = random.triangular(0.2, 0.5)
        elif bodytype == "athletic":
            muscular = random.triangular(0.3, 0.7)
            overweight = random.triangular(0.0, 0.2)
            skinny = random.triangular(0.3, 0.5)
        elif bodytype == "average":
            muscular = random.triangular(0.0, 0.5)
            overweight = random.triangular(0.2, 0.6)
            skinny = random.triangular(0.1, 0.2)
        elif bodytype == "corpulent":
            muscular = random.triangular(0.1, 0.5)
            overweight = random.triangular(0.3, 0.7)
            skinny = random.triangular(0.0, 0.1)
        elif bodytype == "obese":
            muscular = random.triangular(0.1, 0.4)
            overweight = random.triangular(0.5, 0.9)
            skinny = random.triangular(0.0, 0.05)
        else:
            raise KeyError("Please provide an available bodytype not", bodytype)

        return muscular, overweight, skinny

    # enddef

    ##################################################################
    def _get_height_param(height, gender):
        if gender == "male":
            if height == "short":
                return random.triangular(160.0, 175.0)
            elif height == "average":
                return random.triangular(170.0, 185.0)
            elif height == "tall":
                return random.triangular(180.0, 195.0)
        else:
            if height == "short":
                return random.triangular(150.0, 165.0)
            elif height == "average":
                return random.triangular(160.0, 175.0)
            elif height == "tall":
                return random.triangular(170.0, 185.0)
        # endif
        raise KeyError("Please provide an availabe bodyheight value, not", height)

    # enddef

    ##################################################################
    def _get_skin_params(skin_tone, skin_type, gender, age):
        params = {
            "tone": RandomUniformDiscrete(0.100, 2.000),
            "redness": RandomUniformDiscrete(-0.200, 0.800),
            "saturation": RandomUniformDiscrete(0.000, 1.500),
            "normal_strength": random.randint(1, 4),
            "roughness_multiplier": RandomUniformDiscrete(1.500, 2.000),
            "dark_areas": RandomUniformDiscrete(0.000, 2.000),
            "light_areas": RandomUniformDiscrete(0.000, 2.000),
            "freckles": RandomUniformDiscrete(0.000, 0.500),
            "splotches": RandomUniformDiscrete(0.000, 0.500),
            "beauty_spots_amount_": random.randint(0, 100),  # TODO clarify what this is
            "beauty_spots_opacity": RandomUniformDiscrete(0.000, 0.500),
            "beauty_spots_amount": RandomUniformDiscrete(0.000, 1.000),
            "sagging": round(random.triangular(0.0, 0.1), 2),
            "wrinkles": round(random.triangular(0.0, 0.1), 2),
        }

        if age == "young":
            params["beauty_spots_opacity"] = RandomUniformDiscrete(0.000, 0.500)
            params["beauty_spots_amount"] = RandomUniformDiscrete(0.000, 0.400)
            params["sagging"] = round(random.triangular(0.0, 0.1), 2)
            params["wrinkles"] = round(random.triangular(0.0, 0.5), 2)
        elif age == "adult":
            params["beauty_spots_opacity"] = RandomUniformDiscrete(0.000, 0.500)
            params["beauty_spots_amount"] = RandomUniformDiscrete(0.000, 0.800)
            params["sagging"] = round(random.triangular(0.1, 0.8), 2)
            params["wrinkles"] = round(random.triangular(0.4, 2.1), 2)
        elif age == "senior":
            params["beauty_spots_opacity"] = RandomUniformDiscrete(0.000, 1.000)
            params["beauty_spots_amount"] = RandomUniformDiscrete(0.000, 1.800)
            params["sagging"] = round(random.triangular(0.6, 1.0), 2)
            params["wrinkles"] = round(random.triangular(2.5, 10.0), 2)
        else:
            raise KeyError("Please provide an available age value, not", age)
        return params

    # enddef

    ##################################################################
    def _get_eyes_params(eye_color, gender):
        params = {
            "iris_color": [random.random(), random.random(), random.random(), 1.00],
            "eyebrows_style": "random",
            "eyebrows_length": None,  # TODO implement
            "eyelashes_lenght": None,  # TODO implement
            "hair_lightness": 0.3,
            "hair_redness": 0.9,
            "hair_roughness": 0.3,
        }
        if eye_color == "brown":
            params["iris_color"] = [
                random.uniform(0.26, 0.35),
                random.uniform(0.10, 0.20),
                random.uniform(0.00, 0.10),
                1.00,
            ]
        elif eye_color == "blue":
            params["iris_color"] = [
                random.uniform(0.05, 0.10),
                random.uniform(0.15, 0.20),
                random.uniform(0.30, 0.40),
                1.00,
            ]
        elif eye_color == "green":
            params["iris_color"] = [
                random.uniform(0.10, 0.20),
                random.uniform(0.35, 0.45),
                random.uniform(0.00, 0.10),
                1.00,
            ]
        else:
            raise KeyError(
                "Please provide an available eye color value, not", eye_color
            )
        return params

    # enddef

    ##################################################################
    def _get_hair_params(hair_length, hair_color, skin_tone, skin_type, gender, age):
        _hair_groups = {}
        _hair_groups["female"] = {
            "long": [
                "Bob Bangs",
                "Bob Long",
                "Medium Center Part",
                "Medium Side Part",
                "Undercut",
                "Wavy Bob Bangs",
            ],
            "average": [
                "Afro Dreads",
                "Afro",
                "Curly Afro",
                "Dreadlocks",
                "Bob Short",
                "Bun Bangs",
                "Bun",
                "Ponytail Short",
                "Ponytail",
            ],
            "short": [
                "Curls High Top Fade",
                "Bowl",
                "Combed Stylized",
                "Flat top",
                "Mohawk",
                "Pixie Messy",
                "Pixie",
                "Slicked Back Side Part",
                "Slicked Back",
                "Spiked Up",
                "Buzzcut Curly Fade",
                "Buzzcut Fade",
                "Short Combed",
                "Short Curly Fade",
                "Short Side Part",
            ],
        }
        _hair_groups["male"] = {
            "long": [
                "Bob Long",
                "Medium Center Part",
                "Medium Side Part",
                "Undercut",
                "Wavy Bob Bangs",
            ],
            "average": [
                "Afro Dreads",
                "Afro",
                "Curly Afro",
                "Dreadlocks",
                "Bun",
                "Ponytail Short",
                "Ponytail",
            ],
            "short": [
                "Curls High Top Fade",
                "Bowl",
                "Combed Stylized",
                "Flat top",
                "Mohawk",
                "Pixie Messy",
                "Pixie",
                "Slicked Back Side Part",
                "Slicked Back",
                "Spiked Up",
                "Buzzcut Curly Fade",
                "Buzzcut Fade",
                "Short Combed",
                "Short Curly Fade",
                "Short Side Part",
            ],
        }

        random_hair_style = (
            None
            if hair_length == "bald"
            else random.choice(_hair_groups[gender][hair_length])
        )
        params = {
            "hair_style": random_hair_style,
            "length": round(random.triangular(0.7, 1.0, 0.9), 3),
            "lightness": 0.5,  # TODO clarify if this should be random
            "redness": random.triangular(
                0.0, 1.0
            ),  # TODO clarify if this should be random
            "roughness": random.triangular(
                0.0, 1.0
            ),  # TODO clarify if this should be random
            "salt_and_pepper": 0.0,  # TODO clarify if this should be random
            "roots": 0.0,  # TODO clarify if this should be random
            "hue": 0.5,
        }

        if hair_color == "black":
            params["lightness"] = random.uniform(0.0, 0.2)
        elif hair_color == "dark":
            params["lightness"] = random.uniform(0.2, 0.4)
        elif hair_color == "average":
            params["lightness"] = random.uniform(0.35, 0.7)
        elif hair_color == "light":
            params["lightness"] = random.uniform(0.7, 1.0)

        if age == "adult":
            params["salt_and_pepper"] = random.uniform(0.0, 0.80)
        elif age == "senior":
            params["salt_and_pepper"] = random.uniform(0.5, 1.00)
        return params

    # enddef

    ##################################################################
    def _get_outfit_params(clothing, clothing_color, gender):
        sets = []
        if clothing == "casual":
            sets = ["Casual", "Summer", "Winter"]
        elif clothing == "business":
            sets = ["Office"]
        else:
            raise KeyError("Please provide an available clothing style, not", clothing)
        # endif
        print(sets)
        outfit_set = random.choice(sets)
        outfit_list = generator_params.dict_outfits[gender][outfit_set]
        print(outfit_list)
        outfit = random.choice(outfit_list)
        outfit_style = "{}/{}".format(outfit_set, outfit)

        outfit_palette = "RANDOM_FULL"

        if clothing_color == "dark":
            outfit_palette = "DARK"
        elif clothing_color == "bright":
            outfit_palette = "BRIGHT"

        outfit_params = {"outfit_style": outfit_style, "outfit_palette": outfit_palette}

        footwear_params = {"footwear_style": "random"}
        return outfit_params, footwear_params

    # enddef

    params = {}

    gender = _get_param("gender", ["male", "female"])
    skin_type = _get_param("type", ["asian", "black", "caucasian"])
    age = _get_param("age", ["young", "adult", "senior"])
    bodytype = _get_param(
        "bodytype", ["thin", "athletic", "average", "corpulent", "obese"]
    )
    height = _get_param("bodyheight", ["short", "average", "tall"])
    skin_tone = _get_param("skin_tone", ["dark", "average", "bright"])
    hair_length = _get_param("hair_length", ["bald", "short", "average", "long"])
    hair_color = _get_param("hair_color", ["black", "dark", "average", "light"])
    eye_color = _get_param("eye_color", ["blue", "green", "brown"])
    clothing = _get_param("clothing", ["casual", "business"])
    clothing_color = _get_param("clothing_color", ["bright, dark"])

    params["gender"] = gender

    params["body"] = _get_type_param(skin_type, gender)
    params["muscular"], params["overweight"], params["skinny"] = _get_body_type_params(
        bodytype, gender
    )

    params["height"] = _get_height_param(height, gender)
    params["face"] = "random"

    params["skin"] = _get_skin_params(skin_tone, skin_type, gender, age)

    params["eyes"] = _get_eyes_params(eye_color, gender)

    params["hair"] = _get_hair_params(
        hair_length, hair_color, skin_tone, skin_type, gender, age
    )

    params["outfit"], params["footwear"] = _get_outfit_params(
        clothing, clothing_color, gender
    )

    # no makeup and beards for now..
    # TODO add beard

    return params


# enddef
