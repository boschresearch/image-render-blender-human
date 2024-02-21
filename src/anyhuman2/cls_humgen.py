#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: humgen.py
# Created Date: Thursday, August 12th 2021, 8:33:34 am
# Author: Dirk Fortmeier (BEG/ESD1)
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
###


import bpy
import bmesh

import random
import os
import os.path
import colorsys
import collections

import json

from pathlib import Path

from anyblend import node
from anyblend.util.node import GetByLabelOrId
from anyblend.collection import RemoveCollection
import addon_utils



color_dict = {
    # color set from HG3D (see HG_COLORS.py)
    "C0": {
        "light_grayblue": (0.53, 0.75, 1.0, 1.0),
        "light_blue": (0.36, 0.59, 1.0, 1.0),
        "grey": (0.96, 1.0, 1.0, 1.0),
        "dark_gray": (0.46, 0.48, 0.49, 1.0),
        "darkest_gray": (0.18, 0.19, 0.2, 1.0),
        "turquise": (0.27, 0.47, 0.48, 1.0),
        "silver": (0.61, 0.76, 0.74, 1.0),
        "purple": (0.48, 0.21, 0.43, 1.0),
        "green": (0.35, 0.46, 0.15, 1.0),
        "dark_blue": (0.12, 0.19, 0.34, 1.0),
    },
    "RANDOM_FULL": {
        "light_grayblue": (0.53, 0.75, 1.0, 1.0),
        "light_blue": (0.36, 0.59, 1.0, 1.0),
        "silver": (0.61, 0.76, 0.74, 1.0),
        "dark_blue": (0.12, 0.19, 0.34, 1.0),
        "darkest_gray": (0.18, 0.19, 0.2, 1.0),
        "turquise": (0.27, 0.47, 0.48, 1.0),
        "purple": (0.48, 0.21, 0.43, 1.0),
        "green": (0.35, 0.46, 0.15, 1.0),
        "yellow": (0.48, 0.46, 0.14, 1.0),
        "red": (0.48, 0.08, 0.06, 1.0),
    },
    "DARK": {
        "dark_blue": (0.12, 0.19, 0.34, 1.0),
        "darkest_gray": (0.18, 0.19, 0.2, 1.0),
        "turquise": (0.27, 0.47, 0.48, 1.0),
        "purple": (0.48, 0.21, 0.43, 1.0),
        "green": (0.35, 0.46, 0.15, 1.0),
        "red": (0.48, 0.08, 0.06, 1.0),
    },
    "BRIGHT": {
        "light_grayblue": (0.53, 0.75, 1.0, 1.0),
        "light_blue": (0.36, 0.59, 1.0, 1.0),
        "silver": (0.61, 0.76, 0.74, 1.0),
        "turquise": (0.27, 0.47, 0.48, 1.0),
        "purple": (0.48, 0.21, 0.43, 1.0),
        "green": (0.35, 0.46, 0.15, 1.0),
        "yellow": (0.48, 0.46, 0.14, 1.0),
        "red": (0.48, 0.08, 0.06, 1.0),
    },
}


