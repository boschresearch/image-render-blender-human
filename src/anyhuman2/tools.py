#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: \ops.py
# Created Date: Friday, March 25th 2022
# Author: Dirk Fortmeier (BEG/ESD4)
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
import random


############################################################################################
def FixClothBoneWeights(skinMesh, clothMeshes, paramMaxDist=10.0):

    # use this option to use two separte kd trees for estimation of closest vertex
    # this can help when there is self-intersection of the skin at the armpits
    bUseTwoTrees = False

    for clothMesh in clothMeshes:
        noVertices = len(skinMesh.data.vertices)

        # sort the skin vertices into to separate trees based on their orientation
        # this is a hack to prevent wrong assignemnt in the armpits of
        # big humans (intersection)
        skinVertexTreeLF = mathutils.kdtree.KDTree(noVertices)
        skinVertexTreeRF = mathutils.kdtree.KDTree(noVertices)

        for i, vertex in enumerate(skinMesh.data.vertices):
            vertexWorld = skinMesh.matrix_world @ vertex.co

            normalWorld = vertex.normal
            leftFacing = normalWorld.x >= 0
            if leftFacing and bUseTwoTrees:
                skinVertexTreeLF.insert(vertexWorld, i)
            else:
                skinVertexTreeRF.insert(vertexWorld, i)
            # endif
        # endfor skinvertex

        skinVertexTreeLF.balance()
        skinVertexTreeRF.balance()

        clothMesh.vertex_groups.clear()

        context = bpy.context
        scene = context.scene

        for vertex_group in skinMesh.vertex_groups:
            clothMesh.vertex_groups.new(name=vertex_group.name)

        sum = 0.0
        count = 0
        for name, kb in clothMesh.data.shape_keys.key_blocks.items():
            sum += kb.value
            count += 1

        mult = sum if sum < 1.0 else sum / float(count)

        for id_cloth_vertex, clothVertex in enumerate(clothMesh.data.vertices):
            clothVertexWorld = clothMesh.matrix_world @ clothVertex.co

            x = clothVertex.co

            for name, kb in clothMesh.data.shape_keys.key_blocks.items():
                x += (kb.data[id_cloth_vertex].co - clothVertex.co) * kb.value
            # endfor

            clothVertexWorld = clothMesh.matrix_world @ x
            clothNormalWorld = clothMesh.matrix_world.to_3x3() @ clothVertex.normal
            leftFacing = clothNormalWorld.x >= 0

            if leftFacing and bUseTwoTrees:
                closestVectorWorld, id_skin_vertex, dist = skinVertexTreeLF.find(
                    clothVertexWorld
                )
            else:
                closestVectorWorld, id_skin_vertex, dist = skinVertexTreeRF.find(
                    clothVertexWorld
                )
            # endif

            skin_vertex = skinMesh.data.vertices[id_skin_vertex]

            if dist < paramMaxDist:
                already_in = []
                for g in skin_vertex.groups:
                    group = clothMesh.vertex_groups[g.group]

                    weight = g.weight

                    if not group.name in already_in:
                        group.add([id_cloth_vertex], weight, "ADD")
                        already_in.append(group.name)
                    # endif
                # endfor
            # endif
    # endfor clothMesh


# enddef

# debug code for testing within blender
# skinMesh = bpy.data.objects['HG_Body.001']
# clothMeshes = [
#    bpy.data.objects['HG_Flannel_Female.002']
#    ]
#
# FixClothBoneWeights(skinMesh, clothMeshes)
#
# print("done")


############################################################################################
def RandomUniformDiscrete(_fMin, _fMax, _iCount=101):
    """Returns uniformly distributed random values over _iCount equally spaced discrete values in range [_fMin, _fMax]

    Parameters
    ----------
    _fMin : float
        minimal value
    _fMax : float
        maximal value
    _iCount : int
        number of discrete values

    Returns
    -------
    float
        a random value
    """

    if _iCount < 2:
        raise RuntimeError("Count value has to be >= 2")
    # endif

    fRand = random.randint(0, _iCount - 1) / (_iCount - 1)
    fRand = fRand * (_fMax - _fMin) + _fMin

    return fRand


# enddef
