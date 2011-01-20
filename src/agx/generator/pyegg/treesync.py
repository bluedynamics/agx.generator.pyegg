# Copyright BlueDynamics Alliance - http://bluedynamics.com
# GNU General Public License Version 2

from agx.core import TreeSyncPreperator
from agx.core.util import read_target_node
from node.ext.uml.interfaces import IClass
from node.ext.directory.interfaces import IDirectory
from node.ext.python.interfaces import IModule
from node.ext.python import Module

class PackageSyncer(TreeSyncPreperator):
    
    def __call__(self, source):
        super(PackageSyncer, self).__call__(source)
        if IClass.providedBy(source) \
          and IDirectory.providedBy(self.anchor) \
          and (source.__parent__.stereotype('pyegg:pypackage') is not None \
          or source.__parent__.stereotype('pyegg:pyegg') is not None):
            modulename = '%s.py' % source.name.lower()
            self.anchor[modulename] = Module()
            self.anchor = self.anchor[modulename]
        elif IClass.providedBy(source) \
          and IModule.providedBy(self.anchor) \
          and (source.__parent__.stereotype('pyegg:pypackage') is not None \
          or source.__parent__.stereotype('pyegg:pyegg') is not None):
            modulename = '%s.py' % source.name.lower()
            container = self.anchor.__parent__
            container[modulename] = Module()
            self.anchor = container[modulename]
        else:
            if source.__parent__ is None:
                return
            target_node = read_target_node(source.__parent__, self.target)
            if not target_node:
                super(PackageSyncer, self).__call__(source)
                return
            if len(target_node.path) < len(self.anchor.path):
                self.anchor = target_node