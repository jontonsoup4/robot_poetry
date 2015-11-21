from distutils.core import setup

setup(
    name='robot_poetry',
    version='0.1.0',
    author='Jonathan Reed',
    author_email='jontonsoup4@gmail.com',
    description='Creates poems from text',
    url='https://github.com/jontonsoup4/robot_poetry',
    packages=['robot_poetry', 'robot_poetry.data'],
    package_data={'robot_poetry.data': ['*']},
    install_requires=['nltk>=3.0.5'],
)
