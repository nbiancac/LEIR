#!/user/bdisoft/operational/bin/Python/PRO/bin/python
import numpy as np
import matplotlib.pyplot as plt
import pickle as pkl
import os, time
import glob
import argparse
import pytimber
import pandas as pd 
from datetime import datetime, timedelta
import time


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
mydb=pytimber.pagestore.PageStore('LEIR.db',db_dir)
#plt.switch_backend('agg')

parser = argparse.ArgumentParser(description="Intensity evolution and BPMs.")
parser.add_argument('-t1', action = 'store', dest = 't1', type = str, help='tstart.')
parser.add_argument('-t2', action = 'store', dest = 't2', type = str, help='tend.')
parser.add_argument('-rw', action = 'store', dest = 'rw', type = int, help='moving average.', default = 1)
parser.add_argument('-nm', action = 'store', dest = 'nm', type = int, help='Interval of down-sampling in minutes.', default = 5)
parser.add_argument('-c', action = 'store', dest = 'fundamental', type = str, help='USER cycle', default = 'EARLY')

args = parser.parse_args()

t1 = args.t1
t2 = args.t2
nm = args.nm; print('Downsampling every '+str(nm)+' min.')
rw = args.rw; print('Rolling average with '+str(rw)+' samples.')
fundamental = args.fundamental; print('Cycle: '+str(fundamental))

if t2: 
	t1 = time.mktime(datetime.strptime(t1, "%Y-%m-%d %H:%M:%S.%f").timetuple())
	t2 = time.mktime(datetime.strptime(t2, "%Y-%m-%d %H:%M:%S.%f").timetuple())
else: 
	t1 = time.mktime(datetime.strptime(t1, "%Y-%m-%d %H:%M:%S.%f").timetuple())
	t2 = t1+ 3600*nT


data_bfield = mydb.get([PS_bfield_variables()[var] for var in PS_bfield_variables()], t1,t2)
data_pos_bpm = mydb.get([bpm_position_variables()[var] for var in bpm_position_variables()], t1, t2)
data_cycle = mydb.get('LEI.LSA:CYCLE',t1,t2)
data_bct =  mydb.get([bct_line_variables()[var] for var in bct_line_variables()], t1, t2)
data_bct_ring =  mydb.get([bct_ring_variables()[var] for var in bct_ring_variables()], t1, t2)

df_bfield_v=[]
for var in PS_bfield_variables():
	t, v = data_bfield[PS_bfield_variables()[var]]
	df_bfield_ = pd.DataFrame(v,columns = [var], index=t)
	df_bfield_.index.name='timestamp'
	df_bfield_v.append(df_bfield_)
df_PS_bfield = pd.concat(df_bfield_v, axis = 1)

# get BPM positions
df_bpm_v=[]
for var in bpm_position_variables():
	t, v = data_pos_bpm[bpm_position_variables()[var]]
	df_bpm_ = pd.DataFrame(v,columns = [var+'_%d'%ii for ii in np.arange(v.shape[1])], index=t)
	df_bpm_.index.name='timestamp'
	df_bpm_v.append(df_bpm_)
df_pos_bpm = pd.concat(df_bpm_v, axis = 1)

# get cycles
t, v = data_cycle['LEI.LSA:CYCLE']
df_c = pd.DataFrame(v, columns = ['cycle'], index = t,dtype=str) 
df_c.index.name='timestamp'

# get BCT in the line
df_bct = []
for var in bct_line_variables():
	t, v = data_bct[bct_line_variables()[var]]
	#df_bct_ = pd.DataFrame((v),columns = [var], index = t)
	df_bct_ = pd.DataFrame((v),columns = [var+'_%d'%ii for ii in np.arange(v.shape[1])], index = t)
	df_bct_.index.name='timestamp'
	df_bct.append(df_bct_)

df_bct_line = pd.concat(df_bct,axis=1)

# get BCT in the ring
for var in bct_ring_variables():
	t, v = data_bct_ring[bct_ring_variables()[var]]
	df_bct = pd.DataFrame(v,columns = [var], index = t) 
	df_bct.index.name='timestamp'

# there is a delay in the timestamps between ring and injection line: this may cut some acquisitions in the ring BCT dataframe. Equalized here.
if len(df_bct)<len(df_bct_line):
	df_bct_line.drop(df_bct_line.index[-1],inplace=True)
if len(df_bct)<len(df_pos_bpm):
	df_pos_bpm.drop(df_pos_bpm.index[-1],inplace=True)


df_bct_line.index = df_bct.index[0:len(df_bct_line.index)]
df_pos_bpm.index = df_bct.index[0:len(df_pos_bpm.index)]
df = pd.concat([df_bct,df_bct_line,df_c, df_pos_bpm],axis=1)

# select NOMINAL
df = df[df['cycle'].str.contains(fundamental)]
if fundamental == 'NOMINAL':
	N_inj = 1
	ind_inj = np.array([245, 445, 645, 845, 1045, 1245, 1445])
else:
	N_inj = 1
	ind_inj = np.array([245])

