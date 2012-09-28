# Copyright BlueDynamics Alliance - http://bluedynamics.com
# GNU General Public License Version 2

from zope.component.interfaces import ComponentLookupError
from agx.core import (
    handler,
    token,
)
from agx.core.util import read_target_node
from node.ext.directory.interfaces import IDirectory
from agx.generator.pyegg.utils import (
    get_copyright,
    as_comment,
    sort_classes_in_module,
    egg_source,
    class_base_name,
    class_full_name,
)

from node.ext.python.utils import Imports
from node.ext.python.interfaces import IFunction

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
    sort_classes_in_module(module)


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
        if not module.name.endswith('.py'):
            continue #XXX thats perhaps not the perfect solution to sk
        if IDirectory.providedBy(module) \
          or module.name == '__init__.py' \
          or module in ignores:
            continue
        if len(module) > 1:
            continue
        if len(module):
            bl = module[module.keys()[0]]
            if IFunction.providedBy(bl):
               continue 
            if bl.lines != as_comment(get_copyright(source)):
                continue
        del module.parent[module.name]
        
@handler('apiexporter', 'uml2fs', 'semanticsgenerator',
         'api' )
def apiexporter(self, source,target):
    '''takes classes with 'api' stereotype and imports them into 
    the pyegg's __init__.py'''
    
    egg=egg_source(source)
    targetegg=read_target_node(egg, target.target)
    init=targetegg['__init__.py']
    imps=Imports(init)
    klass=read_target_node(source, target.target)
    imps.set(class_base_name(klass),[[source.name,None]])
