from agx.core import (
    Scope,
    registerScope,
)
from node.ext.uml.interfaces import (
    IModel,
    IPackage,
    IClass,
    IOperation,
    IProperty,
    IGeneralization,
)


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


class ApiScope(PackageScope):

    def __call__(self, node):
        if node.stereotype('pyegg:api') is None:
            return False
        return True


class AutoimportScope(PackageScope):

    def __call__(self, node):
        if node.stereotype('pyegg:autoimport') is None:
            return False
        return True

class ConsoleScriptScope(Scope):

    def __call__(self, node):
        return node.stereotype('pyegg:console_script') is not None


registerScope('console_script', 'uml2fs', None , ConsoleScriptScope)

class SimpleBuildoutScope(Scope):

    def __call__(self, node):
        return node.stereotype('pyegg:simple_buildout') is not None


registerScope('simple_buildout', 'uml2fs', None , SimpleBuildoutScope)


registerScope('pythonegg', 'uml2fs', None, EggScope)
registerScope('pypackage', 'uml2fs', None, PackageScope)
registerScope('pymodule', 'uml2fs', None, ModuleScope)
registerScope('pyclass', 'uml2fs', [IClass], Scope)
registerScope('pyfunction', 'uml2fs', [IOperation], Scope)
registerScope('pydecorator', 'uml2fs', None, DecoratorScope)
registerScope('pyattribute', 'uml2fs', [IProperty], Scope)
registerScope('generalization', 'uml2fs', [IGeneralization], Scope)
registerScope('api', 'uml2fs', None, ApiScope)
registerScope('autoimport', 'uml2fs', [IPackage], AutoimportScope)
