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


@handler('classgeneralization', 'uml2fs', 'connectorgenerator', 'pyclass')
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
         'generalization')
def inheritancetokenizer(self, source, target):
    """Write inheritanceorder to token.
    """
    tgv = TaggedValues(source)
    order = tgv.direct('order', 'pyegg:derive', -1)
    if order == -1:
        return
    tok = token(source.specific.path, True, order=dict())
    tok.order[source.general.name] = order