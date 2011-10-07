# Copyright BlueDynamics Alliance - http://bluedynamics.com
# GNU General Public License Version 2

from agx.core import (
    handler,
    token,
)
from agx.core.util import read_target_node
from node.ext.uml.utils import (
    Inheritance,
    TaggedValues,
    UNSET,
)
from node.ext import python
from node.ext.python.utils import Imports


def base_name(class_):
    """Extract base name for Class.
    """
    path = class_.path
    path = path[:len(path) - 1]
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


@handler('classgeneralization', 'uml2fs', 'connectorgenerator',
         'pyclass', order=10)
def generalization(self, source, target):
    """Create generalization.
    """
    inheritance = Inheritance(source)
    targetclass = read_target_node(source, target.target)
    for obj in inheritance.values():
        if not obj.context.name in targetclass.bases:
            targetclass.bases.append(obj.context.name)
            tgv = TaggedValues(obj.context)
            import_from = tgv.direct('import', 'pyegg:stub')
            if import_from is not UNSET:
                imp = Imports(targetclass.parent)
                imp.set(import_from, [[obj.context.name, None]])
        derive_from = read_target_node(obj.context, target.target)
        if not derive_from:
            continue
        if targetclass.parent is not derive_from.parent:
            imp = Imports(targetclass.parent)
            imp.set(base_name(derive_from), [[derive_from.classname, None]])


@handler('inheritanctokenizer', 'uml2fs', 'connectorgenerator',
         'generalization', order=20)
def inheritancetokenizer(self, source, target):
    """Write inheritanceorder to token.
    """
    tgv = TaggedValues(source)
    order = tgv.direct('order', 'pyegg:derive', -1)
    if order == -1:
        return
    tok = token(source.specific.path, True, order=dict())
    tok.order[source.general.name] = order


@handler('pyfunctionfromclass', 'uml2fs', 'connectorgenerator',
         'pyclass', order=30)
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
    if not source.parent.stereotype('pyegg:pymodule'):
        container = module.parent['__init__.py']
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