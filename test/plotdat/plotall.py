import os,sys
from subprocess import call
import time

from optparse import OptionParser

parser=OptionParser()

parser.add_option("-f","--force",action='store_true',default=False,help="Force all plots to be reproduced")

opts,args=parser.parse_args()


dat={
	"plotdat/chhiggs_cutflow.txt":"plot/CutFlow.pdf",
	"plotdat/chhiggs_njets.txt":"plot/NJets.pdf",
	"plotdat/chhiggs_met.txt":"plot/EtMiss.pdf",
	"plotdat/chhiggs_tau1pt.txt":"plot/Tau1Pt.pdf",
	"plotdat/chhiggs_mt.txt":"plot/Mt.pdf",
	"plotdat/chhiggs_mt_ewk.txt":"plot/Mt_Embed.pdf",
	"plotdat/chhiggs_met_ewk.txt":"plot/EtMiss_Embed.pdf",
	"plotdat/chhiggs_met_ewk2.txt":"plot/EtMiss_Embed2.pdf",
	#"plotdat/chhiggs_mtmc.txt":"plot/MtMC.pdf",
	#"plotdat/tmva_bdt0.txt":"plot/Bdt0.pdf",
	#"plotdat/tmva_bdt1.txt":"plot/Bdt1.pdf",
	#"plotdat/tmva_cutflow.txt":"plot/TmvaCutFlow.pdf",
	#"plotdat/tmva_mt.txt":"plot/TmvaMt.pdf",
	"plotdat/chhiggs_metqcd.txt":"plot/EtMissQCDInvIso.pdf",
	#"plotdat/chhiggs_metband.txt":"plot/EtMissBand.pdf",
	"plotdat/qcdpurity_control_etmiss.txt":"plot/EtMiss_Control.pdf",
	"plotdat/qcdpurity_control_taupt.txt":"plot/TauPt_Control.pdf",
	#"plotdat/qcdpurity_mt.txt":"plot/MtQCDOnly.pdf",
	"plotdat/chhiggs_yields.txt": "plot/Yields.pdf",
	"plotdat/ewk_full.txt":"plot/EWK_EtMiss_Full.pdf",
	"plotdat/ewk_ht_full.txt":"plot/EWK_HT_Full.pdf",
	"plotdat/chhiggs_rbb.txt":"plot/RbbMin.pdf",
	"plotdat/chhiggs_rcoll.txt":"plot/RCollMin.pdf",
	}

print "I will consider the following files",dat.keys()

try:
	os.mkdir("plot")
except : pass

for d in dat.keys():
	fname=dat[d]
	run=False
	if not os.path.isfile(fname): run=True
	if not run and time.ctime(os.path.getmtime(fname)) < time.ctime(os.path.getmtime(d)) : run=True
	if opts.force: run=True
	if run:
		cmd="python plot.py -d " + d
		print "-> will run on ",d,"'"+cmd+ "'"
		call("python plot.py -d " + d,shell=True)

