"""Usage: pip install ."""

import re
from setuptools import setup, find_packages

# Get the version number
with open('sphinx_aiida/__init__.py') as f:
    MATCH_EXPR = "__version__[^'\"]+(['\"])([^'\"]+)"
    VERSION = re.search(MATCH_EXPR, f.read()).group(2).strip()

if __name__ == '__main__':
    setup(
        name='sphinx_aiida',
        version=VERSION,
        description='Sphinx extension for documenting AiiDA and its plugins.',
        author='Dominik Gresch',
        author_email='greschd@gmx.ch',
        license='MIT',
        classifiers=[
            'Development Status :: 3 - Alpha', 'Environment :: Plugins',
            'Framework :: AiiDA', 'Intended Audience :: Science/Research',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2.7',
            'Topic :: Scientific/Engineering :: Physics'
        ],
        keywords='aiida sphinx documentation',
        packages=find_packages(exclude=['aiida']),
        include_package_data=True,
        install_requires=[
            'aiida-core',
            'sphinx',
        ],
        extras_require={'dev': ['yapf', 'pre-commit']},
    )
