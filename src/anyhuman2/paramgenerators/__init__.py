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
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# -----
# Copyright (c) 2022 Robert Bosch GmbH and its subsidiaries.
# All rights reserved.
# -----
###

import random

# from . import file
from . import persona
from . import random_full
from . import random_realistic
from . import zwicky

######################################################################
def ComputeParams(mode, params, overwrite, generator_params):
    """
    Computes a set of parameters for human generation.
    Currently available modes are:
    - PERSONA: for a set of names ('alice', 'bob',  ...), return predefined values
    - RANDOM_FULL: randomize every parameter of its possible range
    - RANDOM_REALISTIC: randomize every parameter but within realistically apearing bounds
    - ZWICKY: randomize based on a Zwicky box like description
    - FILE: specify a path to a json file with predefined values

    Parameters
    ----------
    mode : string
        Mode for parameter computation, see above
    params : dict
        dictionary of parameters for the mode, see the implementation of the mode for details
    overwrite : dict
        dict of parameters that shall overwrite the computed values

    Returns
    -------
    dict
        dictionary with parameters for human generation

    """
    new_params = GetParams(mode, params, generator_params)


    return new_params


# enddef

######################################################################
def GetParams(mode, params, generator_params):
    """
    Computes a set of parameters for human generation.
    Currently available modes are:
    - PERSONA: for a set of names ('alice', 'bob',  ...), return predefined values
    - RANDOM_FULL: randomize every parameter of its possible range
    - RANDOM_REALISTIC: randomize every parameter but within realistically apearing bounds
    - ZWICKY: randomize based on a Zwicky box like description
    - FILE: Reads JSON which was exported using HumGenV4 as_dict() function

    Parameters
    ----------
    mode : string
        Mode for parameter computation, see above
    params : dict
        dictionary of parameters for the mode, see the implementation of the mode for details
    generator_params:
        TODO

    Returns
    -------
    dict
        dictionary with parameters for human generation

    """
    new_params = {}

    if mode == "RANDOM_FULL":
        new_params = random_full.FullyRandomizeParams(params, generator_params)
    elif mode == "RANDOM_REALISTIC":
        new_params = random_realistic.RealisticRandomizeParams(params, generator_params)
    elif mode == "ZWICKY":
        new_params = zwicky.ZwickyParams(params, generator_params)
    elif mode == "PERSONA":
        new_params = persona.PersonaParams(params, generator_params)
    elif mode == "FILE":
        new_params = file.FileParams(params)
    else:
        raise NotImplementedError(
            f"Please specify a valid mode for anyhuman parameter generation, not {mode}"
        )

    return new_params

