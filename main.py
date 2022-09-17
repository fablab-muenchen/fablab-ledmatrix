from providers import MVVProvider, ClockProvider
from providers.matrix import Matrix


m = Matrix()
providers = [
    #TextProvider(m,"test"),
    #ScreenProvider(m),
    #Provider(m),
    ClockProvider(m),
    MVVProvider(
        matrix=m,
        station='de:09162:8',
        title="ABFAHRTEN Donnersb.Brücke",
        station_filter=lambda x: x['departureTimeMinutes'] >= 5 and x['label'].startswith("S")
        ),
    MVVProvider(
        matrix=m, 
        station='de:09162:1150', 
        title="ABFAHRTEN Heimeranplatz", 
        station_filter=lambda x: x['departureTimeMinutes'] >= 5 and 
                    ( x['product'] == "UBAHN" or x['product'] == "SBAHN" )
        ),
    MVVProvider(
        matrix=m, 
        station='de:09162:102', 
        title="ABFAHRTEN Gollierplatz", 
        station_filter=lambda x: x['departureTimeMinutes'] >= 1
        ),
    MVVProvider(
        matrix=m, 
        station='de:09162:65', 
        title="ABFAHRTEN Trappentreustr", 
        station_filter=lambda x: x['departureTimeMinutes'] >= 1
        ),
    ]
while True:
    for p in providers:
        p.displayContent(10)