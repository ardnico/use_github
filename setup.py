import io
import re
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

requires = [pkg.strip() for pkg in open('requirements.txt', 'r').readlines()]

version = ''
with open('use_github3/__init__.py', 'r') as fd:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)
if not version:
    raise RuntimeError('Cannot find version information')

setup(
    name='use_github',
    packages=['use_github3'],
    version=version,
    description='this module is available for daily operations',
    long_description=io.open('README.md', mode='r', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    author='ardnico',
    author_email='leaf.sun2@gmail.com',
    install_requires=requires,
    url='https://github.com/ardnico/use_github',
    download_url='https://github.com/ardnico/use_github/releases',
    keywords=['github', 'api', 'auditlog'],
        classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)