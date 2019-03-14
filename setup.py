from setuptools import setup, find_packages

setup(
	name='project1',
	version='1.0',
	author='akhila podupuganti',
	authour_email='akhila.podupuganti-1@ou.edu',
	packages=find_packages(exclude=('tests', 'docs')),
	setup_requires=['pytest-runner'],
	tests_require=['pytest']	
)