v = np.array([np.asarray(el,dtype=float) for el in df['ER.BCTDC'].values])
df_bct_new = pd.DataFrame(v, index = df.index , columns = ['ER.BCTDC_'+str(ii)+'ms' for ii in np.arange(v.shape[1])])
df = pd.concat([df,df_bct_new])
df.drop('ER.BCTDC', inplace=True)
df['date'] = pd.to_datetime(df.index, unit = 's')+pd.Timedelta('02:00:00')
df = df.resample('1T', on = 'date').mean()

# Get injected intensity and transmission loss
delta_inj = []
trans_inj = []

for d in np.arange(N_inj):
    df['inj_%d'%d] = df['ER.BCTDC_'+str(150+ ind_inj[d])+'ms']- df['ER.BCTDC_'+str(150+ ind_inj[d]-1)+'ms']
    df['trans_%d'%d] = df['ER.BCTDC_'+str(150+ ind_inj[d] + 199)+'ms']/ df['ER.BCTDC_'+str(150+ ind_inj[d])+'ms'] 


#get PS field
t_PS=[]; v_PS=[]
for irow, row in enumerate(df_PS_bfield.index):
	t_PS.append(row+1e-3*np.arange(len(df_PS_bfield['PR.SCBFC'].iloc[irow])))	
	v_PS.append(df_PS_bfield['PR.SCBFC'].iloc[irow])
t_PS=np.hstack(np.array(t_PS))
v_PS=np.hstack(np.array(v_PS))


# Get injection efficiency
for n_inj in np.arange(N_inj):
	df['eff_%d'%n_inj] = df['inj_%d'%n_inj]/df['EI.BCT10_%d'%n_inj]
	df['PS_field_%d'%n_inj] = np.interp(pd.to_numeric(df.index)+150e-3+200e-3*n_inj, t_PS,v_PS)


saveDir = '..//Monitoring/'
t1_str = pd.to_datetime(df.index+2*3600, unit='s').min().strftime('%Y-%m-%d %H:%M:%S')
t2_str = pd.to_datetime(df.index+2*3600, unit='s').max().strftime('%Y-%m-%d %H:%M:%S')

dire = saveDir+'/'+fundamental.replace(':','_')+'/'+t1_str.replace(':','_').replace(' ','_')+'_'+t2_str.replace(':','_').replace(' ','_')+'/'
try: os.system('mkdir -p '+dire)
except : pass




rw = 1 # rolling window number of samples

for n_inj in np.arange(N_inj):
	fig,(ax1,ax2) = plt.subplots(2,1,figsize=(10,10), sharex = True)	
	for var in bct_line_variables():
		ax1.plot(df.index, df[var+'_%d'%n_inj].rolling(rw).mean().values, label = var)
	ax1.legend(bbox_to_anchor=(1.04,1), loc="upper left")
	ax1.set_xticklabels([])
	ax1.set_ylabel('N [1e10 c]')
	ax1.set_title(fundamental+', intensity of injection #%d overview'%n_inj)
	
	ax2.plot(df.index, 100*df['eff_%d'%n_inj].rolling(rw).mean().values,'-k')
	ax2.legend(['Efficiency'], loc = 0)
	ax2.set_ylabel('Inj. efficiency [%]')
	
	ax3 = ax2.twinx()
	ax3.plot(df.index, 100*df['trans_%d'%n_inj].rolling(rw).mean().values,'-r')
	ax3.legend(['Transmission'], loc = 2)
	ax3.set_ylabel('Trans. efficiency [%]')
	ax2.set_ylim(0,100)	
	ax3.set_ylim(0,100)		
	
	plt.subplots_adjust(right=0.7)
	plt.savefig(dire+'Intensity_and_Efficiency_Inj%d.png'%n_inj)


for n_inj in np.arange(N_inj):
	fig,(ax1,ax2,ax3) = plt.subplots(3,1,figsize=(10,10), sharex = True)	
	df_ = df.filter(regex='.*HOR_POS.*%d'%n_inj)	
	
	for var in np.sort(df_.keys()):
		ax1.plot(df_.index,df_[var].rolling(rw).mean().values, label = var.replace(':HOR_POSITIONS_%d'%n_inj,''))
	df_ = df.filter(regex='.*VER_POS.*%d'%n_inj)
	
	for var in np.sort(df_.keys()):
		ax2.plot(df_.index,df_[var].rolling(rw).mean().values, label = var.replace(':VER_POSITIONS_%d'%n_inj,''))
	
	ax1.set_xticklabels([])
	ax1.set_ylabel('H position [mm]')	
	ax1.legend(bbox_to_anchor=(1.04,1), loc="upper left")
	ax1.set_title(fundamental+', injection #%d overview'%n_inj)
	
	ax2.set_xticklabels([])
	ax2.set_ylabel('V position [mm]')	
	ax2.legend(bbox_to_anchor=(1.04,1), loc="upper left")
	
	ax3.plot(df_.index, 100*df['eff_%d'%n_inj].rolling(rw).mean().values)
	ax3.set_ylabel('Inj. efficiency [%]')	
	ax3.set_ylim(0,100)
	
	plt.subplots_adjust(right=0.7)
	plt.savefig(dire+'Line_and_Efficiency_Inj%d.png'%n_inj)


