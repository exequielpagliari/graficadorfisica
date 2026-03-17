import unittest
from graph_tool.vector_calculator import Vector2D, VectorCalculator
from graph_tool.exceptions import CalculationError

class TestVectorCalculator(unittest.TestCase):
    def test_suma(self):
        v1 = Vector2D(3, 4)
        v2 = Vector2D(1, 2)
        calc = VectorCalculator(v1=v1, v2=v2, operacion="suma")
        res = calc.calcular()
        self.assertEqual(res.x, 4.0)
        self.assertEqual(res.y, 6.0)

    def test_resta(self):
        v1 = Vector2D(5, 5)
        v2 = Vector2D(2, 3)
        calc = VectorCalculator(v1=v1, v2=v2, operacion="resta")
        res = calc.calcular()
        self.assertEqual(res.x, 3.0)
        self.assertEqual(res.y, 2.0)

    def test_multiplicacion_escalar(self):
        v1 = Vector2D(3, -1)
        calc = VectorCalculator(v1=v1, escalar=2, operacion="multiplicacion")
        res = calc.calcular()
        self.assertEqual(res.x, 6.0)
        self.assertEqual(res.y, -2.0)

    def test_division_escalar(self):
        v1 = Vector2D(10, -5)
        calc = VectorCalculator(v1=v1, escalar=5, operacion="division")
        res = calc.calcular()
        self.assertEqual(res.x, 2.0)
        self.assertEqual(res.y, -1.0)

    def test_magnitud_angulo(self):
        v1 = Vector2D(3, 3) # Ángulo de 45°
        self.assertAlmostEqual(v1.angulo, 45.0)
        self.assertAlmostEqual(v1.magnitud, 4.242640687119285)

    def test_vector_division_by_zero_raises_calculation_error(self):
        """Test that division by zero raises CalculationError with proper message."""
        v1 = Vector2D(10, 5)
        calc = VectorCalculator(v1=v1, escalar=0, operacion="division")
        
        with self.assertRaises(CalculationError) as context:
            calc.calcular()
        
        self.assertEqual(str(context.exception), "División por cero no permitida.")
        self.assertEqual(context.exception.operation, "calcular")

    def test_vector_division_by_zero_via_truediv_raises_calculation_error(self):
        """Test that Vector2D.__truediv__ raises CalculationError for division by zero."""
        v1 = Vector2D(10, 5)
        
        with self.assertRaises(CalculationError) as context:
            result = v1 / 0
        
        self.assertEqual(str(context.exception), "División por cero no permitida.")

    def test_vector_missing_v1_raises_calculation_error(self):
        """Test that missing v1 raises CalculationError."""
        calc = VectorCalculator(v1=None, v2=Vector2D(1, 2), operacion="suma")
        
        with self.assertRaises(CalculationError) as context:
            calc.calcular()
        
        self.assertIn("v1", str(context.exception))

    def test_vector_missing_escalar_raises_calculation_error(self):
        """Test that missing escalar raises CalculationError for division."""
        calc = VectorCalculator(v1=Vector2D(1, 2), escalar=None, operacion="division")
        
        with self.assertRaises(CalculationError) as context:
            calc.calcular()
        
        self.assertIn("escalar", str(context.exception))

    def test_vector_missing_operation_raises_calculation_error(self):
        """Test that missing operation raises CalculationError."""
        calc = VectorCalculator(v1=Vector2D(1, 2), v2=Vector2D(3, 4), operacion=None)
        
        with self.assertRaises(CalculationError) as context:
            calc.calcular()
        
        self.assertIn("operación", str(context.exception))

if __name__ == '__main__':
    unittest.main()
