
import json
import os


class GeneralRandomParameters():
    """Class to generate universally needed random parameters for HumGenV4 Armatures
        Uses own Random instance for reproducibility
 
    """
    def __init__(self, params:dict, generator_config:dict, rnd) :
        self.params:dict = params
        self.generator_config:dict = generator_config
        self.rnd = rnd
        self.sGender:str = self.params.get("sGender", self.rnd.choice(["male", "female"]))
        
    
    def GetGender(self) -> str:
        return self.sGender
    
    def ArmatureName(self) -> str:
        """Name the armature if any information is available
        """
        if "sId" in self.params:
            sArmatureName = self.params["sId"]
        elif "sPersonaId" in self.params:
            sArmatureName = self.params["sPersonaId"].title()
        else:
            sArmatureName = None
        return sArmatureName

    def RandomizeOutfit(self) -> str:
        """Function to select a random outfit
            lIgnoredOutfitsFemale... List of female outfits which are ignored
            lIgnoredOutfitsMale... List of male outfits which are ignored

        Parameters
        ----------
        generator_config : dict
            dict consisting of subdirectories containing different models, outfits, footwear, hair styles,...
        """
        # Ignored Outfits
        lIgnoredOutfitsFemale = ["Flight Suit", "Lab Tech", "Pirate", "BBQ"]
        lIgnoredOutfitsMale = ["Lab Tech", "Pirate"]

        outfit_list = [
            item
            for item in self.generator_config.dict_clothes[self.sGender]
            if item not in (lIgnoredOutfitsMale + lIgnoredOutfitsFemale)
        ]

        # Select an outfit
        outfit = self.generator_config.dict_clothes[self.sGender][self.rnd.choice(outfit_list)].replace('/', os.sep)
        return outfit

    def RandomFootwear(self) -> str:
        """Function that selects a footwear from a sub dictionary of generator_config
        Parameters
        ----------
        generator_config : dict
            dict consisting of subdirectories containing different models, outfits, footwear, hair styles,...
        """
        # Select footwear
        footwear = self.rnd.choice(list(self.generator_config.dict_footwear[self.sGender].values())).replace('/', os.sep)
        return footwear

    def RandomizeHair(self) -> tuple:
        """Function to randomize different hairs such as regular hair (normal head hair), face hair (beard) for male
           armature, a select a random eyebrow.
    

        Parameters
        ----------
        generator_config : dict
            dict consisting of subdirectories containing different models, outfits, footwear, hair styles,...
        Returns
        -------
        fMale : float
            0...female, 1... female
        dFaceHair : dict
            dictionary containing information about gender specific face hair. Base appearance is chosen from dict_face_hair
        dBeardLength : dict
            dictionary which contains specific information about the particle systems used to generate facial hair   
        sRegularHair : string
            Relative path to a hair style
        sEyebrows : string
            Selected eyebrow preset
        """
        # Gender specific actions
        if self.sGender == "female":
            dFaceHair = {} # Facial hair
            dBeardLength = {} # Beard length
            fMale = 0.0
        elif self.sGender == "male":
            # Coin flip for beard or no beard
            fMale = 1.0
            dFaceHair = {} # Facial hair
            if self.rnd.random() < 0.5:
                sFaceHair = self.rnd.choice(list(self.generator_config.dict_face_hair["male"].values())) # Facial hair
                dFaceHair = {
                    "set": sFaceHair,
                    "lightness": self.rnd.uniform(0, 1.0),
                    "redness": self.rnd.uniform(0, 1.0),
                    "roughness": self.rnd.uniform(0, 1.0),
                    "salt_and_pepper": self.rnd.uniform(0, 1.0),
                    "roots": self.rnd.uniform(0, 1.0),
                    "root_lightness": self.rnd.uniform(0, 5.0),
                    "root_redness": self.rnd.uniform(0, 1.0),
                    "roots_hue": self.rnd.uniform(0, 1.0),
                    "fast_or_accurate": 1.0, # Accurate
                    "hue": self.rnd.uniform(0, 1.0),
                }
                # Randomize facial hair concerning length
                addon_path = self.generator_config.dict_info["HumGenV4 Path"]
                face_hair_path = sFaceHair.replace('/', '\\')
                with open(os.path.join(addon_path, face_hair_path), 'r') as f:
                    file = json.load(f)
                dBeardLength = file
                for key, value in enumerate(dBeardLength["hair_systems"]):
                    dBeardLength["hair_systems"][value].update({"length": self.rnd.uniform(0, 1.0)})
            else:
                dBeardLength = {} # Empty
            # endif
        # endif


        # Eye brows are part of the hair particle and can not be accessed via a dictionary, there we provide them as list
        eyebrows = [
                'Eyebrows_001',
                'Eyebrows_002',
                'Eyebrows_003',
                'Eyebrows_004',
                'Eyebrows_005',
                'Eyebrows_006',
                'Eyebrows_007',
                'Eyebrows_008',
                'Eyebrows_009'
                ]
        sEyebrows = self.rnd.choice(eyebrows)
        # Regular hair
        sRegularHair = self.rnd.choice(list(self.generator_config.dict_regular_hair[self.sGender].values()))
        return (fMale, dFaceHair, dBeardLength, sRegularHair, sEyebrows)

    def RandomizeSkin(self) -> str:
        """Select random skin texture from presets.
        """
        texture = self.rnd.choice(list(self.generator_config.dict_textures[self.sGender].values()))
        return(texture)

    def RandomizeHeight(self) -> tuple: 
        """Function to generate a randomly sized armature.
        """


        # Height generation, see HumGenV4 ...\height.py
        height = self.rnd.uniform(140, 200) # in cm
        if height > 184:
            fHeight_200 = (height - 184) / (200 - 184)
            fHeight_150 = 0.0
        else:
            fHeight_150 = -((height - 150) / (184 - 150) - 1)
            fHeight_200 = 0.0
        # endif

        return(fHeight_150, fHeight_200, height)
    
    ############################################################################################
    def RandomUniformDiscrete(self, _fMin, _fMax, _iCount=101):
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

        fRand = self.rnd.randint(0, _iCount - 1) / (_iCount - 1)
        fRand = fRand * (_fMax - _fMin) + _fMin

        return fRand


# enddef