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

from .labelling.cls_label_skeleton import BoneLabel


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
        addon_path = bpy.context.preferences.addons[self.addon_name].preferences["filepath_"]
        content_packs = os.path.join(addon_path, "content_packs")
        textures = os.path.join(content_packs, "8K_Textures.json")
        base_humans = os.path.join(content_packs, "Base_Humans.json")
        base_hair = os.path.join(content_packs, "Base_Hair.json")
        base_clothes = os.path.join(content_packs, "Base_Clothes.json")
        base_poses = os.path.join(content_packs, "Base_Poses.json")

        class HumGenConfigValues:
            def __init__(self):
                self.dict_textures = {}  # Textures
                self.dict_models = {}  # Humans
                self.dict_regular_hair = {}  # Hair
                self.dict_face_hair = {}  # Face hair
                self.dict_clothes = {}  # Clothes
                self.dict_footwear = {}  # Footwear
                self.dict_poses = {}  # Poses

            def CreateDictionary(self, filelist: list, gender_position: int):
                """
                Creates dictionaries for regular hair, textures, models, regular head hair, and face hair based on the given file list.

                Parameters:
                - filelist (list): A list of file paths.
                - gender_position (int): The position of gender ("male" or "female") in the file path.

                Returns:
                - dictName (dict)
                """
                dictName = {}
                for file_path in filelist:
                    components = file_path.split("/")
                    gender = components[gender_position]  # Extracting the gender (second component)
                    filename = components[-1].split(".")[0]  # Extracting the filename without extension
                    if gender == "male":
                        if gender not in dictName:
                            dictName[gender] = {}
                        dictName[gender][filename] = file_path
                    if gender == "female":
                        if gender not in dictName:
                            dictName[gender] = {}
                        dictName[gender][filename] = file_path
                    else:
                        if gender not in dictName:
                            dictName[gender] = {}
                        dictName[gender][filename] = file_path
                return dictName
                # enddef

        self.generator_config = HumGenConfigValues()

        # Create textures dictionary
        with open(textures) as json_file:
            dict = json.load(json_file)
            filtered_elements = [
                file
                for file in dict["files"]
                if ("Default 8K" in file)
                and (("female" in file) or ("male" in file))
                and file.endswith(".png")
                and "__MACOSX" not in file
                and "PBR" not in file
            ]

        self.generator_config.dict_textures = HumGenConfigValues.CreateDictionary(self, filtered_elements, 1)

        # Create models dictionary
        with open(base_humans) as json_file:
            dict = json.load(json_file)
            filtered_elements = [
                file
                for file in dict["files"]
                if ("models" in file)
                and (("female" in file) or ("male" in file))
                and file.endswith(".json")
                and "__MACOSX" not in file
            ]

        self.generator_config.dict_models = HumGenConfigValues.CreateDictionary(self, filtered_elements, 1)

        # Create regular head hair dictionary
        with open(base_hair) as json_file:
            dict = json.load(json_file)
            filtered_elements = [
                file
                for file in dict["files"]
                if "head" in file and (("female" in file) or ("male" in file)) and file.endswith(".json")
            ]

        self.generator_config.dict_regular_hair = HumGenConfigValues.CreateDictionary(self, filtered_elements, 2)

        # Create face hair dictionary
        with open(base_hair) as json_file:
            dict = json.load(json_file)
            filtered_elements = [file for file in dict["files"] if "face_hair" in file and file.endswith(".json")]
        for file_path in filtered_elements:
            components = file_path.split("/")
            gender = "male"  # Only male have facial hair
            filename = components[-1].split(".")[0]  # Extracting the filename without extension
            if gender == "male":
                if gender not in self.generator_config.dict_face_hair:
                    self.generator_config.dict_face_hair[gender] = {}
                self.generator_config.dict_face_hair[gender][filename] = file_path

        # Create Clothes dictionary
        with open(base_clothes) as json_file:
            dict = json.load(json_file)
            filtered_elements = [
                file
                for file in dict["files"]
                if "outfits" in file and (("female" in file) or ("male" in file)) and file.endswith(".blend")
            ]

        self.generator_config.dict_clothes = HumGenConfigValues.CreateDictionary(self, filtered_elements, 1)

        # Create Footwear dictionary
        with open(base_clothes) as json_file:
            dict = json.load(json_file)
            filtered_elements = [
                file
                for file in dict["files"]
                if "footwear" in file and (("female" in file) or ("male" in file)) and file.endswith(".blend")
            ]

        self.generator_config.dict_footwear = HumGenConfigValues.CreateDictionary(self, filtered_elements, 1)

        # Create Footwear dictionary
        with open(base_clothes) as json_file:
            dict = json.load(json_file)
            filtered_elements = [
                file
                for file in dict["files"]
                if "footwear" in file and (("female" in file) or ("male" in file)) and file.endswith(".blend")
            ]

        self.generator_config.dict_footwear = HumGenConfigValues.CreateDictionary(self, filtered_elements, 1)

        # Create Poses dictionary
        with open(base_poses) as json_file:
            dict = json.load(json_file)
            filtered_elements = [file for file in dict["files"] if "poses" in file and file.endswith(".blend")]

        self.generator_config.dict_poses = HumGenConfigValues.CreateDictionary(self, filtered_elements, 1)
        # enddef

        # Add info about humgenv4 addon path
        self.generator_config.dict_info = {"HumGenV4 Path": addon_path}

    # enddef

    def AddLabelsFromJSON(self, _sHandLabelFile: str):
        objRig = self.human_obj.objects.rig
        objArmature = objRig.data
        self.xBoneLabel.AddHandLabels(_sLabelFile=_sHandLabelFile, _objArmature=objArmature, _objRig=objRig)
        return

    # enddef

    def CreateHumanFromJSON(self, _sJsonFile: str):
        """_summary_

        Parameters
        ----------
        _sJsonFile : str
            abs file path with filename of human description in JSON format

        Returns
        -------
        blender object
            human armature, to be selected in blender by the given name

        Raises
        ------
        RuntimeError
            raises ...
        """

        try:
            with open(_sJsonFile) as json_file:
                dictAnyhuman = json.load(json_file)
        except FileNotFoundError:
            return
        except json.JSONDecodeError as e:
            print(f"Invalid JSON syntax: {e}")
            return

        try:
            self.human_obj = self.Human.from_preset(dictAnyhuman["dictHumGen_V4"])
        except KeyError as e:
            print(f"ERROR: {e}")

        self.human_obj.name = (_sJsonFile.rsplit("\\", 1)[1]).rsplit(".", 1)[0]

        try:
            self.xBoneLabel = BoneLabel(_human=self.human_obj)
        except AttributeError as e:
            print("Human not generated successfully")
            print(f"ERROR: {e}")
            return

        if dictAnyhuman["dictCustom"]["bOpenPoseHandLabels"]:
            # TODO: clean code, pass _sHandLabelFile dynamically
            sHandLabelFile = "C:\\h4\\image-render-setup\\repos\\image-render-blender-human\\src\\anyhuman2\\labelling\\mapping\\openpose_hand_humgen.json"
            self.AddLabelsFromJSON(_sHandLabelFile=sHandLabelFile)
        # endif

        if dictAnyhuman["dictCustom"]["bFacialRig"]:
            self.human_obj.expression.load_facial_rig()
            sWFLWLableFile = "C:\\h4\\image-render-setup\\repos\\image-render-blender-human\\src\\anyhuman2\\labelling\\mapping\\WFLW_bones.json"
            self.xBoneLabel.ImportSkeletonData(_sSkeletonDataFile=sWFLWLableFile)
        # endif

        return self.human_obj.objects.rig

    # enddef

    def ExportJSON(self, _sFilename: str):
        # INFO: stock bones 102, after adding 42 handlabels, 144
        # TODO: Better validation required,
        if len(self.human_obj.objects.rig.data.bones) == 144:
            bOpenPoseHandLabelsPresent = True
        else:
            bOpenPoseHandLabelsPresent = False

        dictAnyhuman = {
            "dictCustom": {
                "sGender": self.human_obj.gender,
                "bOpenPoseHandLabels": bOpenPoseHandLabelsPresent,
                "bFacialRig": self.human_obj.expression.has_facial_rig,
                "sPoseFilename": self.human_obj.pose.as_dict(),
                "dBeardLength": self.dBeardLength,
            },
            "dictHumGen_V4": self.human_obj.as_dict(),
        }

        sCurrentDirectory = os.path.dirname(os.path.abspath(__file__))
        sJsonFile = os.path.join(sCurrentDirectory, "personas/" + _sFilename)

        with open(sJsonFile, "w") as xFp:
            json.dump(dictAnyhuman, xFp, indent=4)

    # enddef

    def CreateHuman(self, generatedParams: dict):
        """
        Create human from a dictAnyhuman (or a dictHumGen_V4 dictionary) which is a composition of the standard
        HumGenV4 as_dict() + some additional parameters such as gender, pose, labels,...
        dictAnyhuman: dictionary, containing information about the human that will be generated.
        Parameters:
            - params (dict): catharsys like dictionary
            - generatedParams (dict): dictAnyhuman
            Returns:
            - dictName (dict)
        """
        # Reading values from dict and splitting it to custom and HumGenV4 dicts
        # case: anyhuman dictionary (= custom dict + humgen dict)
        if "dictCustom" in generatedParams.keys():
            dictCustom = generatedParams["dictCustom"]
            dictHumGenV4 = generatedParams["dictHumGen_V4"]
            sGender = dictCustom["sGender"]
            self.dBeardLength = dictCustom["dBeardLength"]
            # Get preset for selected gender
            self.chosen_option = self.Human.get_preset_options(sGender)
            # Use previously generated HumGenV4 compatible directory
            self.human_obj = self.Human.from_preset(dictHumGenV4)
            self.xBoneLabel = BoneLabel(_human=self.human_obj)
            if self.xBoneLabel is None:
                print("ERROR: Human not generated successfully, hence instance of BoneLabel not created")
            # If dbeardLength is not empty (False), custom parameters must be loaded after human has been created
            if sGender == "male" and bool(dictCustom["dBeardLength"]) == True:
                for i, key in enumerate(self.dBeardLength["hair_systems"]):
                    # obtain the particle system which is connected to the hair system
                    particle_system = self.human_obj.hair.particle_systems[key].settings.name
                    # Set the length of the respective particle system to the value in the dict
                    bpy.data.particles[particle_system].child_length = self.dBeardLength["hair_systems"][key]["length"]
            else:
                pass
            # endif
            # Set facial rig
            if dictCustom["bFacialRig"] is True:
                self.human_obj.expression.load_facial_rig()
                # TODO: pass sWFLWLableFile  dynamically
                sWFLWLableFile = "C:\\h4\\image-render-setup\\repos\\image-render-blender-human\\src\\anyhuman2\\labelling\\mapping\\WFLW_bones.json"
                # TODO: Fix eyebrow_WFLW labels
                self.xBoneLabel.ImportSkeletonData(_sSkeletonDataFile=sWFLWLableFile)
            else:
                pass
            # endif
            # Add hand labels
            if dictCustom["bOpenPoseHandLabels"] is True:
                # TODO: pass sHandLabelFile dynamically
                sHandLabelFile = "C:\\h4\\image-render-setup\\repos\\image-render-blender-human\\src\\anyhuman2\\labelling\\mapping\\openpose_hand_humgen.json"
                self.AddLabelsFromJSON(_sHandLabelFile=sHandLabelFile)
            else:
                pass
            # endif
        # case: only humgen dictionary
        else:
            if generatedParams["keys"]["Male"] >= 0.5:
                sGender = "male"
                dictHumGenV4 = generatedParams
            else:
                sGender = "female"
                dictHumGenV4 = generatedParams
            # endif
        # endif
        return self.human_obj.props["body_obj"]

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
