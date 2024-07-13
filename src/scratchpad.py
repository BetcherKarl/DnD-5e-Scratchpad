from utils.die_roller import Die_Roller
from utils.die import Die


roller = Die_Roller()

def roll_test(command:str, iterations:int):
    global roller
    results = []
    for _ in range(iterations):
        results.append(roller.roll(command))

    results.sort()
    return results

print(roller.roll('1d4 * 1d8'))

results = roll_test('1d8 / 1d4', 100)

print(f"{results[0]}\n{results[-1]}")