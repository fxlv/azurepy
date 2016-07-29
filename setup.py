from setuptools import setup

setup(name='azurepy',
      version='0.0.3',
      description='Wrapper around Azure python module and CLI tools',
      url='http://github.com/fxlv/azurepy',
      author='Kaspars Mickevics',
      author_email='kaspars@fx.lv',
      install_requires=['azure>=0.9.0'],
      packages=['azurepy'],
      zip_safe=False)
