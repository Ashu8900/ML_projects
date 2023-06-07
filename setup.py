from setuptools import find_packages,setup
from typing import List

HYPEN_E_DOT ='-e .'
def get_requires(file_path):
    List[str] 
    '''
    Returns a list of Requirement
    '''
    requirements = []
    with open(file_path, 'r') as file_obj:
        requirements = file_obj.readlines()
        requirements= [ req.replace("\n","")for req in requirements]
        
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
            
    return requirements 
    


setup(
    name="ML PROJECTS",
    version='0.0.1',
    author="Ashutosh",
    author_email="3414ashu@gmail.com",
    packages=find_packages(),
    install_requires=get_requires('requirements.txt')
)