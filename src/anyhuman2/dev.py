#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: \_dev.py
# Created Date: Thursday, March 10th 2022, 3:49:45 pm
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
from anyhuman2 import ops


###############################################################################################################################
def _testHumanGeneration():
    """
    This function can be used to test the generation of humans from within Blender
    """
    active_tests = [
        # "ZWICKY",
        # "ZWICKY_GRID",
        # "RANDOM_FULL_GRID",
        # "RANDOM_FULL",
        # "RANDOM_REALISTIC",
        # "RANDOM_REALISTIC_GRID",
        # "PERSONA",
        # "LEGACY",
        # "FILE", # HumGenV4 Test
        "FULL_RANDOM", # HumgGenV4 Test
    ]
    try:
        dx = 1.2
        dy = 1.0
        bpy.context.scene.cursor.location = (0, 0, 0)

        if "LEGACY" in active_tests:
            bpy.context.scene.cursor.location[0] = 0
            obj = ops.GenerateHuman({"sId": "Armature.001", "sGender": "female"})
            bpy.context.scene.cursor.location[1] += 1.5

            # PlaceHumanOnSeat(obj, {'sEmptyBaseName': 'seat_1'})
        # endif
        if "FILE" in active_tests:
            bpy.context.scene.cursor.location[0] = 0
            obj = ops.GenerateHuman(
                {
                    "sId": "Seth",
                    "sMode": "FILE",
                    "mParamConfig": {
                        "sFilename": "C:\\Users\\mnt1lr\\Documents\\work\\Cathy_HumGenV4_Development\\image-render-setup\\repos\image-render-blender-human\\src\\anyhuman\\personas\\HG_Seth.json"
                    },
                }
            )

        if "PERSONA" in active_tests:
            bpy.context.scene.cursor.location[0] = 0
            obj = ops.GenerateHuman(
                {
                    "xSeed": 1,
                    "sId": "Alice",
                    "sMode": "PERSONA",
                    "mParamConfig": {"sPersonaId": "alice"},
                }
            )
            bpy.context.scene.cursor.location[0] += dx
            obj = ops.GenerateHuman(
                {
                    "xSeed": 1,
                    "sId": "Bob",
                    "sMode": "PERSONA",
                    "mParamConfig": {"sPersonaId": "bob"},
                }
            )
            bpy.context.scene.cursor.location[1] += dy
        # endif

        if "RANDOM_FULL" in active_tests:
            bpy.context.scene.cursor.location[0] = 0
            obj = ops.GenerateHuman(
                {
                    "sId": "Armature.001",
                    "sMode": "RANDOM_FULL",
                    "mParamConfig": {"sGender": "female"},
                }
            )
            bpy.context.scene.cursor.location[0] += dx
            obj = ops.GenerateHuman(
                {
                    "sId": "Armature.002",
                    "sMode": "RANDOM_FULL",
                    "mParamConfig": {"sGender": "male"},
                }
            )
            bpy.context.scene.cursor.location[1] += dy
        # endif
            
        # HumGen V4 test
        if "FULL_RANDOM" in active_tests:
            bpy.context.scene.cursor.location[0] = 0
            obj = ops.GenerateHuman(
                {
                    "sId": "Armature.001",
                    "sMode": "FULL_RANDOM",
                    "mParamConfig": {"sGender": "female"},
                }
            )
            bpy.context.scene.cursor.location[0] += dx
            obj = ops.GenerateHuman(
                {
                    "sId": "Armature.002",
                    "sMode": "FULL_RANDOM",
                    "mParamConfig": {"sGender": "male"},
                }
            )
            bpy.context.scene.cursor.location[1] += dy
        # endif

        if "RANDOM_FULL_GRID" in active_tests:
            for y in range(0, 2):
                bpy.context.scene.cursor.location[0] = 0
                for x in range(0, 4):
                    bpy.context.scene.cursor.location[0] += dx
                    obj = ops.GenerateHuman({"sId": "Armature.0{}{}".format(y, x), "sMode": "RANDOM_FULL"})
                bpy.context.scene.cursor.location[1] += dy
        # endif

        if "RANDOM_REALISTIC" in active_tests:
            bpy.context.scene.cursor.location[0] = 0
            obj = ops.GenerateHuman(
                {
                    "sId": "Armature.001",
                    "sMode": "RANDOM_REALISTIC",
                    "mParamConfig": {"gender": "male"},
                }
            )
            bpy.context.scene.cursor.location[0] += dx
            obj = ops.GenerateHuman(
                {
                    "sId": "Armature.002",
                    "sMode": "RANDOM_REALISTIC",
                    "mParamConfig": {"gender": "female"},
                }
            )
            bpy.context.scene.cursor.location[1] += dy
        # endif

        if "RANDOM_REALISTIC_GRID" in active_tests:
            for y in range(0, 2):
                bpy.context.scene.cursor.location[0] = 0
                for x in range(0, 4):
                    bpy.context.scene.cursor.location[0] += dx
                    obj = ops.GenerateHuman(
                        {
                            "sId": "Armature.0{}{}".format(y, x),
                            "sMode": "RANDOM_REALISTIC",
                        }
                    )
                bpy.context.scene.cursor.location[1] += dy
        # endif

        if "ZWICKY" in active_tests:
            zwicky_charlie = {
                "gender": "male",
                "type": "caucasian",
                "bodytype": ["thin", "athletic"],
                "height": "tall",
                "hair": "short",
                "clothing": "casual",
            }
            zwicky_dave = {
                "gender": "male",
                "type": "black",
                "bodytype": ["athletic", "average", "corpulent"],
                "height": ["short", "average"],
                "hair": "bald",
                "clothing": "business",
            }
            zwicky_elliot = {
                "type": "asian",
            }
            bpy.context.scene.cursor.location[0] = 0
            obj = ops.GenerateHuman(
                {
                    "xSeed": 1,
                    "sId": "Charlie",
                    "sMode": "ZWICKY",
                    "mParamConfig": zwicky_charlie,
                }
            )
            bpy.context.scene.cursor.location[0] += dx
            obj = ops.GenerateHuman(
                {
                    "xSeed": 2,
                    "sId": "Dave",
                    "sMode": "ZWICKY",
                    "mParamConfig": zwicky_dave,
                }
            )
            bpy.context.scene.cursor.location[0] += dx
            obj = ops.GenerateHuman(
                {
                    "xSeed": 3,
                    "sId": "Elliot",
                    "sMode": "ZWICKY",
                    "mParamConfig": zwicky_elliot,
                }
            )
            bpy.context.scene.cursor.location[1] += dy
        # endif

        if "ZWICKY_GRID" in active_tests:
            for y in range(0, 2):
                bpy.context.scene.cursor.location[0] = 0
                for x in range(0, 4):
                    bpy.context.scene.cursor.location[0] += dx
                    obj = ops.GenerateHuman({"sId": "Armature.0{}{}".format(y, x), "sMode": "ZWICKY"})
                bpy.context.scene.cursor.location[1] += dy
        # endif

    except Exception as e:
        bpy.context.area.ui_type = "TEXT_EDITOR"
        raise e
    # endtry


# enddef


# uncomment the following line when testing the script in Blender:

if __name__ == "__main__":
    _testHumanGeneration()
