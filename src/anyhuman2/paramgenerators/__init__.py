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

from . import file
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
    new_params = ResolveRandomParams(mode, new_params, generator_params)

    # overwrite the configuration values if present in overwrite dict
    # also, deal with nested values (only overwrite values given in overwrite dict)
    for key, value in overwrite.items():
        if isinstance(value, dict):
            for inner_key, inner_value in value.items():
                new_params[key][inner_key] = inner_value
            # endfor
        else:
            new_params[key] = value
        # endif

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


def ResolveRandomParamValue(mode, param, params, generator_params):
    # get a set of parameters matching to generator mode
    new_params = GetParams(mode, params, generator_params)

    value = "random"
    if param == "eyebrows_style":
        value = random.randint(0, 10)
    # elif param == 'face':
    #     pass
    elif param == "outfit_style":
        value = new_params["outfit"]["outfit_style"]
        pass
    # elif param == 'outfit_color':
    # pass
    # elif param == 'footwear_style':
    #     pass
    else:
        print(f"!!! param {param} could not be randomized")
    # endif
    return value


######################################################################
def ResolveRandomParamsRecursive(mode, rec_params, params, generator_params):
    for key, value in rec_params.items():
        print(key)
        if isinstance(value, dict):
            rec_params[key] = ResolveRandomParamsRecursive(
                mode, value, params, generator_params
            )
        elif value == "random":
            print(value)
            rec_params[key] = ResolveRandomParamValue(
                mode, key, params, generator_params
            )
        # endif
    # endfor

    return rec_params


######################################################################
def ResolveRandomParams(mode, params, generator_params):
    """
    Resolve all entires 'random' in a dict of human generation parameters.

    Parameters
    ----------
    params : dict
        dict of parameters created by a parameter generator
    generator_params : dict
        dictionary of settings of humgen plugin

    Returns
    -------
    params
        dictionary with parameters for human generation without random entries
    """
    params = ResolveRandomParamsRecursive(mode, params, params, generator_params)

    return params
