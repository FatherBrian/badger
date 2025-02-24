from setuptools import setup, find_packages

setup(
    name='badger',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'click==8.1.7',
        'pydantic==2.6.0',
        'pandas==2.2.0',
        'scipy==1.12.0',
        'pyyaml==6.0.1',
    ],
    entry_points={
        'console_scripts': [
            'badger = cli.cli:cli',  # 'badger' command runs cli()
        ],
    },
    author='Brian Fotheringham',
    description='Data contract validation and observability tool for Data and AI Teams',
    license='MIT',
)