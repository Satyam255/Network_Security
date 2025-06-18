'''
The setup.py file is used to package the Python project.
it is an essential part of Python projects that need to be distributed or installed.
It is used by setuptools, a library written specifically for this purpose.
to define the package metadata, dependencies, and other configurations.
'''

from setuptools import setup, find_packages
from typing import List

def get_requirements() -> List[str]:
    """
    Reads the requirements file and returns a list of dependencies.
    
    :param file_path: Path to the requirements file.
    :return: List of dependencies.
    """
    requirement_list:List[str] = []
    try:
      with open('requirements.txt', 'r') as file:
        # Read lines from the file
        lines = file.readlines()
        # process each line 
        for line in lines:
           requirements = line.strip()
           ##ignore empty lines and comments and - e.
           if requirements and requirements != '-e .':
                requirement_list.append(requirements)
        
    except FileNotFoundError:
       print("Requirements file not found.")

    return requirement_list

setup(
   name="Network Security",
   versions="0.0.1",
    author="Satyam255",
    packages=find_packages(),
    install_requires=get_requirements()
)