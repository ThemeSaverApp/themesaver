from setuptools import setup
from setuptools.command.install import install
import os

setup(
    name='themesaver',
    version='2.0.0',
    py_modules=['ThemeSaver'],
    install_requires=[
        'Click',
        'pyqt5',
        'python-dotenv',
        'tqdm'
    ],
    entry_points={
        'console_scripts': [
            'themesaver = ThemeSaver:group',
        ],
    }
)

