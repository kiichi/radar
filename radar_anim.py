import os
import matplotlib
matplotlib.rcParams['figure.figsize'] = [12.0, 9.0]
import matplotlib.pyplot as plt
import numpy as np
import pyart
import urllib

#folder = 'sample_data'
folder = 'sample_data_rad3'

for filename in os.listdir(folder):
	if filename == '.DS_Store':
		continue
	print folder+'/'+filename
	plt.clf()
	radar = pyart.io.read_nexrad_level3(folder+'/'+filename)
	#radar = pyart.io.read(folder+'/'+filename)
	display = pyart.graph.RadarMapDisplay(radar)
	display.plot_ppi_map( 'reflectivity', vmin=-32, vmax=80, cmap='pyart_NWSRef', 
		#min_lon=-157.1, max_lon=-156, min_lat=71.2, max_lat=71.6,
		#lat_0=?,lng_0=?,
		resolution='c',title_flag=False,colorbar_flag=False, embelish=False,
		)
	#display.plot_ppi_map( 'reflectivity',  cmap='pyart_NWSRef', resolution='c', embelish=False)
	#display.basemap.drawcounties()
	#p=display.basemap.plot([-97.75], [30.25], 'k*', ms=15, latlon=True)
	#figprops = dict(figsize=(18,6), dpi=72, facecolor='blue')
	#fig = plt.figure(1,**figprops)
	fig=plt.figure(1)
	fig.canvas.draw()
	fig.savefig('output/'+filename+'.png', dpi=72, transparent=True)
