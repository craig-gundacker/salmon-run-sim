
# Project Name

Salmon Run Simulation

## Description

Salmon run simulation (very, very roughly) models a salmon run that might take place off the coast of southeast Alaska or a similar locale.  There are three entities involved in the model: salmon, fishing boats, and bears.  The program runs until all the salmon have either spawned or been caught (by human or bear).  The size of the population is monitored at set intervals, and if it drops below a certain threshold, a salmon boat is removed from the harvest—much like a fisheries department might do in the real world.  Additionally, disease pressure reduces the salmon population during the run.  On each iteration, fishing boats and bears have a probabilistic chance of catching a salmon.  If the boat fails to locate enough salmon, it risks going bankrupt.  Similarly, bears can potentially starve if they go long enough without a meal.  However, bears that are good hunters, increase their chances of successfully breeding.  If the number of spawning salmon meets or exceeds a target rate, then the run is considered “sustainable”.

This program is loosely based on a simulation written by the authors of [Python Programming in Context, 2nd edition](https://www.amazon.com/Python-Programming-Context-Bradley-Miller/dp/1449699391).

## Prerequisites

- Python 3.x installed on your machine.

## Installation

1. **Navigate to the project directory:**

   Open Git CMD or your terminal and navigate to the directory where you want to clone the repository:

   ```bash
   cd repository
   ```

2. **Clone the repository:**

   Then run:

   ```bash
   git clone https://github.com/craig-gundacker/salmon-run-sim
   ```

## Running the Application

To run the simulation, execute the main Python file using:

```bash
python SimApp.py
```

This command will start the simulation and output the results to your terminal.

## Usage

The application initializes a coast with a specified width and height, then populates it with a set number of salmon, boats, and bears. It then runs a simulation where these entities interact based on predefined rules.

## Additional Information

- **Configuration:** You can adjust parameters like the number of salmon, boats, and bears by modifying the respective variables in `SimApp.py`.

- **Dependencies:** Ensure that all dependencies —`Coast`, `Salmon`, `Bear`, `Boat`—are correctly implemented and accessible within your project directory.
