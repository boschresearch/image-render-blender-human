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
from mathutils import Vector
import bpy
from HumGen3D import Human


class BoneLabel:
    def __init__(self, _human: Human):
        """
        A LabelBone is a label attached to a bone or vertex group and identifies itself as landmark.
        It can be openpose hand label bone and/or WFLW label bone and so on
        """

        self.objRig = _human.objects.rig  # bpy.data.objects["HG_XXXX"]
        self.objArmature = _human.objects.rig.data  # bpy.data.armatures["metarig"]
        self.objHGBody = _human.objects.body  # bpy.data.armatures["HG_Body"]

        self.lOpenPoseHandLabels = []

    def LoadHandMappings(self, _sHandLabelsFile: str):
        try:
            with open(_sHandLabelsFile, "r") as json_file:
                lOpenPoseHandLabels = json.load(json_file)
                return lOpenPoseHandLabels
                # print(f"{len(self.label_config.lOpenPoseHandLabels)} labels found for hand mapping")
        except FileNotFoundError:
            print(f"File not found: {_sHandLabelsFile}")
            return []

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from file: {e}")
            return []

    # enddef

    def AddHandLabels(self, _sLabelFile: str, _objArmature: bpy.types.Armature, _objRig: bpy.types.Object):
        self.lOpenPoseHandLabels = self.LoadHandMappings(_sLabelFile)
        if len(self.lOpenPoseHandLabels) is None:
            return
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
                new_bone.length = 0.01  # in meters
                # new_bone.use_connect = True
            # endif sAttachTo == 'head':
            else:
                new_bone = _objArmature.edit_bones.new(str(sOpenposeLabel))
                print(f"{sParent}\t{sAttachTo}\t{sOpenposeLabel}")
                new_bone.parent = parent_bone
                new_bone.head = parent_bone.tail
                new_bone.tail = parent_bone.tail.cross(Vector((1, 1, 1)))
                new_bone.length = 0.01  # in meters
                new_bone.use_connect = True
            # endelse
        # endfor
        # TODO: set to original/previous mode
        bpy.ops.object.mode_set(mode="OBJECT")
        return

    # enddef

    # ************************************* BEGIN EXPORT FUNCTIONS ********************************************************

    def ExportSkeletonData(self, _sExportOutputPath: str):
        # STEP 1: Extract bones of skeletons
        dicSkeletons = self.ExtractSkeletons(_objArmature=objArmature, _objHGBody=objHGBody, _objRig=objRig)
        # STEP 2: Split skeletons and label them based on type (Std, Openpose)
        dicLabelledSkeletons_a = self.SplitSkeletons(_dicSkeletons=dicSkeletons)
        # STEP 3: Add vertex groups to each of labelled skeletons
        self.ExportVertexGroups(_objHGBody=objHGBody, _dicLabelledSkeletons=dicLabelledSkeletons_a)
        # STEP 4: Export each labelled skeleton
        self.ExportSkeletons(_dicLabelledSkeletons=dicLabelledSkeletons_a, _sOutputPath=sExportOutputPath)
        print("exported")
        return {"FINISHED"}

    # enddef

    def ExportVertexGroups(self, _objHGBody, _dicLabelledSkeletons):
        for sSkeletonType, dicSkeletonData in _dicLabelledSkeletons.items():
            for group in _objHGBody.vertex_groups:
                vertex_indices = [
                    v.index for v in _objHGBody.data.vertices if group.index in [vg.group for vg in v.groups]
                ]
                dicVertexGroup = {"sName": group.name, "lVertices": vertex_indices}
                dicSkeletonData["lVertexGroups"].append(dicVertexGroup)
            # endfor
        # endfor

    # enddef

    # Extract bones of all types of skeletons into a dictionary
    def ExtractSkeletons(self, _objArmature, _objHGBody, _objRig):
        dicSkeletons = {
            # "lVertexGroups": [],
            # "sSkeletonType": "Std",
            "lBones": [
                # {
                #    "sRootBone": "head",
                #    "sName": "RightEar",
                #    "sParent": "spine"
                #    "fEnvelope": 0.05,
                #    "fHeadRadius": 0.02,
                #    "lConstraints": []
                # }
            ]
        }

        bpy.context.view_layer.objects.active = _objRig
        bpy.ops.object.mode_set(mode="POSE")

        # Collect bone information
        for objBone, bone in zip(_objArmature.bones, _objRig.pose.bones):
            lPartsBySemiColon = bone.name.split(";")

            if lPartsBySemiColon[0] == "AT.Label" and len(lPartsBySemiColon) == 3:
                sSkeletonType = lPartsBySemiColon[1]
                sBoneName = lPartsBySemiColon[2]

                dicBone = {
                    "sType": sSkeletonType,
                    "sName": sBoneName,
                    "lHead": list(bone.head),
                    "lTail": list(bone.tail),
                    "sParent": bone.parent.name if bone.parent else "",
                    "fEnvelope": objBone.envelope_distance,
                    "fHeadRadius": objBone.head_radius,
                    "lConstraints": []
                    # Add more bone properties as needed
                }

                for cons in bone.constraints:
                    if cons.type == "STRETCH_TO":
                        dicConstraint = {
                            "sType": cons.type,
                            "sBone": bone.name,
                            "sTarget": cons.target.name if cons.target else "",
                            "sSubtarget": cons.subtarget if cons.subtarget else "",
                            "sVolume": cons.volume,
                            "sKeepAxis": cons.keep_axis,
                            "fInfluence": cons.influence,
                        }
                        dicBone["lConstraints"].append(dicConstraint)
                    # endif cons.type == "STRETCH_TO"

                    if cons.type == "LIMIT_LOCATION":
                        dicConstraint = {
                            "sType": cons.type,
                            "sBone": bone.name,
                            "fMinX": cons.min_x,
                            "fMinY": cons.min_y,
                            "fMinZ": cons.min_z,
                            "fMaxX": cons.max_x,
                            "fMaxY": cons.max_y,
                            "fMaxZ": cons.max_z,
                            "bAffectTransform": cons.use_transform_limit,
                            "sOwnerSpace": cons.owner_space,
                            "fInfluence": cons.influence,
                        }
                        dicBone["lConstraints"].append(dicConstraint)
                    # endif cons.type == "LIMIT_LOCATION"

                    if cons.type == "DAMPED_TRACK":
                        dicConstraint = {
                            "sType": cons.type,
                            "sBone": bone.name,
                            "sTarget": cons.target.name if cons.target else "",
                            "sTrackAxis": cons.track_axis,
                            "sOwnerSpace": cons.owner_space,
                            "fInfluence": cons.influence,
                        }
                        dicBone["lConstraints"].append(dicConstraint)
                    # endif cons.type == "DAMPED_TRACK"

                    if cons.type == "CHILD_OF":
                        dicConstraint = {
                            "sType": cons.type,
                            "sBone": bone.name,
                            "sTarget": cons.target.name if cons.target else "",
                            "sSubtarget": cons.subtarget if cons.subtarget else "",
                            "bUseLocationX": cons.use_location_x,
                            "bUseLocationY": cons.use_location_y,
                            "bUseLocationZ": cons.use_location_z,
                            "bUseRotationX": cons.use_rotation_x,
                            "bUseRotationY": cons.use_rotation_y,
                            "bUseRotationZ": cons.use_rotation_z,
                            "bUseScaleX": cons.use_scale_x,
                            "bUseScaleY": cons.use_scale_y,
                            "bUseScaleZ": cons.use_scale_z,
                            "fInfluence": cons.influence,
                        }
                        dicBone["lConstraints"].append(dicConstraint)
                    # endif cons.type == "CHILD_OF"

                    if cons.type == "COPY_LOCATION":
                        dicConstraint = {
                            "sType": cons.type,
                            "sBone": bone.name,
                            "sTarget": cons.target.name if cons.target else "",
                            "sSubtarget": cons.subtarget if cons.subtarget else "",
                            "bUseX": cons.use_x,
                            "bUseY": cons.use_y,
                            "bUseZ": cons.use_z,
                            "bInvertX": cons.invert_x,
                            "bInvertY": cons.invert_y,
                            "bInvertZ": cons.invert_z,
                            "sTargetSpace": cons.target_space,
                            "sOwnerSpace": cons.owner_space,
                            "fInfluence": cons.influence,
                        }
                        dicBone["lConstraints"].append(dicConstraint)
                    # endif cons.type == "COPY_LOCATION"
                # endfor cons in bone.constraints

                dicSkeletons["lBones"].append(dicBone)

        return dicSkeletons

    # enddef

    # split skeletons based on sSkeletonType
    def SplitSkeletons(self, _dicSkeletons):
        dicLabelledSkeletons = {}
        for dicBone in _dicSkeletons["lBones"]:
            sSkeletonType = dicBone["sType"]
            if sSkeletonType not in dicLabelledSkeletons:
                dicLabelledSkeletons[sSkeletonType] = {
                    "sSkeletonType": sSkeletonType,
                    "lBones": [],
                    "lVertexGroups": [],
                }
            dicLabelledSkeletons[sSkeletonType]["lBones"].append(dicBone)
        return dicLabelledSkeletons

    # enddef

    # ExportSkeletons
    def ExportSkeletons(self, _dicLabelledSkeletons, _sOutputPath):
        for sSkeletonType, dicSkeletonData in _dicLabelledSkeletons.items():
            sFilename = f"{sSkeletonType}_bones.json"
            sOutputFile = _sOutputPath + sFilename
            with open(sOutputFile, "w") as sJsonFile:
                json.dump(dicSkeletonData, sJsonFile, indent=4)
            print(f"Saved {sSkeletonType} bones to {sFilename}")

    # enddef

    # ************************************* END EXPORT FUNCTIONS ********************************************************

    # ************************************* BEGIN IMPORT FUNCTIONS ********************************************************

    def ImportSkeletonData(self, _sSkeletonDataFile):
        # STEP 1: Parse input json and extract skeletal bones with constraints and vertex groups
        dicSkeleton = self.ParseSkeleton(_sInSkeletonFile=_sSkeletonDataFile)
        # STEP 2: Add vertex groups to objHGBody (Mesh)
        self.CreateVertexGroups(_objMesh=objHGBody, _lVertexGroups=dicSkeleton["lVertexGroups"])
        # STEP 3: Add bones
        self.ImportSkeletonBones(_dicSkeleton=dicSkeleton, _objArmature=objArmature, _objRig=objRig)
        # STEP 4: Add constraints
        self.AddConstraints(_dicSkeleton=dicSkeleton, _objArmature=objArmature, _objRig=objRig)

        return {"FINISHED"}

    # add bone based on contents of _dicBone
    def AddBone(self, _sSkeletonType, _dicBone, _objArmature, _objRig):
        bpy.context.view_layer.objects.active = _objRig
        bpy.ops.object.mode_set(mode="EDIT")

        sNewBoneName = "AT.Label;" + _sSkeletonType + ";" + _dicBone["sName"]
        objNewBone = _objArmature.edit_bones.get(str(sNewBoneName))
        if objNewBone is not None:
            print("Error: %s already present - only updating envelope_distance & head_radius", str(sNewBoneName))
            # _objArmature.edit_bones.remove(objNewBone)
            objNewBone.envelope_distance = _dicBone["fEnvelope"]
            objNewBone.head_radius = _dicBone["fHeadRadius"]
            return
        objNewBone = _objArmature.edit_bones.new(sNewBoneName)

        xParentBone = _objArmature.edit_bones.get(_dicBone["sParent"])
        objNewBone.parent = xParentBone if xParentBone else None

        lHead = Vector((_dicBone["lHead"][0], _dicBone["lHead"][1], _dicBone["lHead"][2]))
        lTail = Vector((_dicBone["lTail"][0], _dicBone["lTail"][1], _dicBone["lTail"][2]))
        objNewBone.head = lHead
        objNewBone.tail = lTail
        objNewBone.envelope_distance = _dicBone["fEnvelope"]
        objNewBone.head_radius = _dicBone["fHeadRadius"]
        # bpy.ops.object.mode_set(mode="POSE")

    # enddef

    def AddConstraints(self, _dicSkeleton, _objArmature, _objRig):
        # pose mode
        bpy.context.view_layer.objects.active = _objRig
        bpy.ops.object.mode_set(mode="POSE")

        for dicBone in _dicSkeleton["lBones"]:
            # construct bone name
            sPoseBoneName = "AT.Label;" + dicBone["sType"] + ";" + dicBone["sName"]

            # get pose bone
            objPoseBone = _objRig.pose.bones[sPoseBoneName]

            # add constraints
            for objConstraint in dicBone["lConstraints"]:
                if objConstraint["sType"] == "STRETCH_TO":
                    self.AddConstraintStretchTo(objPoseBone, objConstraint)
                elif objConstraint["sType"] == "LIMIT_LOCATION":
                    self.AddConstraintLimitLocation(objPoseBone, objConstraint)
                elif objConstraint["sType"] == "CHILD_OF":
                    self.AddConstraintChildOf(objPoseBone, objConstraint)
                elif objConstraint["sType"] == "COPY_LOCATION":
                    self.AddConstraintCopyLocation(objPoseBone, objConstraint)
                else:
                    print("Error: new constraint %s found", objConstraint["sType"])
            # endfor objConstraint in _dicBone

        # get into object mode
        bpy.ops.object.mode_set(mode="OBJECT")

    # enddef

    # add STRETCH_TO constraint
    def AddConstraintStretchTo(_self, xPoseBone, _lStretchConstraint):
        xNewConstraint = _xPoseBone.constraints.new("STRETCH_TO")
        xNewConstraint.target = bpy.data.objects[_lStretchConstraint["target"]]
        xNewConstraint.subtarget = _lStretchConstraint["subtarget"]
        xNewConstraint.keep_axis = _lStretchConstraint["sKeepAxis"]
        xNewConstraint.volume = _lStretchConstraint["sVolume"]
        xNewConstraint.influence = _lStretchConstraint["fInfluence"]

    # enddef

    # add LIMIT_LOCATION constraint
    def AddConstraintLimitLocation(self, _xPoseBone, _lLimitLocationConstraint):
        xNewConstraint = _xPoseBone.constraints.new("LIMIT_LOCATION")
        xNewConstraint.target = objHGBodyNew
        xNewConstraint.type = _lLimitLocationConstraint["sType"]
        xNewConstraint.max_x = _lLimitLocationConstraint["fMaxX"]
        xNewConstraint.max_y = _lLimitLocationConstraint["fMaxY"]
        xNewConstraint.max_z = _lLimitLocationConstraint["fMaxZ"]
        xNewConstraint.min_x = _lLimitLocationConstraint["fMinX"]
        xNewConstraint.min_y = _lLimitLocationConstraint["fMinY"]
        xNewConstraint.min_z = _lLimitLocationConstraint["fMinZ"]
        xNewConstraint.use_transform_limit = _lLimitLocationConstraint["bUseTransformLimit"]
        xNewConstraint.owner_space = _lLimitLocationConstraint["sOwnerSpace"]
        xNewConstraint.influence = _lLimitLocationConstraint["fInfluence"]

    # enddef

    # add CHILD_OF constraint
    def AddConstraintChildOf(self, _xPoseBone, lChildOfConstraint):
        xNewConstraint = _xPoseBone.constraints.new("CHILD_OF")
        xNewConstraint.target = objHGBodyNew
        xNewConstraint.subtarget = lChildOfConstraint["sSubtarget"]
        xNewConstraint.keep_axis = lChildOfConstraint["sKeepAxis"]
        xNewConstraint.volume = lChildOfConstraint["sVolume"]
        xNewConstraint.influence = lChildOfConstraint["fInfluence"]

    # enddef

    # add COPY_LOCATION constraint
    def AddConstraintCopyLocation(self, _xPoseBone, _lConstraintCopyLocation):
        xNewConstraint = _xPoseBone.constraints.new("COPY_LOCATION")
        xNewConstraint.target = objHGBodyNew
        xNewConstraint.subtarget = _lConstraintCopyLocation["sSubtarget"]
        xNewConstraint.use_x = _lConstraintCopyLocation["bUseX"]
        xNewConstraint.use_y = _lConstraintCopyLocation["bUseY"]
        xNewConstraint.use_z = _lConstraintCopyLocation["bUseZ"]
        xNewConstraint.invert_x = _lConstraintCopyLocation["bInvertX"]
        xNewConstraint.invert_y = _lConstraintCopyLocation["bInvertY"]
        xNewConstraint.invert_z = _lConstraintCopyLocation["bInvertZ"]
        xNewConstraint.target_space = _lConstraintCopyLocation["sTargetSpace"]
        xNewConstraint.owner_space = _lConstraintCopyLocation["sOwnerSpace"]
        xNewConstraint.influence = _lConstraintCopyLocation["fInfluence"]

    # enddef

    # Import bones and add to rig
    def ImportSkeletonBones(self, _dicSkeleton, _objArmature, _objRig):
        sSkeletonType = _dicSkeleton["sSkeletonType"]
        for dicBone in _dicSkeleton["lBones"]:
            self.AddBone(sSkeletonType, dicBone, _objArmature, _objRig)

    # enddef

    # import skeleton from json file
    def ParseSkeleton(self, _sInSkeletonFile):
        with open(_sInSkeletonFile, "r") as sJsonFile:
            dicSkeleton = json.load(sJsonFile)
        return dicSkeleton

    # enddef

    # import and create vertex groups
    def CreateVertexGroups(self, _objMesh, _lVertexGroups):
        for dicVertexGroup in _lVertexGroups:
            if _objMesh.vertex_groups.find(dicVertexGroup["sName"]) == -1:
                xVertexGroup = _objMesh.vertex_groups.new(name=dicVertexGroup["sName"])
                # Default weight=1.0, type='ADD'
                xVertexGroup.add(dicVertexGroup["lVertices"], 1.0, "ADD")
        # endfor

    # enddef


# ************************************* END IMPORT FUNCTIONS ********************************************************
