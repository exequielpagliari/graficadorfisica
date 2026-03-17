import unittest
from graph_tool.force_calculator import ForceCalculator
from graph_tool.exceptions import CalculationError


class TestForceCalculator(unittest.TestCase):
    def setUp(self):
        self.m = 10.0
        self.f = 100.0
        self.a = 5.0
        self.calc = ForceCalculator(masa=self.m, fuerza=self.f, aceleracion=self.a)

    def test_newton_basic(self):
        """Test basic Newton calculation F = m * a."""
        calc = ForceCalculator(masa=10.0, fuerza=None, aceleracion=5.0)
        result = calc.calcular_newton()
        self.assertEqual(result["fuerza"], 50.0)

    def test_plano_inclinado_basic(self):
        """Test basic inclined plane calculation."""
        calc = ForceCalculator(masa=10.0, angulo=30.0, fuerza=0.0)
        result = calc.calcular_plano_inclinado()
        self.assertIn("aceleracion", result)

    def test_hooke_basic(self):
        """Test basic Hooke's law calculation."""
        calc = ForceCalculator(k=100.0, x=0.5)
        result = calc.calcular_hooke()
        self.assertEqual(result["fuerza"], 50.0)

    def test_force_missing_masa_raises_calculation_error(self):
        """Test that missing masa raises CalculationError in calcular_plano_inclinado."""
        calc = ForceCalculator(masa=None, angulo=30.0)
        
        with self.assertRaises(CalculationError) as context:
            calc.calcular_plano_inclinado()
        
        self.assertIn("masa", str(context.exception).lower())
        self.assertEqual(context.exception.operation, "calcular_plano_inclinado")

    def test_force_missing_angulo_raises_calculation_error(self):
        """Test that missing angulo raises CalculationError in calcular_plano_inclinado."""
        calc = ForceCalculator(masa=10.0, angulo=None)
        
        with self.assertRaises(CalculationError) as context:
            calc.calcular_plano_inclinado()
        
        self.assertIn("angulo", str(context.exception).lower())
        self.assertEqual(context.exception.operation, "calcular_plano_inclinado")

    def test_force_missing_masa_in_newton_raises_calculation_error(self):
        """Test that missing masa raises CalculationError in calcular_newton when calculating aceleración."""
        calc = ForceCalculator(masa=None, fuerza=100.0, aceleracion=None)
        
        with self.assertRaises(CalculationError) as context:
            calc.calcular_newton()
        
        self.assertIn("masa", str(context.exception).lower())
        self.assertEqual(context.exception.operation, "calcular_newton")


if __name__ == "__main__":
    unittest.main()
