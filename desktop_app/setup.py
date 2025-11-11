"""
Setup script for Aditya Setu Desktop Application
"""
from setuptools import setup, find_packages
import os

# Read the README file if it exists
readme_file = os.path.join(os.path.dirname(__file__), 'README.md')
long_description = ''
if os.path.exists(readme_file):
    with open(readme_file, 'r', encoding='utf-8') as f:
        long_description = f.read()

setup(
    name='aditya-setu-desktop',
    version='1.0.0',
    description='Aditya Setu - Health Assessment Desktop Application',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Aditya Setu Team',
    author_email='info@adityasetu.com',
    url='https://github.com/yourusername/aditya-setu',
    packages=find_packages(),
    install_requires=[
        'sqlalchemy>=1.4.0',
        'bcrypt>=3.2.0',
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'aditya-setu=main:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Healthcare Industry',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)


