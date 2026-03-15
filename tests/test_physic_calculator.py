import unittest
from graph_tool.physic_calculator import PhysicCalculator

class TestPhysicCalculator(unittest.TestCase):
    
    def test_mru_velocidad(self):
        """Calcula velocidad en MRU: pi=0, pf=10, t=2 -> v=5"""
        calc = PhysicCalculator(posicion_inicial=0.0, posicion_final=10.0, tiempo=2.0, aceleracion=0.0)
        calc.calcular()
        self.assertAlmostEqual(calc.velocidad, 5.0)
        self.assertAlmostEqual(calc.velocidad_inicial, 5.0)

    def test_mrua_distancia(self):
        """Calcula distancia en MRUA: vi=0, a=2, t=10 -> pf=100"""
        calc = PhysicCalculator(posicion_inicial=0.0, velocidad_inicial=0.0, aceleracion=2.0, tiempo=10.0)
        calc.calcular()
        self.assertAlmostEqual(calc.posicion_final, 100.0)

    def test_mrua_frenado(self):
        """Calcula aceleración de frenado: vi=20, vf=0, t=4 -> a=-5"""
        calc = PhysicCalculator(velocidad_inicial=20.0, velocidad_final=0.0, tiempo=4.0)
        calc.calcular()
        self.assertAlmostEqual(calc.aceleracion, -5.0)

    def test_mrua_tiempo_cuadratica(self):
        """Calcula tiempo usando cuadrática: pi=0, pf=100, vi=0, a=2 -> t=10"""
        calc = PhysicCalculator(posicion_inicial=0.0, posicion_final=100.0, velocidad_inicial=0.0, aceleracion=2.0)
        calc.calcular()
        self.assertAlmostEqual(calc.tiempo, 10.0)

if __name__ == '__main__':
    unittest.main()
