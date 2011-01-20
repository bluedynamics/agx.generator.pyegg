# Copyright BlueDynamics Alliance - http://bluedynamics.com
# GNU General Public License Version 2

from agx.core import Scope
from agx.io.uml.interfaces import IModel
from agx.io.uml.interfaces import IPackage

class PackageScope(Scope):
    
    def __init__(self, name, interfaces):
        self.name = name
        self.interfaces = [IPackage]

    def __call__(self, node):
        if not Scope.__call__(self, node) \
          or IModel.providedBy(node) \
          or node.stereotype('pyegg:pyegg') is not None \
          or node.stereotype('pyegg:pymodule') is not None:
            return False
        return True

class EggScope(PackageScope):
    
    def __call__(self, node):
        if not Scope.__call__(self, node) \
          or IModel.providedBy(node) \
          or node.stereotype('pyegg:pyegg') is None:
            return False
        return True

class ModuleScope(PackageScope):
    
    def __call__(self, node):
        if not Scope.__call__(self, node) \
          or IModel.providedBy(node) \
          or node.stereotype('pyegg:pymodule') is None:
            return False
        return True

class DecoratorScope(PackageScope):
    
    def __call__(self, node):
        if node.stereotype('pyegg:decorator') is None:
            return False
        return True