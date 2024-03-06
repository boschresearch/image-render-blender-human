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
    Male, dFaceHair, dBeardLength, sRegularHair, sEyebrows = universal_params.RandomizeHair()
    sGender = universal_params.GetGender()
    height_150, height_200, height = universal_params.RandomizeHeight()
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
            "asian": random.uniform(-1.0, 1.0),
            "black": random.uniform(-1.0, 1.0),
            "caucasian": random.uniform(-1.0, 1.0),
            "variation_1": random.uniform(-1.0, 1.0),
            "variation_10": random.uniform(-1.0, 1.0),
            "variation_11": random.uniform(-1.0, 1.0),
            "variation_2": random.uniform(-1.0, 1.0),
            "variation_3": random.uniform(-1.0, 1.0),
            "variation_4": random.uniform(-1.0, 1.0),
            "variation_5": random.uniform(-1.0, 1.0),
            "variation_6": random.uniform(-1.0, 1.0),
            "variation_7": random.uniform(-1.0, 1.0),
            "variation_8": random.uniform(-1.0, 1.0),
            "variation_9": random.uniform(-1.0, 1.0),
            "cheek_fullness": random.uniform(-1.0, 1.0),
            "cheek_zygomatic_bone": random.uniform(-1.0, 1.0),
            "cheek_zygomatic_proc": random.uniform(-1.0, 1.0),
            "chin_dimple": random.uniform(-1.0, 1.0),
            "chin_height": random.uniform(-1.0, 1.0),
            "chin_size": random.uniform(-1.0, 1.0),
            "chin_width": random.uniform(-1.0, 1.0),
            "ear_antihelix_shape": random.uniform(-1.0, 1.0),
            "ear_height": random.uniform(-1.0, 1.0),
            "ear_lobe_size": random.uniform(-1.0, 1.0),
            "ear_turn": random.uniform(-1.0, 1.0),
            "ear_width": random.uniform(-1.0, 1.0),
            "Eye Depth": random.uniform(-1.0, 1.0),
            "Eye Distance": random.uniform(-1.0, 1.0),
            "Eye Height": random.uniform(-1.0, 1.0),
            "eyelid_fat_pad": random.uniform(-1.0, 1.0),
            "eyelid_rotation": random.uniform(-1.0, 1.0),
            "eyelid_shift_horizontal": random.uniform(-1.0, 1.0),
            "eyelid_shift_vertical": random.uniform(-1.0, 1.0),
            "eye_height": random.uniform(-1.0, 1.0),
            "eye_orbit_size": random.uniform(-1.0, 1.0),
            "eye_tilt": random.uniform(-1.0, 1.0),
            "eye_width": random.uniform(-1.0, 1.0),
            "jaw_location_horizontal": random.uniform(-1.0, 1.0),
            "jaw_location_vertical": random.uniform(-1.0, 1.0),
            "jaw_width": random.uniform(-1.0, 1.0),
            "muzzle_location_horizontal": random.uniform(-1.0, 1.0),
            "muzzle_location_vertical": random.uniform(-1.0, 1.0),
            "lip_cupid_bow": random.uniform(-1.0, 1.0),
            "lip_height": random.uniform(-1.0, 1.0),
            "lip_location": random.uniform(-1.0, 1.0),
            "lip_offset": random.uniform(-1.0, 1.0),
            "lip_width": random.uniform(-1.0, 1.0),
            "nose_angle": random.uniform(-1.0, 1.0),
            "nose_bridge_height": random.uniform(-1.0, 1.0),
            "nose_bridge_width": random.uniform(-1.0, 1.0),
            "nose_height": random.uniform(-1.0, 1.0),
            "nose_location": random.uniform(-1.0, 1.0),
            "nose_nostril_flare": random.uniform(-1.0, 1.0),
            "nose_nostril_turn": random.uniform(-1.0, 1.0),
            "nose_tip_angle": random.uniform(-1.0, 1.0),
            "nose_tip_length": random.uniform(-1.0, 1.0),
            "nose_tip_size": random.uniform(-1.0, 1.0),
            "nose_tip_width": random.uniform(-1.0, 1.0),
            "Eye Scale": random.uniform(-1.0, 1.0),
            "browridge_center_size": random.uniform(-1.0, 1.0),
            "browridge_loc_horizontal": random.uniform(-1.0, 1.0),
            "browridge_loc_vertical": random.uniform(-1.0, 1.0),
            "forehead_size": random.uniform(-1.0, 1.0),
            "temple_size": random.uniform(-1.0, 1.0),
            "aged_male": random.uniform(-1.0, 1.0),
            "aged_young": random.uniform(-1.0, 1.0),
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
            "cavity_strength": random.uniform(0, 1.0),
            "gender_specific": {
                "mustache_shadow": random.uniform(0, 1.0),
                "beard_shadow": random.uniform(0, 1.0)
            }
            },
        "eyes": {
            "pupil_color": [random.uniform(0, 1.0), random.uniform(0, 1.0), random.uniform(0, 1.0), 1.00],
            "sclera_color": [random.uniform(0, 1.0), random.uniform(0, 1.0), random.uniform(0, 1.0), 1.00],
        },
        "height": {
            "set": height
        },
        "hair": {
            "eyebrows": {
                "set": sEyebrows,
                "lightness": random.uniform(0, 1.0),
                "redness": random.uniform(0, 1.0),
                "roughness": random.uniform(0, 1.0),
                "salt_and_pepper": random.uniform(0, 1.0),
                "roots": random.uniform(0, 1.0),
                "root_lightness": random.uniform(0, 1.0),
                "root_redness": random.uniform(0, 1.0),
                "roots_hue": random.uniform(0, 1.0),
                "fast_or_accurate": random.uniform(0, 1.0),
                "hue": random.uniform(0, 1.0)
            },
            "regular_hair": {
                "set": sRegularHair,
                "lightness": RandomUniformDiscrete(0.1, 3.9, 39), # From Anyhuman1
                "redness": RandomUniformDiscrete(0.1, 0.9, 9), # From Anyhuman1
                "roughness": RandomUniformDiscrete(0.1, 0.9, 9), # From Anyhuman1
                "salt_and_pepper": RandomUniformDiscrete(0.1, 0.9, 9), # From Anyhuman1
                "roots": RandomUniformDiscrete(0.1, 0.9, 9), # From Anyhuman1
                "root_lightness": random.uniform(0, 1.0),
                "root_redness": random.uniform(0, 1.0),
                "roots_hue": random.uniform(0, 1.0),
                "fast_or_accurate": random.uniform(0, 1.0),
                "hue": random.uniform(0, 1.0),
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
                "sPoseFilename": None,
                "dBeardLength" : dBeardLength,
            },
        "dictHumGen_V4": NewHumGenV4Config
    }

    return dictAnyHuman


# enddef
