
doors = ["A", "B", "C"]

winning_door = "A"
winning_door

chosen_door = input("Choose a door from 'A', 'B', or 'C': ").upper()
# in: A
chosen_door

wrong_door = "B"
wrong_door

print(f"Door '{wrong_door}' is not the winning door")
switch_choice = input("Would you like to switch your choice [y/n]").lower()
# in: n
switch_choice

if switch_choice == "y":
	chosen_door, = [d for d in doors if d not in [wrong_door, chosen_door]]
chosen_door

if chosen_door == winning_door:
	print("Congrats, you won!", end="")
else:
	print("Too bad! better luck next time!", end="")
