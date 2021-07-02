import solver

eqs = [
    "20*a - 20*a = 0",
    "10*a = 150",
    "min(20, 0*a) + 50*a = 100",
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
    "min(500, 600*a) - min(500, 600*a) = 0",
    "min(400, 600*a) = 400",
    "max(400*a, 600) = 600",
    "min(100, 400*a) + max(300, 400*a) = 400",
    "min(400*a, 100) = 500",
    "max(400*a, 100) = 50",
    "max(300, 400*a) = 300"
]


if __name__ == "__main__":
    for i, eq in enumerate(eqs):
        print(f"Solving {i + 1}: {eq}...")
        print(solver.get_cons_var_terms(eq))
        # sol = solver.auto_solve(eq, "a")
        # print(f"Solution is {sol}")
        # print("==========================")
