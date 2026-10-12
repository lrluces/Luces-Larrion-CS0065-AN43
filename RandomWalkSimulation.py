import agentpy as ap
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from IPython.display import HTML, display

# -------- Get user input --------

num_agents = int(input("Enter number of agents: "))
grid_size = int(input("Enter grid size (e.g., 10 for 10x10): "))
num_steps = int(input("Enter number of steps: "))

if num_agents <= 0 or grid_size <= 0 or num_steps <= 0:
    raise ValueError("All inputs must be positive integers.")

if num_agents > grid_size ** 2:
    raise ValueError(
        "The number of agents cannot exceed the number of grid cells "
        "when collision avoidance is enabled."
    )


# -------- Agent Definition --------

class RandomWalker(ap.Agent):

    def setup(self):
        self.path = []

    def step(self):
        # Preferred movement toward the upper-right
        moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        weights = [0.4, 0.1, 0.4, 0.1]
        direction = random.choices(moves, weights=weights, k=1)[0]

        x, y = self.model.grid.positions[self]

        new_x = max(
            0,
            min(self.model.p.grid_size[0] - 1, x + direction[0])
        )
        new_y = max(
            0,
            min(self.model.p.grid_size[1] - 1, y + direction[1])
        )

        new_position = (new_x, new_y)

        # Collision avoidance
        occupied_positions = {
            self.model.grid.positions[agent]
            for agent in self.model.agents
            if agent != self
        }

        if new_position not in occupied_positions:
            self.model.grid.move_to(self, new_position)

        self.path.append(self.model.grid.positions[self])


# -------- Model Definition --------

class RandomWalkModel(ap.Model):

    def setup(self):
        self.grid = ap.Grid(
            self,
            self.p.grid_size,
            torus=False,
            track_empty=True
        )

        self.agents = ap.AgentList(
            self,
            self.p.agents,
            RandomWalker
        )

        # Assign unique random starting positions
        self.grid.add_agents(
            self.agents,
            random=True,
            empty=True
        )

        for agent in self.agents:
            agent.path.append(self.grid.positions[agent])

    def step(self):
        # Random order reduces first-agent advantage
        agents_in_random_order = list(self.agents)
        random.shuffle(agents_in_random_order)

        for agent in agents_in_random_order:
            agent.step()


# -------- Parameters --------

parameters = {
    "agents": num_agents,
    "grid_size": (grid_size, grid_size),
    "steps": num_steps
}


# -------- Run Simulation --------

model = RandomWalkModel(parameters)

if not hasattr(model, "agents"):
    model.setup()

for _ in range(num_steps):
    model.step()


# -------- Create Animation from Recorded Paths --------

fig, ax = plt.subplots(figsize=(7, 7))

ax.set_xlim(-0.5, grid_size - 0.5)
ax.set_ylim(-0.5, grid_size - 0.5)
ax.set_xticks(range(grid_size))
ax.set_yticks(range(grid_size))
ax.set_title("Random Walk with Preferred Direction and Collision Avoidance")
ax.set_xlabel("X position")
ax.set_ylabel("Y position")
ax.grid(True)

colors = plt.cm.tab20(np.linspace(0, 1, num_agents))

initial_positions = np.array([
    agent.path[0]
    for agent in model.agents
])

scat = ax.scatter(
    initial_positions[:, 0],
    initial_positions[:, 1],
    s=150,
    c=colors,
    edgecolors="black",
    zorder=5
)


def update(frame):
    current_positions = [
        agent.path[frame]
        for agent in model.agents
    ]

    scat.set_offsets(np.array(current_positions))

    for i, agent in enumerate(model.agents):
        visible_path = agent.path[:frame + 1]
        path_x = [position[0] for position in visible_path]
        path_y = [position[1] for position in visible_path]
        lines[i].set_data(path_x, path_y)

    ax.set_title(
        f"Random Walk Simulation — Step {frame}/{num_steps}"
    )

    return [scat] + lines


ani = animation.FuncAnimation(
    fig,
    update,
    frames=range(num_steps + 1),
    interval=400,
    blit=False,
    repeat=False
)

display(HTML(ani.to_jshtml()))
plt.close(fig)


print("\n=== FINAL POSITION ANALYSIS ===")

final_positions = [
    model.grid.positions[agent]
    for agent in model.agents
]

for i, position in enumerate(final_positions, start=1):
    print(f"Agent {i} finished at: {position}")

x_coords = [position[0] for position in final_positions]
y_coords = [position[1] for position in final_positions]

print("\n--- Distribution Summary ---")
print(f"Average X position: {np.mean(x_coords):.2f}")
print(f"Average Y position: {np.mean(y_coords):.2f}")
print(f"Unique occupied cells: {len(set(final_positions))}")
print(f"Maximum coordinate: {grid_size - 1}")