import unittest
from graph_tool.projectile_calculator import ProjectileCalculator

class TestProjectileCalculator(unittest.TestCase):
    def test_tiro_horizontal(self):
        """Lanzamiento horizontal: v0=20, angulo=0, h0=10 -> alcance=20.2s"""
        calc = ProjectileCalculator(v0=20, angulo_deg=0, h0=10, g=9.8)
        res = calc.calcular()
        # t = sqrt(2h/g) = sqrt(20/9.8) = 1.428s
        # x = v0 * t = 20 * 1.428 = 28.56m
        self.assertAlmostEqual(res['alcance_max'], 28.57, delta=0.1)
        self.assertAlmostEqual(res['altura_max'], 10.0)

    def test_tiro_45_grados(self):
        """Lanzamiento a 45 grados: v0=30, angulo=45, h0=0 -> alcance=91.8m"""
        calc = ProjectileCalculator(v0=30, angulo_deg=45, h0=0, g=9.8)
        res = calc.calcular()
        # R = (v0^2 * sin(2*theta)) / g = (900 * 1) / 9.8 = 91.83m
        self.assertAlmostEqual(res['alcance_max'], 91.83, delta=0.1)
        self.assertAlmostEqual(res['altura_max'], 22.95, delta=0.1)

if __name__ == '__main__':
    unittest.main()
