# Inofficial HumGen V4 Documentation

# Beginning

- `from HumGen3D import Human`
- `o = Human.get_preset_options()`
- `h = Human.from_preset(o[0])`

# General parameters in exported JSON

## Age

|              | Value Range                     | Description      |
| ------------ | ------------------------------- | ---------------- |
| set          | `'Isn't this fun?'`             | Age of the human |
| age_color    | `"Isn't this fun?"`             |                  |
| age_wrinkels | `-- is en-dash, --- is em-dash` |                  |

## Details on functions
### Eyes

- Pupil color and iris color are used interchangeably used

### Hair

- `h.hair.eyebrows.set` --> Range Eyebrows_001...Eyebrows_009

### Expression
