from Router import Router

Routers = [None]*20

for i in range(len(Routers)):
    Routers[i] = Router(f"Router{i}")


for Router in Routers:
    print(Router.name)