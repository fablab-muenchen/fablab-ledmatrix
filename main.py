from providers import Provider,ScreenProvider,TextProvider
from providermvv import ProviderMVV
from matrix import Matrix


m = Matrix()
providers = [
    #TextProvider(m,"test"),
    #ScreenProvider(m),
    #Provider(m),
    ProviderMVV(m)
    ]
while True:
    for p in providers:
        p.displayContent(5)