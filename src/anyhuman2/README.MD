# Inofficial HumGen V4 Documentation

# Beginning

- `from HumGen3D import Human`
- `o = Human.get_preset_options('male')`
- `h = Human.from_preset(o[0])`

# General parameters in exported JSON

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
