import json
import agent
import socialContext
import socialGroup

class FileManager:
    def __init__(self, fileAgents, fileContext):
        self.fileAgents = fileAgents
        self.fileContext = fileContext
        
        self.agents = []

        initA = self.initAgents()
        initC = self.initContext()
        
        self.loadedInput = (initA and initC)
        
    def readJSONFile(self, file):
        data = None
        try:
            # open JSON file
            f = open(file)
            # returns JSON object as a dictionary
            data = json.load(f)
        except:
            print("Problem opening or loading file!")
        return data
    
    def initAgents(self):
        #agents not initialized yet
        data = self.readJSONFile(self.fileAgents)
        if data is not None:
            for d in data['agents']:
                nameA = d['name']
                charA = {}
                kbA = []
                for c in d['characteristics']:
                    charA[c['name']] = c['value']
                for kb in d['knowledgeBase']:
                    nameSG = kb['name']
                    charSG = {}
                    emotionalValence = kb['emotionalValence']
                    for ckb in kb['characteristics']:
                        charSG[ckb['name']] = ckb['value']
                    kbA.append(socialGroup.SocialGroup(nameSG, charSG, emotionalValence))
                self.agents.append(agent.Agent(nameA, charA, kbA))

            #Clustering
            self.thresholdDist = data['thresholdDist']
            #Normative Fit
            self.thresholdNormative = data['thresholdNormative']
            #Comparative fit
            self.comparativeFitAlpha = data['comparativeFitAlpha']
            self.comparativeFitBeta = data['comparativeFitBeta']
            self.minimalSalienceThreshold = data['minimalSalienceThreshold']
            return True
        return False
    
    def initContext(self):
        data = self.readJSONFile(self.fileContext)
        if data is not None:
            theme = {}
            for t in data['context']['theme']:
                theme[t['name']] = t['weight']
            
            agentsCtxNames = data['context']['agentsPresent']
            agentsCtx = []
            for a in self.agents:
                if a.name in agentsCtxNames:
                    agentsCtx.append(a)
                    
            self.socialCtxObj = socialContext.SocialContext(agentsCtx, theme)
            return True
        return False
    