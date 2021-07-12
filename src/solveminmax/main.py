from solveminmax.solver import auto_solve

linear_eqs = [
    "20*a - 20*a = 0",
    "10*a = 150",
    "min(20, 0*a) + 50*a = 100",
    "20*a - 20*a = 0",
    "20*a - 5*a = 0",
    "5*a = -1",
    "-20*a = 1"
]

finite_eqs = [
    "min(20, 30) + min(30, 40*a) = 40",
    "min(20, 0*a) + min(20, 30*a) + 50*a = 50",
    "0*a + min(20, 30*a) = 15",
    'min(400, 400*a) + min(400, 400*a) + min(0, 100*a) = 200',
    "min(400, 500*a) = 300",
    "min(500*a, 400) = 300",
    "800*a + min(300, 400*a) + min(300, 400*a) = 1000",
    "750*a + min(300, 400*a) + min(300, 400*a) + 50*a = 1000",
    "min(500, 600*a) + max(400, 500*a) = 500",
    "800*a + 2*min(300, 400*a) = 1000",
    "-2*min(300, 400*a) = -600"
]

interval_eqs = [
    "min(500, 600*a) - min(500, 600*a) = 0",
    "min(400, 600*a) = 400",
    "max(400*a, 600) = 600",
    "min(100, 400*a) + max(300, 400*a) = 400",
    "max(300, 400*a) = 300"
]

none_eqs = [
    "min(400*a, 100) = 500",
    "max(400*a, 100) = 50",
    "min(20*a, 30) - min(20*a, 30) = 40"
]

negative_eqs = [
    "min(500, 800*a) - max(800*a, 700) = -200",
    "min(-30, 40*a) = -30",
    "min(30, -40*a) = 40"
]

error_eqs = [
    "min(20*a) = 300",
    "",
    " "
]

eqs = ["linear_eqs", "finite_eqs", "interval_eqs", "none_eqs", "negative_eqs"]

if __name__ == "__main__":
    for div in eqs:
        print("------------------------")
        print(f"Solving in {div}...")
        for i, eq in enumerate(eval(div)):
            print(f"Solving {i + 1}: {eq}")
            sol = auto_solve(eq, "a")
            print(f"Solution is {sol}")
            print()