for n_inj in np.arange(N_inj):
	fig,(ax1,ax2,ax3) = plt.subplots(3,1,figsize=(10,10), sharex = True)	
	for var in bct_line_variables():
		ax1.plot(df.index, df[var+'_%d'%n_inj].rolling(rw).mean().values, label = var)
	ax1.legend(bbox_to_anchor=(1.04,1), loc="upper left")
	ax1.set_xticklabels([])
	ax1.set_ylabel('N [1e10 c]')
	ax1.set_title(fundamental+', injection #%d and PS magnetic field'%n_inj)
	
	ax2.plot(df.index, 100*df['eff_%d'%n_inj].rolling(rw).mean().values,'-k')
	ax2.legend(['Efficiency'], loc = 0)
	ax2.set_ylim(0,100)
	ax2.set_ylabel('Inj. efficiency [%]')
	
	ax3.plot(df.index,df['PS_field_%d'%n_inj],'.-')
	ax3.legend(['PS magnetic field'], loc = 0)
	plt.subplots_adjust(right=0.7)
	plt.savefig(dire+'Line_and_Magnetic_Inj%d.png'%n_inj)


import itertools
from bokeh.layouts import column
from bokeh.palettes import Category10
from bokeh.plotting import figure, output_file, show
from bokeh.io import curdoc

curdoc().clear()

def color_gen():
    for c in itertools.cycle(Category10[10]):
        yield c

########## Intensity and PS magnetic field ################
color = color_gen()
color.next()

s1 = figure(plot_width=800, plot_height=250,x_axis_type="datetime", title = fundamental+', Intensity and PS field')

n_inj = 0

for var in bct_line_variables():
    print var
    c = color.next()
    s1.line(df.index, df[var+'_%d'%n_inj].rolling(rw).mean().values, color=c,line_width=2, alpha=0.8,
       muted_color= c, muted_alpha=0.1, legend=var)
s1.legend.location = "top_left"
s1.legend.click_policy="mute"


s2 = figure(plot_width=800, plot_height=250,x_axis_type="datetime",x_range=s1.x_range)
s2.line(df.index, 100*df['eff_%d'%n_inj].rolling(rw).mean().values,color='black',line_width=2, alpha=0.8,
       muted_color= 'black', muted_alpha=0.1, legend='Efficiency')

s3 = figure(plot_width=800, plot_height=250,x_axis_type="datetime",x_range=s1.x_range)
s3.line(df.index, df['PS_field_%d'%n_inj].values,color='black',line_width=2, alpha=0.8,
       muted_color= 'black', muted_alpha=0.1, legend='PS main field')

output_file(dire+"Line_and_Magnetic_Inj%d.html"%n_inj, title="Example")

show(column(s1, s2,s3))


##########33 BPMs and efficiency ################
df_ = df.filter(regex='.*HOR_POS.*%d'%n_inj)
s1 = figure(plot_width=800, plot_height=250,x_axis_type="datetime", title = fundamental+', BPM and inj. efficiency')

color = color_gen()
color.next()

for var in np.sort(df_.keys()):
    c = color.next()
    df_ = df.filter(regex='.*HOR_POS.*%d'%n_inj)
    s1.line(df.index, df_[var].rolling(rw).mean().values, color=c,line_width=2, alpha=0.8,
       muted_color= c, muted_alpha=0.1, legend=var.replace(':HOR_POSITIONS_%d'%n_inj,''))
    s1.legend.location = "top_left"
    s1.legend.click_policy="mute"

s1.yaxis.axis_label = 'H position [mm]'

df_ = df.filter(regex='.*VER_POS.*%d'%n_inj)
s2 = figure(plot_width=800, plot_height=250,x_axis_type="datetime",x_range=s1.x_range)

color = color_gen()
color.next()

for var in np.sort(df_.keys()):
    c = color.next()
    s2.line(df.index, df_[var].rolling(rw).mean().values, color=c,line_width=2, alpha=0.8,
       muted_color= c, muted_alpha=0.1, legend=var.replace(':VER_POSITIONS_%d'%n_inj,''))
    s2.legend.location = "top_left"
    s2.legend.click_policy="mute"

s2.yaxis.axis_label = 'V position [mm]'

s3 = figure(plot_width=800, plot_height=250,x_axis_type="datetime", y_range=(0,100),x_range=s1.x_range)
s3.line(df.index, 100*df['eff_%d'%n_inj].rolling(rw).mean().values, color='black',line_width=2, alpha=0.8,
       muted_color= 'black', muted_alpha=0.1, legend='Injection efficiency')

s3.xaxis.axis_label = 'Time'
s3.yaxis.axis_label = 'Inj. efficiency [%]'

output_file(dire+"Line_and_Efficiency_Inj%d.html"%n_inj, title="Example")

show(column(s1, s2, s3))


print('Done.')

plt.show()


