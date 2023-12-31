from distutils.core import setup


setup(name='ECM_GUI',
      version='0.1.0',
      description='Lithium-ion battery simulator using equivalent circuit model',
      author='Moin Ahmed',
      author_email='moinahmed100@gmail.com',
      install_requires=['numpy', 'matplotlib', 'scipy', 'pytest'],
      packages=['parameter_sets', 'src', 'examples', 'tests'])
