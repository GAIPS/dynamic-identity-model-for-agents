class Agent:
    def __init__(self, name, characteristics, normativeGroups, scenario = None):
        self.name = name
        #collection of the agent's personal characteristics (each one with a name and a value 0 to 1)
        self.personalCharacteristics = characteristics
        #collection of normative groups in the agent's KB
        self.normativeGroups = normativeGroups
        
        self.scenario = scenario     
        #for the rest of the model calculations
        self.salientIdentity = None
    