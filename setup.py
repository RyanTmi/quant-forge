from setuptools import setup, find_packages


def main() -> None:
    setup(
        name="quant-forge",
        version="0.1",
        packages=find_packages(),
        author="Ryan Timeus",
        description="",
        install_requires=[
            "numpy",
            "scipy",
            "pandas",
            "matplotlib",
            "yfinance",
        ],
    )


if __name__ == "__main__":
    main()
