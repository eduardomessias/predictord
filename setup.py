from setuptools import find_packages, setup

setup(
    name = 'predictord',
    version = '1.0.1',
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
    install_requires = [
        'flask',
        'yfinance',
        'plotly'
    ]
)