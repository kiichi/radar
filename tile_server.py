from distutils.dir_util import mkpath
from globalmaptiles import *
import os
import matplotlib
matplotlib.rcParams['figure.figsize'] = [3.57,3.57]
import matplotlib.pyplot as plt
import numpy as np
import pyart
import urllib
from flask import Flask, request, send_file
from flask import jsonify

app = Flask(__name__,static_url_path='')

mercator = GlobalMercator()
radar = None

@app.route('/')
def index():
    return 'Index Page'

@app.route('/tile/')
def send_tile():
    # test
    zoomlevel = 8
    lat = 40.742995
    lon = -73.993475

    tz = zoomlevel
    mx, my = mercator.LatLonToMeters( lat, lon )
    tx, ty = mercator.MetersToTile( mx, my, tz )
    bounds = mercator.TileBounds( tx, ty, tz)

    mkpath("cache/%s/%s" % (tz, tx))
    tilefilename = "cache/%s/%s/%s.png" % (tz, tx, ty)
    print tilefilename
    if os.path.isfile(tilefilename):
        return send_file(tilefilename, mimetype='image/png')

    bounds = mercator.TileLatLonBounds(tx, ty, tz)
    print bounds[0],bounds[1],bounds[2],bounds[3],

    display = pyart.graph.RadarMapDisplay(radar)
    display.plot_ppi_map( 'reflectivity', vmin=-32, vmax=80, cmap='pyart_NWSRef',
        min_lat=bounds[0],min_lon=bounds[1],  max_lat=bounds[2], max_lon=bounds[3],
        lat_0=lat,lon_0=lon,
        resolution='c',title_flag=False,colorbar_flag=False, embelish=False,
        )
    fig=plt.figure(1)
    fig.canvas.draw()

    fig.savefig(tilefilename, dpi=72, transparent=True)
    return send_file(tilefilename, mimetype='image/png')

@app.route('/get_tiles/')
def get_tiles():
    zoomlevel = 8
    minlat = 38.12345
    minlon = -75.12345
    maxlat = 42.742995
    maxlon = -71.993475

    tz = zoomlevel
    mx, my = mercator.LatLonToMeters(minlat,minlon)
    tminx, tminy = mercator.MetersToTile(mx,my,tz)
    mx, my = mercator.LatLonToMeters(maxlat,maxlon)
    tmaxx, tmaxy = mercator.MetersToTile(mx,my,tz)

    arr = []
    for ty in range(tminy, tmaxy+1):
        for tx in range(tminx, tmaxx+1):
            arr.append( (tx,ty) )
    print arr
    return jsonify(status='ok',tiles=arr)


if __name__ == '__main__':
    radar = pyart.io.read_nexrad_level3('sample_data_rad3/KOKX_SDUS21_N1QOKX_201510031824')
    print 'Radar data has been loaded: ', radar.latitude['data'][0],radar.longitude['data'][0]
    app.run(debug=True)
