import re
from pokeai import PokeDoctor

def main():
    doctor = PokeDoctor()
    running = True
    while running:
        userInput = input("Input your exists pokemon types(split by comma): ")
        existsTypes = re.split("\s*,|，\s*",userInput)
        data = doctor.getReport(existsTypes)
        print(data)

if __name__ == "__main__":
    main()
