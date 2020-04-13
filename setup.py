try:
    from setuptools import setup
except:
    from distutils.core import setup

config = {
    'description': 'Final exercise from "Learn Python 3 the Hard Way" (Zed Shaw)',
    'author': 'William Hitoshi Tsunoda Meira',
    'url': '',
    'version': '0.1',
    'install_requires': ['flask', 'flask-login', 'flask-sqlalchemy', 'flask-wtf', 'flash-bcrypt'],
    'tests_require': ['pytest'],
    'packages': ['gothonweb'],
    'scripts': [],
    'name': 'gothonweb'
}

setup(**config)
