# Copyright BlueDynamics Alliance - http://bluedynamics.com
# GNU General Public License Version 2

from zope.component.interfaces import ComponentLookupError
from agx.core import (
    handler,
    token,
)
from agx.core.util import read_target_node
from node.ext import python
from node.ext.uml.utils import (
    TaggedValues,
    UNSET,
)
from agx.generator.pyegg.utils import get_copyright


@handler('inheritanceorder', 'uml2fs', 'semanticsgenerator',
         'pyclass', order=10)
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


@handler('pyfunctionfromclass', 'uml2fs', 'semanticsgenerator',
         'pyclass', order=20)
def pyfunctionfromclass(self, source, target):
    """Convert Class to function if class has stereotype function set.
    """
    if source.stereotype('pyegg:function') is None:
        return
    class_ = read_target_node(source, target.target)
    dec_keys = [dec.name for dec in class_.decorators()]
    decorators = [class_.detach(key) for key in dec_keys]
    module = class_.parent
    container = module
    #delmodule = False
    if not source.parent.stereotype('pyegg:pymodule'):
        container = module.parent['__init__.py']
        #delmodule = True
    functions = container.functions(class_.classname)
    if functions:
        if len(functions) > 1:
            raise "expected exactly one function by name '%s'" \
                % class_.classname
        function = functions[0]
    else:
        function = python.Function(class_.classname)
        function.__name__ = function.uuid
        container.insertlast(function)
    #if delmodule:
    #    if len(module) > 2:
            # XXX: improve -> expects copyright block and function
            #      check for docstring block by compairing contents
    #        del module[str(class_.uuid)]
    #    else:
    #        del module.parent[module.name]
    #else:
    #    del module[str(class_.uuid)]
    del module[str(class_.uuid)]
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


@handler('inheritancesorter', 'uml2fs', 'semanticsgenerator', 
         'pymodule', order=30)
def inheritancesorter(self, source, target):
    """Sort classes in modules by inheritance dependencies.
    """
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
    module = read_target_node(source, target.target)
    classes=module.classes()
    for cl in classes:
        module.detach(cl.name)
    bubblesort(classes, cmp)
    for cl in classes:
        module.insertlast(cl)


@handler('emptymoduleremoval', 'uml2fs', 'semanticsgenerator',
         'pymodule', order=40)
def emptymoduleremoval(self, source, target):
    #import pdb;pdb.set_trace()
    if source.parent.stereotype('pyegg:pymodule'):
        return
    module = read_target_node(source, target.target)
    if module.name == '__init__.py':
        return
    if len(module) > 1:
        return
    if len(module):
        bl = module[module.keys()[0]]
        if bl.lines != get_copyright(source):
            return
    del module.parent[module.name]