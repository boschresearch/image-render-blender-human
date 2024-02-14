# Anyhuman2

Anyhuman2 is an addon for Catharsys. It is using a [fork of HumGen V4](https://github.com/mnt1lr/HumGen3D/tree/testing), maintaining the same interfaces as Anyhuman (based on HumGen V3).

- JSON files
- Full-random parameters

[InofficialHumGenV4Documentation](#Inofficial-HumGen-V4-Documentation)

# Beginning

- `from HumGen3D import Human`
- `o = Human.get_preset_options('male')`
- `h = Human.from_preset(o[0])`

[GeneralParametersInExportedJSON](#General-parameters-in-exported-JSON)

## Age

### Age parameters accessible via API

|              | Value Range | Description               |
| ------------ | ----------- | ------------------------- | ------- |
| set          | `20...80`   | Age of the human in years |
| age_color    | `0...1`     | unknown                   |
| age_wrinkels | `0...6`     |                           | unknown |

### Age parameters accessible via Blender

|              | Value Range | Description               |
| ------------ | ----------- | ------------------------- | ------- |
| set          | `20...80`   | Age of the human in years |
| age_color    | `0...1`     | unknown                   |
| age_wrinkels | `0...6`     |                           | unknown |

## Eyes parameters accessible via API

|                | Value Range | Description |
| -------------- | ----------- | ----------- | --------------------- |
| iris_color     | `0...1`     | Iris color  | 4 Vector (R, G, B, A) |
| outer_material | Material    | Shader      | Shader network        |
| inner_material | Material    | Shader      | Shader network        |
| sclera_color   | `0...1`     |             | 4 Vector (R, G, B, A) |

- Pupil color and iris color are used interchangeably used

### Hair

- `h.hair.eyebrows.set` --> Range Eyebrows_001...Eyebrows_009

### Expression

## Good to know
- `ear_livekeys = human.keys.filtered("face_proportions", "ears”)`

Each of them gives back a LiveKeyItem https://github.com/OliverJPost/HumGen3D/blob/main/human/keys/keys.py#L212
With methods like “value” getter and setter and “set_without_update” for changing large amount of livekeys

