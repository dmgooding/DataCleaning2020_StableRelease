import ROOT
import sys
import os
import numpy as np
import time

start_time = time.time()

nbins = 101
first_bin = 0
last_bin = 100

f = ROOT.TFile.Open("sum.root")

add1 = ROOT.TH1F('add1', 'all', nbins, first_bin, last_bin)
for i in range(nbins):
	add1.SetBinContent(i,1.0)

Total = f.Total

DC = f.DCsac
DC.Divide(Total)
DC.Scale(-1.0)
DC.Add(add1)


CC = f.CCsac
CC.Divide(Total)
CC.Scale(-1.0)
CC.Add(add1)

DCfit = ROOT.TF1("DCfit", "pol1(0)", 5,10)
DCfit.SetParameter(0,0.02)
DCfit.SetParameter(1,0.00000001)
DCfit.FixParameter(1,0.0)

CCfit = ROOT.TF1("CCfit", "pol1(0)", 5, 10)
CCfit.SetParameter(0,0.02)
CCfit.SetParameter(1,0.00000001)
CCfit.FixParameter(1,0.0)

DC.Fit(DCfit, "RB")
CC.Fit(CCfit, "RB")

Outname = "AvgSac.dat"
outfile = open(Outname, 'a')
outfile.write('CC DC')
outfile.write(' ')
outfile.write(str(CCfit.GetParameter(0)))
outfile.write(' ')
outfile.write(str(DCfit.GetParameter(0)))
outfile.close()

testing = ROOT.TFile('test', 'RECREATE')
CC.Write()
DC.Write()
testing.Close()


print("--- %s seconds ---" % (time.time() - start_time))
