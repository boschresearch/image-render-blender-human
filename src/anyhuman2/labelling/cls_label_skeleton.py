"""WORK IN PROGRESS

Returns
-------
_type_
    _description_

Raises
------
RuntimeError
    _description_
"""


import os
import json
from math import Vector
import bpy

from ..cls_humgen import HumGenWrapper


class BoneLabel:
    version_info = None
    try:
        version_info = HumGenWrapper.get_installed_humgen_version()
    except ImportError:
        # Handle ImportError if get_installed_humgen_version is not available
        pass

    if version_info and version_info[0] == 4:
        from HumGen3D import Human
    elif version_info and version_info[0] == 3:
        from humgen3d import Human
    else:
        from HumGen3D import Human

    def __init__(self):
        """
        Sets lists for label bones
        """

        # TODO: get these automatically without hardcoding
        objRig = bpy.data.objects["Armature.1"]
        objArmature = bpy.data.armatures["metarig"]

        # json file with relative (to current file) path
        sHandLabelsFilePath = "mapping\\openpose_hand.json"
        sCurrentDirectory = os.getcwd()
        sHandLabelsFile = os.path.join(sCurrentDirectory, sHandLabelsFilePath)

        self.lOpenPoseHandLabels = []
        # self.lOpenPoseFaceLabels = []

        def loadHandMappings(_sHandLabelsFile: str):
            try:
                with open(_sHandLabelsFile, "r") as json_file:
                    lOpenPoseHandLabels = json.load(json_file)
                    return lOpenPoseHandLabels
                    # print(f"{len(self.label_config.lOpenPoseHandLabels)} labels found for hand mapping")
            except FileNotFoundError:
                print(f"File not found: {_sHandLabelsFile}")
                return None

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from file: {e}")
                return None

        # enddef

        self.lOpenPoseHandLabels = loadHandMappings(sHandLabelsFile)
        if len(self.label_config.lOpenPoseHandLabels) == 0:
            raise RuntimeError("hand mapping file empty")

    # enddef

    def AddLabelBones(self, _objArmature: bpy.types.Armature, _objRig: bpy.types.Object):
        if _objArmature is None:
            print("Error _objArmature not found")
            return

        bpy.context.view_layer.objects.active = _objRig
        bpy.ops.object.mode_set(mode="EDIT")

        for i in self.lOpenPoseHandLabels:
            sParent = i["sBone"]
            sAttachTo = i["sAttachTo"]
            sOpenposeLabel = i["sLabelBone"]

            parent_bone = _objArmature.edit_bones.get(str(sParent))
            openpose_mark_bone = _objArmature.edit_bones.get(str(sOpenposeLabel))
            if parent_bone is None:
                print(f"Error: {sParent} not found")
                return
            # endif parent_bone is None:
            if openpose_mark_bone is not None:
                print(f"Error: {sOpenposeLabel} already present")
                continue
            # endif openpose_mark_bone is not None:
            if sAttachTo == "head":
                new_bone = _objArmature.edit_bones.new(str(sOpenposeLabel))
                print(f"{sParent}\t{sAttachTo}\t{sOpenposeLabel}")
                # parent_bone = armature.edit_bones.get(str(sParent))
                new_bone.parent = parent_bone
                new_bone.head = parent_bone.head
                new_bone.tail = parent_bone.head.cross(Vector((1, 1, 1)))
                new_bone.length = 1.0  # cm
                # new_bone.use_connect = True
            # endif sAttachTo == 'head':
            else:
                new_bone = _objArmature.edit_bones.new(str(sOpenposeLabel))
                print(f"{sParent}\t{sAttachTo}\t{sOpenposeLabel}")
                new_bone.parent = parent_bone
                new_bone.head = parent_bone.tail
                new_bone.tail = parent_bone.tail.cross(Vector((1, 1, 1)))
                new_bone.length = 0.01
                new_bone.use_connect = True
            # endelse
        # endfor
        # TODO: set to original/previous mode
        # bpy.ops.object.mode_set(mode="OBJECT")
        return

    # enddef execute

    ############################################################################################
    def _make_rel_path(self, s):
        if os.name == "nt":
            s = s.replace("/", "\\")
        return s

    # enddef

    ############################################################################################

    # enddef
