import numpy as np
from datetime import datetime as dt

class ImpedanceData:
    def __init__(self, dataFile):
        self.currentID = 'A'
        self.parseHeader(dataFile)
        self.findDataLines(dataFile)
        self.parseData(dataFile)

    def parseHeader(self, dataFile):
        with open(dataFile, 'r') as dataFile:
            lines = dataFile.readlines()
            for line in lines:
                line = line.replace(":", " ")
                line = line.replace("\n", "")
                line = line.replace("\t", "")
                lineData = line.split(" ")
                #print(lineData)
                if lineData[0] == 'ID':
                    self.currentID = lineData[-1]
                if lineData[0] == 'MODE':
                    if self.currentID == 'A':
                        self.mode = lineData[-1]
                elif lineData[0] == 'START':
                    self.startVoltage = float(lineData[-1])
                elif lineData[0] == 'STOP':
                    self.stopVoltage = float(lineData[-1])
                elif lineData[0] == 'STEP':
                    self.stepVoltage = float(lineData[-1])
                elif lineData[0] == 'DATE':
                    self.recordedDate = dt.strptime(lineData[-1], "%m/%d/%Y")
                elif lineData[0] == 'TIME':
                    timeData = lineData[-3] + " " + lineData[-2] + " " + lineData[-1]
                    self.recordedTime = dt.strptime(timeData, "%H %M %S")
                elif lineData[0] == 'PNTS':
                    self.numberPoints = int(lineData[-1])

    def findDataLines(self, dataFile):
        with open(dataFile, 'r') as dataFile:
            lines = dataFile.readlines()
            currentLine = 0
            dataLines = []
            for line in lines:
                lineData = line.split(" ")
                if lineData[0] == "DATA:": # begin reading data
                    self.dataStartLine = currentLine + 3
                    break
                currentLine += 1

    def parseData(self, dataFile):
        with open(dataFile, 'r') as dataFile:
            lines = dataFile.readlines()
            headerLine = lines[self.dataStartLine-1]
            headerLine = headerLine.replace("\n", "")
            self.dataTypes = headerLine.split("\t")
            self.dataTypes = [x for x in self.dataTypes if x != ""]
            self.data = {}
            for dataType in self.dataTypes:
                self.data[dataType] = np.array([])

            lines = lines[self.dataStartLine:-4]
            if len(lines) != self.numberPoints:
                raise ValueError("number lines not equal to data lines. Issue with parsing.")

            for line in lines:
                line = line.replace("\n", "")
                lineData = line.split("\t")
                for i in range(len(self.dataTypes)):
                    self.data[self.dataTypes[i]] = np.append(self.data[self.dataTypes[i]], float(lineData[i]))

