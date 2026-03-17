import unittest
from graph_tool.energy_calculator import EnergyCalculator
from graph_tool.exceptions import CalculationError

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

    def test_energy_missing_masa_raises_calculation_error(self):
        """Test that missing masa raises CalculationError in calcular_cinetica."""
        calc = EnergyCalculator(masa=None, velocidad=10.0)
        
        with self.assertRaises(CalculationError) as context:
            calc.calcular_cinetica()
        
        self.assertIn("masa", str(context.exception).lower())
        self.assertEqual(context.exception.operation, "calcular_cinetica")

    def test_energy_missing_velocidad_raises_calculation_error(self):
        """Test that missing velocidad raises CalculationError in calcular_cinetica."""
        calc = EnergyCalculator(masa=5.0, velocidad=None)
        
        with self.assertRaises(CalculationError) as context:
            calc.calcular_cinetica()
        
        self.assertIn("velocidad", str(context.exception).lower())
        self.assertEqual(context.exception.operation, "calcular_cinetica")

    def test_energy_missing_altura_raises_calculation_error(self):
        """Test that missing altura raises CalculationError in calcular_potencial_gravitatoria."""
        calc = EnergyCalculator(masa=5.0, altura=None)
        
        with self.assertRaises(CalculationError) as context:
            calc.calcular_potencial_gravitatoria()
        
        self.assertIn("altura", str(context.exception).lower())
        self.assertEqual(context.exception.operation, "calcular_potencial_gravitatoria")

    def test_energy_missing_k_raises_calculation_error(self):
        """Test that missing k raises CalculationError in calcular_potencial_elastica."""
        calc = EnergyCalculator(k=None, x=0.5)
        
        with self.assertRaises(CalculationError) as context:
            calc.calcular_potencial_elastica()
        
        self.assertIn("k", str(context.exception).lower())
        self.assertEqual(context.exception.operation, "calcular_potencial_elastica")

    def test_energy_missing_x_raises_calculation_error(self):
        """Test that missing x raises CalculationError in calcular_potencial_elastica."""
        calc = EnergyCalculator(k=100.0, x=None)
        
        with self.assertRaises(CalculationError) as context:
            calc.calcular_potencial_elastica()
        
        self.assertIn("x", str(context.exception).lower())
        self.assertEqual(context.exception.operation, "calcular_potencial_elastica")

if __name__ == "__main__":
    unittest.main()
