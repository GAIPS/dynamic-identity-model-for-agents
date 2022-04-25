class SocialGroup:
    def __init__(self, name, characteristics, accessibility):
        self.name = name
        #collection of the prototypical characteristics of the SG (each one with a name and a value 0 to 100)
        self.characteristics = characteristics
        #initial accessibility of the normative group
        self.accessibility = accessibility
        
        #for the rest of the model calculations
        self.type = 0; #not present - 0, present - 1
        self.dispersion = None;
        self.fitness = None;
        self.salience = None;
        #for the plots
        self.salienceSteps = []
        self.accessibilitySteps = []
        self.salienceFinalStep = []
        self.accessibilityFinalStep = []
    