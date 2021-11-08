from pathlib import Path

from setuptools import find_packages, setup

with open(Path(__file__).parent / 'README.md') as f:
    long_description = f.read()

setup(
    name='python-openca-tools',
    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': [
            'openca-tools = openca_tools.scripts.main:cmd',
        ],
    },
    version='0.1.0',
    license='MIT',
    description=(
        'Python client and command-line tool for processing Open Government '
        'Canada (open.canada.ca) datasets.'
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Elyas Khan',
    author_email='mail@ely.as',
    url='https://github.com/ely-as/python-openca-tools',
    project_urls={
        'Source': 'https://github.com/ely-as/python-openca-tools',
        'Tracker': 'https://github.com/ely-as/python-openca-tools/issues',
    },
    keywords=[],
    install_requires=[
        'beautifulsoup4',
        'lxml',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Typing :: Typed',
    ],
)
