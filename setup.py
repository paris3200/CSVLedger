from setuptools import setup

setup(
    name="csvledger",
    version="0.1",
    author="Jason Paris",
    author_email="paris3200@gmail.com",
    description="convert csv to ledgercli format",
    py_modules=["csvledger"],
    install_requires=["Click"],
    entry_points="""
        [console_scripts]
        csvledger=csvledger:cli
    """,
)
