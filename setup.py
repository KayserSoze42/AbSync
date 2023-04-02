from setuptools import setup, find_packages
import pathlib

path = pathlib.Path(__file__).parent.resolve()

description = (path / "README.md").read_text(encoding="utf-8")

setup(

    name="AbSync",
    version="1.0.0",
    description="Simple Python Sync Scheduler",
    url="https://github.com/KayserSoze42/AbSync",

    entry_points = {
        'console_scripts': [
            'AbSync=AbSync.AbSync:main'
            ],
    },

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Version Control",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],

    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3, <4",
    install_requires=["schedule"]

)
