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
from .GeneralRandomParameters import GeneralRandomParameters 

############################################################################################
def FullyRandomizeParams(params, generator_config):
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
    universal_params = GeneralRandomParameters(params, generator_config)
    Male, dFaceHair, sRegularHair, sEyebrows = universal_params.RandomizeHair()
    sGender = universal_params.GetGender()
    height_150, height_200 = universal_params.RandomizeHeight()
    outfit = universal_params.RandomizeOutfit()
    sFootwear = universal_params.RandomFootwear()
    sSkinTexture = universal_params.RandomizeSkin()

    # HumGenV4 Config
    NewHumGenV4Config = {
        "age": {
            "set": random.randrange(20, 81),
            "age_color": 0.0,
            "age_wrinkles": 0.0
            },
        "keys": {
            "Forearm Length": random.uniform(0, 1.0),
            "Forearm Thickness": random.uniform(0, 1.0),
            "Hand Length": random.uniform(0, 1.0),
            "Hand Thickness": random.uniform(0, 1.0),
            "Hand Width": random.uniform(0, 1.0),
            "Upper Arm Length": random.uniform(0, 1.0),
            "Upper Arm Thickness": random.uniform(0, 1.0),
            "Neck Length": random.uniform(0, 1.0),
            "Neck Thickness": random.uniform(0, 1.0),
            "Foot Length": random.uniform(0, 1.0),
            "Shin Length": random.uniform(0, 1.0),
            "Shin Thickness": random.uniform(0, 1.0),
            "Thigh Length": random.uniform(0, 1.0),
            "Thigh Thickness": random.uniform(0, 1.0),
            "height_150": height_150,
            "height_200": height_200,
            "muscular": random.uniform(0, 1.0),
            "overweight": random.uniform(0, 1.0),
            "skinny": random.uniform(0, 1.0),
            "Back Muscles": random.uniform(0, 1.0),
            "Biceps": random.uniform(0, 1.0),
            "Calves Muscles": random.uniform(0, 1.0),
            "Chest Muscles": random.uniform(0, 1.0),
            "Forearm Muscles": random.uniform(0, 1.0),
            "Hamstring Muscles": random.uniform(0, 1.0),
            "Lower Butt Muscles": random.uniform(0, 1.0),
            "Quad Muscles": random.uniform(0, 1.0),
            "Shoulder Muscles": random.uniform(0, 1.0),
            "Traps Muscles": random.uniform(0, 1.0),
            "Triceps": random.uniform(0, 1.0),
            "Upper Butt Muscles": random.uniform(0, 1.0),
            "Stylized": random.uniform(0, 1.0),
            "Belly Size": random.uniform(0, 1.0),
            "Breast Size": random.uniform(0, 1.0),
            "Chest Height": random.uniform(0, 1.0),
            "Chest Width": random.uniform(0, 1.0),
            "Hips Height": random.uniform(0, 1.0),
            "Hips Size": random.uniform(0, 1.0),
            "Shoulder Width": random.uniform(0, 1.0),
            "Waist Thickness": random.uniform(0, 1.0),
            "asian": 0.0,
            "black": 0.5,
            "caucasian": 0.0,
            "variation_1": 0.0,
            "variation_10": 0.0,
            "variation_11": 0.0,
            "variation_2": 0.0,
            "variation_3": 0.0,
            "variation_4": 1.0,
            "variation_5": 0.0,
            "variation_6": 0.0,
            "variation_7": 0.0,
            "variation_8": 0.0,
            "variation_9": 0.0,
            "cheek_fullness": 0.0,
            "cheek_zygomatic_bone": 0.0,
            "cheek_zygomatic_proc": 0.0,
            "chin_dimple": 0.0,
            "chin_height": 0.0,
            "chin_size": 0.0,
            "chin_width": 0.0,
            "ear_antihelix_shape": 0.0,
            "ear_height": 0.0,
            "ear_lobe_size": 0.0,
            "ear_turn": 0.0,
            "ear_width": 0.0,
            "Eye Depth": 0.0,
            "Eye Distance": 0.0,
            "Eye Height": 0.0,
            "eyelid_fat_pad": 0.0,
            "eyelid_rotation": 0.0,
            "eyelid_shift_horizontal": 0.0,
            "eyelid_shift_vertical": 0.0,
            "eye_height": 0.0,
            "eye_orbit_size": 0.0,
            "eye_tilt": 0.0,
            "eye_width": 0.0,
            "jaw_location_horizontal": 0.0,
            "jaw_location_vertical": 0.0,
            "jaw_width": 0.0,
            "muzzle_location_horizontal": 0.0,
            "muzzle_location_vertical": 0.0,
            "lip_cupid_bow": 0.0,
            "lip_height": 0.0,
            "lip_location": 0.0,
            "lip_offset": 0.0,
            "lip_width": 0.0,
            "nose_angle": 0.0,
            "nose_bridge_height": 0.0,
            "nose_bridge_width": 0.0,
            "nose_height": 0.0,
            "nose_location": 0.0,
            "nose_nostril_flare": 0.0,
            "nose_nostril_turn": 0.0,
            "nose_tip_angle": 0.0,
            "nose_tip_length": 0.0,
            "nose_tip_size": 0.0,
            "nose_tip_width": 0.0,
            "Eye Scale": 0.0,
            "browridge_center_size": 0.0,
            "browridge_loc_horizontal": 0.0,
            "browridge_loc_vertical": 0.0,
            "forehead_size": 0.0,
            "temple_size": 0.0,
            "aged_male": 0.0,
            "aged_young": 0.0,
            "Male": Male,
            "LIVE_KEY_PERMANENT": 1.0,
            "LIVE_KEY_TEMP_": 0.0
            },
        "skin": {
            "tone": RandomUniformDiscrete(0.1, 1.9, 51), # From Anyhuman1
            "redness": RandomUniformDiscrete(-0.2, 0.8, 51), # From Anyhuman1
            "saturation":RandomUniformDiscrete(0.1, 0.9, 51), # From Anyhuman1
            "normal_strength": random.randint(1, 2), # From Anyhuman1
            "roughness_multiplier": RandomUniformDiscrete(1.5, 2.0, 51), # From Anyhuman1
            "freckles": RandomUniformDiscrete(0.0, 0.5, 101), # From Anyhuman1
            "splotches": RandomUniformDiscrete(0.0, 0.5, 101), # From Anyhuman1
            "texture.set": sSkinTexture,
            "cavity_strength": 0.0,
            "gender_specific": {
                "mustache_shadow": 0.0,
                "beard_shadow": 0.0
            }
            },
        "eyes": {
            "pupil_color": [random.uniform(0, 1.0), random.uniform(0, 1.0), random.uniform(0, 1.0), 1.00],
            "sclera_color": [random.uniform(0, 1.0), random.uniform(0, 1.0), random.uniform(0, 1.0), 1.00],
        },
        "height": {
            "set": RandomUniformDiscrete(160, 185, 26) # From Anyhuman1
        },
        "hair": {
            "eyebrows": {
                "set": sEyebrows,
                "lightness": 0.10000000149011612,
                "redness": 0.8999999761581421,
                "roughness": 0.44999998807907104,
                "salt_and_pepper": 0.0,
                "roots": 0.0,
                "root_lightness": 0.5,
                "root_redness": 0.0,
                "roots_hue": 0.5,
                "fast_or_accurate": 0.0,
                "hue": 0.5
            },
            "regular_hair": {
                "set": sRegularHair,
                "lightness": RandomUniformDiscrete(0.1, 3.9, 39), # From Anyhuman1
                "redness": RandomUniformDiscrete(0.1, 0.9, 9), # From Anyhuman1
                "roughness": RandomUniformDiscrete(0.1, 0.9, 9), # From Anyhuman1
                "salt_and_pepper": RandomUniformDiscrete(0.1, 0.9, 9), # From Anyhuman1
                "roots": RandomUniformDiscrete(0.1, 0.9, 9), # From Anyhuman1
                "root_lightness": 0.0,
                "root_redness": 0.8999999761581421,
                "roots_hue": 0.5,
                "fast_or_accurate": 0.0,
                "hue": 0.5
            },
            "face_hair": dFaceHair
        },
        "clothing": {
            "outfit": {
                "set": outfit
            },
            "footwear": {
                "set": sFootwear
            }
        }
    }

    dictAnyHuman = {"dictCustom":
            {
                "sGender": sGender,
                "bOpenPoseHandLabels": False,
                "bFacialRig": True ,
                "sPoseFilename": None
            },
        "dictHumGen_V4": NewHumGenV4Config
    }

    return dictAnyHuman


# enddef
