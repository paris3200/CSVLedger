from setuptools import setup

setup(
    name="csvledger",
    version="0.1",
    py_modules=["csvledger"],
    install_requires=["Click",],
    entry_points="""
        [console_scripts]
        csvledger=csvledger:cli
    """,
)
