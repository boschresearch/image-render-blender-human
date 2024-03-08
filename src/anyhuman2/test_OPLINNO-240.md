### About [OPLINNO-239](https://github.com/mnt1lr/image-render-blender-human/tree/feature/OPLINNO-239---add-WFLW-face-labels):


- JSON files
    - [WFLW_Bones.json](https://github.com/mnt1lr/image-render-blender-human/blob/feature/OPLINNO-240---add-missing-v4-WFLW-eyebrow-labels/src/anyhuman2/labelling/mapping/WFLW_Bones.json) contains WFLW label bones for face

### What changed?

lVertexGroups renamed to 

OLD JSON :

    ```json
    {
        "sSkeletonType": "WFLW",
        "lBones": [
            {
                "sType": "WFLW",
                "sName": "WFLW_0_V1",
                "lHead": [...],
                "lTail": [...],
                "sParent": "head",
                "fEnvelope": 0.25,
                "fHeadRadius": 0.10000000149011612,
                "lConstraints": [
                    {
                        ...
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
        
NEW JSON :

    ```json
    {
        "sSkeletonType": "WFLW",
        "lBones": [
            {
                "sType": "WFLW",
                "sName": "WFLW_0_V1",
                "lHead": [...],
                "lTail": [...],
                "sParent": "head",
                "fEnvelope": 0.25,
                "fHeadRadius": 0.10000000149011612,
                "lConstraints": [
                    {
                        ...
                    }
                ]
            },{...},{...},{...}
        ],
        
        "lLabelVertices": 
        [
            {
                "sObject":"HG_Eyes",
                "lLabels":[
                    {
                        "sName": "eyeball.L",
                        "lVertices": [24]
                    },
                    {
                        "sName": "eyeball.R",
                        "lVertices": [1923]
                    }
                ]
            },
            {
                "sObject":"HG_Body",
                "lLabels":[
                    {
                        "sName": "WFlW_19",
                        "lVertices": [2421]
                    },
                    {
                        "sName": "WFLW_20",
                        "lVertices": [1923,1921]
                    }
                ]
            }
        ]
    }
    ```

### Limitations:
Limited to following constraints
> COPY_LOCATION


### How to test [OPLINNO-240](https://github.com/mnt1lr/image-render-blender-human/tree/feature/OPLINNO-240---add-missing-v4-WFLW-eyebrow-labels)
- 1. In dev.py, enable `FILE` mode, pass `src\\anyhuman2\\personas\\FILE_male.json` as `sFilename` under `mParamConfig` (line ~69). Make sure bOpenPoseHandLabels & bFacialRig are `True` in json file
- 2. change file input for sHandLabelFile & sWFLWLableFile (line. 291 & 297)
- 3. Hit play by opening `dev.py` in blender debug mode, Face labels should show up


### Next work
- 1. Improve left eyebrow labels position (should mirror right arrow labels), updates reflect in `WFLW_bones.json`
