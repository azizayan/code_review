from setuptools import setup, find_packages

setup(
    name="ml-reviewer",
    version="0.1.0",
    description="A CLI tool for reviewing ML code and data hygiene",
    author="azizayan",
    packages=find_packages(),  
    install_requires=[
        "rich",
        "pandas",
        
    ],
    entry_points={
        "console_scripts": [
            "reviewer=ml_reviewer.main:main_cli_entry_point", 
        ],
    },
)