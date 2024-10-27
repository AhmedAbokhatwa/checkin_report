from setuptools import setup, find_packages

setup(
    name='checkin_report',
    version='0.0.1',
    description='A custom Frappe app',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'frappe'
    ]
)
