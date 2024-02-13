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


from . import tools

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

        addon_path = bpy.context.preferences.addons[HumGenWrapper.addon_name].preferences["filepath_"]
        content_packs_path = os.path.join(addon_path, "content_packs")
        base_human_path = os.path.join(addon_path, "models")
        hair_path = os.path.join(addon_path, "hair")
        outfit_path = os.path.join(addon_path, "outfits")

        class HumGenConfigValues:
            def __init__(self):
                self.list_females = []
                self.list_males = []
                self.dict_female_head_hair = {}
                self.dict_male_head_hair = {}
                self.dict_male_face_hair = {}
                self.dict_female_outfits = collections.defaultdict(list)
                self.dict_male_outfits = collections.defaultdict(list)

            # enddef

        # endclass

        self.generator_config = HumGenConfigValues()
        


        for dir_, _, files in os.walk(base_human_path):
            for file_name in files:
                rel_dir = os.path.relpath(dir_, base_human_path)
                rel_file = os.path.join("models", rel_dir, file_name)
                rel_file = os.path.sep + rel_file
                if ".json" in rel_file:
                    file_name = os.path.splitext(os.path.basename(rel_file))[0]
                    if "female" in rel_file:
                        self.generator_config.list_females.append(file_name)
                    elif "male" in rel_file:
                        self.generator_config.list_males.append(file_name)
                    # endif gender
                # endif model
            # endfor
        # endfor

        for dir_, _, files in os.walk(hair_path):
            for file_name in files:
                rel_dir = os.path.relpath(dir_, hair_path)
                rel_file = os.path.join("hair", rel_dir, file_name)
                rel_file = os.path.sep + rel_file
                if "head" in rel_file and ".json" in rel_file:
                    file_name = os.path.splitext(os.path.basename(rel_file))[0]
                    if "female" in rel_file:
                        self.generator_config.dict_female_head_hair[file_name] = rel_file
                    elif "male" in rel_file:
                        self.generator_config.dict_male_head_hair[file_name] = rel_file
                    # endif gender
                if "face_hair" in rel_file and ".json" in rel_file:
                    file_name = os.path.splitext(os.path.basename(file_name))[0]
                    self.generator_config.dict_male_face_hair[file_name] = rel_file
                # endif face/head hair
            # endif hair
        # endfor

        for dir_, _, files in os.walk(outfit_path):
            for file_name in files:
                rel_dir = os.path.relpath(dir_, hair_path)
                rel_file = os.path.join("outputs", rel_dir, file_name)
                rel_file = os.path.sep + rel_file
                components = Path(rel_file).parts
                if ".blend" in rel_file and len(components) > 5:
                    set_name = components[5]
                    file_name = os.path.splitext(os.path.basename(rel_file))[0]

                    # skip faulty outfits
                    if file_name in ["BBQ_Barbara", "New_Intern"]:
                        continue

                    if "female" in rel_file:
                        self.generator_config.dict_female_outfits[set_name].append(file_name)
                    elif "male" in rel_file:
                        self.generator_config.dict_male_outfits[set_name].append(file_name)
                    # endif gender
                # endif face/head hair
            # endif hair
        # endfor

        if len(self.generator_config.list_males) == 0:
            raise RuntimeError("list of male model files empty")

        if len(self.generator_config.dict_male_head_hair) == 0:
            raise RuntimeError("list of male hair model files empty")

        if len(self.generator_config.dict_male_face_hair) == 0:
            raise RuntimeError("list of male face hair model files empty")

        if len(self.generator_config.list_females) == 0:
            raise RuntimeError("list of female model files empty")

        if len(self.generator_config.dict_female_head_hair) == 0:
            raise RuntimeError("list of female hair model files empty")

        if len(self.generator_config.dict_female_outfits) == 0:
            raise RuntimeError("list of female outfit files empty")

        if len(self.generator_config.dict_male_outfits) == 0:
            raise RuntimeError("list of male outfit files empty")

        self.generator_config.dict_bodies = {
            "male": self.generator_config.list_males,
            "female": self.generator_config.list_females,
        }
        self.generator_config.dict_hair = {
            "male": self.generator_config.dict_male_head_hair,
            "female": self.generator_config.dict_female_head_hair,
        }

        self.generator_config.dict_outfits = {
            "male": self.generator_config.dict_male_outfits,
            "female": self.generator_config.dict_female_outfits,
        }

        try:
            self.generator_config.persona_path = Path(bpy.context.space_data.text.filepath).parent.resolve()
        except AttributeError:
            self.generator_config.persona_path = Path(__file__).parent.resolve()
        # endtry
        self.generator_config.persona_path = Path.joinpath(self.generator_config.persona_path, "personas")

    # enddef

    ############################################################################################
    def _make_rel_path(self, s):
        if os.name == "nt":
            s = s.replace("/", "\\")
        return s

    # enddef

    ############################################################################################

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

        self.human_obj = self.Human.from_preset(_sJsonFile)

        return self.human_obj.objects.rig

    def CreateFullRandomHuman(self, sGender:str):
        """ 
            Create fully random human using the HumGen3D V4 API
            sName: Give the human a name
        """

        # Get preset for selected gender
        self.chosen_option = self.Human.get_preset_options(sGender) 

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
        if sGender == "male":
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
        if sGender == "male":
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
    
        # Save all values to JSON
        
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
