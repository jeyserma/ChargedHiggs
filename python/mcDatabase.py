#!env python

import re
import os,sys
import math
from optparse import OptionParser
from subprocess import call, check_output

parser = OptionParser(usage = "usage");
parser.add_option("-e","--eos",dest="eos",type="string",help="eos directory to scout, will not read the files in the pSet",default="");
parser.add_option("-x","--xsec",dest="xsec",type="float",help="Use external cross-section",default=-1);
parser.add_option("-l","--label",dest="label",type="string",help="MC label",default="DYamcatnlo");
parser.add_option("-f","--file",dest="file",type="string",help="mc_database file name",default="dat/mc_database.txt");
parser.add_option("-r","--recursive", dest='rec', action= 'store_true', help="do same for each subdir", default =False);
parser.add_option("-p","--pileup",dest="pu",type="string",help="TODO FIXME")

(opts,args)=parser.parse_args()

EOS = "/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select"
if '/eos/user' in opts.eos: EOS += " root://eosuser"

if opts.rec:
	cmd = EOS +" find -d "
	#if '/eos/user' in opts.eos: 
	cmd += " --childcount "
	cmd+=opts.eos
	list = check_output(cmd,shell=True);
	for line in list.split('\n'):
		if line =='': continue
		print "Line is '"+line+"'"
		dir = line.split() [0]
		ndir = line.split() [1]
		nfiles = line.split() [2]
		#
		nd = float(re.sub('ndir=','',ndir) )
		nf = float(re.sub('nfiles=','',nfiles) )
		dir = re.sub('/eos/cms','',dir)
		if dir[-1] == '/' : dir = dir[:-1] # remove trailing slash

		## find label: directory not containing only numbers, hyphens, underscore, or empty
		dirs=dir.split('/')
		idx=len(dirs) -1 
		while idx >=0 :
			label = dirs[idx]
			if re.match( '^[0-9_\-]*$',label): 
				idx -= 1
			else:
				break
		if idx <0: label = re.sub('.*/','',dir)
		## 
		if nf >0 and not re.match("Run2015",dir) and not re.match("Run2016",dir) and "/failed" not in dir: ## remove data
			print "Found one directory:",dir
			cmd = "python %s -e %s -x %f -l %s -f %s"%(sys.argv[0],dir,opts.xsec,label,opts.file)
			print "going to execute",cmd
			call(cmd,shell=True)
	exit(0)

cmd = EOS+ " find -f " + opts.eos

outputList = check_output(cmd,shell=True)
fileList0 = outputList.split() ## change lines into list
if '/eos/user' in opts.eos:
	fileList = [ re.sub("/eos/user","root://eosuser///eos/user",f) for f in fileList0 if '/failed/' not in f ]
else:
	fileList = [ re.sub("/eos/cms","root://eoscms//",f) for f in fileList0 if '/failed/' not in f ]

import ROOT as r
r.gROOT.SetBatch()

## TODO count mcWeights, nEntries
n=0
myTmp= r.TFile.Open("/tmp/" + os.environ["USER"] + "/mytmp.root","RECREATE")
myTmp.cd()
sum=r.TH1D("SumWeights","Sum of mcWeights",1,0,2)

for idx,fName in enumerate(fileList):
	print "processing file:",idx,"/",len(fileList)," : ", fName
	fROOT = r.TFile.Open( fName )
	if idx == 0:
		myTmp.cd()
		h_xSec = fROOT.Get("nero/xSec").Clone("myxSec")
		hScales = fROOT.Get("nero/scaleReweightSums").Clone("myScales")
		hPdfs = fROOT.Get("nero/pdfReweightSums").Clone("myPdfs")
	else:
		h = fROOT.Get("nero/xSec")
		hScalesTmp = fROOT.Get("nero/scaleReweightSums")
		hPdfsTmp = fROOT.Get("nero/pdfReweightSums")
		if h.GetBinContent(2) == 0 : 
			print "Error is 0, xsec is",h.GetBinContent(1),"try to continue"
		else:
			print "\txSec in file is ",h.GetBinContent(1)/h.GetBinContent(2),"+/-",math.sqrt(1./h.GetBinContent(2))
		h_xSec.Add( h )
		hScales.Add( hScalesTmp )
		hPdfs.Add( hPdfsTmp )

	t = fROOT.Get("nero/all")
	mysum=r.TH1D("mysum","Sum of mcWeights",1,0,2)
	t.Draw("1>>mysum","mcWeight") ##>>+ doesn't work
	sum.Add(mysum)
	n += t.GetEntries()
	fROOT.Close()


