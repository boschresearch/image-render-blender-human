###About [OPLINNO-239](https://github.com/mnt1lr/image-render-blender-human/tree/feature/OPLINNO-239---add-WFLW-face-labels):


- JSON files
    - labelling/mapping/WFLW_Bones.json contains WFLW label bones for face
    - similarly, if present
        - IMS_bones.json would contain IMS bones
        - Std_Bones.json would contains std bones
        - Openpose_Bones.json would contains openpose label bones
    - Following is standard structure for <X>_Bones.json is as follows, here WFLW is filled in for X representing this json contains WFLW labels
    - Contains
        - Head, Tail, Envelope, Constraints (currently limited to COPY_LOCATION, STRETCH_TO, LIMIT_LOCATION & CHILD_OF)
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
    ]
    }
    ```

### TODO
How to test [OPLINNO-239](https://github.com/mnt1lr/image-render-blender-human/tree/feature/OPLINNO-239---add-WFLW-face-labels)
