from sklearn.cluster import KMeans
import numpy as np
import math
import matplotlib.pyplot as plt
import socialGroup
import csv
import os

class Simulation:
    def __init__(self, numSteps, numRuns, agents, socialCtx, thresholdCluster, thresholdNormative, comparativeFitAlpha, comparativeFitBeta, thresholdMinimalSalience, outputF, dictator):
        self.numSteps = numSteps
        self.numRuns = numRuns
        
        self.agents = agents
        self.socialCtx = socialCtx
        self.thresholdCluster = thresholdCluster
        self.thresholdNormative = thresholdNormative
        self.comparativeFitAlpha = comparativeFitAlpha
        self.comparativeFitBeta = comparativeFitBeta
        self.thresholdMinimalSalience = thresholdMinimalSalience
        self.outputF = outputF
        self.outputCSVfile = self.outputF + '/output.csv'
        self.dictator = dictator

        self.plotSymbols = ["o", "v", "H", "*", "X", "d", "P", "s", "D", "p"]
        self.colors = ["red", "blue"]
        self.colorsAgents = ["yellow", "aqua", "green", "pink", "brown", "darkorange", "purple", "gray", "olive", "magenta"]
        self.maxCharacteristic = 100
        
        
        if os.path.exists(self.outputCSVfile):
            os.remove(self.outputCSVfile)
        self.csvPropertiesAgents()
        
        self.cycle()
    
    def distanceToCentroids(self, first, second):
        distance = []
        lenFirst = len(first)
        for i in range(0, lenFirst):          
            auxDist = self.distanceWeights(first[i], second[i])           
            distance.append(auxDist)
        return distance
    
    def distanceWeights(self, first, second):
        lenThird = len(self.contextWeights)
        lDist = abs(np.array(first)-np.array(second))
        auxDist = 0
        #weighted euclidian distance
        for j in range(0, lenThird):
            auxDist += self.contextWeights[j] * (lDist[j])**2 
        dist = math.sqrt(auxDist)
        return dist
    
    '''CSV Functions'''
    def csvPropertiesAgents(self):
        #Simulation properties
        with open(self.outputCSVfile, 'a', newline='') as csvfile:
            fieldnames = ['num_runs', 'num_steps', 'num_agents', 'threshold_cluster', 'threshold_normative', 'threshold_minimal_salience', 'comparative_fit_alpha', 'comparative_fit_beta']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)        
            writer.writeheader()
            writer.writerow({'num_runs': self.numRuns, 'num_steps': self.numSteps, 'num_agents': len(self.agents), 'threshold_cluster': self.thresholdCluster, 'threshold_normative': self.thresholdNormative, 'threshold_minimal_salience': self.thresholdMinimalSalience, 'comparative_fit_alpha': self.comparativeFitAlpha, 'comparative_fit_beta': self.comparativeFitBeta})
            writer = csv.writer(csvfile)
            writer.writerow([''])
        #Agents        
        with open(self.outputCSVfile, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            lst = ['agent_name']
            for c in self.socialCtx.theme:
                lst.append(c)
            writer.writerow(lst)
            for a in self.agents:
                lst = [a.name]
                for c in a.personalCharacteristics:
                    lst.append(a.personalCharacteristics[c])
                writer.writerow(lst)
            writer.writerow([''])
   
    #Agent Salience and Accessibility by groups
    def csvSalienceAccessibility(self):
        with open(self.outputCSVfile, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            numGroups = len(self.clustersCentroids)
            for j in range(0, numGroups):
                writer.writerow(['group' + str(j+1)])
                writer.writerow([''])
                for a in self.socialCtx.agentsPresent:
                    sg = a.knowledgeBase[j]
                    writer.writerow([a.name])
                    writer.writerow(['salience'])
                    salience = np.round(np.array(sg.salienceSims), 4)
                    writer.writerow(salience)
                    accessibility = np.round(np.array(sg.accessibilitySims), 4)
                    writer.writerow(['accessibility'])
                    writer.writerow(accessibility)
                    writer.writerow([''])
            writer.writerow([''])
    #Group Wealth
    def csvWealth(self):
        with open(self.outputCSVfile, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for i, sg in enumerate(self.dictator.groupsAverageWealthSims):
                writer.writerow(['group' + str(i+1)])
                writer.writerow(['wealth'])
                wealth = np.round(np.array(self.dictator.groupsAverageWealthSims[sg]), 4)
                writer.writerow(wealth)
                writer.writerow([''])
        
    '''Agents Cycle'''               
    def cycle(self):
        self.clustering()
        #print("\n")
        #Run simulation
        for r in range(0, self.numRuns):
            self.ingroupNr=0
            self.outgroupNr=0
            for s in range(0, self.numSteps + 1):
                #For each agent
                for idxAgent, a in enumerate(self.socialCtx.agentsPresent):
                    #print("Agent " + a.name)
                    self.normativeFit(a)
                    self.comparativeFit(a)
                    self.accessibility(a, idxAgent)
                    self.salienceSocialGroup(a)
                    self.salientActiveIdentity(a, idxAgent)
                    self.listGraphics(a)
                    emotValence = self.playDictatorGame(a, idxAgent)
                    self.updateAccessibility(a, emotValence)
                    #print("\n")
                self.computeAverageWealth()
            print("Simulation " + str(r))        
            self.clearSimulation()
        
        self.csvSalienceAccessibility()
        self.csvWealth()
        self.showSalienceAccessibilityPlots(True)
        self.showSalienceAccessibilityPlots(False)
        self.showAverageWealthGroupsPlots()
    
    '''Clustering'''    
    def clustering(self):
        kMeansCycle = True
        k = 1
        
        self.dataAgents = []   
        self.contextWeights = []    
        weightsFilled = False
        
        #data to cluster
        for a in self.socialCtx.agentsPresent:
            aux = []
            for c in self.socialCtx.theme:
                aux.append(a.personalCharacteristics[c]/self.maxCharacteristic)
                if not weightsFilled:
                    self.contextWeights.append(self.socialCtx.theme[c])
            weightsFilled = True
            self.dataAgents.append(aux)
        
        lenAgents = len(self.dataAgents)
                
        #iterative k means
        while kMeansCycle:            
            km = KMeans(n_clusters=k)
            km = km.fit(self.dataAgents)
            self.clustersLabels = km.labels_
            self.clustersCentroids = km.cluster_centers_
            
            centroidsList = []
            #centroids list
            for i in range(0, lenAgents):
                centroidsList.append(self.clustersCentroids[self.clustersLabels[i]])
                      
            #distance of agents to centroid
            distance = self.distanceToCentroids(self.dataAgents, centroidsList)
      
            if any(dist > self.thresholdCluster for dist in distance):
                k+=1
            else:
                kMeansCycle = False
                
        self.printClustering(k)
        
    def printClustering(self, k):
        #print("---- CLUSTERING ----")
        #plot - scale axis
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.yaxis.set_major_locator(plt.MultipleLocator(10))
        ax.xaxis.set_major_locator(plt.MultipleLocator(10))
        ax.grid()
        
        lenColorsClusters = len(self.colors)
        lenSymbolsAgents = len(self.plotSymbols)
        
        #print the results
        #print(str(k) + " clusters")
        for i in range(0, k):
            #print("Cluster " + str(i+1))
            #print("Centroid " + str(self.clustersCentroids[i]))
            #print("Agents")
            for j in range(0, len(self.dataAgents)):
                if(self.clustersLabels[j] == i):
                    name = self.socialCtx.agentsPresent[j].name
                    #print(name)
                    #plotting the agents - 2 variables
                    if len(self.dataAgents[j]) == 2:
                        x = self.dataAgents[j][0]*self.maxCharacteristic
                        y = self.dataAgents[j][1]*self.maxCharacteristic
                        symbol = self.plotSymbols[j%lenSymbolsAgents]
                        color = self.colors[i%lenColorsClusters]
                        plt.scatter(x, y, c=color, marker=symbol, label=name)
                        #plt.annotate(name, (x,y))

        #plotting the centroids - 2 variables
        if len(self.dataAgents[0]) == 2:
            for c in range(0, len(self.clustersCentroids)):
                x = self.clustersCentroids[c][0]*self.maxCharacteristic
                y = self.clustersCentroids[c][1]*self.maxCharacteristic
                plt.scatter(x, y, c='black')
                plt.annotate("Cluster " + str(c+1), (x, y))
            plt.title('Clusters of Agents')
            themeKeys = list(self.socialCtx.theme)  
            plt.xlabel(themeKeys[0])
            plt.ylabel(themeKeys[1])
            plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fancybox=True, shadow=True)           
            plt.savefig(self.outputF + '/clustersAgents.png', bbox_inches='tight')
            plt.clf()
    
    '''Normative Fit'''
    def normativeFit(self, a):
        #print("---- NORMATIVE FIT ----")
        #verify if social group characteristics matches with context
        matchingSocialGroups = []
        for sg in a.knowledgeBase:
            socialGroupCtx = True
            centroidSG = []
            for t in self.socialCtx.theme:
                if t not in sg.characteristics:
                    socialGroupCtx = False
                else:
                    centroidSG.append(sg.characteristics[t]/self.maxCharacteristic)
            if socialGroupCtx:
                matchingSocialGroups.append([sg, centroidSG])
        
        a.presentGroups = []
        #distance centroids clusters to centroids social groups matching context KB
        for i, c in enumerate(self.clustersCentroids):
            presentAgentsSG = []
            for j, l in enumerate(self.clustersLabels):
                if l == i:
                    presentAgentsSG.append(j)
            foundKnownSG = False
            for m in matchingSocialGroups:
                #distance between cluster centroid and kb sg centroid
                distanceClusterSG = self.distanceWeights(m[1], c)
                #compare to threshold
                if distanceClusterSG < self.thresholdNormative:
                    #print("Found similar social group in knowledge base " + m[0].name)
                    #print("Centroid " + str(m[1]))
                    foundKnownSG = True
                    #save in agent group
                    a.presentGroups.append(m + [presentAgentsSG])                       
            if not foundKnownSG:
                name = "Group " + (str(len(a.knowledgeBase) + 1))
                newSGcharacteristics = {}
                for idx, t in enumerate(self.socialCtx.theme):
                    newSGcharacteristics[t] = c[idx]*self.maxCharacteristic
                newSG = socialGroup.SocialGroup(name, newSGcharacteristics)
                a.knowledgeBase.append(newSG)
                #print("Unknown social group added to knowledge base " + name)
                #print("Centroid " + str(c))                
                #save in agent group
                a.presentGroups.append([newSG, c, presentAgentsSG])
        
    '''Comparative Fit'''
    def dispersion(self, sg): 
        dispersion = []
        for i in sg:
            dispersionIndividual = []
            #only calculate dispersion with agents that belong to the group
            agentsGroup = i[2]
            for j in agentsGroup:
                dispersionIndividual.append(self.distanceWeights(self.dataAgents[j], i[1]))
            dispersion.append(np.mean(dispersionIndividual, axis=0))
        return np.mean(dispersion, axis=0)/self.thresholdNormative #MENTION: Don't really understand where this division comes from...it appears in old articles but in current one it is not explained
    
    def distance(self, centroidInGroup, centroidOutGroup):
        meanCentroidIn = np.mean(centroidInGroup, axis=0)
        meanCentroidOut = np.mean(centroidOutGroup, axis=0)
        return self.distanceWeights(meanCentroidIn, meanCentroidOut)
         
    def comparativeFit(self, a):
        #print("---- COMPARATIVE FIT ----")
        #there is more than one social group
        if len(a.presentGroups) > 1:
            for idx, g in enumerate(a.presentGroups):
                inGroup = [g]
                outGroup = [x for i,x in enumerate(a.presentGroups) if i!=idx] 
                
                #print("Social Group " + g[0].name)
                
                #compute distance between in group and outgroup(s)
                distanceBetweenGroups = self.distance([item[1] for item in inGroup], [item[1] for item in outGroup]) #in case theres more than one outgroup (or ingroup)
                #print("Distance between in group and out group(s) " + str(distanceBetweenGroups))
                
                #compute dispersion in group and out group(s)
                dispersionInGroup = self.dispersion(inGroup)
                #print("Dispersion In Group " + str(dispersionInGroup))
                dispersionOutGroup = self.dispersion(outGroup)
                #print("Dispersion Out Group(s) " + str(dispersionOutGroup))
                
                #compute fitness - same for every sg in this context
                fitness = self.comparativeFitAlpha * distanceBetweenGroups + ((1 - self.comparativeFitAlpha) * (self.comparativeFitBeta * (1-dispersionInGroup) + (1 - self.comparativeFitBeta) * dispersionOutGroup)) #MENTION: this formula makes more sense! Higher in group dispersion -> lower fitness and Higher out group dispersion --> higher fitness      
                #print("Fitness of " + g[0].name + " " + str(fitness))
                #update fitness for each sg
                g[0].fitness = fitness
        #only one social group - fitness is 0 - personal identity
        else:
            for g in a.presentGroups:
                g[0].fitness = 0
                
    '''Accessibility'''
    def accessibility(self, a, idxAgent):
        for sg in a.presentGroups:
            #if accessibility of SG was not initialized           
            if sg[0].accessibility is None:
                sg[0].accessibility = 1 - self.distanceWeights(self.dataAgents[idxAgent], sg[1])
            else:
                return
        #self.normalizeAccessibility(a)
        
    def updateAccessibility(self, a, emotionalValenceDictator = 0):
        sid = a.salientSocialIdentity
        if emotionalValenceDictator == 0:
            emotionalValence = sid.emotionalValence
        else:
            emotionalValence = emotionalValenceDictator
       
        if sid is not None:
            #print("---- UPDATE ACCESSIBILITY ----")
            #print("Salient Social Identity " + sid.name)
            previousAccessibility = sid.accessibility
            #print("Previous Accessibility " + str(previousAccessibility))           
            newAccessibility = np.clip(previousAccessibility + sid.salience * emotionalValence, 0, 1)
            sid.accessibility = newAccessibility
            #print("New Accessibility " + str(newAccessibility))
        
        #self.normalizeAccessibility(a)

    def normalizeAccessibility(self, a):
        #Find norm of social group accessibility
        normAccessibility = 0
        for sg in a.presentGroups:
            normAccessibility += sg[0].accessibility**2
        normAccessibility = math.sqrt(normAccessibility)
        #Normalize accessibility
        for sg in a.presentGroups:
            sg[0].accessibility /= normAccessibility
                              
    '''Salience'''
    def salienceSocialGroup(self, a):
        #print("---- SALIENCE ----")
        for sg in a.presentGroups:
            #print("Social Group " + sg[0].name)
            fitness = sg[0].fitness
            accessibility = sg[0].accessibility
            #print("Fitness " + str(fitness))
            #print("Accessibility " + str(accessibility))
            #compute salience 
            salience = fitness * accessibility
            #print("Salience " + str(salience))
            #update salience for each sg
            sg[0].salience = salience
            
    def salientActiveIdentity(self, a, idxAgent):
        #print("---- SALIENT IDENTITY ----")
        salienceVal = 0
        identity = None
        identityName = "personal"
        #more than one social group - social identity
        if len(a.presentGroups) > 1:
            #find social identity with highest salience
            for sg in a.presentGroups:
                auxVal = sg[0].salience
                if  auxVal > salienceVal:
                    salienceVal = auxVal
                    identity = sg
            identityName = identity[0].name
            if salienceVal >= self.thresholdMinimalSalience: #only updating salient social identity again if its salience is above or equal to threshold        
                a.salientSocialIdentity = identity[0]
        else:
            a.salientSocialIdentity = None
            
        #print("Salient Identity " + identityName) 
        
        #active identity characteristics - linear interpolation
        #print("---- ACTIVE IDENTITY ----")
        for i, t in enumerate(self.socialCtx.theme):
            personalVal = self.dataAgents[idxAgent][i]
            if identity is not None:
                identityVal = identity[1][i]
            else:
                identityVal = personalVal
            interRes = personalVal + (identityVal-personalVal) * salienceVal; 
    
    '''Plot Functions'''
    def listGraphics(self, a):
        for sg in a.knowledgeBase:
            salience = sg.salience if sg.salience is not None else 0
            accessibility = sg.accessibility if sg.accessibility is not None else 0
            sg.salienceSteps.append(salience)
            sg.accessibilitySteps.append(accessibility)
   
    def showSalienceAccessibilityPlots(self, salience=True):
        numGroups = len(self.clustersCentroids)
        lenColors = len(self.colorsAgents)
        for j in range(0, numGroups):
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
            ax.yaxis.set_major_locator(plt.MultipleLocator(0.1))
            ax.xaxis.set_major_locator(plt.MultipleLocator(5))
            ax.grid()     
            for i, a in enumerate(self.socialCtx.agentsPresent):
                #plot - scale axis
                sg = a.knowledgeBase[j]
                colorPlot = self.colorsAgents[i%lenColors]
                if salience:
                    plt.plot(sg.salienceSims, color=colorPlot, label=a.name)
                else:
                    plt.plot(sg.accessibilitySims,'--', color=colorPlot, label=a.name)
            if salience:
                plt.title('Salience of Group ' + str(j+1))
            else:
                plt.title('Accessibility of Group ' + str(j+1))
            plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fancybox=True, shadow=True)
            plt.xlim(0, self.numSteps) 
            plt.ylim(0, 1)
            plt.xlabel("Steps")
            if salience:
                plt.ylabel("Salience")
                plt.savefig(self.outputF + '/salienceGroup' + str(j+1) + '.png', bbox_inches='tight')
            else:
                plt.ylabel("Accessibility")                
                plt.savefig(self.outputF + '/accessibilityGroup' + str(j+1) + '.png', bbox_inches='tight')
            plt.clf()
    
    def showAverageWealthGroupsPlots(self):
        lenColorsClusters = len(self.colors)
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.yaxis.set_major_locator(plt.MultipleLocator(2000))
        ax.xaxis.set_major_locator(plt.MultipleLocator(5))
        ax.grid()
        for i, sg in enumerate(self.dictator.groupsAverageWealthSims):
            #randColor = (random.random(), random.random(), random.random())
            colorPlot = self.colors[i%lenColorsClusters]
            plt.plot(self.dictator.groupsAverageWealthSims[sg], color=colorPlot, label='Avg Wealth (' + sg + ')')
        plt.title('Average Wealth Groups')
        plt.legend(fancybox=True, shadow=True)
        plt.xlim(0, self.numSteps)
        plt.ylim(0, 12000)
        plt.xlabel("Steps")
        plt.ylabel("Money")
        plt.savefig(self.outputF + '/averageWealth.png')
        plt.clf()
        
    '''Dictator Game'''
    def playDictatorGame(self, giver, idxGiver):
        inGroup = False
        idxReceiver = np.random.choice([i for i in range(0,len(self.socialCtx.agentsPresent)) if i != idxGiver])
        for g in giver.presentGroups:
            agentsPresentGroup = g[2]
            if idxReceiver in agentsPresentGroup and idxGiver in agentsPresentGroup:
                inGroup = True
                self.ingroupNr+=1
            elif idxGiver in agentsPresentGroup:
                self.outgroupNr+=1
            
        return self.dictator.offer(giver, self.socialCtx.agentsPresent[idxReceiver], giver.salientSocialIdentity.salience, inGroup, self.thresholdMinimalSalience)

    #Average Wealth
    def computeAverageWealth(self):
        #one agent is enough because they know about all groups: should i change this?
        agent = self.socialCtx.agentsPresent[0]
        groups = agent.presentGroups
        for g in groups:
            agentsObj = []
            groupName = g[0].name
            agents = g[2]
            for a in agents:
                agentsObj.append(self.socialCtx.agentsPresent[a])
            self.dictator.updateAverageWealth(groupName, agentsObj)
    
    '''Clear Simulation'''
    def clearSimulation(self):
        agentsSim = self.socialCtx.agentsPresent
        for a in agentsSim:
            a.clear(self.numRuns)
        self.dictator.clear(self.numRuns)               