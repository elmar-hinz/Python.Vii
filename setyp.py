try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Vim Clone ',
    'author': 'Elmar Hinz',
    'url': 'https://github.com/elmar-hinz/Python.Vii',
    'download_url': 'https://github.com/elmar-hinz/Python.Vii',
    'author_email': 't3elmar@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['vii'],
    'scripts': [],
    'name': 'vii'
}

setup(**config)
