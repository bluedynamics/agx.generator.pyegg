Integration Test (doctest style)
================================

This is an integration test. It assumes there is a working agx binary as in the
agx.dev setup after running buildout. Steps performed:

- delete generated code, if any
- get & check the generators help output
- generate code from test model in testing/data/agx.testpackage.uml
- check for generated files & directories (if they exist as expected)
- delete the generated files again & check for non-existence

Todo:
- what if we want the generated code to remain on the file system? flag/variable?
- test re-generation over generated code after model change

We would like to start with a fresh setup, no generated files. We delete them::

    >>> import os
    >>> import shutil
    >>>
    >>> #print(os.path.abspath(datadir))
    >>> if os.path.exists(os.path.join(datadir, 'agx.testpackage')):
    ...     shutil.rmtree(os.path.join(datadir, 'agx.testpackage'))
    ...     print("deleted generated code")
    deleted generated code
    >>> 1+1
    2

Some configuration settings for what is to come::

    >>> base_path = os.path.abspath(
    ...    os.path.join(datadir, '..', '..', '..', '..', '..', '..', '..', '..')) + os.sep
    >>> agx_bin = os.path.join(base_path, 'bin', 'agx')
    >>> pyegg_path = os.path.join('devsrc', 'agx.generator.pyegg', 'src', 'agx', 'generator', 'pyegg')
    >>> model_uml = os.path.join(base_path, pyegg_path, 'testing', 'data', 'agx.testpackage.uml')
    >>> pp = os.path.join(pyegg_path, 'profiles', 'pyegg.profile.uml')
    >>> profiles = base_path + pp
    >>> profiles
    '...devsrc/agx.generator.pyegg/src/agx/generator/pyegg/profiles/pyegg.profile.uml'
    >>> output_dir = os.path.join(datadir, 'agx.testpackage')
    >>> output_dir
    '...devsrc/agx.generator.pyegg/src/agx/generator/pyegg/testing/data/agx.testpackage'

    >>> agx_bin
    '...bin/agx'

    >>> model_uml
    '...devsrc/agx.generator.pyegg/src/agx/generator/pyegg/testing/data/agx.testpackage.uml'

    >>> profiles
    '...agx.dev/devsrc/agx.generator.pyegg/src/agx/generator/pyegg/profiles/pyegg.profile.uml'


Now we spin up the generator and check the help output::

    >>> os.path.exists(agx_bin)
    True

    >>> import subprocess
    >>> out, err = subprocess.Popen([agx_bin, '-h'], stdout=subprocess.PIPE).communicate()
    >>> err
    >>> out
    "Usage: agx UMLFILE options\n\nOptions:\n  -h, --help            show this help message and exit\n  -o /target/path, --output-directory=/target/path\n                        Write generated code to TARGET\n  -p /path/to/profile1.uml;/path/to/profile2.uml, --profiles=/path/to/profile1.uml;/path/to/profile2.uml\n                        Comma separated Paths to profile file(s)\n  -e profilename1;profilename2, --export-profiles=profilename1;profilename2\n                        Comma separated profile names to export for model\n  -l, --listprofiles    List of available profiles\n  -i, --info            AGX Version and flavour info.\n  -d, --debug           Additional output of debug information.\n  -m, --postmortem      Enable postmortem debugger.\n  -t, --listtemplates   list available model templates\n  -c template_name, --create=template_name\n                        Create a model from a model template by name. (see '-t' option)\n  -s, --short           option for short machine readable messages\n"

This time we generate some code::

#    >>> str(subprocess.check_output([agx_bin, model_uml]))
#    this will leave it spin for a while. needs fixing. XXX

::
    >>> out, err = subprocess.Popen([agx_bin, model_uml, '-p', profiles, '-o', output_dir], stdout=subprocess.PIPE).communicate()
    >>> err
    >>> out
    "INFO  AGX ... - (c) BlueDynamics Alliance, http://bluedynamics.com, GPL 2\nINFO  Generator ... sec.\n"

Check for the existence of generated files and directories::

    >>> testpackage_path = os.path.join(datadir, 'agx.testpackage')
    >>> os.path.exists(os.path.join(testpackage_path, 'setup.py'))
    True
    >>> os.path.exists(os.path.join(testpackage_path, 'LICENSE.rst'))
    True
    >>> os.path.exists(os.path.join(testpackage_path, 'MANIFEST.rst'))
    True
    >>> os.path.exists(os.path.join(testpackage_path, 'README.rst'))
    True
    >>> os.path.isdir(os.path.join(testpackage_path, 'src'))
    True
    >>> os.path.isdir(os.path.join(testpackage_path, 'src', 'agx'))
    True
    >>> os.path.exists(os.path.join(testpackage_path, 'src', 'agx', '__init__.py'))
    True
    >>> os.path.isdir(os.path.join(testpackage_path, 'src', 'agx', 'testpackage'))
    True
    >>> os.path.exists(os.path.join(testpackage_path, 'src', 'agx', 'testpackage', '__init__.py'))
    True
    >>> os.path.exists(os.path.join(testpackage_path, 'src', 'agx', 'testpackage', 'classinegg.py'))
    True
    >>> os.path.exists(os.path.join(testpackage_path, 'src', 'agx', 'testpackage', 'testmodule.py'))
    True
    >>> os.path.isdir(os.path.join(testpackage_path, 'src', 'agx', 'testpackage', 'somepackage'))
    True
    >>> os.path.exists(os.path.join(testpackage_path, 'src', 'agx', 'testpackage', 'somepackage', 'packageclass.py'))
    True

Check if we can delete something that has been generated...::

    >>> if os.path.exists(os.path.join(datadir, 'agx.testpackage')):
    ...     shutil.rmtree(os.path.join(datadir, 'agx.testpackage'))
    ...     print("deleted generated code")
    deleted generated code

And that files were really deleted::

    >>> os.path.exists(os.path.join(testpackage_path, 'setup.py'))
    False
    >>> os.path.exists(os.path.join(testpackage_path, 'LICENSE.rst'))
    False
    >>> os.path.exists(os.path.join(testpackage_path, 'MANIFEST.rst'))
    False
    >>> os.path.exists(os.path.join(testpackage_path, 'README.rst'))
    False
    >>> os.path.isdir(os.path.join(testpackage_path, 'src'))
    False
