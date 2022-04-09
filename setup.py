from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from themesaver.Misc.postInstall import postInstall
import os, atexit
from pathlib import Path

long_description = ( Path(os.path.dirname(__file__)) / "README.md").read_text()


class new_install(install):
    def __init__(self, *args, **kwargs):
        super(new_install, self).__init__(*args, **kwargs)
        atexit.register(postInstall)

setup(
    name='themesaver',
    version='1.2.4',
    description='A python script to manage your rices',
    url='https://github.com/techcoder20/themesaver',
    author='RPICoder',
    author_email='rpicoder@protonmail.com',
    include_package_data=True,
    license='GPLV3',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'Click',
        'pyqt5',
        'python-dotenv',
        'tqdm'
    ],
    entry_points={
        'console_scripts': [
            'themesaver = themesaver.themesaver:group',
        ],
    },
    cmdclass={'install': new_install},
)