print "---------------------------------------------"
print "internal xSec = ",h_xSec.GetBinContent(1)/h_xSec.GetBinContent(2), "+/-", math.sqrt(1./h_xSec.GetBinContent(2))
print "SumWeights = ", sum.GetBinContent(1)
print "Tot Entries = ", n
print "---------------------------------------------"
### LABEL dir Entries xSec
f = open (opts.file,"a")
print>>f, opts.label,opts.eos, sum.GetBinContent(1),

if opts.xsec >0 : 
	print>>f, opts.xsec,
else: 
	## AUTOMAGIC CROSS SECTIONS -- INTERNAL if not written here
	try:
		xsec= h_xSec.GetBinContent(1)/h_xSec.GetBinContent(2)
	except: 
		xsec=0
	## DY
	if 'DYJets' in opts.label or 'DY' in opts.label: xsec=6025.
	## SIG
	elif 'ChargedHiggs_HplusTB_HplusToTauNu_M-200' in opts.label: xsec=0.02952842256
	elif 'ChargedHiggs_HplusTB_HplusToTauNu_M-300' in opts.label: xsec=0.002366
	elif 'ChargedHiggs_HplusTB_HplusToTauNu_M-350' in opts.label: xsec=0.0013458646
	elif 'ChargedHiggs_HplusTB_HplusToTauNu_M-400' in opts.label: xsec=0.000836289779
	elif 'ChargedHiggs_HplusTB_HplusToTauNu_M-500' in opts.label: xsec=0.000382537512
	elif 'ChargedHiggs_HplusTB_HplusToTauNu_M-220' in opts.label: xsec=0.005344 #???
	elif 'ChargedHiggs_HplusTB_HplusToTauNu_M-250' in opts.label: xsec=0.005344 #??
	### TT
	elif 'TT' in opts.label: xsec=831
	## ST
	elif 'ST_s-channel_4f_InclusiveDecays' in opts.label: xsec=10.32
	elif 'ST_t-channel_antitop_4f' in opts.label: xsec=80.95
	elif 'ST_t-channel_top_4f' in opts.label: xsec=136.02
	elif 'ST_tW_antitop_5f' in opts.label: xsec=30.09
	elif 'ST_tW_top_5f' in opts.label: xsec=30.11
	### WJETS
	elif 'WJets' in opts.label: xsec=61526.7
	elif 'W0' in opts.label: xsec=34273.632815
	elif 'W1' in opts.label: xsec=18455.979619
	elif 'W2' in opts.label: xsec=6035.904629
	elif 'W3' in opts.label: xsec=1821.46719
	elif 'W4' in opts.label: xsec=939.684984
	##VV
	elif 'WWTo2L2Nu-powheg' in opts.label: xsec=12.46
	elif 'WZTo1L1Nu2Q' in opts.label: xsec=10.71
	elif 'WZTo1L3Nu' in opts.label: xsec=3.033
	elif 'WZTo2L2Q' in opts.label: xsec=5.595
	elif 'WZTo3LNu' in opts.label: xsec=4.42965
	elif 'ZZTo2L2Q' in opts.label: xsec=0.564
	elif 'ZZTo4L' in opts.label: xsec=1.256
	elif 'WWToLNuQQ' in opts.label: xsec=52
	##
	#elif '' in opts.label: xsec=
	## INTERNAL
	print>>f,  xsec,

if hScales.GetBinContent(1) > 0:
	print>>f, "SCALES",
	for i in range(0,6):
		print>>f, sum.GetBinContent(1)/hScales.GetBinContent(i+1),

if hPdfs.GetBinContent(1) > 0:
	print>>f, "PDFS",
	for i in range(0,100):
		print>>f, sum.GetBinContent(1)/hPdfs.GetBinContent(i+1), 
print >>f,"" ##new line
print "---------------------------------------------"

