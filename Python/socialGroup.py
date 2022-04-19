class SocialGroup:
    def __init__(self, name, characteristics, emotionalValence = 0.05):
        self.name = name
        #collection of the prototypical characteristics of the SG (each one with a name and a value 0 to 100)
        self.characteristics = characteristics
        #emotional valence to use in the computation of the accessibility if this social identity is salient
        self.emotionalValence = emotionalValence
        
        #just to obtain social identity
        self.fitness = None
        self.accessibility = None
        self.salience = None

        self.accessibilitySteps = []
        self.salienceSteps = []
        
        self.salienceSums = []
        self.salienceSims = []
        self.accessibilitySums = []
        self.accessibilitySims = []
    
    def clear(self, simNum):
        self.fitness = None
        self.accessibility = None
        self.salience = None
        
        lenSums = len(self.salienceSums)
        if lenSums > 0:
            for i in range(0, lenSums):
                self.salienceSums[i] += self.salienceSteps[i]
                self.accessibilitySums[i] += self.accessibilitySteps[i]
        else:
            self.salienceSums = self.salienceSteps
            self.accessibilitySums = self.accessibilitySteps

        self.salienceSims = [x / simNum for x in self.salienceSums] 
        self.accessibilitySims = [x / simNum for x in self.accessibilitySums] 
            
        self.accessibilitySteps = []
        self.salienceSteps = []