import os
import matplotlib
matplotlib.rcParams['figure.figsize'] = [12.0, 9.0]
import matplotlib.pyplot as plt
import numpy as np
import pyart
import urllib

folder = 'sample_data_rad3'

for filename in os.listdir(folder):
	print filename
	plt.clf()
	#radar = pyart.io.read('sample_data/'+filename)
	radar = pyart.io.read_nexrad_level3(folder+'/'+filename)
	display = pyart.graph.RadarMapDisplay(radar)
	display.plot_ppi_map( 'reflectivity', vmin=-32, vmax=80, cmap='pyart_NWSRef', resolution='c', embelish=False)
	display.basemap.drawcounties()
	p=display.basemap.plot([-97.75], [30.25], 'k*', ms=15, latlon=True)
	figprops = dict(figsize=(8,6), dpi=100, facecolor='white')
	fig = plt.figure(1,**figprops)
	fig.canvas.draw()
	fig.savefig('output/'+filename+'.png', dpi=72)
