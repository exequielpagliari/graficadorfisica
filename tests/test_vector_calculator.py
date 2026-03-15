import unittest
from graph_tool.vector_calculator import Vector2D, VectorCalculator

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

if __name__ == '__main__':
    unittest.main()
