from os import path
from setuptools import setup, find_packages

import bakrep

# Get the long description from the README file
setup_dir = path.abspath(path.dirname(__file__))
with open(path.join(setup_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='bakrep-cli',
    version=bakrep.__version__,
    description='BakRep CLI: a commandline tool for the batch download of BakRep datasets',
    keywords=['bioinformatics', 'annotation', 'bacteria', 'genomes', 'bakrep'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='GPLv3',
    author='Lukas Jelonek',
    author_email='lukas.jelonek@computational.bio.uni-giessen.de',
    url='https://bakrep.computational.bio',
    packages=find_packages(include=['bakrep']),
    python_requires='>=3.9',
    include_package_data=False,
    zip_safe=False,
    install_requires=[
        'requests >= 2.32'
    ],
    entry_points={
        'console_scripts': [
            'bakrep=bakrep.cli:entrypoint'
        ]
    },
    classifiers=[
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Natural Language :: English'
    ],
    project_urls={
        'Documentation': 'https://github.com/ag-computational-bio/bakrep-cli',
        'Source': 'https://github.com/ag-computational-bio/bakrep-cli',
        'Bug Reports': 'https://github.com/ag-computational-bio/bakrep-cli/issues',
        'CI': 'https://github.com/ag-computational-bio/bakrep-cli/actions'
    },
)