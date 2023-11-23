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

try:
    from humgen3d.API import HG_Human, HG_Batch_Generator
except Exception as xEx:
    print("Error initializing anyhuman module:\n{}".format(str(xEx)))
# endtry

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
    def __init__(self):
        """
        Sets lists for base humans/hair/beard styles from humgen content folder
        """
        addon_name = "humgen3d"
        addon_path = bpy.context.preferences.addons[addon_name].preferences["filepath"]
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
    def CreateHuman(self, _sName, _mParams, _bDeleteBackup=True):
        """
        generates a random human given gender and name

        Parameters
        ----------
        _sName : string
            name human armature should get. The name, the huamn generator creates automatically
            is overwritten by this name
        _mParams: dict
            dictionary of all values that should be used for generation of the human

        Returns
        -------
        blender object
            human armature, to be selected in blender by the given name
        Raises
        ------
        RuntimeError
            raises "Unknown gender" if gender is not either "male" or "female"
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

        # Possibilities to make sure, no object is selected, if selected objects bring trouble
        # try:
        #     bpy.context.view_layer.objects.active = None
        # except Exception as e:
        #     print(e)

        # for obj in bpy.context.selected_objects:
        #    obj.select_set(False)
        # for obj in bpy.data.objects:
        #     obj.select_set(False)

        try:
            bpy.ops.object.select_all(action="DESELECT")
        except Exception as xEx:
            print("Error deselcting all objects:\n{}".format(str(xEx)))
        # end try deselect all

        try:
            bpy.ops.object.mode_set(mode="OBJECT", toggle=False)
        except Exception as xEx:
            print("Error setting mode to 'OBJECT':\n{}".format(str(xEx)))
        # endtry

        sGender = _mParams["gender"]

        body_rel_file = "/models/{}/{}.json".format(sGender, _mParams["body"])
        body_rel_file = self._make_rel_path(body_rel_file)

        self.human_obj = HG_Human()

        # this needs to be run to populate internal values of the plugin
        self.human_obj.get_starting_human_options(gender=sGender)

        self.human_obj.create(chosen_starting_human=body_rel_file)

        name_human = self.human_obj.body_object.material_slots[0].name

        self._prepare_body(sGender, _mParams)
        self._prepare_skin(sGender, name_human, _mParams)
        self._prepare_eyes(sGender, _mParams)
        self._prepare_hair(sGender, name_human, _mParams)

        self.human_obj.finish_creation_phase()

        # calculate the bodies weight and volume
        skin = self.human_obj.body_object

        bm = bmesh.new()

        bm.from_object(skin, depsgraph=bpy.context.evaluated_depsgraph_get())

        volume = bm.calc_volume()
        self.human_obj.rig_object["volume"] = volume

        density = 1.0
        self.human_obj.rig_object["weight"] = volume * density * 1000.0

        self._prepare_outfit(sGender, _mParams)

        tools.FixClothBoneWeights(
            skinMesh=self.human_obj.body_object,
            clothMeshes=self.human_obj.clothing_objects,
        )

        self._prepare_pose(sGender, _mParams)

        self.human_obj.name = _sName

        # HumGen3D creates a backup collection that is needed in case
        # the user wants to go back to creation phase
        # since this is not needed here, the backup collection is deleted

        # print("Removing backup collection...")
        if _bDeleteBackup:
            RemoveCollection("HumGen_Backup [Don't Delete]")
        # print("done.")

        try:
            if original_type is not None:
                bpy.context.area.type = original_type
            # endif
        except Exception as xEx:
            print("Error setting context area type back to '{}':\n{}".format(original_type, str(xEx)))
        # endtry

        return self.human_obj.rig_object

    # enddef

    ############################################################################################
    def ModifyHuman(self, gender, _mParams):
        self._prepare_outfit(gender, _mParams)
        self._prepare_pose(gender, _mParams)

    # enddef

    ############################################################################################
    def _prepare_body(self, gender, params):
        # set skinny value to 0-0.2 as  persons too skinny look odd
        for number, key in enumerate(bpy.data.shape_keys):
            try:
                bpy.data.shape_keys[number].key_blocks["bp_Muscular"].value = params["muscular"]
                bpy.data.shape_keys[number].key_blocks["bp_Overweight"].value = params["overweight"]
                bpy.data.shape_keys[number].key_blocks["bp_Skinny"].value = params["skinny"]
            except Exception as e:
                print(e)
            # endtry
        # endfor

        bpy.data.scenes["Scene"].HG3D.human_length = params["height"]

        if params["face"] == "random":
            bpy.ops.hg3d.random(random_type="face_all")

        elif "variation" in params["face"]:
            for number, key in enumerate(bpy.data.shape_keys):
                try:
                    bpy.data.shape_keys[number].key_blocks["pr_asian"].value = 0.0
                    bpy.data.shape_keys[number].key_blocks["pr_black"].value = 0.0
                    bpy.data.shape_keys[number].key_blocks["pr_caucasian"].value = 0.0
                    bpy.data.shape_keys[number].key_blocks["pr_{}".format(params["face"])].value = 1.0
                except Exception as e:
                    print(e)
                # endtry
            # endfor
        else:
            raise NotImplementedError
        # endif

    # enddef

    ############################################################################################
    def _prepare_skin(self, _sGender, _sNameHuman, _mParams):
        nodes = bpy.data.materials[_sNameHuman].node_tree.nodes
        dicSkin = _mParams["skin"]

        # skin parameters
        nodes["Skin_tone"].inputs[1].default_value = dicSkin["tone"]
        nodes["Skin_tone"].inputs[2].default_value = dicSkin["redness"]
        nodes["Skin_tone"].inputs[3].default_value = dicSkin["saturation"]
        nodes["Normal Map"].inputs[0].default_value = dicSkin["normal_strength"]
        nodes["R_Multiply"].inputs[1].default_value = dicSkin["roughness_multiplier"]

        bpy.data.scenes["Scene"].HG3D.skin_sss = "on"
        bpy.data.scenes["Scene"].HG3D.underwar_switch = "on"

        nodes["Darken_hsv"].inputs[2].default_value = dicSkin["dark_areas"]
        nodes["Lighten_hsv"].inputs[2].default_value = dicSkin["light_areas"]
        nodes["Freckles_control"].inputs[3].default_value = dicSkin["freckles"]
        nodes["Splotches_control"].inputs[3].default_value = dicSkin["splotches"]
        nodes["BS_Control"].inputs[1].default_value = dicSkin["beauty_spots_amount_"]
        nodes["BS_Control"].inputs[2].default_value = dicSkin["beauty_spots_amount"]
        nodes["BS_Opacity"].inputs[1].default_value = dicSkin["beauty_spots_opacity"]

        xPriBsdfIns = nodes["Principled BSDF"].inputs
        if "Subsurface" in xPriBsdfIns:
            xPriBsdfIns["Subsurface"].default_value = 0.07
        elif "Subsurface Weight" in xPriBsdfIns:
            xPriBsdfIns["Subsurface Weight"].default_value = 0.07
        else:
            RuntimeError("Cannot find subsurface parameter of 'Principled BSDF' node")
        # endif

        # set sacked skin
        for number, key in enumerate(bpy.data.shape_keys):
            try:
                bpy.data.shape_keys[number].key_blocks["age_old.Transferred"].value = dicSkin["sagging"]
            except Exception as e:
                print(e)
            # endtry
        # endfor

        # bpy.data.shape_keys["Key.001"].key_blocks["age_old.Transferred"].value = 0.2
        nodes["HG_Age"].inputs[1].default_value = dicSkin["wrinkles"]

        # setting beard shadow for male and make-up for female
        if _sGender == "male":
            try:
                nodes["Gender_Group"].inputs[2].default_value = _mParams["beard"]["shadow_mustache"]
                nodes["Gender_Group"].inputs[3].default_value = _mParams["beard"]["shadow_beard"]
            except TypeError:
                pass
            except ValueError:
                pass
            except KeyError:
                pass
            # endtry

        elif _sGender == "female":
            try:
                xGenGrpIn = nodes["Gender_Group"].inputs
                dicMakeup = _mParams["makeup"]

                # add make up but no foundation
                xGenGrpIn[2].default_value = dicMakeup["foundation_amount"]
                xGenGrpIn[3].default_value = dicMakeup["foundation_color"]
                xGenGrpIn[4].default_value = dicMakeup["blush_opacity"]
                xGenGrpIn[5].default_value = dicMakeup["blush_color"]
                xGenGrpIn[6].default_value = dicMakeup["eyeshadow_opacity"]
                xGenGrpIn[7].default_value = dicMakeup["eyeshadow_color"]
                xGenGrpIn[8].default_value = dicMakeup["lipstick_opacity"]
                xGenGrpIn[9].default_value = dicMakeup["lipstick_color"]
                xGenGrpIn[10].default_value = dicMakeup["eyeliner_opacity"]
                xGenGrpIn[11].default_value = dicMakeup["eyeliner_color"]
            except TypeError:
                pass
            except KeyError:
                pass
            # endtry

        else:
            raise RuntimeError("Unknown gender")
        # endif gender

    # enddef

    ############################################################################################
    def _prepare_eyes(self, gender, params):
        eye_nodes = bpy.data.materials[".HG_Eyes_Inner"].node_tree.nodes
        eye_nodes["HG_Eye_Color"].inputs[2].default_value = params["eyes"]["iris_color"]

        if "eyebrows_style" in params["eyes"]:
            eyebrowsindex = -1
            try:
                eyebrowsindex = int(params["eyes"]["eyebrows_style"])
            except ValueError:
                pass

            if params["eyes"]["eyebrows_style"] == "random":
                raise RuntimeError(
                    "random value not supported here, has to be resolved before with ResolveRandomParameters(...)"
                )
                eyebrowsindex = random.randint(0, 10)
            elif eyebrowsindex != -1:
                pass
            else:
                raise NotImplementedError
            # endif

            for i in range(0, eyebrowsindex):
                bpy.ops.hg3d.eyebrowswitch(forward=True)
            # endfor
        # endif

    # enddef

    ############################################################################################
    def _prepare_hair(self, _sGender, _sNameHuman, _mParams):
        # nodes = bpy.data.materials[name_human].node_tree.nodes

        bpy.data.scenes["Scene"].HG3D.hair_sub = "All"
        bpy.context.scene.HG3D.hair_shader_type = "accurate"

        dicHair = _mParams["hair"]

        sHairKey = dicHair.get("hair_style")
        if sHairKey is not None:
            hair_style_file = self.generator_config.dict_hair[_sGender][sHairKey]
            hair_style_file = self._make_rel_path(hair_style_file)
            bpy.data.scenes["Scene"].HG3D.pcoll_hair = hair_style_file

            # bpy.data.scenes["Scene"].HG3D.hair_length_ui = dicHair['length']

            hair_head_nodes = self.human_obj.body_object.material_slots[2].material.node_tree.nodes["HG_Hair_V3"]

            hair_head_nodes.inputs[0].default_value = dicHair["lightness"]
            hair_head_nodes.inputs[1].default_value = dicHair["redness"]
            hair_head_nodes.inputs[2].default_value = dicHair["roughness"]
            hair_head_nodes.inputs[3].default_value = dicHair["salt_and_pepper"]
            hair_head_nodes.inputs[4].default_value = dicHair["roots"]
            hair_head_nodes.inputs[8].default_value = dicHair["hue"]

            hair_eye_nodes = self.human_obj.body_object.material_slots[1].material.node_tree.nodes["HG_Hair_V3"]

            dicEyes = _mParams["eyes"]
            hair_eye_nodes.inputs[0].default_value = dicEyes["hair_lightness"]
            hair_eye_nodes.inputs[1].default_value = dicEyes["hair_redness"]
            hair_eye_nodes.inputs[2].default_value = dicEyes["hair_roughness"]
        # endif

        # setting beard for male
        if _sGender == "male":
            if "beard" in _mParams and _mParams["beard"]["beard_style"] is not None:
                bpy.data.scenes["Scene"].HG3D.face_hair_sub = "All"

                beard_key = _mParams["beard"]["beard_style"]
                beard_style_file = self.generator_config.dict_male_face_hair[beard_key]
                beard_style_file = self._make_rel_path(beard_style_file)

                bpy.data.scenes["Scene"].HG3D.pcoll_face_hair = beard_style_file
            # endif
        # endif gender

    # enddef

    ############################################################################################
    def _prepare_outfit(self, _sGender, _mParams):
        ##################################################################
        def getValue(set, key, name, index, default):
            try:
                if key not in set:
                    return default
                elif isinstance(set[key], dict):
                    for dictKey, dictValue in set[key].items():
                        if dictKey in name:
                            return dictValue
                        # endif
                    # endfor
                elif isinstance(set[key], list):
                    # if the config set is a list
                    # return the value of the list at index
                    # and if out of bounds, return last in list
                    index = min(index, len(set[key]) - 1)
                    return set[key][index]
                else:
                    # otherwise simply return the value of configuration set
                    return set[key]
            except Exception as e:
                print("getting value for", set, key, name, "failed! \n", e)
                raise e

        # enddef

        ##################################################################
        def adjustDefaultColorHSV(_xNodeCtr, _fFacH, _fFacS, _fFacV):
            fR = _xNodeCtr.default_value[0]
            fG = _xNodeCtr.default_value[1]
            fB = _xNodeCtr.default_value[2]

            tHsv = colorsys.rgb_to_hsv(fR, fG, fB)
            tRgbDark = colorsys.hsv_to_rgb(tHsv[0] * _fFacH, tHsv[1] * _fFacS, tHsv[2] * _fFacV)

            _xNodeCtr.default_value[0] = tRgbDark[0]
            _xNodeCtr.default_value[1] = tRgbDark[1]
            _xNodeCtr.default_value[2] = tRgbDark[2]

        # endef

        ##################################################################
        def tryAdjustDefaultInputColorHSV(_xNode, _sName, _fFacH, _fFacS, _fFacV):
            xNodeCtr = _xNode.inputs.get(_sName)
            if xNodeCtr is not None:
                adjustDefaultColorHSV(xNodeCtr, _fFacH, _fFacS, _fFacV)
            # endif

        # enddef

        ##################################################################

        dicOutfit = _mParams.get("outfit")
        dicFootwear = _mParams.get("footwear")

        if "outfit" in _mParams and "outfit_style" in dicOutfit:

            def _setOutfit(outfit_style):
                # first choose a random outfit type, otherwise list of options is wrongly
                # populated
                bpy.ops.hg3d.random(random_type="outfit")
                outfit = "/outfits/{}/{}.blend".format(_sGender, outfit_style)
                outfit = self._make_rel_path(outfit)
                bpy.data.scenes["Scene"].HG3D.pcoll_outfit = outfit

            if dicOutfit["outfit_style"] == "random":
                raise RuntimeError(
                    "random value not supported here, has to be resolved before with ResolveRandomParameters(...)"
                )
            elif isinstance(dicOutfit["outfit_style"], str):
                _setOutfit(dicOutfit["outfit_style"])
            else:
                raise NotImplementedError
            # endif
        # endif

        if "footwear" in _mParams and "footwear_style" in dicFootwear:
            if dicFootwear["footwear_style"] == "random":
                bpy.ops.hg3d.random(random_type="footwear")

            elif "/footwear" in dicFootwear["footwear_style"]:
                # first choose a random footwear type, otherwise list of options is wrongly
                # populated
                bpy.ops.hg3d.random(random_type="footwear")
                footwear_file = self._make_rel_path(dicFootwear["footwear_style"])
                bpy.data.scenes["Scene"].HG3D.pcoll_footwear = footwear_file

            else:
                raise NotImplementedError
            # endif
        # endif

        # objects_not_to_pattern = ["HG_Body", "HG_Eyes", "HG_TeethLower", "HG_TeethUpper", "Shoe", "Boot", "Sneaker"]
        # footwear = ["Shoe", "Boot", "Sneaker"]

        ##############################################################################
        # Processing cloths
        if dicOutfit is not None:
            lObjCloth = self.human_obj.clothing_objects
        else:
            lObjCloth = []
        # endif

        for index, objCloth in enumerate(lObjCloth):
            print("Clothing object: {}".format(objCloth.name))

            matCloth = objCloth.material_slots[0].material
            ndHgCtrl = matCloth.node_tree.nodes.get("HG_Control")
            if ndHgCtrl is None:
                print("> HG_Control node NOT found")
                continue
            # endif
            print("> HG_Control node found")

            # brightnessMod = params['outfit'].get(, 1.0)
            fBrightnessFactor = getValue(dicOutfit, "outfit_brightness", objCloth.name, index, 0.8)
            fSaturationFactor = getValue(dicOutfit, "outfit_saturation", objCloth.name, index, 0.8)

            # contrastMod = getValue(dicOutfit, 'outfit_contrast', objCloth.name, index, 2.2)
            outfit_color = getValue(dicOutfit, "outfit_color", objCloth.name, index, "random")
            palette = getValue(dicOutfit, "outfit_palette", objCloth.name, index, "C0")

            sOutfitPattern = getValue(dicOutfit, "outfit_pattern", objCloth.name, index, False)

            bpy.context.view_layer.objects.active = objCloth
            bpy.context.object.active_material = matCloth

            if outfit_color == "random":
                fR, fG, fB, _ = random.choice(list(color_dict[palette].values()))

            elif outfit_color in color_dict[palette]:
                fR, fG, fB, _ = color_dict[palette][outfit_color]

            else:
                raise NotImplementedError
            # endif

            ndHgCtrl.inputs["Main Color_C0"].default_value = (fR, fG, fB, 1.0)
            tryAdjustDefaultInputColorHSV(ndHgCtrl, "Main Color_C0", 1.0, fSaturationFactor, fBrightnessFactor)
            tryAdjustDefaultInputColorHSV(ndHgCtrl, "Stitches", 1.0, fSaturationFactor, fBrightnessFactor)
            tryAdjustDefaultInputColorHSV(ndHgCtrl, "Buttons", 1.0, fSaturationFactor, fBrightnessFactor)

            # insert bright/contrast node
            # base_color_node = ndHgCtrl.inputs["Diffuse"].links[0].from_node
            # mat.node_tree.links.remove(ndHgCtrl.inputs["Diffuse"].links[0])

            # bright_node = node.shader.color.BrightContrast(xSNT=mat.node_tree,
            #                                                sTitle="Bright/Contrast",
            #                                                xColor=base_color_node.outputs["Color"],
            #                                                xBright=-1.0,
            #                                                xContrast=contrastMod)
            # mat.node_tree.links.new(ndHgCtrl.inputs["Diffuse"], bright_node["Color"])

            # randomize roughness multiplier
            ndHgCtrl.inputs["Roughness Multiplier"].default_value = tools.RandomUniformDiscrete(0.8, 1.2, 11)

            # randomize normal strength
            ndHgCtrl.inputs["Normal Strength"].default_value = tools.RandomUniformDiscrete(1.8, 2.2, 11)

            if sOutfitPattern == "random":
                bpy.ops.hg3d.pattern(add=True)
                bpy.ops.hg3d.random(random_type="patterns")

                # only add a patter to every second cloth object
                if random.choice([True, False]):
                    bpy.ops.hg3d.pattern(add=True)
                    bpy.ops.hg3d.random(random_type="patterns")

                    # colorize every second pattern
                    if random.choice([True, False]):
                        bpy.ops.hg3d.color_random(input_name="PC1", color_group="C0")
                        bpy.ops.hg3d.color_random(input_name="PC2", color_group="C0")
                        bpy.ops.hg3d.color_random(input_name="PC3", color_group="C0")
                    # endif
                    # set opacity of every second pattern
                    if random.choice([True, False]):
                        ndHgCtrl.inputs[13].default_value = random.uniform(0.0, 1.0)
                    # endif
                # endif

                # Pattern
                # set brightness of pattern (consisting of PC1, PC2 and PC3) to a more natural level
                tryAdjustDefaultInputColorHSV(ndHgCtrl, "PC1", 1.0, 1.0, 0.6)
                tryAdjustDefaultInputColorHSV(ndHgCtrl, "PC2", 1.0, 1.0, 0.6)
                tryAdjustDefaultInputColorHSV(ndHgCtrl, "PC3", 1.0, 1.0, 0.6)
            # endif

            ndPrince = matCloth.node_tree.nodes.get("Principled BSDF")
            if ndPrince is not None:
                ndPrince.inputs["Specular"].default_value = 0.5
                ndPrince.inputs["Metallic"].default_value = 0.5
            # endif
            print("> done.")
        # endfor clothing

        ##############################################################################
        # Processing footwear
        if dicFootwear is not None:
            lObjFootwear = self.human_obj.footwear_objects
        else:
            lObjFootwear = []
        # endif

        for index, objFootwear in enumerate(lObjFootwear):
            print("Footwear object: {}".format(objFootwear.name))
            matFootwear = objFootwear.material_slots[0].material
            ndHgCtrl = matFootwear.node_tree.nodes.get("HG_Control")
            if ndHgCtrl is None:
                print("> HG_Control node NOT found")
                continue
            # endif
            print("> HG_Control node found")

            bpy.context.view_layer.objects.active = objFootwear
            bpy.context.object.active_material = matFootwear

            footwear_color = getValue(dicFootwear, "footwear_color", objFootwear.name, index, None)
            palette = getValue(dicFootwear, "footwear_palette", objFootwear.name, index, "C0")

            sOutfitPattern = getValue(dicOutfit, "outfit_pattern", objCloth.name, index, False)

            bpy.context.view_layer.objects.active = objCloth
            bpy.context.object.active_material = matCloth

            if footwear_color == "random":
                fR, fG, fB, _ = random.choice(list(color_dict[palette].values()))
            elif footwear_color in color_dict[palette]:
                fR, fG, fB, _ = color_dict[palette][outfit_color]
            # endif

            lColorNames = ["Main Color_C0", "Main Color"]

            for sColorName in lColorNames:
                try:
                    ndHgCtrl.inputs[sColorName]
                    break
                except KeyError:
                    pass
                # endtry
            # endfor

            if footwear_color is not None:
                ndHgCtrl.inputs[sColorName].default_value = (fR, fG, fB, 1.0)

            tryAdjustDefaultInputColorHSV(ndHgCtrl, sColorName, 1.0, 0.9, 0.8)
            tryAdjustDefaultInputColorHSV(ndHgCtrl, "Sole", 1.0, 0.9, 0.5)
            tryAdjustDefaultInputColorHSV(ndHgCtrl, "Back label", 1.0, 0.9, 0.8)

            ndPrince = matFootwear.node_tree.nodes.get("Principled BSDF")
            if ndPrince is not None:
                ndPrince.inputs["Specular"].default_value = 0.5
                ndPrince.inputs["Metallic"].default_value = 0.5
            # endif
            print("> done.")
        # endfor footwear

    # enddef

    ############################################################################################
    def _prepare_pose(self, gender, params):
        # get options need to called first to populate internal list
        lAvailablePoses = self.human_obj.get_pose_options()
        # print("Available Poses: {}".format(lAvailablePoses))

        # choose at least the base pose so the armature has the same bone configuration as the predefined poses
        # (see _match_roll(...) in HG_POSE.py)
        posefilename = params.get("posefilename")
        if posefilename is None:
            posefilename = self._make_rel_path("/poses/Base Poses/HG_A_Pose.blend")
        elif posefilename == "random":
            posefilename = random.choice(lAvailablePoses)
        else:
            posefilename = self._make_rel_path(posefilename)

        # print(f"Pose Filename: {posefilename}")

        # print("Setting pose...")
        self.human_obj.set_pose(chosen_pose_option=posefilename)
        print("done.")

        print("Setting pose filename...")
        bpy.data.scenes["Scene"].HG3D.pcoll_poses = posefilename
        print("done.")

        if "expression" in params:
            if params["expression"] == "random":
                bpy.ops.hg3d.random(random_type="expressions")
            elif "/expressions" in params["expression"]:
                expression_file = self._make_rel_path(params["expression"])
                bpy.data.scenes["Scene"].HG3D.pcoll_expressions = expression_file
            else:
                raise NotImplementedError
            # endif
        # endif

    # enddef


# endclass


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
