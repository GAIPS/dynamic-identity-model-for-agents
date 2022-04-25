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
            for a in data['agents']:
                nameA = a['name']
                charA = {}
                kbA = []
                for c in a['characteristics']:
                    charA[c['name']] = c['value']
                for sg in a['normativeGroups']:
                    nameSG = sg['name']
                    charSG = {}
                    accessibility = sg['accessibility']
                    for c in sg['characteristics']:
                        charSG[c['name']] = c['value']
                    kbA.append(socialGroup.SocialGroup(nameSG, charSG, accessibility))
                self.agents.append(agent.Agent(nameA, charA, kbA))
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
    