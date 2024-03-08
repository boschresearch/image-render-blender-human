#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: __init__.py
# Created Date: Friday, August 27th 2021, 10:50:34 am
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


##################################################################
try:
    import _bpy

    bInBlenderContext = True

except Exception:
    bInBlenderContext = False
# endtry

if bInBlenderContext is True:
    try:
        bl_info = { # needs to be removed 
            "name": "Generate a random Human",
            "blender": (2, 93, 0),
            "category": "Object",
        }

        from . import cls_gen_random_human
        # ## DEBUG ##
        import anybase.module

        # anybase.module.ReloadModule(_sName="anyblend", _bChildren=True, _bDoPrint=True) # Reload module anyblend
        anybase.module.ReloadCurrentChildModules(_bDoPrint=True) # Reload all child modules of the calling function's module
        # ###########
    except Exception as xEx:
        # pass
        print(">>>> Exception importing libs:\n{}".format(str(xEx)))
    # endif
# endif in Blender Context


def register():
    from . import cls_gen_random_human
    cls_gen_random_human.register()


# enddef


def unregister():
    cls_gen_random_human.unregister()


# enddef
