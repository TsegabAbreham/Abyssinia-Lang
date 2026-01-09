import requests


def fetchpokemon(pokemon):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"
    return url



pokemon = input("Enter your pokemon please: ")
response = requests.get(fetchpokemon(pokemon))
print(response)