#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: \ops.py
# Created Date: Thursday, March 10th 2022, 3:44:28 pm
# Author: Christian Perwass (CR/AEC5)
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
import mathutils
import math

import random

import warnings
import json

from anybase import convert

from .cls_humgen import SingletonHumGenWrapper

from .paramgenerators import ComputeParams, ResolveRandomParams

try:
    from humgen3d.API import HG_Human, HG_Batch_Generator
except Exception as xEx:
    print("Error initializing anyhuman module:\n{}".format(str(xEx)))
# endtry


##############################################################################################################
def GenerateHuman(_dicParams, **kwargs):
    """
    Function for generating any human.

    It uses the HumGenWrapper class for first computation of a set of parameters that
    then will be used to create the human.

    The computation of parameters can be based on different approaches as full randomization,
    randomization by a Zwicky-Box specifcation, or directly by given parameters. For a detailed description,
    see the HumGenWrapper class.

    The _dicParams dictionaly can contain the keys:
    - sId: name that should be used for the generated blender object
    - xSeed: object for seeding the randomization
    - sMode: mode for computation of the parameters of the human
    - mParamConfig: dict with parameters for the parameter computation, see HumGenWrapper
    - mOverwrite: dict with parameters that should be used to overwrite the computed paramter values
    - bDeleteBackup: set to False to prevent the deletion of the humgen backup human
        that is necessary for certain operations

    Parameters
    ----------
    _dicParams : dict
        dict with the parameters for human generation

    Returns
    -------
    object
        Blender object
    """

    # print("Starting Generate Human")

    # set a seed for the following randomization
    if "xSeed" in _dicParams:
        import numpy as np
        import random

        np_seed = hash(_dicParams["xSeed"]) % (2**32)

        random.seed(_dicParams["xSeed"])
        np.random.seed(np_seed)

    mode = _dicParams.get("sMode", "RANDOM_REALISTIC")

    lHumanGenerator = SingletonHumGenWrapper()

    params = _dicParams.get("mParamConfig", {})

    if "sGender" in _dicParams:
        warnings.warn(
            "Warning: Using sGender directly in the params of GenerateHuman is deprecated,"
            " please set it in mParamConfig instead",
            DeprecationWarning,
            stacklevel=2,
        )
        params["gender"] = _dicParams["sGender"]

    overwrite = _dicParams.get("mOverwrite", {})

    # gender = _dicParams["sGender"]

    # first compute the parameters that should be used for the creation of the human
    generator_params = ComputeParams(mode, params, overwrite, lHumanGenerator.generator_config)

    # apply
    # params['posefilename'] =_dicParams.get('sPosefile')

    objX = lHumanGenerator.CreateHuman(
        _sName=_dicParams["sId"],
        _mParams=generator_params,
        _bDeleteBackup=_dicParams.get("bDeleteBackup", True),
    )

    objX["generator_param_dict"] = json.dumps(generator_params)

    return objX


# enddef


##############################################################################################################
def ModifyHumanPostCreation(_objX, _dicParams, sMode, **kwargs):
    """
    Modify a human after the creation phase

    Parameters
    ----------
    _objX : Blender object
        Human to be modified
    _dicParams : dict
        Dictionary with configuration arguments
    """

    if "xSeed" in _dicParams:
        import numpy as np
        import random

        random.seed(_dicParams["xSeed"])
        np.random.seed(hash(_dicParams["xSeed"]) % (2**32))

    # first, make sure that nothing is selected in the scene
    # and activate the human
    try:
        bpy.ops.object.select_all(action="DESELECT")
        bpy.context.view_layer.objects.active = _objX
    except Exception as e:
        print(e)

    lHumanGenerator = SingletonHumGenWrapper()

    lHumanGenerator.human_obj = HG_Human(_objX)

    gender = "male"
    if "female" in _objX["generator_param_dict"]:
        gender = "female"

    sRandomMode = _dicParams.get("sRandomMode", "RANDOM_FULL")

    params = _dicParams["mParams"]
    params["gender"] = gender

    params = ResolveRandomParams(sRandomMode, params, lHumanGenerator.generator_config)

    lHumanGenerator.ModifyHuman(gender, params)

    lRevertHandler = []
    if sMode == "INIT":

        def RevertHandler(_sObjName):
            def handler():
                objX = bpy.data.objects.get(_sObjName)
                # TODO add revert handler
                pass
                # endif

            # enddef
            return handler

        # enddef
        lRevertHandler.append(RevertHandler(_objX.name))
    # endif

    return lRevertHandler


# enddef


