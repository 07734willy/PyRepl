
doors = ["A", "B", "C"]

winning_door = "A"
winning_door
# out: 'A'

chosen_door = input("Choose a door from 'A', 'B', or 'C': ").upper()
# in: A
# out: Choose a door from 'A', 'B', or 'C': A
chosen_door
# out: 'A'

wrong_door = "B"
wrong_door
# out: 'B'

print(f"Door '{wrong_door}' is not the winning door")
# out: Door 'B' is not the winning door
switch_choice = input("Would you like to switch your choice [y/n]").lower()
# in: n
# out: Would you like to switch your choice [y/n]n
switch_choice
# out: 'n'

if switch_choice == "y":
	chosen_door, = [d for d in doors if d not in [wrong_door, chosen_door]]
chosen_door
# out: 'A'

if chosen_door == winning_door:
	print("Congrats, you won!", end="")
else:
	print("Too bad! better luck next time!", end="")
# out: Congrats, you won!
# info: missing trailing newline
