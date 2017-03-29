from setuptools import setup, find_packages

requires = [
    'guillotina'
    ]

setup(name='guillotina_swagger',
      version='1.0.0',
      description='Swagger integration for viewing REST on your guillotina install',
      author='Nathan Van Gheem',
      author_email='vangheem@gmail.com',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires)
