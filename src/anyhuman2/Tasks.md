# ToDo's 

- Check if interfaces are the same as in anyhuman1/humgenV3, e.g.
  `ops.GenerateHuman(
              {
                  "sId": "Armature.002",
                  "sMode": "RANDOM_FULL",
                  "mParamConfig": {"sGender": "male"},
              }
              `
- For each function e.g. `CreateFullRandomHuman` there must be:

  - export JSON files, describing the generated human fully must be available. --> as_dict function from Humgen + custom dictionaries (posefilename) resulting generator_params.json; keys in dictionary which are ONLY available in HumgenV4 should have a suffix "V4", e.g. "FaceRigV4": "random"
  - a blend file with the created human --> probably catharsys functionaility; dont work on it
  - An image of the created human --> probably catharsys functionaility; dont work on it
  - Face rig must be available
  - Label bones must exist (vinayak handpose stuff, tobias face label bones) --> lets write functions for handpose labels and face labels --> should be default argument in any function (e.g. `CreateFullRandomHuman`), user has to explicitly turn it off.

- Use as_dict() of HumGenV3 to export a human
- Modify `CreateHumanFromJSON` function so that it can read the output JSON from `CreateFullRandomHuman`

- Write a function which covers the random_realistic.py functionality


