from globalmaptiles import *
zoomlevel = 8
lat = 40.742995
lon = -73.993475

#---------------------------------------------
mercator = GlobalMercator()

tz = zoomlevel
mx, my = mercator.LatLonToMeters( lat, lon )
tx, ty = mercator.MetersToTile( mx, my, tz )
bounds = mercator.TileBounds( tx, ty, tz)
tilefilename = "%s/%s/%s" % (tz, tx, ty)
print tilefilename
bounds = mercator.TileLatLonBounds(tx, ty, tz)
print bounds
