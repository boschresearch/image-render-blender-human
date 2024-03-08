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

import json
import os

######################################################################
def PersonaParams(params, generator_params):
    """ Create a anyhuman from a humgenv4 preset. 

    Parameters
    ----------
    params : dict
        catharsys dictionary
    generator_params : dict
        _description_

    Returns
    -------
    _type_
        _description_
    """
    
    persona_id = params["sPersonaId"].title()
    if params["sId"] in params:
        sArmatureName = params["sId"]
    elif params["sPersonaId"] in params:
        sArmatureName = params["sPersonaId"].title()
    else:
        sArmatureName = None

    HumGenV4AddOnPath = generator_params.dict_info["HumGenV4 Path"]
    # Determine if persona_id is valid humgen preset and the gender of the preset 
    for gender, model in generator_params.dict_models.items():
        if persona_id in model:
            filename = generator_params.dict_models[gender][persona_id]
            FullPath = os.path.join(HumGenV4AddOnPath, filename.replace("/", os.sep))
            with open(FullPath, "r") as file:
                dictHumGen_V4 = json.load(file)

    dictAnyhuman = {
        "dictCustom": {
            "sGender": gender,
            "sArmatureName": sArmatureName,
            "bOpenPoseHandLabels": None,
            "bFacialRig": None,
            "sPoseFilename": None,
            "dBeardLength": None
        },
        "dictHumGen_V4": dictHumGen_V4,
    }
    return dictAnyhuman


# enddef
