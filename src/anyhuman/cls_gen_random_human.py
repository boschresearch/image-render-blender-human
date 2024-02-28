#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: \cls_gen_random_human.py
# Created Date: Friday, May 20th 2022, 11:28:15 am
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
from . import dev


class GenRandomHumans(bpy.types.Operator):
    """Generate a random Human"""  # Use this as a tooltip for menu items and buttons.

    bl_idname = (
        "hg3d.generate"  # Unique identifier for buttons and menu items to reference.
    )
    bl_label = "Generate Humans"  # Display name in the interface.
    bl_options = {"REGISTER"}  # Enable undo for the operator.

    def execute(self, context):  # execute() is called when running the operator.

        dev._testHumanGeneration()

        return {"FINISHED"}  # Lets Blender know the operator finished successfully.

    # enddef


# endclass


def menu_func(self, context):
    self.layout.operator(GenRandomHumans.bl_idname)


# enddef


def register():
    print("anyhuman: register GenRandomHuman...")
    # TODO: Unregistering GenRandomHumans always throws exception. Don't know what the problem is.
    # bpy.utils.register_class(GenRandomHumans)
    # bpy.types.VIEW3D_MT_object.append(menu_func)  # Adds the new operator to an existing menu.


# enddef


def unregister():
    print("anyhuman: unregister GenRandomHuman...")
    # bpy.utils.unregister_class(GenRandomHumans)


# enddef
