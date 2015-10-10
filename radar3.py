#https://github.com/ARM-DOE/pyart/blob/master/pyart/map/grid_mapper.py
import pyart
import numpy as np
import numpy.ma as ma
import pyart.map.grid_mapper as gm
#handle=open('sn.last')
#radar = pyart.io.read_nexrad_level3(handle)

# ... or
#radar = pyart.io.read('KOKX_SDUS21_N1QOKX_201510030004')
#radar = pyart.io.read_nexrad_archive('KGWX_20150703_0815')
radar = pyart.io.read('sn.last')

print 'number of rays:',radar.nrays
print 'number of gates:',radar.ngates
print 'number of sweeks:',radar.nsweeps
print 'lat,lng: ', radar.latitude['data'][0],',',radar.longitude['data'][0]

intervals = radar.range['data']
rows = radar.fields['reflectivity']['data']
for i in range(0,radar.nrays):
	row = rows[i]
	#get index of unmask items
	idx=np.where(~row.mask)
	#print idx,row[idx]
	#print i,'active dbz values',len(idx)
	#print i,len(idx[0])

# map to grid
grd = gm.grid_from_radars( (radar, ),(10, 10, 10),  ((0,400), (-400,400), (-400,400)))
print grd

