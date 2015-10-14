from distutils.dir_util import mkpath
from globalmaptiles import *
import os
import matplotlib

import matplotlib.pyplot as plt
import numpy as np
import pyart
import urllib
from flask import Flask, request, send_file
from flask import jsonify


matplotlib.rcParams['figure.figsize'] = [3.57,3.57]

app = Flask(__name__,static_url_path='')

mercator = GlobalMercator()
radar = None

@app.route('/')
def index():
    return 'Index Page'

#http://localhost:5000/tile/8/75/159.png
@app.route('/tile/<z>/<x>/<y>.png')
def send_tile(z,x,y):
    # test
    # zoomlevel = 8
    # lat = 40.742995
    # lon = -73.993475

    #tz = zoomlevel
    #mx, my = mercator.LatLonToMeters( lat, lon )
    #tx, ty = mercator.MetersToTile( mx, my, tz )

    tz = int(z)
    tx = int(x)
    ty = int(y)


    #bounds = mercator.TileBounds( tx, ty, tz)


    mkpath("cache/%s/%s" % (tz, tx))
    tilefilename = "cache/%s/%s/%s.png" % (tz, tx, ty)
    if os.path.isfile(tilefilename):
        print tilefilename
        return send_file(tilefilename, mimetype='image/png')

    #mx, my = mercator.LatLonToMeters( lat, lon )
    #tx, ty = mercator.MetersToTile( mx, my, tz )
    bounds = mercator.TileLatLonBounds(tx, ty, tz)

    tile_info = "%s: %s"%(tilefilename,bounds)
    print tile_info
    #print tilefilename, bounds[0],bounds[1],bounds[2],bounds[3]
    plt.clf()
    display = pyart.graph.RadarMapDisplay(radar)
    display.plot_ppi_map( 'reflectivity',0, vmin=-32, vmax=80, cmap='pyart_NWSRef',
        min_lat=bounds[0],min_lon=bounds[1],  max_lat=bounds[2], max_lon=bounds[3],
        #lat_0=(bounds[0]+bounds[2])/2.0,lon_0=(bounds[1]+bounds[3])/2.0,
        #title_flag=True,title = tilefilename,
        title_flag=False,
        mask_outside=True,
        #projection="lcc",
        resolution='c',colorbar_flag=False, embelish=False,
        )
    #fig=plt.figure(1)
    #fig.canvas.draw()
    #fig.savefig(tilefilename, dpi=72, transparent=True)

    plt.savefig(tilefilename, dpi=72, transparent=True,pad_inches=0)
    return send_file(tilefilename, mimetype='image/png')

# DEUBUG
#http://localhost:5000/get_tile_list/8/38.12345/-75.12345/42.742995/-71.993475
@app.route('/get_tile_list/<zoom>/<minlat>/<minlon>/<maxlat>/<maxlon>')
def get_tile_list(zoom,minlat,minlon,maxlat,maxlon):
    # zoomlevel = 8
    # minlat = 38.12345
    # minlon = -75.12345
    # maxlat = 42.742995
    # maxlon = -71.993475

    tz = int(zoom)
    minlat = float(minlat)
    minlon = float(minlon)
    maxlat = float(maxlat)
    maxlon = float(maxlon)

    mx, my = mercator.LatLonToMeters(minlat,minlon)
    tminx, tminy = mercator.MetersToTile(mx,my,tz)
    mx, my = mercator.LatLonToMeters(maxlat,maxlon)
    tmaxx, tmaxy = mercator.MetersToTile(mx,my,tz)

    arr = []
    for ty in range(tminy, tmaxy+1):
        for tx in range(tminx, tmaxx+1):
            arr.append( {"x":tx,"y":ty} )
    print arr
    return jsonify(status='ok',tiles=arr)

# DEUBUG
#http://localhost:5000/get_tile_info/8/40.8217465/-73.588846
@app.route('/get_tile_info/<zoom>/<lat>/<lon>')
def get_tile_info(zoom,lat,lon):
    tz = int(zoom)
    lat = float(lat)
    lon = float(lon)
    mx, my = mercator.LatLonToMeters( lat, lon )
    tx, ty = mercator.MetersToTile( mx, my, tz )
    bounds = mercator.TileLatLonBounds(tx, ty, tz)
    #cache/8/75/159.png 39.9097362345 -74.53125 40.9798980696 -73.125
    #40.9798980696 -74.53125 42.0329743324 -73.125 cache/8/75/159.png
    #(39.90973623453719, -74.53125, 40.979898069620155, -73.12499999999999)
    #39.9097362345 -74.53125 40.9798980696 -73.125

    print bounds
    print bounds[0],bounds[1],bounds[2],bounds[3],

    return jsonify(status='ok',tiles={"x":tx,"y":ty,"z":tz})

# DEUBUG
#http://localhost:5000/sample
@app.route('/sample')
def sample_tile():
    #cache/8/75/159.png 39.9097362345 -74.53125 40.9798980696 -73.125
    #bounds = mercator.TileLatLonBounds(75, 158, 8)
    #print bounds[0],bounds[1],  bounds[2], bounds[3]
    #print "min_lat=39.9097362345,min_lon=-74.53125,  max_lat=40.9798980696, max_lon=-73.125"
    plt.clf()
    matplotlib.rcParams['figure.figsize'] = [12,12]
    tilefilename = "cache/sample.png"
    display = pyart.graph.RadarMapDisplay(radar)
    display.plot_ppi_map( 'reflectivity', vmin=-32, vmax=80, cmap='pyart_NWSRef',
        title_flag=False,#title = tilefilename,
        mask_outside=True,
        min_lat=39.9097362345,min_lon=-74.53125,  max_lat=40.9798980696, max_lon=-73.125,
        #min_lat=bounds[0],min_lon=bounds[1],  max_lat=bounds[2], max_lon=bounds[3],
        #projection="merc",
        resolution='c',colorbar_flag=False, embelish=False,
        )

    #display.basemap.drawcounties()

    # fig=plt.figure(1)
    # fig.canvas.draw()
    # fig.savefig(tilefilename, dpi=72, transparent=True)
    #fig = plt.figure(figsize=[3.57,3.57])
    #fig.canvas.draw()

    plt.savefig(tilefilename, dpi=72, transparent=True,pad_inches=0,bbox_inches=0)
    return send_file(tilefilename, mimetype='image/png')

if __name__ == '__main__':
    radar = pyart.io.read_nexrad_level3('sample_data_rad3/KOKX_SDUS21_N1QOKX_201510031824')
    print 'Radar data has been loaded: ', radar.latitude['data'][0],radar.longitude['data'][0]
    app.run(debug=True)
