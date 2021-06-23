import numpy as np

from src.package import solve_sum_minmax


class TestClass:
    def test_1(self):
        eq = 'min(400, 400*a) + min(400, 400*a) + min(0, 100*a)'
        value = 200
        assert solve_sum_minmax.solve_sum_minmax(eq, value) == 0.25

    def test_2(self):
        """If only has one equation. """
        eq = "min(400, 400*a)"
        value = 400
        assert solve_sum_minmax.solve_sum_minmax(eq, value) is None

    def test_3(self):
        eq = "min(400, 500*a)"
        value = 300
        assert solve_sum_minmax.solve_sum_minmax(eq, value) == 0.6

    def test_4(self):
        """If a is on the left. """
        eq = "min(500*a, 400)"
        value = 300
        assert solve_sum_minmax.solve_sum_minmax(eq, value) == 0.6

    def test_5(self):
        """If have constants before min. """
        eq = "800*a + 2*min(300, 400*a)"
        value = 1000
        assert solve_sum_minmax.solve_sum_minmax(eq, value) == 0.625

    def test_6(self):
        """If the equation has both min and max. """
        eq = "min(500, 600*a) + max(400, 500*a)"
        value = 500
        assert solve_sum_minmax.solve_sum_minmax(eq, value) == 0.16666


