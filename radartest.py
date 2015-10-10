#~/anaconda/bin/python radar.py
#https://github.com/jjhelmus/scipy2015_talk/blob/master/SciPy2015_OpenAccessRadar_jjh.ipynb
#https://github.com/matplotlib/basemap/blob/master/examples/save_background.py
import matplotlib
matplotlib.rcParams['figure.figsize'] = [12.0, 9.0]
import matplotlib.pyplot as plt
import numpy as np
import pyart
handle=open('sn.last')
radar = pyart.io.read_nexrad_level3(handle)
display = pyart.graph.RadarMapDisplay(radar)
display.plot_ppi_map( 'reflectivity', vmin=-32, vmax=80, cmap='pyart_NWSRef', resolution='c', embelish=False)
display.basemap.drawcounties()
p=display.basemap.plot([-97.75], [30.25], 'k*', ms=15, latlon=True)
figprops = dict(figsize=(8,6), dpi=100, facecolor='white')
fig = plt.figure(1,**figprops)
fig.canvas.draw()
fig.savefig('sn.last.png', dpi=100)

'''
map = Basemap(projection='moll',lon_0=0)
map.drawcoastlines()
map.drawmapboundary(fill_color='aqua')
map.fillcontinents(color='coral',lake_color='aqua')
fig.canvas.draw()
'''
