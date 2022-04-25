from sklearn.cluster import KMeans
import numpy as np
import math
import matplotlib.pyplot as plt
import socialGroup

class Simulation:
    def __init__(self, numSteps, numRuns, agents, socialCtx, outputF):
        self.numSteps = numSteps
        self.numRuns = numRuns
        
        self.agents = agents
        self.socialCtx = socialCtx
        self.thresholdCluster = 0.3
        self.thresholdNormative = 0.2
        self.thresholdMinimalSalience = 0.2
        self.outputF = outputF
        #For Plots
        plt.rcParams['font.size'] = 12
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = ['Bahnschrift']
        plt.rcParams["font.weight"] = "normal"
        self.plotSymbols = ["o", "v", "H", "*", "X", "d", "P", "s", "D", "p"]
        self.colors = ["orange", "deepskyblue"]
        self.colorsAgents = ["yellow", "aqua", "green", "pink", "brown", "darkorange", "purple", "gray", "olive", "magenta"]
        self.plotLine = ['x','+']
             
        self.contextWeights = []
        for c in self.socialCtx.theme:
            self.contextWeights.append(self.socialCtx.theme[c])
        
        self.cycle()
    
    def plotStyle(self, plot):
        plot.grid(color='gray', linewidth=1.0)
        plot.spines['top'].set_visible(False)
        plot.spines['right'].set_visible(False)
        plot.spines['bottom'].set_visible(False)
        plot.spines['left'].set_visible(False)
    
    def distanceToCentroids(self, first, second):
        distance = []
        lenFirst = len(first)
        for i in range(0, lenFirst):          
            auxDist = self.distanceWeights(first[i], second[i])           
            distance.append(auxDist)
        return distance
    
    def distanceWeights(self, first, second):
        lenWeights = len(self.contextWeights)
        #when theme is empty
        if lenWeights == 0:
            lenWeights = len(first)  
        lDist = abs(np.array(first)-np.array(second))
        auxDist = 0
        #weighted euclidean distance
        for i in range(0, lenWeights):
            w = 0.5 #when theme is empty
            if len(self.contextWeights) > 0:
                w = self.contextWeights[i]
            auxDist += w * (lDist[i])**2 
        dist = math.sqrt(auxDist)
        return dist
       
    '''Agents Cycle'''               
    def cycle(self):
        self.clustering()
        #Run simulation
        for r in range(0, self.numRuns):
            for s in range(0, self.numSteps):
                #For each agent
                for idxAgent, a in enumerate(self.socialCtx.agentsPresent):
                    self.normativeFit(a, idxAgent)
                    self.comparativeFit(a)
                    self.salienceSocialGroup(a)
                    self.salientActiveIdentity(a)
                    self.listGraphics(a, s, r)
                    #Decision Making functions here (decide on proper action)
                    #Perception Module functions here (evaluate outcome)
                    self.updateAccessibility(a)
            print("Simulation " + str(r))        
            self.clearSimulation()
        
        self.showSalienceAccessibilityPlots()
    
    '''Clustering'''    
    def clustering(self):
        kMeansCycle = True
        k = 1
        
        self.dataAgents = []   
        
        #data to cluster
        for a in self.socialCtx.agentsPresent:
            aux = []
            theme = self.socialCtx.theme
            #when theme is empty
            if len(theme) == 0:
                theme = a.personalCharacteristics
            for c in theme:
                aux.append(a.personalCharacteristics[c])
            self.dataAgents.append(aux)
        
        lenAgents = len(self.dataAgents)
                
        #iterative k means
        while kMeansCycle:            
            km = KMeans(n_clusters=k, random_state=0)
            km = km.fit(self.dataAgents)
            self.clustersLabels = km.labels_
            self.clustersCentroids = km.cluster_centers_
            
            centroidsList = []
            #centroids list
            for i in range(0, lenAgents):
                centroidsList.append(self.clustersCentroids[self.clustersLabels[i]])
                      
            if len(self.socialCtx.theme) > 0:
                #distance of agents to centroid
                distance = self.distanceToCentroids(self.dataAgents, centroidsList)

                if any(dist > self.thresholdCluster for dist in distance):
                    k+=1
                else:
                    kMeansCycle = False
            else: #when theme is empty
                kMeansCycle = False
                
        self.printClustering(k)
        
    def printClustering(self, k):
        #plot - scale axis
        fig = plt.figure(figsize = (7,5))
        ax = fig.add_subplot(1, 1, 1)
        ax.yaxis.set_major_locator(plt.MultipleLocator(0.1))
        ax.xaxis.set_major_locator(plt.MultipleLocator(0.1))
        self.plotStyle(ax)
        
        lenColorsClusters = len(self.colors)
        lenSymbolsAgents = len(self.plotSymbols)
        
        #print the results
        for i in range(0, k):
            x = []
            y = []
            symbol = self.plotSymbols[i%lenSymbolsAgents]          
            for j in range(0, len(self.dataAgents)):
                if(self.clustersLabels[j] == i):
                    #plotting the agents
                    x.append(self.dataAgents[j][0])
                    y.append(self.dataAgents[j][1])
            color = self.colors[i%lenColorsClusters]
            plt.scatter(x, y, c=color, marker=symbol, s = 50, label="Agents in Social Cluster " + str(i+1))

        #plotting the centroids
        for c in range(0, len(self.clustersCentroids)):
            x = self.clustersCentroids[c][0]
            y = self.clustersCentroids[c][1]
            plt.scatter(x, y, marker='X', s = 50, c='black')
            plt.annotate("Center SC " + str(c+1), (x, y+0.01), ha='center')
            plt.annotate("(" + str(np.around(x,2)) + ", " + str(np.around(y,2)) +")", (x, y-0.05), ha='center')
        
        plt.title('Social Clusters in the Environment:\nResult from the interpretation of the social context')
        if len(self.socialCtx.theme) == 0:
            self.socialCtx.theme = self.socialCtx.agentsPresent[0].personalCharacteristics
        themeKeys = list(self.socialCtx.theme)  
        plt.xlabel(themeKeys[0])
        plt.ylabel(themeKeys[1])
        plt.legend(fancybox=True)        
        plt.savefig(self.outputF + '/clustersAgents.png', bbox_inches='tight')
        plt.clf()
    
    '''Normative Fit'''
        
    def dispersion(self, sg, agentsGroup): 
        diff = []
        #only calculate dispersion with agents that belong to the group
        for j in agentsGroup:
            diff.append(self.distanceWeights(self.dataAgents[j], sg))
        return np.mean(diff, axis=0)/self.thresholdNormative

    def normativeFit(self, a, idxA):
        #verify if the characteristics of the normative social groups match with the context's theme
        matchSGs = []
        for sg in a.normativeGroups:
            match = True
            centroidSG = []
            theme = self.socialCtx.theme
            #when theme is empty
            if len(theme) == 0:
                theme = a.personalCharacteristics
            for t in theme:
                if t not in sg.characteristics:
                    match = False
                    sg.type = 0
                else:
                    centroidSG.append(sg.characteristics[t])
            if match:
                matchSGs.append([sg, centroidSG])
        
        #distance centroids clusters to centroids social groups matching context KB
        for i, c in enumerate(self.clustersCentroids):
            agentsGroup = []
            for j, l in enumerate(self.clustersLabels):
                if l == i:
                    agentsGroup.append(j)
                    
            #get dispersion of cluster
            dispersionGroup = self.dispersion(c, agentsGroup)
            
            #initial accessibility
            initAcc = 1 - self.distanceWeights(self.dataAgents[idxA], c)
            
            knownSG = False
            for m in matchSGs:
                #distance between cluster centroid and kb sg centroid
                distClusterKB = self.distanceWeights(m[1], c)
                #compare to threshold
                if distClusterKB < self.thresholdNormative:
                    knownSG = True
                    m[0].dispersion = dispersionGroup
                    m[0].type = 1
                    if m[0].accessibility is None:
                        m[0].accessibility = initAcc
    
            #new normative group (will only be considered as normative group in the next time step)
            if not knownSG: 
                name = "Group " + (str(len(a.normativeGroups) + 1))
                newSGchar = {}
                theme = self.socialCtx.theme
                if len(theme) == 0:
                    theme = a.personalCharacteristics
                for idx, t in enumerate(theme):
                    newSGchar[t] = c[idx]
                newSG = socialGroup.SocialGroup(name, newSGchar, initAcc)
                newSG.dispersion = dispersionGroup
                newSG.type = 1
                a.normativeGroups.append(newSG)
        
    '''Comparative Fit'''
    
    #we are assuming that there can be more than one out-group
    def dispersionCF(self, sg): 
        dispersion = []
        for i in sg:
            dispersion.append(i.dispersion)
        return np.mean(dispersion, axis=0)
    
    def distanceCF(self, inGroup, outGroup):
        centroidIn = []
        for sg in inGroup:
            ct = []
            for c in sg.characteristics:
                ct.append(sg.characteristics[c])
            centroidIn.append(ct)
        centroidOut = []
        for sg in outGroup:
            ct = []
            for c in sg.characteristics:
                ct.append(sg.characteristics[c])
            centroidOut.append(ct)
            
        meanCentroidIn = np.mean(centroidIn, axis=0)
        meanCentroidOut = np.mean(centroidOut, axis=0)
        return self.distanceWeights(meanCentroidIn, meanCentroidOut)
         
    def comparativeFit(self, a):
        presentGroups = []
        #Get present groups only
        for sg in a.normativeGroups:
            if sg.type == 1:
                presentGroups.append(sg)
                
        #there is more than one social group
        if (len(presentGroups)) > 1:
            for idx, g in enumerate(presentGroups):
                inGroup = [g]
                outGroup = [x for i,x in enumerate(presentGroups) if i!=idx]    
                #compute distance between in group and outgroup(s)
                distanceBetweenGroups = self.distanceCF(inGroup, outGroup) #in case theres more than one outgroup (or ingroup)
                #compute dispersion in group and out group(s)
                dispersionInGroup = self.dispersionCF(inGroup)
                dispersionOutGroup = self.dispersionCF(outGroup)
                #compute fitness
                fitness = distanceBetweenGroups/2 + ((1 - dispersionInGroup) + dispersionOutGroup)/4
                #update fitness for each sg
                g.fitness = fitness
        #only one social group - fitness is 0 - personal identity
        else:
            for g in presentGroups:
                g.fitness = 0
                
    '''Salience'''

    def normalizeAccessibility(self, a):
        sumAcc = 0
        for sg in a.normativeGroups:
            if sg.accessibility is not None:
                sumAcc += sg.accessibility**2
        normAcc = np.sqrt(sumAcc)
        for sg in a.normativeGroups:
            if sg.accessibility is not None:
                sg.accessibility /= normAcc
                              
    '''Salience'''
    def salienceSocialGroup(self, a):
        for sg in a.normativeGroups:
            if sg.type == 1:
                fitness = sg.fitness
                accessibility = sg.accessibility
                #compute salience 
                salience = fitness * accessibility
                #update salience for each sg
                sg.salience = salience
            
    def salientActiveIdentity(self, a):
        salienceVal = 0
        identity = None
        identityName = "personal"
        presentGroups = []
        #Get present groups only
        for sg in a.normativeGroups:
            if sg.type == 1:
                presentGroups.append(sg)
        
        #more than one social group - social identity
        if len(presentGroups) > 1:
            #find social identity with highest salience
            for sg in presentGroups:
                auxVal = sg.salience
                if  auxVal > salienceVal:
                    salienceVal = auxVal
                    identity = sg
            if salienceVal > self.thresholdMinimalSalience: #only updating salient social identity again if its salience is above or equal to threshold        
                a.salientIdentity = identity
            else:
                a.salientIdentity = None
        else:
            a.salientIdentity = None    
        self.normalizeAccessibility(a)
    
    '''Accessibility Update'''
        
    def updateAccessibility(self, a, constant = 0.01):
        sid = a.salientIdentity    
        if sid is not None:
            prevAccessibility = sid.accessibility
            newAccessibility = prevAccessibility + sid.salience * constant
            sid.accessibility = newAccessibility
        self.normalizeAccessibility(a)
    
    '''Plot Functions'''
    def listGraphics(self, a, s, r):
        for sg in a.normativeGroups:
            if sg.type == 1:
                salience = sg.salience if sg.salience is not None else 0
                accessibility = sg.accessibility if sg.accessibility is not None else 0
                if sg.salienceSteps == []:
                    sg.salienceSteps = [0] * self.numSteps
                if sg.accessibilitySteps == []:
                    sg.accessibilitySteps = [0] * self.numSteps
                sg.salienceSteps[s] += salience
                sg.accessibilitySteps[s] += accessibility
                if (s == self.numSteps - 1):
                    if len(sg.accessibilityFinalStep) == 0:
                        sg.accessibilityFinalStep = [0] * self.numRuns
                    sg.accessibilityFinalStep[r] = accessibility
                    if len(sg.salienceFinalStep) == 0:
                        sg.salienceFinalStep = [0] * self.numRuns
                    sg.salienceFinalStep[r] = salience
   
    def showSalienceAccessibilityPlots(self):
        numGroups = len(self.clustersCentroids)
        lenColors = len(self.colors)
        lenLine = len(self.plotLine)
        fig = plt.figure(figsize = (7,5))
        ax = fig.add_subplot(1, 1, 1)
        ax.yaxis.set_major_locator(plt.MultipleLocator(0.1))
        ax.xaxis.set_major_locator(plt.MultipleLocator(5))
        self.plotStyle(ax)
        sP = []
        aP = []
        for sg in range(0, numGroups):           
            agentsGroup = []
            currCluster = 0
            for a, c in enumerate(self.clustersLabels):
                if c == sg:
                    currCluster = c
                    agentsGroup.append(self.socialCtx.agentsPresent[a])
            lenAgents = len(agentsGroup)
            salienceSimsAgents = [0]*self.numSteps
            accessibilitySimsAgents = [0]*self.numSteps
            salienceFinalStepAgents = [0]*self.numRuns
            accessibilityFinalStepAgents = [0]*self.numRuns
            for agent in agentsGroup:                
                #plot - scale axis
                sgKB = agent.normativeGroups[currCluster]
                salienceSimsAgents += np.array([x / self.numRuns for x in sgKB.salienceSteps])
                accessibilitySimsAgents += np.array([x / self.numRuns for x in sgKB.accessibilitySteps])
                salienceFinalStepAgents += np.array([x for x in sgKB.salienceFinalStep])
                accessibilityFinalStepAgents += np.array([x for x in sgKB.accessibilityFinalStep])
            colorPlot = self.colors[sg%lenColors]
            linePlot = self.plotLine[sg%lenLine]
            salienceSims = np.array(salienceSimsAgents/lenAgents)
            plt.plot(salienceSims, color=colorPlot, linewidth=2.5, marker=linePlot, markevery=3, label='Avg Salience of SSI for Agents in Cluster ' + str(sg+1))
            accessibilitySims = np.array(accessibilitySimsAgents/lenAgents)             
            plt.plot(accessibilitySims,'--', linewidth=2.5, color=colorPlot, marker=linePlot, markevery=3, label='Avg Accessibility of SSI for Agents in Cluster ' + str(sg+1))
            sP.append(salienceSims)
            aP.append(accessibilitySims)
        plt.title('Average Salience and Accessibility of \nSalient Social Identity for Agents in each Cluster')
        if len(sP) == 2:
            plt.fill_between(np.arange(self.numSteps), sP[0], sP[1], color="grey", alpha=0.3)
        if len(aP) == 2:
            plt.fill_between(np.arange(self.numSteps), aP[0], aP[1], color="grey", alpha=0.3)
        plt.legend(fancybox=True)
        plt.xlim(0, self.numSteps-1) 
        plt.ylim(0, 1)
        plt.xlabel("Number of Steps")
        plt.ylabel("Salience and Accessibility")                   
        plt.savefig(self.outputF + '/salienceAccessibility.png', bbox_inches='tight')
        plt.clf()       
    
    '''Clear Simulation'''
    def clearSimulation(self):
        for a in self.socialCtx.agentsPresent:
            for sg in a.normativeGroups:
                if sg.type == 1:
                    sg.fitness = None
                    sg.accessibility = None
                    sg.salience = None
                    sg.type = 0 