##############################################################################################################
def DoPlaceHumanOnSeat(
    object,
    seat_basename,
    fRotateZ,
    xShift,
    **kwargs,
):
    """
    Place a generated human (Armature) on a seat defined by empties in the Blender scene.

    Seats in a vehicle are expected to be:
    - seat_1: driver seat
    - seat_2: front passenger
    - seat_3: left passenger on rear bench seat
    - seat_4: middle passenger on rear bench seat
    - seat_5: right passenger on rear bench seat

    The empties should be named ('x' indicating the seat number):
    - seat_x_seat
    - seat_x_foot_rest
    - seat_x_back_rest
    - seat_x_head_rest
    - seat_x_leg_constraint

    Parameters
    ----------
    object : Blender object
        Human to be posed
    seat_basename : str
        Name of the seat the human will be placed on. Should be in the format
        'seat_x'
    fRotateZ : float
        Rotation around z Axis in radians, default value is math.pi
    xShift : mathutil.vector[3]
        Shift in Armature Coordinates to fine tune asset placement
    """

    seat_obj_name = "{}_seat".format(seat_basename)

    # first, switch to edit mode
    bpy.context.view_layer.objects.active = object
    bpy.ops.object.mode_set(mode="EDIT", toggle=False)

    # add constraints

    # set object origin to spine to add object constraint to seat empty
    bpy.ops.object.mode_set(mode="POSE")
    scene = bpy.context.scene
    spine_pose = object.pose.bones["spine"]
    # armature.edit_bones.active = spine

    # set cursor to position of spine bone
    xTargetLocation = object.matrix_local @ (spine_pose.head + xShift)
    # set orgin to position of cursor (spine bone location)
    scene.cursor.location = xTargetLocation
    bpy.ops.object.mode_set(mode="OBJECT", toggle=False)
    object.select_set(True)
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
    # Rotation around z axis, default 180 degree.
    object.rotation_euler[2] = fRotateZ

    # create additonal empty at seat location and rotate around z axis
    seat_placement_name = "{}_placement".format(seat_basename)
    seat_placement = bpy.data.objects.new(seat_placement_name, None)
    bpy.context.scene.collection.objects.link(seat_placement)
    seat_placement.scale = mathutils.Vector([0.1, 0.1, 0.1])
    seat_placement.parent = bpy.data.objects[seat_obj_name]

    # create constraints to glue human origin to seat location and rotation
    object.constraints.new("COPY_LOCATION")
    object.constraints["Copy Location"].target = seat_placement
    object.constraints.new("COPY_ROTATION")
    xCopyRot = object.constraints["Copy Rotation"]
    xCopyRot.use_y = False
    xCopyRot.use_x = False
    xCopyRot.use_z = True
    xCopyRot.target = seat_placement


# enddef


##############################################################################################################
def PlaceHumanOnSeat(obj, args, sMode, **kwargs):
    """
    Place a generated human (Armature) on a seat defined by empties in the Blender scene.
    The args dictionary supports the following settings:

        sId: Blender Name of the Armature
        sGender: 'female' or 'male'
        xSeed: Seed for RNG for reproducability purposes
        fRotateZ : Rotation of Human asset around z Axis
        fShiftX : Shift x Axis, in Armature Coordinates to fine tune asset placement, default value 0.0
        fShiftY : Shift y Axis, in Armature Coordinates to fine tune asset placement, default value 0.0
        fShiftZ : Shift z Axis, in Armature Coordinates to fine tune asset placement, default value 0.0
        lShift : List [fShiftX,fShifty,fShiftZ] in Armature Coordinates
            Note that if lShift and individual shifts are passed the shifts are added, default value [0.0, 0.0, 0.0]

    Parameters
    ----------
    obj : Blender object
        Human to be posed
    args : dict
        Dictionary with configuration arguments
    """

    # Extract modifier parameters
    fRotateZ = convert.DictElementToFloat(args, "fRotateZ", fDefault=math.pi)
    fShiftX = convert.DictElementToFloat(args, "fShiftX", fDefault=0.0)
    fShiftY = convert.DictElementToFloat(args, "fShiftY", fDefault=0.0)
    fShiftZ = convert.DictElementToFloat(args, "fShiftZ", fDefault=0.0)
    lShift = convert.DictElementToFloatList(args, "lShift", iLen=3, lDefault=[0.0, 0.0, 0.0])

    # construct complete shift vector from shift passed as list and individual shifts
    lShift[0] += fShiftX
    lShift[1] += fShiftY
    lShift[2] += fShiftZ
    xShift = mathutils.Vector(lShift)

    if "xSeed" in args:
        import numpy as np
        import random

        random.seed(args["xSeed"])
        np.random.seed(hash(args["xSeed"]) % (2**32))
    # endif

    # first, make sure that nothing is selected in the scene
    try:
        bpy.ops.object.select_all(action="DESELECT")
    except Exception as e:
        print(e)

    DoPlaceHumanOnSeat(
        object=obj,
        fRotateZ=fRotateZ,
        xShift=xShift,
        seat_basename=args["sEmptyBaseName"],
    )

    lRevertHandler = []
    if sMode == "INIT":

        def RevertHandler(_sObjName):
            def handler():
                objX = bpy.data.objects.get(_sObjName)
                # TODO add revert handler
                pass
                # endif

            # enddef
            return handler

        # enddef
        lRevertHandler.append(RevertHandler(obj.name))
    # endif

    return lRevertHandler


