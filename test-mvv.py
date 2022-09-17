#!/usr/bin/env python3

from providers import MVVProvider, Matrix


m = Matrix()
mvv = MVVProvider(
        matrix=m,
        station='de:09162:8',
        title="ABFAHRTEN Donnersb.Brücke",
        station_filter=lambda x: x['departureTimeMinutes'] >= 5 and x['label'].startswith("S")
        )
mvv.saveTestImage()





