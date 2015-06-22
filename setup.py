from distutils.core import setup

setup(
    name = 'PyFense',
    version = '0.8.6',
    license = 'GPLv3',
    packages = ['pyfense'],
    package_data = {
        'pyfense': [
            'assets/*.*',
            'data/*.*']
    },

    install_requires = ['pyglet>=1.2.2', 'cocos2d>=0.6.0', 'numpy>=1.9.2'],

    maintainer = 'n',
    maintainer_email = 'l.nimar.b@gmail.com',

    description = 'PyFense is a tower defense game built in Python \
        using the Cocos2d framework.',

    entry_points = {
        'console_scripts': ['pyfense = pyfense.py:main']
    },
    #scripts = ['pyfense/pyfense.py', 'pyfense.py'],
    keywords = "pyfense tower defense td",
    classifiers = [
        'Programming Language :: Python',
        'Topic :: Games/Entertainment']
)
