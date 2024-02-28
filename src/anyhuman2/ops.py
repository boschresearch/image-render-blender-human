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

from typing import Optional
from anybase import convert

from .cls_humgen import SingletonHumGenWrapper

from .paramgenerators import ComputeParams, ResolveRandomParams

try:
    from HumGen3D import Human as HG_Human
except Exception as xEx:
    print("Error initializing anyhuman module:\n{}".format(str(xEx)))
# HumGen V3 Legacy
# try:
#     from humgen3d.API import HG_Human, HG_Batch_Generator
# except Exception as xEx:
#     print("Error initializing anyhuman module:\n{}".format(str(xEx)))
# # endtry


##############################################################################################################
def GenerateHuman(_dicParams, **kwargs):
    """
    Function for generating any human.

    It uses the HumGenWrapper class for first computation of a set of parameters that
    then will be used to create the human.

    The computation of parameters can be based on different approaches as full randomization,
    randomization by a Zwicky-Box specification, or directly by given parameters. For a detailed description,
    see the HumGenWrapper class.

    The _dicParams dictionary can contain the keys:
    - sId: name that should be used for the generated blender object
    - xSeed: object for seeding the randomization
    - sMode: mode for computation of the parameters of the human
    - mParamConfig: dict with parameters for the parameter computation, see HumGenWrapper
    - mOverwrite: dict with parameters that should be used to overwrite the computed parameter values
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
    generated_params = ComputeParams(mode, params, overwrite, lHumanGenerator.generator_config)

    # apply
    # params['posefilename'] =_dicParams.get('sPosefile')

    if _dicParams.get("sMode") == "FILE":
        objX = lHumanGenerator.CreateHumanFromJSON(params["sFilename"])
    elif _dicParams.get("sMode") == "FULL_RANDOM":
        objX = lHumanGenerator.CreateFullRandomHuman(_dicParams)
    else:
        objX = lHumanGenerator.CreateHuman(params, generated_params)


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
    _objArmature,
    _sSeatBasename,
    _fRotateZ,
    _xShift,
    _bApplyConstraints,
    _iFrameNumber: Optional[int] = None,
):
    """
    Place a generated human (its Armature) on a seat defined by empties in the Blender scene.

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
    _objArmature : Blender armature object
        the linked Human Skeleton to be posed
    _sSeatBasename : str
        Name of the seat the human will be placed on. Should be in the format
        'seat_x'
    _fRotateZ : float
        Rotation around z-Axis (i.e. up-Axis) in radians, default value is math.pi
    _xShift : mathutil.Vector[3]
        Shift in Armature coordinates to fine tune asset placement
    _bApplyConstraints: bool
        Whether to apply the Blender rotation and location constraint and copying to armature's pose.
    _iFrameNumber: Optional[int]
        The frame number to insert the keyframe in the pose animation (only applies if _bApplyConstraints=True)
    """

    sSeatObjectName = "{}_seat".format(_sSeatBasename)

    # first, switch to edit mode
    bpy.context.view_layer.objects.active = _objArmature
    bpy.ops.object.mode_set(mode="EDIT", toggle=False)

    # add constraints

    # set object origin to spine to add object constraint to seat empty
    bpy.ops.object.mode_set(mode="POSE")
    xScene = bpy.context.scene
    xRootBone = _objArmature.pose.bones["spine"]
    # armature.edit_bones.active = spine

    # set cursor to position of spine bone
    xTargetLocation = _objArmature.matrix_local @ (xRootBone.head + _xShift)
    # set orgin to position of cursor (spine bone location)
    xScene.cursor.location = xTargetLocation
    bpy.ops.object.mode_set(mode="OBJECT", toggle=False)
    _objArmature.select_set(True)
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR")

    # create additonal empty at seat location and rotate around z axis
    sSeatPlacementName = "{}_placement".format(_sSeatBasename)
    objSeatPlacementEmpty = bpy.data.objects.new(sSeatPlacementName, None)

    bpy.context.scene.collection.objects.link(objSeatPlacementEmpty)
    objSeatPlacementEmpty.scale = mathutils.Vector([0.1, 0.1, 0.1])
    objSeatPlacementEmpty.parent = bpy.data.objects[sSeatObjectName]
    # Rotation around z axis, default 180 degree.
    objSeatPlacementEmpty.rotation_euler[2] = _fRotateZ

    # create constraints to glue human origin to seat location and rotation
    _objArmature.constraints.new("COPY_LOCATION")
    _objArmature.constraints["Copy Location"].target = objSeatPlacementEmpty
    _objArmature.constraints.new("COPY_ROTATION")
    xCopyRot = _objArmature.constraints["Copy Rotation"]
    xCopyRot.use_y = False
    xCopyRot.use_x = False
    xCopyRot.use_z = True
    xCopyRot.target = objSeatPlacementEmpty

    if _bApplyConstraints:
        # ------------ new part ---------------
        # apply the copy-rotation and copy-location modifiers and move all global transformation
        # into the root pose-bone transformation
        bpy.context.view_layer.update()
        bpy.ops.object.select_all(action="DESELECT")
        _objArmature.select_set(True)
        bpy.context.view_layer.objects.active = _objArmature
        bpy.ops.constraint.apply(constraint="Copy Rotation", owner="OBJECT")
        bpy.ops.constraint.apply(constraint="Copy Location", owner="OBJECT")
        bpy.context.view_layer.update()

        # now the rotation and translation is applied and copied to the armatures
        # location and rotation parameters
        # however, we need to apply it to the root bone transformation in pose mode

        _objArmature.rotation_mode = "QUATERNION"
        xMatrixWorld = _objArmature.matrix_world

        bpy.context.view_layer.objects.active = _objArmature
        bpy.ops.object.mode_set(mode="POSE")

        xRootBone = _objArmature.pose.bones["spine"]
        xRootBone.rotation_mode = "QUATERNION"

        xRootRestBone = _objArmature.data.bones["spine"]
        xRootRestMatrix = xRootRestBone.matrix_local
        xRootRestMatrix_inv = mathutils.Matrix(xRootRestMatrix)
        xRootRestMatrix_inv.invert()

        # Blender computes the global armature transformation as:
        #   Object_transfrom * Rest_pose_transform * pose_transform * inverse_Rest_pose_transform
        # Hence, we need to take care of the rest-pose matrix when moving the global object transformation
        # to the root's pose-bone transformation
        # Rot_obj * Rot_rest * Rot_pose * Rot_rest^-1 = Rot_rest * Rot_posenew * Rot_rest^-1
        # => R_posenew = Rot_rest^-1 * Rot_obj * Rot_rest * Rot_pose
        # same applies to the translation...

        xTransformRoot = xRootRestMatrix_inv @ xMatrixWorld @ xRootRestMatrix
        xRootRotationNew = xTransformRoot.to_3x3() @ xRootBone.rotation_quaternion.to_matrix()
        xRootBone.rotation_quaternion = xRootRotationNew.to_quaternion()
        xRootLocationNew = xTransformRoot @ xRootBone.location
        xRootBone.location = xRootLocationNew

        # iCurFrame = bpy.context.scene.frame_current
        # spine_pose.keyframe_insert(data_path='rotation_quaternion',frame=iCurFrame)
        # spine_pose.keyframe_insert(data_path='location',frame=iCurFrame)

        # We need to insert the root pose as a keyframe otherwise it seems to be overwritten when the scene
        # is updated in Blender and the frame is set at a later point (via bpy.context.scene.frame_current)
        # TODO: this is not clear what frame to set, hence keep it as an optional argument
        iFrameNumber = 1
        if _iFrameNumber is not None:
            iFrameNumber = _iFrameNumber

        xRootBone.keyframe_insert(data_path="rotation_quaternion", frame=iFrameNumber)
        xRootBone.keyframe_insert(data_path="location", frame=iFrameNumber)

        # not sure what this does but it needs to be set to false
        _objArmature.data.bones["spine"].use_local_location = True

        # set the transform in the armature object to identity since it is now copied to the pose (via xMatrixWorld)
        _objArmature.location = mathutils.Vector((0, 0, 0))
        _objArmature.rotation_quaternion = mathutils.Matrix.Identity(3).to_quaternion()

        bpy.ops.object.mode_set(mode="OBJECT", toggle=False)

    # endif


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
    bApplyConstraints = convert.DictElementToBool(args, "bApplyConstraints", bDefault=False)
    iFrameNumber = convert.DictElementToInt(args, "iFrameNumber", iDefault=1)

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
        _objArmature=obj,
        _fRotateZ=fRotateZ,
        _xShift=xShift,
        _sSeatBasename=args["sEmptyBaseName"],
        _bApplyConstraints=bApplyConstraints,
        _iFrameNumber=iFrameNumber,
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
