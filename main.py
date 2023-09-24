# Note about the PokeAPI:
# - PokeAPI does not require an API key
# - If an api key is required, usually you will have to register for an account and then they will provide you with an API key and then follow the documentation in order to see how you can add the apikey to the url and see how it connects..

# The random module is already built-in python so it requires to use of command terminal to install it.
import random

# Install this module using the command terminal and type: python -m pip install requests (https://pypi.org/project/requests/)
# The requests module allows us to send http requests.
import requests

BASE_URL = "https://pokeapi.co/api/v2/"
caughtPokemon = [] # store list of pokemons caught
pokemon_data = ""

#Prints an amazing ASCII Art title at the beginning of the program
def printHeader():
    return r"""
__________       __
\______   \____ |  | __ ____   _____   ____   ____
 |     ___/  _ \|  |/ // __ \ /     \ /  _ \ /    \
 |    |  (  <_> )    <\  ___/|  Y Y  (  <_> )   |  \
 |____|   \____/|__|_ \\___  >__|_|  /\____/|___|  /
                     \/    \/      \/            \/

    """


# Function to fetch data from the PokeAPI
def fetch_pokemon_data(pokemonName):
    response = requests.get(f"{BASE_URL}/pokemon/{pokemonName.lower()}/")
    # check if client successfully connects to api and response status code is 200
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to fetch data from the PokeAPI.")
        return None


def getRandomPokemon():
    # Generate a random Pokémon ID between 1 and 898
    pokemonID = random.randint(1, 898)
    url = f"{BASE_URL}pokemon/{pokemonID}/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def outputToTextFile():
    detailedPokemonData = []  # Create a list to store detailed data for each Pokémon

    for pokemon_name in caughtPokemon:

        pokemonData = fetch_pokemon_data(pokemon_name)
        if pokemonData:
            detailedPokemonData.append(pokemonData)

    if detailedPokemonData:
        # Write to file
        with open('my_pokemon_details.txt', 'w') as file:
            file.write("--- My Pokémons ---\n")
            for i, pokemonData in enumerate(detailedPokemonData, start=1):
                file.write(f"Unique User ID: {pokemonData['name'].upper()[:3]}{pokemonData['id']}\n")
                file.write(f"{i}. {pokemonData['name'].capitalize()} (ID: {pokemonData['id']})\n")
                # Types Information
                file.write("Types:\n")
                for pokemon_type in pokemonData['types']:
                    file.write(f"- {pokemon_type['type']['name'].capitalize()}\n")
                # Height and Width Information
                file.write(f"Height: {pokemonData['height']} decimetres\n")
                file.write(f"Weight: {pokemonData['weight']} hectograms\n")
                file.write("Abilities:\n")
                # Abilities Information

                for ability in pokemonData['abilities']:
                    file.write(f"- {ability['ability']['name'].capitalize()} (Hidden: {ability['is_hidden']})\n")
                file.write("-------------------\n\n")
        print("\nData written to 'my_pokemon_details.txt'.\n")
    else:
        print("\nNo Pokémon data to write.\n")


def main():
    # Print the header
    print(printHeader())

    while True:
        # Displays the menu options
        menuOptions()

        choice = input("Enter your choice (1/2/3/4): ")

        if choice == "1":
            pokemonData = getRandomPokemon()
            # if pokemon data is there, ask if u want to catch it or not
            if pokemonData:
                print(f"\nYou found a: {pokemonData['name'].capitalize()}!!!")

                printPokemonTypes(pokemonData)

                while True:
                    catch_choice = input("\n\nWould you like to catch it? (Y/N): ").upper()
                    if catch_choice == "Y":
                        catchPokemonAndAddToInventory(pokemonData)
                        break
                    elif catch_choice == "N":
                        print(f"\n{pokemonData['name'].capitalize()} ran away! ;__;\n")
                        break
                    else:
                        print("Invalid choice. Please enter 'Y' or 'N'.")
            else:
                print("Failed to fetch Pokémon data.")

        elif choice == "2":
            if caughtPokemon:
                print(f"\nPokemon Caught: {len(caughtPokemon)}\n{caughtPokemon}\n")
            else:
                print("\nNo Pokemons Caught.\n")

        elif choice == "3":
            outputToTextFile()


        elif choice == "4":
            print("\nExiting...\n")
            return False

        else:
            print("\nInvalid choice. Please select a valid option.\n")


def catchPokemonAndAddToInventory(pokemonData):
    caughtPokemon.append(pokemonData['name'].capitalize())
    print(f"\n{pokemonData['name'].capitalize()} has been caught!")
    print(f"{pokemonData['name'].capitalize()} added to my collection!\n")


def printPokemonTypes(pokemonData):
    print("Types:", end=" ")
    for pokemonType in pokemonData['types']:
        print(f"{pokemonType['type']['name'].capitalize()}", end=" ")


def menuOptions():
    print("1. Catch a Pokemon")
    print("2. See Pokemons Caught")
    print("3. Output To Text File")
    print("4. Exit")


if __name__ == "__main__":
    main()
