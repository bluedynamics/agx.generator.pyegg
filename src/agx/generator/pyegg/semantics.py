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
    
def cmp(a,b):
    if b.classname in a.bases:
        res= 1
    elif a.classname in b.bases:
        res= -1
    else:
        res= 0
        
    return res
    
def bubblesort(arr,cmp):
    for j in range(len(arr)):
        for i in range(j,len(arr)):
            if cmp(arr[i],arr[j])<0:
                tmp=arr[j]
                arr[j]=arr[i]
                arr[i]=tmp

@handler('inheritancesorter', 'uml2fs', 'semanticsgenerator', 'pymodule', order=90)
def inheritancesorter(self, source, target):
    """Create python modules.
    """
    module = read_target_node(source,target.target)
    classes=module.filteredvalues(IClass)
    for cl in classes:
        module.detach(cl.__name__)
        
    bubblesort(classes,cmp)
    
    for cl in classes:
        module.insertlast(cl)

