class DictatorGame:
    def __init__(self, baselineOffer, potSize, emotRelevanceInGroup, emotRelevanceOutGroup):
        self.baselineOffer = baselineOffer
        self.potSize = potSize
        self.emotRelevanceInGroup = emotRelevanceInGroup
        self.emotRelevanceOutGroup = emotRelevanceOutGroup
        self.groupsAverageWealthSteps = {}
        
        self.groupsAverageWealthSums = {}
        self.groupsAverageWealthSims = {}
    
    def offer(self, agentOffering, agentReceiving, salience, inGroupBool, minSalienceThreshold):
        #formula of offer
        if salience < minSalienceThreshold: #no group 
            offer = self.baselineOffer/100 * self.potSize
        else:    
            if inGroupBool:
                offer = (self.baselineOffer/100 * self.potSize) * (1 + salience)
            else:
                offer = (self.baselineOffer/100 * self.potSize) * (1 - salience)
        #update agent money
        agentOffering.moneyReceived += self.potSize - offer
        agentReceiving.moneyReceived += offer
        
        if inGroupBool: 
            return self.emotRelevanceInGroup
        else:
            return self.emotRelevanceOutGroup
    
    def updateAverageWealth(self, groupName, agents):
        sumMoney = 0
        lenAgents = len(agents)
        for a in agents:
            sumMoney += a.moneyReceived
        avg = sumMoney/lenAgents
        if (groupName in self.groupsAverageWealthSteps):
            self.groupsAverageWealthSteps[groupName].append(avg)
        else:
            self.groupsAverageWealthSteps[groupName] = [avg]
    
    def clear(self, simNum):
        for sg in self.groupsAverageWealthSteps:
            
            wealth = self.groupsAverageWealthSteps[sg]
            if sg in self.groupsAverageWealthSums:
                lenWealth = len(wealth)
                for i in range(0, lenWealth):
                    self.groupsAverageWealthSums[sg][i] += wealth[i]
            else:
                self.groupsAverageWealthSums[sg] = wealth
                
        for sg in self.groupsAverageWealthSums:
            aux = []
            sumWealth = self.groupsAverageWealthSums[sg]
            for el in sumWealth:
                aux.append(el/simNum)
                
            self.groupsAverageWealthSims[sg] = aux
                
        self.groupsAverageWealthSteps = {}
