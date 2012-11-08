# Copyright BlueDynamics Alliance - http://bluedynamics.com
# GNU General Public License Version 2

import os
import uuid
from zope.component.interfaces import ComponentLookupError
from node.ext import python
from node.ext.uml.utils import (
    TaggedValues,
    UNSET,
)
from agx.core import token


def templatepath(name):
    return os.path.join(os.path.dirname(__file__), 'templates/%s' % name)


def as_comment(lines):
    if not lines:
        return list()
    return ['# %s' % line.strip() for line in lines]


def get_copyright(source):
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
    return cp


def set_copyright(source, module):
    block = python.Block()
    block.__name__ = str(uuid.uuid4())
    block.lines = as_comment(get_copyright(source))
    values = module.values()
    if len(values) == 0:
        module[block.name] = block
    else:
        first = values[0]
        if isinstance(first, python.Block):
            if first.text == block.text:
                return
        module.insertbefore(block, values[0])


def _module_path(path):
    ret = list()
    while True:
        next = path.pop()
        if next == 'src':
            break
        if next.endswith('.py'):
            next = next[:len(next) - 3]
        ret.append(next)
    ret.reverse()
    return '.'.join(ret)


def class_full_name(class_):
    """Extract full name for Class.
    """
    return '%s.%s' % (class_base_name(class_), class_.classname)


def class_base_name(class_):
    """Extract base name for Class.
    """
    path = class_.path
    path = path[:len(path) - 1]
    return _module_path(path)


def egg_source(source):
    """Look up source node representing the python egg.
    """
    node = source
    while True:
        if node.stereotype('pyegg:pyegg'):
            break
        node = node.parent
        if not node:
            raise RuntimeError(u"Element mapping to python egg not found.")
    return node


def sort_classes_in_module(module):
    classes = module.values()

    def cmp(a, b):
        try:
            deptok_a = token(str(a.uuid), False, depends_on=set())
            if b in deptok_a.depends_on:
                return 1
        except ComponentLookupError:
            pass

        try:
            deptok_b = token(str(b.uuid), False, depends_on=set())
            if a in deptok_b.depends_on:
                return -1
        except ComponentLookupError:
            pass

        return 0

    def bubblesort(arr, cmp):
        for j in range(len(arr)):
            for i in range(j, len(arr)):
                if cmp(arr[i], arr[j]) < 0:
                    module.swap(arr[i], arr[j])

    bubblesort(classes, cmp)


def implicit_dotted_path(node):
    '''returns the dotted python path of an entity, if the entity is a class
    and not modelled into a module the implicitely created module
    will be added to the path'''
    # XXX that docstring has some bad grammar. ',' -> '.' ?!? two sentences?
    path = node.path
    pack = node.parent

    if not pack.stereotype('pyegg:module'):
        path.insert(-1, node.name.lower())

    return '.'.join(path[1:])


def is_class_a_function(klass):
    if klass.stereotype('pyegg:function'):
        return True
    try:
        tok = token(str(klass.uuid), False, is_function=False)
        if tok.is_function:
            return True
    except ComponentLookupError:
        pass
