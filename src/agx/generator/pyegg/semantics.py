# Copyright BlueDynamics Alliance - http://bluedynamics.com
# GNU General Public License Version 2

from zope.component.interfaces import ComponentLookupError
from agx.core import (
    handler,
    token,
)
from agx.core.util import read_target_node
from node.ext.directory.interfaces import IDirectory
from node.ext.uml.utils import (
    TaggedValues,
    UNSET,
)
from agx.generator.pyegg.utils import (
    get_copyright,
    as_comment,
)


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


@handler('dependencysorter', 'uml2fs', 'semanticsgenerator', 
         'pymodule', order=30)
def dependencysorter(self, source, target):
    """Sort classes in modules dependencies.
    """
    module = read_target_node(source, target.target)
    classes=module.classes()

    def cmp(a, b):
        try:
            deptok_a=token(str(a.uuid),False,depends_on=set())
            if b in deptok_a.depends_on:
                return 1
        except ComponentLookupError:
            pass
        
        try:
            deptok_b=token(str(b.uuid),False,depends_on=set())
            if a in deptok_b.depends_on:
                return -1
        except ComponentLookupError:
            pass
        
        return 0
    def bubblesort(arr, cmp):
        for j in range(len(arr)):
            for i in range(j, len(arr)):
                if cmp(arr[i], arr[j]) < 0:
                    module.swap(arr[i],arr[j])

    bubblesort(classes, cmp)


@handler('eggemptymoduleremoval', 'uml2fs', 'semanticsgenerator',
         'pythonegg', order=40)
@handler('packageemptymoduleremoval', 'uml2fs', 'semanticsgenerator',
         'pypackage', order=40)
def emptymoduleremoval(self, source, target):
    directory = read_target_node(source, target.target)
    try:
        modtok = token('pymodules', False)
        ignores = modtok.modules
    except ComponentLookupError, e:
        # no modules created with <<pymodule>> packages
        ignores = set()
    for name in directory.keys():
        module = directory[name]
        if IDirectory.providedBy(module) \
          or module.name == '__init__.py' \
          or module in ignores:
            continue
        if len(module) > 1:
            continue
        if len(module):
            bl = module[module.keys()[0]]
            if bl.lines != as_comment(get_copyright(source)):
                continue
        del module.parent[module.name]