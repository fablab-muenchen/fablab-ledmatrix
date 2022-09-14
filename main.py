from time import pthread_getcpuclockid
from providers import Provider,ScreenProvider,TextProvider
from matrix import Matrix


m = Matrix()
providers = [
    TextProvider(m,"test"),
    ScreenProvider(m),
    Provider(m)
    ]
while True:
    for p in providers:
        p.displayContent(5)