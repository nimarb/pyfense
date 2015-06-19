from setuptools import setup, find_packages

setup(
	name = 'PyFense'
	version = '1.0'
	packages = find_packages()
	package_data = {
		'assets': ['*.*'],
		'data' : ['*.*'],
	}
	
	author = 'Group C'
	description = 'PyFense is a tower defense game built in Python using the Cococs2d framework.'
	
	entry_points = {
		'console_scripts' : ['pyfense = pyfense.py']
		
	}
)