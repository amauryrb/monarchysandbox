# Monarchy Sandbox Simulation

This project is a political sandbox simulation designed to explore the dynamics between church influence, state power, and population groups in an aspirational monarchy setting. The simulation models three population groups: Monarchists, Liberals, and the Undecided, and examines how various factors affect their interactions over time.

## Project Structure

- **src/**: Contains the main simulation code.
  - **simulation.py**: The main entry point for the simulation, initializing parameters and running the simulation loop.
  - **models/**: Contains the core logic for the simulation dynamics.
    - **dynamics.py**: Defines functions and classes that model interactions between population groups, church influence, state power, and resources.
  - **utils/**: Contains utility functions for the project.
    - **plotting.py**: Includes functions for generating plots and visualizations of simulation results.
  - **__init__.py**: Marks the `src` directory as a Python package.

- **notebooks/**: Contains Jupyter notebooks for interactive exploration of the simulation.
  - **sandbox_exploration.ipynb**: Used for running the simulation and visualizing results.

- **data/**: Contains data-related documentation.
  - **README.md**: Provides information about the datasets used in the project.

- **tests/**: Contains unit tests for the simulation logic.
  - **test_simulation.py**: Ensures that the functions and classes in `simulation.py` and `dynamics.py` work as expected.

- **requirements.txt**: Lists the Python packages required for the project.

- **environment.yml**: Used to create a conda environment for the project.

- **.gitignore**: Specifies files and directories to be ignored by Git.

## Installation

To set up the project, clone the repository and install the required dependencies:

```bash
# Clone the repository
git clone <repository-url>
cd monarchy-sandbox

# Install dependencies
pip install -r requirements.txt
```

Alternatively, you can create a conda environment using the `environment.yml` file:

```bash
conda env create -f environment.yml
conda activate <environment-name>
```

## Usage

To run the simulation, execute the `simulation.py` file:

```bash
python src/simulation.py
```

You can also explore different scenarios and visualize results using the Jupyter notebook located in the `notebooks` directory.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.