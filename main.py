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
        title="Donnersb.Brücke",
        station_filter=lambda x: x['departureTimeMinutes'] >= 5 and x['type'] == "S-Bahn"
        ),
    MVVProvider(
        matrix=m, 
        station='de:09162:1150', 
        title="Heimeranplatz", 
        station_filter=lambda x: x['departureTimeMinutes'] >= 5 and 
                    ( x['type'] == "U-Bahn" or x['type'] == "S-Bahn" )
        ),
    MVVProvider(
        matrix=m, 
        station='de:09162:102', 
        title="Gollierplatz", 
        station_filter=lambda x: x['departureTimeMinutes'] >= 1
        ),
    MVVProvider(
        matrix=m, 
        station='de:09162:65', 
        title="Trappentreustr", 
        station_filter=lambda x: x['departureTimeMinutes'] >= 1
        ),
    ]
while True:
    for p in providers:
        p.displayContent(10)