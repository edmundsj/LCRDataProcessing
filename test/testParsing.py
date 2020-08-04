from UnitTesting.shorthand import *
from DataProcessing.LCR.source.parser import ImpedanceData
import unittest

class TestParser(unittest.TestCase):
    def setUp(self):
        self.data = ImpedanceData('data/test_data.dat')

    def testExtractHeader(self):
        desiredMode = "SWEEP"
        actualMode = self.data.mode
        assertStringEqual(actualMode, desiredMode)

        desiredStartVoltage = 10
        actualStartVoltage = self.data.startVoltage
        assertEqual(actualStartVoltage, desiredStartVoltage, "stop voltage")

        desiredStopVoltage = -20
        actualStopVoltage = self.data.stopVoltage
        assertEqual(actualStopVoltage, desiredStopVoltage, "start voltage")

        desiredStepVoltage = -0.25
        actualStepVoltage = self.data.stepVoltage
        assertEqual(actualStepVoltage, desiredStepVoltage, errorMessage="step voltage")

        desiredPoints = 121
        actualPoints = self.data.numberPoints
        assertEqual(actualPoints, desiredPoints, errorMessage="number points")

    def testfindDataLines(self):
        desiredStartLine = 28
        actualStartLine = self.data.dataStartLine
        assertEqual(actualStartLine, desiredStartLine)

    def testParseDataHeader(self):
        # Confirm we got the right data types
        actualDataTypes = self.data.dataTypes
        desiredDataTypes = ['Z', 'THETA', 'BIAS', 'VM', 'IM']
        assertArrayEqual(actualDataTypes, desiredDataTypes)

    def testParseDataLength(self):
        # Confirm we got the right length of data
        desiredDataPoints = 121
        actualDataPointsZ = len(self.data.data['Z'])
        actualDataPointsBIAS = len(self.data.data['BIAS'])
        actualDataPointsTHETA = len(self.data.data['THETA'])
        actualDataPointsVM = len(self.data.data['VM'])
        actualDataPointsIM = len(self.data.data['IM'])
        assertEqual(desiredDataPoints, actualDataPointsZ)
        assertEqual(desiredDataPoints, actualDataPointsBIAS)
        assertEqual(desiredDataPoints, actualDataPointsTHETA)
        assertEqual(desiredDataPoints, actualDataPointsVM)
        assertEqual(desiredDataPoints, actualDataPointsIM)

    def testParseDataData(self):
        desiredZData = 5.57723*1e6
        actualZData = self.data.data['Z'][1]
        assertAlmostEqual(desiredZData, actualZData)

        desiredBIASData = 8.5
        actualBIASData = self.data.data['BIAS'][6]
        assertAlmostEqual(desiredBIASData, actualBIASData)
