# Copyright BlueDynamics Alliance - http://bluedynamics.com
# GNU General Public License Version 2

from zope.component.interfaces import ComponentLookupError
from agx.core import (
    handler,
    token,
)
from agx.core.util import read_target_node
from node.ext import python
from node.ext.python.interfaces import IClass
from node.ext.uml.utils import (
    TaggedValues,
    UNSET,
)

@handler('inheritanceorder', 'uml2fs', 'semanticsgenerator', 'pyclass')
def inheritanceorder(self, source, target):
    """Fix inheritance order.
    """
    try:
        tok = token(source.path, False)
        bases = tok.order.items()
        bases_sorted = sorted(bases, key=lambda x: x[1])
        bases_sorted = [base for base, order in bases_sorted]
        target = read_target_node(source, target.target)
        bases_orgin = target.bases
        bases = list()
        for base in bases_sorted:
            bases.append(base)
        for base in bases_orgin:
            if not base in bases_sorted:
                bases.append(base)
        target.bases = bases
    except ComponentLookupError, e:
        pass
    
def cmp(a, b):
    if b.classname in a.bases:
        return 1
    elif a.classname in b.bases:
        return -1
    return 0

def bubblesort(arr, cmp):
    for j in range(len(arr)):
        for i in range(j, len(arr)):
            if cmp(arr[i], arr[j]) < 0:
                tmp = arr[j]
                arr[j] = arr[i]
                arr[i] = tmp

@handler('inheritancesorter', 'uml2fs', 'semanticsgenerator', 'pymodule', order=90)
def inheritancesorter(self, source, target):
    """Sort classes in modules by inheritance dependencies.
    """
    module = read_target_node(source, target.target)
    classes=module.filteredvalues(IClass)
    for cl in classes:
        module.detach(cl.__name__)
    bubblesort(classes, cmp)
    for cl in classes:
        module.insertlast(cl)

@handler('pyfunctionfromclass', 'uml2fs', 'semanticsgenerator', 'pyclass')
def pyfunctionfromclass(self, source, target):
    """Convert Class to function if class has stereotype function set.
    """
    if source.stereotype('pyegg:function') is None:
        return
    class_ = read_target_node(source, target.target)
    dec_keys = [dec.name for dec in class_.decorators()]
    decorators = [class_.detach(key) for key in dec_keys]
    parent = class_.parent
    functions = parent.functions(class_.classname)
    if functions:
        if len(functions) > 1:
            raise "expected exactly one function by name '%s'" \
                % class_.classname
        function = functions[0]
    else:
        function = python.Function(class_.classname)
        function.__name__ = function.uuid
        parent.insertbefore(function, class_)
    del parent[str(class_.uuid)]
    tgv = TaggedValues(source)
    _args = tgv.direct('args', 'pyegg:function')
    _kwargs = tgv.direct('kwargs', 'pyegg:function')
    if _args is not UNSET:
        function.s_args = _args
    if _kwargs is not UNSET:
        function.s_kwargs = _kwargs
    other_decorators = function.decorators()
    for dec in decorators:
        exists = 0
        for other in other_decorators:
            if dec.equals(other):
                exists = 1
        if exists:
            continue
        function[str(dec.uuid)] = dec