from db import *


def get_data():
    # grandma = Person.select().where(Person.name == 'Grandma L.').get()
    # grandma = Person.get(Person.name == 'Grandma')
    # print(grandma.name)
    # print(grandma.birthday)
    # print(grandma.id)

    for person in Person.select():
        print(person, person.name)

    query = Pet.select().where(Pet.animal_type == 'cat')
    for pet in query:
        print(pet.name, pet.owner.name)


if __name__ == '__main__':
    get_data()
