class Agent:
    def __init__(self, name, characteristics, knowledgeBase):
        self.name = name
        #collection of the agent's personal characteristics (each one with a name and a value 0 to 100)
        self.personalCharacteristics = characteristics
        #collection of social groups in the agent's KB
        self.knowledgeBase = knowledgeBase
        
        self.salientSocialIdentity = None
    
        self.presentGroups = []
        
        #dictator game
        self.moneyReceived = 0
        
    def clear(self, simNum):
        self.salientSocialIdentity = None
        self.presentGroups = []
        self.moneyReceived = 0
        for sg in self.knowledgeBase:
            sg.clear(simNum)