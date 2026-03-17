import unittest
from graph_tool.energy_calculator import EnergyCalculator

class TestEnergyCalculator(unittest.TestCase):
    def setUp(self):
        self.m = 2.0
        self.v = 10.0
        self.h = 5.0
        self.k = 200.0
        self.x = 0.5
        self.calc = EnergyCalculator(masa=self.m, velocidad=self.v, altura=self.h, k=self.k, x=self.x)

    def test_cinetica(self):
        # Ec = 0.5 * 2 * 10^2 = 100
        self.assertEqual(self.calc.calcular_cinetica(), 100.0)

    def test_potencial_gravitatoria(self):
        # Epg = 2 * 9.8 * 5 = 98
        self.assertAlmostEqual(self.calc.calcular_potencial_gravitatoria(), 98.0)

    def test_potencial_elastica(self):
        # Epe = 0.5 * 200 * 0.5^2 = 0.5 * 200 * 0.25 = 25
        self.assertEqual(self.calc.calcular_potencial_elastica(), 25.0)

    def test_resolver_variable_v(self):
        calc = EnergyCalculator(masa=2.0)
        calc.resolver_variable("cinetica", 100.0)
        self.assertEqual(calc.v, 10.0)

    def test_resolver_variable_h(self):
        calc = EnergyCalculator(masa=2.0)
        calc.resolver_variable("gravitatoria", 98.0)
        self.assertAlmostEqual(calc.h, 5.0)

if __name__ == "__main__":
    unittest.main()
