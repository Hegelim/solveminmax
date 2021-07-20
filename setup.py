import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="solveminmax",
    version="0.1.3",
    author="Yewen Zhou",
    author_email="yz4175@columbia.edu",
    description="A package to solve the sum of min/max equations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hegelim/solve-sum-minmax",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
