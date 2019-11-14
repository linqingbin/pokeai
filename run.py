import re
from pokeai import PokeDoctor


def main():
    doctor = PokeDoctor()
    running = True
    while running:
        userInput = input("Input your exists pokemon types(split by comma): ")
        existsTypes = re.split(r"\s*[,，、]\s*", userInput)
        data = doctor.getReport(existsTypes)
        print("Goodness types: ", ", ".join(data["goodness"]))
        print("Weakness types: ", ", ".join(data["weakness"]))
        print("Recommend next types: ", ", ".join(data["next"]))


if __name__ == "__main__":
    main()
