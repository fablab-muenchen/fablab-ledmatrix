from providers import MVVProvider, ClockProvider
from providers.matrix import Matrix

m = Matrix()
providers = [
    # TextProvider(m,"test"),
    # ScreenProvider(m),
    # Provider(m),
    ClockProvider(m),
    MVVProvider(
        matrix=m,
        station='de:09162:8',
        title="Donnersb.Brücke",
        offset=5,
        transport_types=["SBAHN"],
    ),
    MVVProvider(
        matrix=m,
        station='de:09162:1150',
        title="Heimeranplatz",
        offset=5,
        transport_types=["UBAHN", "SBAHN"],
    ),
    MVVProvider(
        matrix=m,
        station='de:09162:102',
        title="Gollierplatz",
        offset=1,
    ),
    MVVProvider(
        matrix=m,
        station='de:09162:65',
        title="Trappentreustr",
        offset=1,
    ),
]
while True:
    for p in providers:
        p.displayContent(10)
