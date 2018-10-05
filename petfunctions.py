import requests
from secret import SECRET_KEY

def get_random_pet():
        
        resp = requests.get("http://api.petfinder.com/pet.getRandom",
        params={"key":SECRET_KEY,"format":"json","output":"basic"})

        random_pet = resp.json()

        pet_name = random_pet['petfinder']['pet']['name']['$t']
        pet_age = random_pet['petfinder']['pet']['age']['$t']
        pet_url = random_pet['petfinder']['pet']['media']['photos']['photo'][1]['$t']

        pet_list = [pet_name,pet_age,pet_url]

    return pet_list