# enddef


##############################################################################################################
def UpdateImageFilePath(obj, args, sMode):
    """
    Update all material nodes of a human to use the proper HumGen asset library path.

    Parameters
    ----------
    obj : Blender object
        Human to be updated
    args : dict
        Dictionary with configuration arguments

    """

    sAddonPath = bpy.context.preferences.addons["humgen3d"].preferences["filepath"]

    sBase = args.get("sBase", "HumanGeneratorV3")

    for child in obj.children:
        for materialSlot in child.material_slots:
            for node in materialSlot.material.node_tree.nodes:
                if hasattr(node, "image") and node.image is not None:
                    sOrigPath = node.image.filepath

                    aStartPos = sOrigPath.find(sBase)

                    sNewPath = sAddonPath + sOrigPath[aStartPos + len(sBase) :]

                    node.image.filepath = sNewPath
                # endif
            # endfor
        # endfor
    # endfor

    lRevertHandler = []
    if sMode == "INIT":

        def RevertHandler(_sObjName):
            def handler():
                objX = bpy.data.objects.get(_sObjName)
                # TODO add revert handler
                pass
                # endif

            # enddef
            return handler

        # enddef
        lRevertHandler.append(RevertHandler(obj.name))
    # endif

    return lRevertHandler


# enddef


##############################################################################################################
def ReplaceMaterials(obj, args, sMode, **kwargs):
    """
    Switches all material nodes of a human to a material from an addon asset library.

    The args dictionary supports the following settings:

    - sReplacementBlendFile: Path to the asset library
    - xSeed: object for seeding the randomization
    - bFilterGender: remove materials from randomization that do not match the gender

    Parameters
    ----------
    obj : Blender object
        Human to be updated
    args : dict
        Dictionary with configuration arguments

    """

    def filterByGender(name2materials):
        sGender = "female" if obj["HG"]["gender"] == 1 else "male"

        newName2materials = {}

        for name, lMaterials in name2materials.items():
            lNewEntry = [mat for mat in lMaterials if sGender in mat.lower()]
            newName2materials[name] = lNewEntry
        # endfor

        return newName2materials

    # enddef

    if "xSeed" in args:
        random.seed(args["xSeed"])
    # endif

    if "sReplacementBlendFile" not in args:
        raise Exception("sReplacementBlendFile not given")

    if "bFilterGender" in args:
        bFilterGender = args["bFilterGender"]
    else:
        bFilterGender = False
    # endif

    sLibPath = args["sReplacementBlendFile"]

    with bpy.data.libraries.load(sLibPath, link=True) as (data_src, data_dst):
        data_dst.texts = ["RandomizeShader.py"]

    xReplaceModule = data_dst.texts[0].as_module()

    for xChild in obj.children:
        name2materials = xReplaceModule.name2materials

        if bFilterGender:
            name2materials = filterByGender(name2materials)
        # endif

        for sName, lMaterials in name2materials.items():
            if sName in xChild.name:
                sMaterial = random.choice(lMaterials)
                # Link the material
                with bpy.data.libraries.load(sLibPath, link=False) as (data_src, data_dst):
                    data_dst.materials = [sMaterial]
                # endwith

                if len(data_dst.materials) == 0 or data_dst.materials[0] is None:
                    raise RuntimeError(f"Material with name {sMaterial} not found in {sLibPath}")
                # endif

                for mat in data_dst.materials:
                    xChild.data.materials[0] = mat
                # endfor

                # then call the randomization
                xReplaceModule.randomizeShader(xChild.data.materials[0].name)

                # TODO set original material fake user to false
            # endif
        # endfor
    # endfor

    lRevertHandler = []
    if sMode == "INIT":

        def RevertHandler(_sObjName):
            def handler():
                objX = bpy.data.objects.get(_sObjName)
                # TODO add revert handler
                pass
                # endif

            # enddef
            return handler

        # enddef
        lRevertHandler.append(RevertHandler(obj.name))
    # endif

    return lRevertHandler


# enddef
