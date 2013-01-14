import agx.generator.pyegg
from zope.interface import implementer
from agx.core.interfaces import IProfileLocation


@implementer(IProfileLocation)
class ProfileLocation(object):
    name = u'pyegg.profile.uml'
    package = agx.generator.pyegg
