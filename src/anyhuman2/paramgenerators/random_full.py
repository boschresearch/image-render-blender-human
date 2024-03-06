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

from ..tools import RandomUniformDiscrete
from ..tools import RandomInstance
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
    rnd = RandomInstance().rnd
    # HumGenV4 Config
    NewHumGenV4Config = {
        "age": {
            "set": rnd.randrange(20, 81),
            "age_color": 0.0,
            "age_wrinkles": 0.0
            },
        "keys": {
            "Forearm Length": rnd.uniform(0, 1.0),
            "Forearm Thickness": rnd.uniform(0, 1.0),
            "Hand Length": rnd.uniform(0, 1.0),
            "Hand Thickness": rnd.uniform(0, 1.0),
            "Hand Width": rnd.uniform(0, 1.0),
            "Upper Arm Length": rnd.uniform(0, 1.0),
            "Upper Arm Thickness": rnd.uniform(0, 1.0),
            "Neck Length": rnd.uniform(0, 1.0),
            "Neck Thickness": rnd.uniform(0, 1.0),
            "Foot Length": rnd.uniform(0, 1.0),
            "Shin Length": rnd.uniform(0, 1.0),
            "Shin Thickness": rnd.uniform(0, 1.0),
            "Thigh Length": rnd.uniform(0, 1.0),
            "Thigh Thickness": rnd.uniform(0, 1.0),
            "height_150": height_150,
            "height_200": height_200,
            "muscular": rnd.uniform(0, 1.0),
            "overweight": rnd.uniform(0, 1.0),
            "skinny": rnd.uniform(0, 1.0),
            "Back Muscles": rnd.uniform(0, 1.0),
            "Biceps": rnd.uniform(0, 1.0),
            "Calves Muscles": rnd.uniform(0, 1.0),
            "Chest Muscles": rnd.uniform(0, 1.0),
            "Forearm Muscles": rnd.uniform(0, 1.0),
            "Hamstring Muscles": rnd.uniform(0, 1.0),
            "Lower Butt Muscles": rnd.uniform(0, 1.0),
            "Quad Muscles": rnd.uniform(0, 1.0),
            "Shoulder Muscles": rnd.uniform(0, 1.0),
            "Traps Muscles": rnd.uniform(0, 1.0),
            "Triceps": rnd.uniform(0, 1.0),
            "Upper Butt Muscles": rnd.uniform(0, 1.0),
            "Stylized": rnd.uniform(0, 1.0),
            "Belly Size": rnd.uniform(0, 1.0),
            "Breast Size": rnd.uniform(0, 1.0),
            "Chest Height": rnd.uniform(0, 1.0),
            "Chest Width": rnd.uniform(0, 1.0),
            "Hips Height": rnd.uniform(0, 1.0),
            "Hips Size": rnd.uniform(0, 1.0),
            "Shoulder Width": rnd.uniform(0, 1.0),
            "Waist Thickness": rnd.uniform(0, 1.0),
            "asian": rnd.uniform(-1.0, 1.0),
            "black": rnd.uniform(-1.0, 1.0),
            "caucasian": rnd.uniform(-1.0, 1.0),
            "variation_1": rnd.uniform(-1.0, 1.0),
            "variation_10": rnd.uniform(-1.0, 1.0),
            "variation_11": rnd.uniform(-1.0, 1.0),
            "variation_2": rnd.uniform(-1.0, 1.0),
            "variation_3": rnd.uniform(-1.0, 1.0),
            "variation_4": rnd.uniform(-1.0, 1.0),
            "variation_5": rnd.uniform(-1.0, 1.0),
            "variation_6": rnd.uniform(-1.0, 1.0),
            "variation_7": rnd.uniform(-1.0, 1.0),
            "variation_8": rnd.uniform(-1.0, 1.0),
            "variation_9": rnd.uniform(-1.0, 1.0),
            "cheek_fullness": rnd.uniform(-1.0, 1.0),
            "cheek_zygomatic_bone": rnd.uniform(-1.0, 1.0),
            "cheek_zygomatic_proc": rnd.uniform(-1.0, 1.0),
            "chin_dimple": rnd.uniform(-1.0, 1.0),
            "chin_height": rnd.uniform(-1.0, 1.0),
            "chin_size": rnd.uniform(-1.0, 1.0),
            "chin_width": rnd.uniform(-1.0, 1.0),
            "ear_antihelix_shape": rnd.uniform(-1.0, 1.0),
            "ear_height": rnd.uniform(-1.0, 1.0),
            "ear_lobe_size": rnd.uniform(-1.0, 1.0),
            "ear_turn": rnd.uniform(-1.0, 1.0),
            "ear_width": rnd.uniform(-1.0, 1.0),
            "Eye Depth": rnd.uniform(-1.0, 1.0),
            "Eye Distance": rnd.uniform(-1.0, 1.0),
            "Eye Height": rnd.uniform(-1.0, 1.0),
            "eyelid_fat_pad": rnd.uniform(-1.0, 1.0),
            "eyelid_rotation": rnd.uniform(-1.0, 1.0),
            "eyelid_shift_horizontal": rnd.uniform(-1.0, 1.0),
            "eyelid_shift_vertical": rnd.uniform(-1.0, 1.0),
            "eye_height": rnd.uniform(-1.0, 1.0),
            "eye_orbit_size": rnd.uniform(-1.0, 1.0),
            "eye_tilt": rnd.uniform(-1.0, 1.0),
            "eye_width": rnd.uniform(-1.0, 1.0),
            "jaw_location_horizontal": rnd.uniform(-1.0, 1.0),
            "jaw_location_vertical": rnd.uniform(-1.0, 1.0),
            "jaw_width": rnd.uniform(-1.0, 1.0),
            "muzzle_location_horizontal": rnd.uniform(-1.0, 1.0),
            "muzzle_location_vertical": rnd.uniform(-1.0, 1.0),
            "lip_cupid_bow": rnd.uniform(-1.0, 1.0),
            "lip_height": rnd.uniform(-1.0, 1.0),
            "lip_location": rnd.uniform(-1.0, 1.0),
            "lip_offset": rnd.uniform(-1.0, 1.0),
            "lip_width": rnd.uniform(-1.0, 1.0),
            "nose_angle": rnd.uniform(-1.0, 1.0),
            "nose_bridge_height": rnd.uniform(-1.0, 1.0),
            "nose_bridge_width": rnd.uniform(-1.0, 1.0),
            "nose_height": rnd.uniform(-1.0, 1.0),
            "nose_location": rnd.uniform(-1.0, 1.0),
            "nose_nostril_flare": rnd.uniform(-1.0, 1.0),
            "nose_nostril_turn": rnd.uniform(-1.0, 1.0),
            "nose_tip_angle": rnd.uniform(-1.0, 1.0),
            "nose_tip_length": rnd.uniform(-1.0, 1.0),
            "nose_tip_size": rnd.uniform(-1.0, 1.0),
            "nose_tip_width": rnd.uniform(-1.0, 1.0),
            "Eye Scale": rnd.uniform(-1.0, 1.0),
            "browridge_center_size": rnd.uniform(-1.0, 1.0),
            "browridge_loc_horizontal": rnd.uniform(-1.0, 1.0),
            "browridge_loc_vertical": rnd.uniform(-1.0, 1.0),
            "forehead_size": rnd.uniform(-1.0, 1.0),
            "temple_size": rnd.uniform(-1.0, 1.0),
            "aged_male": rnd.uniform(-1.0, 1.0),
            "aged_young": rnd.uniform(-1.0, 1.0),
            "Male": Male,
            "LIVE_KEY_PERMANENT": 1.0,
            "LIVE_KEY_TEMP_": 0.0
            },
        "skin": {
            "tone": rnd.uniform(0, 1.0),
            "redness": rnd.uniform(0, 1.0),
            "saturation": rnd.uniform(0, 1.0),
            "normal_strength": rnd.randint(1, 2), # From Anyhuman1
            "roughness_multiplier": rnd.uniform(0, 1.0),
            "freckles": rnd.uniform(0, 1.0),
            "splotches": rnd.uniform(0, 1.0),
            "texture.set": sSkinTexture,
            "cavity_strength": rnd.uniform(0, 1.0),
            "gender_specific": {
                "mustache_shadow": rnd.uniform(0, 1.0),
                "beard_shadow": rnd.uniform(0, 1.0)
            }
            },
        "eyes": {
            "pupil_color": [rnd.uniform(0, 1.0), rnd.uniform(0, 1.0), rnd.uniform(0, 1.0), 1.00],
            "sclera_color": [rnd.uniform(0, 1.0), rnd.uniform(0, 1.0), rnd.uniform(0, 1.0), 1.00],
        },
        "height": {
            "set": height
        },
        "hair": {
            "eyebrows": {
                "set": sEyebrows,
                "lightness": rnd.uniform(0, 1.0),
                "redness": rnd.uniform(0, 1.0),
                "roughness": rnd.uniform(0, 1.0),
                "salt_and_pepper": rnd.uniform(0, 1.0),
                "roots": rnd.uniform(0, 1.0),
                "root_lightness": rnd.uniform(0, 1.0),
                "root_redness": rnd.uniform(0, 1.0),
                "roots_hue": rnd.uniform(0, 1.0),
                "fast_or_accurate": rnd.uniform(0, 1.0),
                "hue": rnd.uniform(0, 1.0)
            },
            "regular_hair": {
                "set": sRegularHair,
                "lightness": rnd.uniform(0, 1.0),
                "redness": rnd.uniform(0, 1.0),
                "roughness": rnd.uniform(0, 1.0),
                "salt_and_pepper": rnd.uniform(0, 1.0),
                "roots": rnd.uniform(0, 1.0),
                "root_lightness": rnd.uniform(0, 1.0),
                "root_redness": rnd.uniform(0, 1.0),
                "roots_hue": rnd.uniform(0, 1.0),
                "fast_or_accurate": rnd.uniform(0, 1.0),
                "hue": rnd.uniform(0, 1.0),
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
