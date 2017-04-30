# setup.py
from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')

setup(
	options  = {'py2exe': {'unbuffered': False, 'bundle_files': 1, 'compressed': False}},
	console  = ['main.py'],
	zipfile  = None,
)
