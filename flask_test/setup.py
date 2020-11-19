#project description
from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(), #what packages are needed
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
