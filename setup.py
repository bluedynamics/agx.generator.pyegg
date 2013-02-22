import os
from setuptools import (
    setup,
    find_packages,
)


version = '1.0a1'
shortdesc = "AGX generator for python and python eggs"
longdesc = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
longdesc += open(os.path.join(os.path.dirname(__file__), 'LICENSE.rst')).read()


setup(name='agx.generator.pyegg',
      version=version,
      description=shortdesc,
      long_description=longdesc,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Programming Language :: Python', 
      ],
      keywords='AGX, Code Generation',
      author='BlueDynamics Alliance',
      author_email='dev@bluedynamics.com',
      url=u'http://github.com/bluedynamics/agx.generator.pyegg',
      license='GNU General Public Licence',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['agx', 'agx.generator'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'node.ext.template',
          'node.ext.python',
          'node.ext.uml',
          'agx.transform.uml2fs',
      ],
      extras_require = dict(
          test=[
            'interlude',
            'agx.generator.uml',
            'agx.transform.uml2fs',
          ]
      ),
      entry_points="""
      # -*- Entry points: -*-
      [agx.generator]
      register = agx.generator.pyegg:register
      """)
