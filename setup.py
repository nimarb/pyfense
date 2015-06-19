from setuptools import setup, find_packages

setup(
	name = 'PyFense',
	version = '0.8',
	packages = find_packages(),
	package_data = {
		'assets': ['*.*'],
		'data' : ['*.*'],
	},

	install_requires = ['pyglet>=1.2.2', 'cocos2d>=0.6.0', 'numpy>=1.9.2'],

	maintainer = 'n',
	maintainer_email = 'l.nimar.b@gmail.com',
	
	description = 'PyFense is a tower defense game built in Python using the Cococs2d framework.',
	
	entry_points = {
		'console_scripts' : ['pyfense = pyfense.py']	
	},
	keywords = "pyfense tower defense",
	classifiers = [        
		'Programming Language :: Python',
        'Topic :: Games/Entertainment']
		
	install_requires = ['pyglet>=1.2.2', 'cocos2d>=0.6.3']

)