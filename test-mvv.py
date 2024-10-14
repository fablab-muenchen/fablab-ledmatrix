#!/usr/bin/env python3

from providers import MVVProvider, Matrix
from providers.mvv_provider import MvvgApi

m = Matrix()
mvv = MVVProvider(
    matrix=m,
    station='de:09162:1150',
    title="Heimeranplatz",
    offset=5,
    transport_types=["UBAHN", "SBAHN"],
)
mvv.saveTestImage()