#########################################################################################################
class HumGenWrapper:
    @staticmethod
    def get_installed_humgen_version():
        humgen_version = None  # Default value if addon not found
        for mod in addon_utils.modules():
            if mod.bl_info.get("name") == "Human Generator 3D":
                humgen_version = mod.bl_info.get("version")
                print(f'HumGen3D Version is: {".".join(map(str, humgen_version))}')
                break  # Stop searching once addon is found
        return humgen_version

    # enddef
    # Import Human class based on the version
    version_info = None
    try:
        version_info = get_installed_humgen_version()
    except ImportError:
        # Handle ImportError if get_installed_humgen_version is not available
        pass

    if version_info and version_info[0] == 4:
        # Check only MAJOR version number
        from HumGen3D import Human

        addon_name = "HumGen3D"
    elif version_info and version_info[0] == 3:
        from humgen3d import Human  # Adjust the import based on your actual module structure

        addon_name = "humgen3d"
    else:
        from HumGen3D import Human

    def __init__(self):
        """
        Sets lists for base humans/hair/beard styles from humgen content folder
        """

        # enddef

    # enddef

    def CreateHumanFromJSON(self, _sJsonFile: str):
        """_summary_

        Parameters
        ----------
        _sJsonFile : str
            abs or relative file path with filename of human descritpion

        Returns
        -------
        blender object
            human armature, to be selected in blender by the given name
        Raises
        ------
        RuntimeError
            raises ...
        """
        bpy.ops.outliner.orphans_purge(do_recursive=True)
        # HumanArmature = None

        original_type = None
        try:
            original_type = bpy.context.area.type
        except Exception as xEx:
            print("Error storing original context area type:\n{}".format(str(xEx)))
        # endtry get area type

        try:
            bpy.context.area.type = "VIEW_3D"
        except Exception as xEx:
            print("Error setting context area type to 'VIEW_3D':\n{}".format(str(xEx)))
        # endtry set area type

        try:
            bpy.ops.object.select_all(action="DESELECT")
        except Exception as xEx:
            print("Error deselecting all objects:\n{}".format(str(xEx)))
        # end try deselect all

        try:
            bpy.ops.object.mode_set(mode="OBJECT", toggle=False)
        except Exception as xEx:
            print("Error setting mode to 'OBJECT':\n{}".format(str(xEx)))
        # endtry

        with open(_sJsonFile) as json_file:
            dictAnyhuman = json.load(json_file)

        if dictAnyhuman["bHandLabels"]:
            print("Hand label present")
            # TODO: Add handlabels
        # endif

        if dictAnyhuman["bFacialRig"]:
            print("facial rig present")
            # TODO: edit facs
        # endif

        self.human_obj = self.Human.from_preset(dictAnyhuman["dictHuman_V4"])
        self.human_obj.name = (_sJsonFile.rsplit("\\", 1)[1]).rsplit(".", 1)[0]
        return self.human_obj.objects.rig

    # enddef

    def ExportJSON(self, _sFilename: str):

        dictAnyhuman = {
            "bHandLabels": False,
            "bFacialRig": self.human_obj.expression.has_facial_rig,
            "sPoseFilename": "path/to/pose/file",
            "dictHuman_V4": self.human_obj.as_dict()
        }

        sCurrentDirectory = os.path.dirname(os.path.abspath(__file__))
        sJsonFile = os.path.join(sCurrentDirectory, "personas/" + _sFilename)

        with open(sJsonFile, 'w') as xFp:
            json.dump(dictAnyhuman, xFp, indent=4)
    # enddef

    def CreateFullRandomHuman(self, params:dict):
        """
            Create fully random human using the HumGen3D V4 API
            sName: Give the human a name
        """
        # Reading values from dict and defining variables
        # Gender
        gender = params["mParamConfig"]["sGender"]
        # Name
        ArmatureName = params["sId"]
        # Get preset for selected gender
        self.chosen_option = self.Human.get_preset_options(gender) 

        # Choose a random base human
        self.human_obj = self.Human.from_preset(random.choice(self.chosen_option))

        # Choose a random integer between 20 and 81 for age
        iHuman_age = random.randrange(20, 81)
        self.human_obj.age.set(iHuman_age)

        # Create dict with random body key values
        random_body_dict = {}
        for i, v in enumerate(self.human_obj.body.keys):
            v.value = random.random()
            random_body_dict.update({v.name : v.value})

        # Randomize clothing
        # Footwear
        footwear = self.human_obj.clothing.footwear
        lFootwear = footwear.get_options()
        sFootwear = random.choice(lFootwear)
        footwear.set(sFootwear)
        # Add a random pattern to footwear
        # TODO check also if pattern parameter are showing via as_dict() function
        if random.random() < 0.5:
            lRandomPattern = footwear.pattern.get_options()
            sFootwearRandomPattern = random.choice(lRandomPattern)
            # to some footwear patterns can not be applied, e.g. garden boots
            try:
                footwear.pattern.set(sFootwearRandomPattern, footwear.objects[0])
            except IndexError:
                pass
            # Apply random base color to the footwear
            # TODO: Dive into blender shaders and do it without Humgens randomize color function
            footwear.randomize_colors(footwear.objects[0])
        else:
            pass

        # Outfit
        outfit = self.human_obj.clothing.outfit
        lOutfits = outfit.get_options()
        sOutfits = random.choice(lOutfits)
        outfit.set(sOutfits)
        # Get list of  pattern for outfit
        lOutfits = outfit.pattern.get_options()
        # TODO check also if pattern parameter are showing via as_dict() function
        # As the outfits have different number of parts (jacket, trousers, tie,...) we need to loop over them
        for i, k in enumerate(outfit.objects):
            # Add a random pattern to each of the different outfit parts
            if random.random() < 0.5:
                outfit.pattern.set(random.choice(lOutfits), outfit.objects[i])
            # Apply random base color to the different parts of the outfits
            # TODO: Dive into blender shaders and do it without Humgens randomize color function
            elif random.random() < 0.5:
                outfit.randomize_colors(outfit.objects[i])
            else:
                pass

            # endif
        # endfor

        # Eyes
        eyes = self.human_obj.eyes
        # Change iris color with Humgens randomize color function
        # TODO: Dive into blender shaders and do it without Humgens randomize color function
        eyes.randomize()
        # TODO: Change sclera color within a reasonable range

        # Face
        face = self.human_obj.face
        # Randomize the face using HumGen Function
        face.randomize()
        # Randomize face with own functions
        # face_dict = dict()
        # for i, v in enumerate(face.keys):
        #     v.value = random.random()
        #     face_dict.update({v.name : v.value})

        # Hair
        # Eye brows
        eyebrows = self.human_obj.hair.eyebrows
        # Fast (0) or accurate shaders (1)
        eyebrows.fast_or_accurate = 1 # Accurate
        eyebrows.hue.value = random.random()
        eyebrows.lightness.value = random.random()
        eyebrows.redness.value = random.random()
        eyebrows.root_lightness.value = random.random()
        eyebrows.root_redness.value = random.random()
        eyebrows.root_redness.value = random.random()
        eyebrows.roots.value = random.random()
        eyebrows.roots_hue.value = random.random()
        eyebrows.roughness.value = random.random()
        eyebrows.salt_and_pepper.value = random.random()
        # Eye lashes
        eyelashes =  self.human_obj.hair.eyelashes
        # Fast (0) or accurate shaders (1)
        eyelashes.fast_or_accurate = 1 # Accurate
        eyelashes.hue.value = random.random()
        eyelashes.lightness.value = random.random()
        eyelashes.redness.value = random.random()
        eyelashes.root_lightness.value = random.random()
        eyelashes.root_redness.value = random.random()
        eyelashes.roots.value = random.random()
        eyelashes.roots_hue.value = random.random()
        eyelashes.roughness.value = random.random()
        eyelashes.salt_and_pepper.value = random.random()
        # Face hair
        if gender == "male":
            face_hair =  self.human_obj.hair.face_hair 
            if random.random() < 0.5:
                # Set a random face hair
                face_hair.set_random()
                # Fast (0) or accurate shaders (1)
                face_hair.fast_or_accurate = 1 # Accurate
                # Set random face hair using a humgen function
                face_hair.hue.value = random.random()
                face_hair.lightness.value = random.random()
                face_hair.lightness.value = random.random()
                face_hair.redness.value = random.random()
                face_hair.root_lightness.value = random.random()
                face_hair.root_redness.value = random.random()
                face_hair.roots.value = random.random()
                face_hair.roots_hue.value = random.random()
                face_hair.roughness.value = random.random()
                face_hair.salt_and_pepper.value = random.random()
            # endif
        # endif

        # Regular hair
        hair =  self.human_obj.hair.regular_hair
        if random.random() < 0.5:
            # Set a random face hair
            hair.set_random()
            # Fast (0) or accurate shaders (1)
            hair.fast_or_accurate = 1 # Accurate
            # Set random face hair using a humgen function
            hair.hue.value = random.random()
            hair.lightness.value = random.random()
            hair.lightness.value = random.random()
            hair.redness.value = random.random()
            hair.root_lightness.value = random.random()
            hair.root_redness.value = random.random()
            hair.roots.value = random.random()
            hair.roots_hue.value = random.random()
            hair.roughness.value = random.random()
            hair.salt_and_pepper.value = random.random()

        # endif

        # Height

        # Skin
        skin =  self.human_obj.skin
        # General settings
        skin.set_subsurface_scattering(True) # Turn on SSS
        # Parameters
        skin.cavity_strength.value = random.random()
        skin.freckles.value = random.uniform(0, 0.5)
        if gender == "male":
            skin.gender_specific.beard_shadow.value = random.random()
            skin.gender_specific.mustache_shadow.value = random.random()
        else:
            pass
        skin.normal_strength.value = random.uniform(0, 10)
        skin.redness.value = random.random()
        skin.roughness_multiplier.value = random.uniform(-10000, 10000)
        skin.saturation.value = random.uniform(0, 2)
        skin.splotches.value = random.uniform(0, 0.5)
        skin.tone.value = random.uniform(0, 3)
        # endif

        # Enable FACS
        self.human_obj.expression.load_facial_rig()

        # Set the name of the armature
        bpy.data.objects["HG_" + self.human_obj.name].name = ArmatureName       
        
    # enddef








###########################################################################################################
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    # enddef


# endclass


###########################################################################################################
class SingletonHumGenWrapper(HumGenWrapper, metaclass=Singleton):
    pass


# endclass
