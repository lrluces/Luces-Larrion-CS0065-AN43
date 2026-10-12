import random

def get_room_state(room_name):
    """Ask the user for a valid initial room state."""
    while True:
        state = input(
            f"Enter the initial state of Room {room_name} "
            "(Dirty/Clean): "
        ).strip().capitalize()

        if state in ["Dirty", "Clean"]:
            return state

        print("Invalid input. Please enter Dirty or Clean.")


def is_dirty(environment, room):
    """Return True when the selected room is dirty."""
    return environment[room] == "Dirty"


def clean_room(environment, room):
    """Change a dirty room's state to clean."""
    environment[room] = "Clean"


def display_grid(environment, agent_location):
    """Display the rooms and the agent's current location."""
    room_display = []

    for room, state in environment.items():
        if room == agent_location:
            room_display.append(f"[{room}: {state} | AGENT]")
        else:
            room_display.append(f"[{room}: {state}]")

    print(" -- ".join(room_display))

class RuleBasedVacuumAgent:

    def __init__(self, starting_location="A"):
        self.location = starting_location

    def perceive_and_act(self, environment):
        """
        Perceive the current room and select an action.

        Rule 1: Clean the current room if it is dirty.
        Rule 2: If the current room is clean, randomly select
                another dirty room.
        Rule 3: Stop if every room is already clean.
        """

        if is_dirty(environment, self.location):
            clean_room(environment, self.location)
            return f"Cleaned Room {self.location}"

        dirty_rooms = [
            room
            for room, state in environment.items()
            if state == "Dirty" and room != self.location
        ]

        if dirty_rooms:
            target_room = random.choice(dirty_rooms)
            old_location = self.location
            self.move(target_room)

            return (
                f"Moved from Room {old_location} "
                f"to dirty Room {target_room}"
            )

        return "No action—all rooms are clean"

    def move(self, target_room):
        """Move the agent to the selected room."""
        self.location = target_room


print("RULE-BASED VACUUM CLEANER AGENT")
print("Bonus version with Rooms A, B, and C")
print()

environment = {
    "A": get_room_state("A"),
    "B": get_room_state("B"),
    "C": get_room_state("C")
}

while True:
    starting_location = input(
        "Enter the agent's starting room (A/B/C): "
    ).strip().upper()

    if starting_location in environment:
        break

    print("Invalid room. Please enter A, B, or C.")

while True:
    try:
        number_of_steps = int(
            input("Enter the number of simulation steps: ")
        )

        if number_of_steps > 0:
            break

        print("The number of steps must be greater than zero.")

    except ValueError:
        print("Please enter a valid whole number.")

agent = RuleBasedVacuumAgent(starting_location)

print("\n=== INITIAL ENVIRONMENT ===")
display_grid(environment, agent.location)

for step in range(1, number_of_steps + 1):
    print(f"\n=== STEP {step} ===")

    print(f"Perception: Room {agent.location} is "
          f"{environment[agent.location]}")

    action = agent.perceive_and_act(environment)

    print(f"Action: {action}")
    print(f"Current location: Room {agent.location}")
    print("Current environment:")
    display_grid(environment, agent.location)

    if all(state == "Clean" for state in environment.values()):
        print("\nAll rooms are clean. The simulation is complete.")
        break

else:
    print("\nThe requested number of steps has been completed.")

print("\n=== FINAL RESULT ===")
print(f"Agent's final location: Room {agent.location}")
display_grid(environment, agent.location)