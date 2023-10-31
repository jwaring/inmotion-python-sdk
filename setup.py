from setuptools import setup

setup(name='inmotion-python-sdk',
      version='0.1',
      description='An SDK to allow Python developers to make use of the inMotion APIs',
      url='http://github.com/jwaring/inmotion-python-sdk',
      author='Jason Waring',
      author_email='jason.waring@softwaringsolutions.com',
      license='Commercial',
      packages=['inmotion'],
      install_requires=[
          'numpy',
          'pycryptodome',
          'python-dotenv',
          'pandas',
          'requests'
      ],
      zip_safe=False)
