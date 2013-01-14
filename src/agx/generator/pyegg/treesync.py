from zope.interface import (
    Interface,
    implementer,
)
from agx.core import TreeSyncPreperator
from agx.core.util import read_target_node
from node.ext.uml.interfaces import (
    IClass,
    IInterface,
)
from node.ext.directory.interfaces import IDirectory
from node.ext.python.interfaces import IModule
from node.ext.python import Module


class IModuleNameChooser(Interface):

    def __call__():
        """Create real module name
        """


@implementer(IModuleNameChooser)
class ModuleNameChooser(object):

    def __init__(self, context):
        self.context = context

    def __call__(self):
        return self.context.name.lower()


class PackageSyncer(TreeSyncPreperator):

    def __call__(self, source):
        super(PackageSyncer, self).__call__(source)
        if (IClass.providedBy(source) or IInterface.providedBy(source)) \
          and IDirectory.providedBy(self.anchor) \
          and (source.parent.stereotype('pyegg:pypackage') is not None \
          or source.parent.stereotype('pyegg:pyegg') is not None):
            modulename = '%s.py' % IModuleNameChooser(source)()
            self.anchor[modulename] = Module()
            self.anchor = self.anchor[modulename]
        elif (IClass.providedBy(source) or IInterface.providedBy(source)) \
          and IModule.providedBy(self.anchor) \
          and (source.parent.stereotype('pyegg:pypackage') is not None \
          or source.parent.stereotype('pyegg:pyegg') is not None):
            modulename = '%s.py' % IModuleNameChooser(source)()
            container = self.anchor.parent
            container[modulename] = Module()
            self.anchor = container[modulename]
        else:
            if source.parent is None:
                return
            target_node = read_target_node(source.parent, self.target)
            if not target_node:
                super(PackageSyncer, self).__call__(source)
                return
            if len(target_node.path) < len(self.anchor.path):
                self.anchor = target_node
