import unittest
from src.simulation import run_simulation  # Adjust the import based on the actual function name
from src.models.dynamics import Dynamics  # Adjust the import based on the actual class/function names

class TestSimulation(unittest.TestCase):

    def setUp(self):
        # Initialize any necessary parameters or state before each test
        self.initial_conditions = {
            'TIMESTEPS': 120,
            'POP': 10000,
            'init_M': 0.15,
            'init_L': 0.6,
            'init_U': 0.25,
        }
        self.dynamics = Dynamics(self.initial_conditions)

    def test_initial_population(self):
        # Test that the initial population is set correctly
        self.assertEqual(self.dynamics.M, int(self.initial_conditions['POP'] * self.initial_conditions['init_M']))
        self.assertEqual(self.dynamics.L, int(self.initial_conditions['POP'] * self.initial_conditions['init_L']))
        self.assertEqual(self.dynamics.U, int(self.initial_conditions['POP'] * self.initial_conditions['init_U']))

    def test_resource_production(self):
        # Test that resources are produced correctly
        initial_resources = self.dynamics.R
        self.dynamics.update_resources()
        self.assertGreater(self.dynamics.R, initial_resources)

    def test_legitimacy_calculation(self):
        # Test that legitimacy is calculated within expected bounds
        legitimacy = self.dynamics.calculate_legitimacy()
        self.assertGreaterEqual(legitimacy, -1.0)
        self.assertLessEqual(legitimacy, 1.0)

    def test_population_growth(self):
        # Test that the population grows correctly over time
        initial_population = self.dynamics.M + self.dynamics.L + self.dynamics.U
        self.dynamics.update_population()
        new_population = self.dynamics.M + self.dynamics.L + self.dynamics.U
        self.assertGreaterEqual(new_population, initial_population)

if __name__ == '__main__':
    unittest.main()