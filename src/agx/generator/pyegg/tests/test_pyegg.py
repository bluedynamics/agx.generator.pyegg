# Copyright BlueDynamics Alliance - http://bluedynamics.com
# GNU General Public License Version 2

import os
import unittest
import doctest
import zope.component
from pprint import pprint
from interlude import interact

optionflags = doctest.NORMALIZE_WHITESPACE | \
              doctest.ELLIPSIS | \
              doctest.REPORT_ONLY_FIRST_FAILURE

TESTFILES = [
    'test_pyegg.txt',
    'test_pyegg_generation.txt',
]

datadir = os.path.join(os.path.dirname(__file__), 'data')


def test_suite():
    return unittest.TestSuite([
        doctest.DocFileSuite(
            file, 
            optionflags=optionflags,
            globs={'interact': interact,
                   'pprint': pprint,
                   'datadir': datadir},
        ) for file in TESTFILES
    ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
