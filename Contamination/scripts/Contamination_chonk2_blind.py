import uproot
import matplotlib.dates as dates
import datetime
import os
import sys
import argparse
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import rootreader as rr
import time
import rat
import ROOT
start_time = time.time()


def get_parser():
	parser = argparse.ArgumentParser(description='nutple input, txt file output of all data cleaning cuts and number of passes for each')
	parser.add_argument('input_path', help='nutuple from Aobo')
	parser.add_argument('out', help='bifurcation output txt')
	parser.add_argument('evID', help='stupid debugging flag')
	
	return parser

def get_args(parser):
	args = parser.parse_args()
	return args

args = get_args(get_parser())



if __name__ == '__main__':
	
	E_LOW = 5.85 #mev
	E_HIGH = 9.0 #mev
	POSR_CUT = 5300 #mm
	DC_path  = int(275977418596578)
	Trig_path = int(5216)
	
	DC_bifur = int(73500)
	DC_trig = int(512)
	
        
        #fsac = open('AvgSac.dat', 'r')
        #for line in fsac.readlines():
        #    x1 = float(line.split(' ')[3])
        #    x2 = float(line.split(' ')[2])
        
         
	#Get data from directory wide
	input_path = args.input_path
	input_file_list = [file for file in os.listdir(input_path)]
	
	
	#initialize totals; contamination is not additive (I think)
	A_total = 0
	B_total = 0
	C_total = 0
	D_total = 0
	for ntuple in input_file_list: #loop over files in a directory
		eCorr = rat.utility().Get().GetReconCorrector()
		eCalib = rat.utility().Get().GetReconCalibrator()
                 
		
		#Get data from files	
		full_path = str(input_path + ntuple) #get the full path name to the file
		data = rr.rootreader(full_path) #root reader generates a python library whose keys are parameters in the ntuple

                #Make pathological cuts ('preliminary cuts')
		PathPass = []	
		PathTrigPassIndices = np.where((data.triggerWord & Trig_path) == 0)[0]
		PathDCPassIndices = np.where((data.dcFlagged & DC_path) == DC_path)[0]
		PathMaskTotalPassIndices = np.intersect1d(PathTrigPassIndices, PathDCPassIndices)
		for q in PathMaskTotalPassIndices:
			if data.fitValid[q] == False:
				continue
			if data.energy[q] < E_LOW:
				continue
			data.energy[q] = eCorr.CorrectEnergyRSP(data.energy[q])
			rho = float(np.sqrt(data.posx[q]*data.posx[q] + data.posy[q]*data.posy[q]))
			realData = bool(True)
			data.energy[q] = eCalib.CalibrateEnergyRSP(realData, data.energy[q], rho, data.posz[q])
			if data.energy[q] > E_HIGH:
				continue
			if data.posr[q] > POSR_CUT:
				continue
			PathPass.append(q)
			
		
		#DC Bifurcation cuts
		BifurDCPassIndices = np.where((data.dcFlagged & DC_bifur) == DC_bifur)[0]
		BifurTrigPassIndices = np.where((data.triggerWord & DC_trig) == 0)[0] 
		DCMaskTotalPassIndices = np.intersect1d(BifurDCPassIndices, BifurTrigPassIndices)
		Q = len(DCMaskTotalPassIndices)
		DC_Bif = np.intersect1d(PathPass, DCMaskTotalPassIndices)
		
		
		#CC Bifurcation cuts
		CC_Bif = []
		for p in PathPass:
			if -0.12 < data.beta14[p] < 0.95 and data.itr[p] > 0.55:
				CC_Bif.append(p)
	
		#calculate A
		IndicesA = np.intersect1d(CC_Bif, DC_Bif)
		eventsA = []
		for a in IndicesA:
			eventsA.append(data.eventID[a])
		A = float(len(IndicesA))
		A_total = A_total + A
		
		#calculate B
		IndicesB = np.setdiff1d(CC_Bif, DC_Bif)
		eventsB = []
		for b in IndicesB:
			eventsB.append(data.eventID[b])
		B = float(len(IndicesB))
		B_total = B_total + B
	
		#calculate C
		IndicesC = np.setdiff1d(DC_Bif, CC_Bif)
		eventsC = []
		for c in IndicesC:
			eventsC.append(data.eventID[c])
		C = float(len(IndicesC))
		C_total = C_total + C
	
		#calculate D
		FailedDC = np.setdiff1d(PathPass, DC_Bif)
		FailedClass = np.setdiff1d(PathPass, CC_Bif)
		IndicesD = np.intersect1d(FailedDC, FailedClass)
		eventsD = []
		for d in IndicesD:
			eventsD.append(data.eventID[d])
		D = float(len(IndicesD))
		D_total = D_total + D
		
	

print("All Done!")

outname = args.out
f2 = open(args.out,'a')
f2.write("A {}".format(A))
f2.write("\n")
f2.write("B {}".format(B))
f2.write("\n")
f2.write("C {}".format(C))
f2.write("\n")
f2.write("D {}".format(D))
f2.write("\n")
f2.write("P {}".format(len(PathPass)))
f2.write("\n")
f2.write("Q {}".format(Q))
f2.write("\n")
f2.close()

f3 = open(args.evID, 'a')
f3.write("A {}".format(eventsA))
f3.write('\n')
f3.write("B {}".format(eventsB))
f3.write('\n')
f3.write("C {}".format(eventsC))
f3.write('\n')
f3.write("D {}".format(eventsD))
f3.write('\n')
	
print("--- %s seconds ---" % (time.time() - start_time))
