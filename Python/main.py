from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QFileDialog, QPushButton, QLabel, QGridLayout, QSpinBox, QComboBox
from PyQt5.QtGui import QPixmap 
import sys
import os
import fileManager
import simulation

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Dynamic Identity Model for Agents'       
        #Initial Configurations
        self.numSteps = 100
        self.numRuns = 30        
        #Valid File Paths Checks
        self.loadedOutput = False
        #File Manager - includes all the information obtained from the simulation input files
        self.fileManager = None
        #Initialize User Interface
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        #Main Grid
        parentLayout = QGridLayout()
        #Main Grid Label
        self.labelInput = QLabel("Configurations of Simulation", self)
        parentLayout.addWidget(self.labelInput, 0, 0, 1, 6)
        self.labelInput.setStyleSheet("font-weight: bold")
        #Agents File
        self.labelAgents = QLabel("Agents:", self)
        self.textAgentsFile = QLineEdit(self)
        self.uploadAgents = QPushButton('...', self)
        parentLayout.addWidget(self.labelAgents, 1, 0, 1, 1)                             
        parentLayout.addWidget(self.textAgentsFile, 1, 1, 1, 4)
        parentLayout.addWidget(self.uploadAgents, 1, 5, 1, 1)
        self.textAgentsFile.setFixedWidth(620)
        self.labelAgents.setFixedWidth(50)
        self.uploadAgents.clicked.connect(lambda: self.openFile('Agents File', self.textAgentsFile))
        #Context File
        self.labelContext = QLabel("Context:", self)
        self.textContextFile = QLineEdit(self)
        self.uploadContext = QPushButton('...', self)        
        parentLayout.addWidget(self.labelContext, 2, 0, 1, 1)
        parentLayout.addWidget(self.textContextFile, 2, 1, 1, 4)                                          
        parentLayout.addWidget(self.uploadContext, 2, 5, 1, 1)
        self.textContextFile.setFixedWidth(620)
        self.labelContext.setFixedWidth(50)
        self.uploadContext.clicked.connect(lambda: self.openFile('Context File', self.textContextFile))
        #Number of Steps
        self.labelSteps = QLabel("Steps:", self)
        self.spinBox = QSpinBox(self)
        parentLayout.addWidget(self.labelSteps, 4, 0, 1, 1)                             
        parentLayout.addWidget(self.spinBox, 4, 1, 1, 1)
        self.spinBox.setRange(0, 100)
        self.spinBox.setValue(self.numSteps)
        self.labelSteps.setFixedWidth(35)
        #Number of Runs            
        self.labelSimulations = QLabel("Runs:", self)
        self.spinBoxRuns = QSpinBox(self)
        parentLayout.addWidget(self.labelSimulations, 4, 2, 1, 1)                             
        parentLayout.addWidget(self.spinBoxRuns, 4, 3, 1, 1)
        self.spinBoxRuns.setRange(0, 100)
        self.spinBoxRuns.setValue(self.numRuns)
        self.labelSimulations.setFixedWidth(35)
        #Output Folder
        self.labelOutput = QLabel("Output:", self)
        self.textOutputFolder = QLineEdit(self)
        self.output = QPushButton('...', self)
        parentLayout.addWidget(self.labelOutput, 3, 0, 1, 1)
        parentLayout.addWidget(self.textOutputFolder, 3, 1, 1, 4)                             
        parentLayout.addWidget(self.output, 3, 5, 1, 1)
        self.labelOutput.setFixedWidth(50)
        self.output.clicked.connect(self.openOutputFolder)
        #Run Simulation Button
        self.runButton = QPushButton('Run', self)
        parentLayout.addWidget(self.runButton, 4, 4, 1, 2)
        self.runButton.clicked.connect(self.runSimulation)
        #Output Files
        self.labelFiles = QLabel("Output Files", self)
        self.imagesComboBox = QComboBox(self)
        self.labelImages = QLabel(self)
        parentLayout.addWidget(self.labelFiles, 6, 0, 1, 6)
        parentLayout.addWidget(self.imagesComboBox, 7, 0, 1, 2)
        parentLayout.addWidget(self.labelImages, 8, 0, 1, 6)
        self.imagesComboBox.currentIndexChanged.connect(self.selectOutputFiles)        
        #Main Grid Show
        self.setLayout(parentLayout)
        self.setFixedWidth(800)
        self.show()
    
    def openFile(self, name, inputFile):
        fileName = QFileDialog.getOpenFileName(self, name, "", "JSON (*.json)")
        inputFile.setText(fileName[0])
        
    def openOutputFolder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Output Folder')
        self.textOutputFolder.setText(folder)
        
    def listOutputFiles(self):
        outputFiles = os.listdir(self.textOutputFolder.text())
        self.imagesComboBox.clear()
        self.imagesComboBox.addItems(outputFiles)       
        self.selectOutputFiles()
       
    def selectOutputFiles(self):
        if self.loadedOutput:
            image = self.textOutputFolder.text() + "/" + self.imagesComboBox.currentText()
            imagePixmap = QPixmap(image)
            self.labelImages.setPixmap(imagePixmap)
            self.labelImages.resize(imagePixmap.width(), imagePixmap.height())
    
    def runSimulation(self):
        self.numRuns = self.spinBoxRuns.value()
        self.numSteps = self.spinBox.value()
        if self.textOutputFolder.text():
            self.loadedOutput = True
        self.fileManager = fileManager.FileManager(self.textAgentsFile.text(), self.textContextFile.text())
        self.identitySalienceMechanism()
        
    def identitySalienceMechanism(self):
        if self.fileManager.loadedInput is True and self.loadedOutput is True:
            simulation.Simulation(self.numSteps, self.numRuns, self.fileManager.agents, self.fileManager.socialCtxObj, self.textOutputFolder.text())    
            self.listOutputFiles()
                           
#Start Application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
