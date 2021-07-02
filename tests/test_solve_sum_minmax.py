from src.package import solver
from sympy import FiniteSet, Interval


class Test:
    def test_1(self):
        """FiniteSet"""
        eq = 'min(400, 400*a) + min(400, 400*a) + min(0, 100*a) = 200'
        assert solver.auto_solve(eq, "a") == FiniteSet(1/4)

    def test_2(self):
        """FiniteSet"""
        eq = "min(400, 500*a) = 300"
        assert list(solver.auto_solve(eq, "a"))[0].evalf() == 0.6

    def test_3(self):
        """If a is on the left. """
        eq = "min(500*a, 400) = 300"
        assert list(solver.auto_solve(eq, "a"))[0].evalf() == 0.6

    def test_4(self):
        eq = "800*a + min(300, 400*a) + min(300, 400*a) = 1000"
        assert solver.auto_solve(eq, "a") == FiniteSet(0.625)

    def test_5(self):
        """If the equation has both min and max. """
        eq = "min(500, 600*a) + max(400, 500*a) = 500"
        assert list(solver.auto_solve(eq, "a"))[0].evalf() == 1/6

    def test_6(self):
        """If has constants before min/max. """
        eq = "800*a + 2*min(300, 400*a) = 1000"
        assert solver.auto_solve(eq, "a") == FiniteSet(5/8)

    def test_7(self):
        eq = "min(500, 600*a) - min(500, 600*a) = 0"
        assert solver.auto_solve(eq, "a") == Interval(0, 1, left_open=True,
                                                      right_open=True)

    def test_8(self):
        eq = "min(400, 600*a) = 400"
        assert solver.auto_solve(eq, "a") == Interval(2/3, 1, left_open=False,
                                                      right_open=True)

    def test_9(self):
        eq = "max(400*a, 600) = 600"
        assert solver.auto_solve(eq, "a") == Interval(0, 1, left_open=True,
                                                      right_open=True)

    def test_10(self):
        eq = "min(100, 400*a) + max(300, 400*a) = 400"
        assert solver.auto_solve(eq, "a") == Interval(1/4, 3/4,
                                                      left_open=False,
                                                      right_open=False)

    def test_11(self):
        eq = "max(300, 400*a) = 300"
        assert solver.auto_solve(eq, "a") == Interval(0, 3/4,
                                                      left_open=True,
                                                      right_open=False)

    def test_12(self):
        eq = "min(400*a, 100) = 500"
        assert solver.auto_solve(eq, "a") is None

    def test_13(self):
        eq = "max(400*a, 100) = 50"
        assert solver.auto_solve(eq, "a") is None

    def test_14(self):
        eq = "20*a - 20*a = 0"
        assert solver.auto_solve(eq, "a") == Interval(0, 1, left_open=True,
                                                      right_open=True)

    def test_15(self):
        eq = "10*a = 150"
        assert solver.auto_solve(eq, "a") == FiniteSet(15)

    def test_16(self):
        eq = "min(20, 0*a) + 50*a = 100"
        assert solver.auto_solve(eq, "a") == FiniteSet(2)

    def test_17(self):
        eq = "min(20, 0*a) + min(20, 30*a) + 50*a = 50"
        assert solver.auto_solve(eq, "a") == FiniteSet(5/8)

    def test_18(self):
        eq = "0*a + min(20, 30*a) = 15"
        assert solver.auto_solve(eq, "a") == FiniteSet(1/2)




