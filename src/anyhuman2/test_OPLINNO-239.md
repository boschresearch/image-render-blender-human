### About [OPLINNO-239](https://github.com/mnt1lr/image-render-blender-human/tree/feature/OPLINNO-239---add-WFLW-face-labels):


- JSON files
    - [WFLW_Bones.json](https://github.com/mnt1lr/image-render-blender-human/blob/feature/OPLINNO-239---add-WFLW-face-labels/src/anyhuman2/labelling/mapping/WFLW_Bones.json) contains WFLW label bones for face
    - similarly, if present under [mapping](https://github.com/mnt1lr/image-render-blender-human/tree/feature/OPLINNO-239---add-WFLW-face-labels/src/anyhuman2/labelling/mapping)
        - IMS_bones.json would contain IMS bones
        - Std_Bones.json would contains std bone labels
        - Openpose_Bones.json would contains openpose labels
    - Following is standard structure for file <<X>>_Bones.json is as follows, here WFLW is filled in for X representing this json contains WFLW labels
    - Contains
        - Head, Tail, Envelope, Constraints (currently limited to `COPY_LOCATION`, `STRETCH_TO`, `LIMIT_LOCATION`, `CHILD_OF` & `DAMPED_TRACK`)
    ```json
    {
        "sSkeletonType": "WFLW",
        "lBones": [
            {
                "sType": "WFLW",
                "sName": "WFLW_0_V1",
                "lHead": [
                    0.29790136218070984,
                    1.3332699537277222,
                    0.8380638360977173
                ],
                "lTail": [
                    0.29790136218070984,
                    1.343269944190979,
                    0.8380638360977173
                ],
                "sParent": "head",
                "fEnvelope": 0.25,
                "fHeadRadius": 0.10000000149011612,
                "lConstraints": [
                    {
                        "sType": "COPY_LOCATION",
                        "sBone": "AT.Label;WFLW;WFLW_0_V1",
                        "sTarget": "HG_Body.001",
                        "sSubtarget": "WFLW_0",
                        "bUseX": true,
                        "bUseY": true,
                        "bUseZ": true,
                        "bInvertX": false,
                        "bInvertY": false,
                        "bInvertZ": false,
                        "sTargetSpace": "WORLD",
                        "sOwnerSpace": "WORLD",
                        "fInfluence": 1.0
                    }
                ]
            },{...},{...},{...}
        ],
        "lVertexGroups": [
            {
                "sObject": "HG_Eyes.001",
                "sName": "eyeball.L",
                "lVertices": [...]
            },{...},{...}
        ]
    }
    ```

### Differences in vertex location of WFLW landmarks in Humgen v3 & Humgen v4 version
    - all good with below few exceptions:
        - OBJECT & POSE MODE:
            - AT.Label;WFLW;WFLW_19_V1
            - More distance b/w 51 & 52
            - 33-41 & 42-50 - eye brows (both left and right side)
            - 96 & 97   - iris
        - EDIT MODE:
            - No issues as in POSE & OBJECT mode, eyebrows labels are intact, but all labels are at a fixed offset from face
    - TODO: fix above exceptions


### How to test [OPLINNO-239](https://github.com/mnt1lr/image-render-blender-human/tree/feature/OPLINNO-239---add-WFLW-face-labels)
- 1. In dev.py, enable `FILE` mode, pass `src\\anyhuman2\\personas\\FILE_male.json` as `sFilename` under `mParamConfig` (line ~69). Make sure bOpenPoseHandLabels & bFacialRig are `True` in json file
- 2. change file input for sHandLabelFile & sWFLWLableFile (line. 291 & 297)
- 3. Hit play by opening `dev.py` in blender debug mode, Face labels should show up (of-course with exceptions as stated above)
