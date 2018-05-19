#!/user/bdisoft/operational/bin/Python/PRO/bin/python
import numpy as np
import matplotlib.pyplot as plt
import pickle as pkl
import os, time
import glob
import argparse
import pytimber
import pandas as pd 

def PS_bfield_variables():
	name = {}
	name['PR.SCBFC'] = 'PR.SCBFC.LT:SAMPLES'
	name['PR.SCBFC-ST'] = 'PR.SCBFC.LT:SAMPLING_TRAIN'
	name['PR.SCBFC-TF'] = 'PR.SCBFC.LT:TIME_UNIT_FACTOR'	
	return name

def bpm_variables():
	name = {}
	name['ITE.BPMI10:HOR_RAWDELTA'] = 'ITE.BPMI10:HOR_RAWDELTA'
	name['ITE.BPMI10:VER_RAWDELTA'] = 'ITE.BPMI10:VER_RAWDELTA'
	name['ITE.BPMI40:HOR_RAWDELTA'] = 'ITE.BPMI40:VER_RAWDELTA'
	name['ITE.BPMI40:VER_RAWDELTA'] = 'ITE.BPMI40:VER_RAWDELTA'
	return name

def bpm_position_variables():
	name={}
	name['ITE.BPMI10:HOR_POSITIONS'] = 'ITE.BPMI10:HOR_POSITIONS'
	name['ITE.BPMI10:VER_POSITIONS'] = 'ITE.BPMI10:VER_POSITIONS'
	name['ITE.BPMI40:HOR_POSITIONS'] = 'ITE.BPMI40:HOR_POSITIONS'
	name['ITE.BPMI40:VER_POSITIONS'] = 'ITE.BPMI40:VER_POSITIONS'
	name['EI.BPMI10:HOR_POSITIONS'] = 'EI.BPMI10:HOR_POSITIONS'
	name['EI.BPMI10:VER_POSITIONS'] = 'EI.BPMI10:VER_POSITIONS'
	name['EI.BPMI30:HOR_POSITIONS'] = 'EI.BPMI30:HOR_POSITIONS'
	name['EI.BPMI30:VER_POSITIONS'] = 'EI.BPMI30:VER_POSITIONS'
	name['ETL.BPMI20:HOR_POSITIONS'] = 'ETL.BPMI20:HOR_POSITIONS'
	name['ETL.BPMI20:VER_POSITIONS'] = 'ETL.BPMI20:VER_POSITIONS'
	name['ETL.BPMI30:HOR_POSITIONS'] = 'ETL.BPMI30:HOR_POSITIONS'
	name['ETL.BPMI30:VER_POSITIONS'] = 'ETL.BPMI30:VER_POSITIONS'
	name['ETL.BPMI40:HOR_POSITIONS'] = 'ETL.BPMI40:HOR_POSITIONS'
	name['ETL.BPMI40:VER_POSITIONS'] = 'ETL.BPMI40:VER_POSITIONS'
	name['ETL.BPMI50:HOR_POSITIONS'] = 'ETL.BPMI50:HOR_POSITIONS'
	name['ETL.BPMI50:VER_POSITIONS'] = 'ETL.BPMI50:VER_POSITIONS'
	name['ETL.BPMI60:HOR_POSITIONS'] = 'ETL.BPMI60:HOR_POSITIONS'
	name['ETL.BPMI60:VER_POSITIONS'] = 'ETL.BPMI60:VER_POSITIONS'
	return name

def bct_line_variables():
	name = {}
	name['ITH.BCT41'] = 'ITH.BCT41:INTENSITY_PER_INJECTION'
	name['ETL.BCT10'] = 'ETL.BCT10:TOTAL_INTENSITY_PER_INJECTION'
	name['ETL.BCT20'] = 'ETL.BCT20:TOTAL_INTENSITY_PER_INJECTION'
	name['EI.BCT10']  = 'EI.BCT10:TOTAL_INTENSITY_PER_INJECTION'
	return name

def bct_ring_variables():
	name = {}
	#name['EXTR'] = 'ER.MTR12.BCTDC:INTENSITY_EJEC_TOTAL'
	name['ER.BCTDC'] = 'ER.BCTDC:INTENSITIES'
	return name


plt.close('all')
db_dir = '../Measurements/datadb/'
os.system('mkdir -p '+db_dir)
mydb=pytimber.pagestore.PageStore('LEIR.db',db_dir)
#plt.switch_backend('agg')

parser = argparse.ArgumentParser(description="Intensity evolution.")
parser.add_argument('-t1', action = 'store', dest = 't1', type = str, help='tstart.')
parser.add_argument('-t2', action = 'store', dest = 't2', type = str, help='tend.', default= np.nan)
parser.add_argument('-nh', action = 'store', dest = 'nT', type = float, help='num of hours.')
args = parser.parse_args()

t0 = args.t1
t2 = args.t2
#t2 = '2018-05-07 23:00:00.000'

from datetime import datetime, timedelta
import time
t0 = time.mktime(datetime.strptime(t0, "%Y-%m-%d %H:%M:%S.%f").timetuple())
DT = 3600 # an hour
if isinstance(t2,str):
	t2 = time.mktime(datetime.strptime(t2, "%Y-%m-%d %H:%M:%S.%f").timetuple())
	nT = np.floor((t2-t0)/DT)
	rest =  t2-t0 - nT*DT
else:
	nT = args.nT

db = pytimber.LoggingDB()

# get bfield raw data  for PS
#t1 = datetime.strptime(t1, "%Y-%m-%d %H:%M:%S.%f")
#t2 = t1
for ii in np.arange(nT):
	t1 = t0 + ii*DT 
	t2 = t1+ DT
	print time.ctime(t1), time.ctime(t2)
	data_bfield = db.get([PS_bfield_variables()[var] for var in PS_bfield_variables()], t1,t2)
	mydb.store(data_bfield)
	data_bpm = db.get([bpm_variables()[var] for var in bpm_variables()], t1, t2)
	mydb.store(data_bpm)
	data_pos_bpm = db.get([bpm_position_variables()[var] for var in bpm_position_variables()], t1, t2)
	mydb.store(data_pos_bpm)
	data_cycle = db.get('LEI.LSA:CYCLE',t1,t2)
	mydb.store(data_cycle)
	data_bct =  db.get([bct_line_variables()[var] for var in bct_line_variables()], t1, t2)
	mydb.store(data_bct)
	data_bct =  db.get([bct_ring_variables()[var] for var in bct_ring_variables()], t1, t2)
	mydb.store(data_bct)

if rest:
	t1 = t0 + nT*DT 
	t2 = t1 + nT*DT + rest
	print time.ctime(t1), time.ctime(t2), t1, t2
	data_bfield = db.get([PS_bfield_variables()[var] for var in PS_bfield_variables()], t1,t2)
	mydb.store(data_bfield)
	data_bpm = db.get([bpm_variables()[var] for var in bpm_variables()], t1, t2)
	mydb.store(data_bpm)
	data_pos_bpm = db.get([bpm_position_variables()[var] for var in bpm_position_variables()], t1, t2)
	mydb.store(data_pos_bpm)
	data_cycle = db.get('LEI.LSA:CYCLE',t1,t2)
	mydb.store(data_cycle)
	data_bct =  db.get([bct_line_variables()[var] for var in bct_line_variables()], t1, t2)
	mydb.store(data_bct)
	data_bct =  db.get([bct_ring_variables()[var] for var in bct_ring_variables()], t1, t2)
	mydb.store(data_bct)

