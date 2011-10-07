# Copyright BlueDynamics Alliance - http://bluedynamics.com
# GNU General Public License Version 2

import os
import uuid
from node.ext import python
from node.ext.uml.utils import (
    TaggedValues,
    UNSET,
)


def templatepath(name):
    return os.path.join(os.path.dirname(__file__), 'templates/%s' % name)


def set_copyright(source, module):
    cp = ''
    while True:
        tgv = TaggedValues(source)
        cp = tgv.direct('copyright', 'pyegg:pyegg')
        if cp is not UNSET:
            break
        if source.parent is None:
            break
        source = source.parent
    if cp == '' or cp == UNSET:
        return
    cp = cp.split(',')
    block = python.Block()
    block.__name__ = str(uuid.uuid4())
    block.lines = ['# %s' % line.strip() for line in cp]
    values = module.values()
    if len(values) == 0:
        module[block.name] = block
    else:
        first = values[0]
        if isinstance(first, python.Block):
            if first.text == block.text:
                return
        module.insertbefore(block, values[0])