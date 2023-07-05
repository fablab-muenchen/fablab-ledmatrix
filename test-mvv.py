#!/usr/bin/env python3

from providers import MVVProvider, Matrix

m = Matrix()
mvv = MVVProvider(
        matrix=m,
        station='de:09162:1150', 
        title="Heimeranplatz", 
        station_filter=lambda x: x['departureTimeMinutes'] >= 5 and 
                    ( x['type'] == "U-Bahn" or x['type'] == "S-Bahn" )
        )
mvv.saveTestImage()





