from setuptools import setup

config = {
    'description': 'Final exercise from "Learn Python 3 the Hard Way" (Zed Shaw)',
    'author': 'William Hitoshi Tsunoda Meira',
    'url': '',
    'version': '0.1',
    'install_requires': [
        'flask',
        'flask-login',
        'flask-sqlalchemy',
        'flask-wtf',
        'flask-bcrypt',
        'flask-moment',
        'flask-migrate',
        'flask-script',
        'flask-mail',
        'flask-session'
    ],
    'dependency_links': [
        'git+https://github.com/rayluo/flask-session@0.3.x#egg=flask-session'
    ],
    'extras_require': {
        'dev': [
            'pycodestyle',
            'pylint'
        ],
        'test': [
            'pytest',
            'pytest-cov'
        ],
    },
    'packages': ['app'],
    'scripts': [],
    'name': 'gothonweb'
}


setup(**config)
