import scope
import hierarchy
import connectors
import semantics


def register():
    """Register this generator.
    """
    import agx.generator.pyegg
    from agx.core.config import register_generator
    register_generator(agx.generator.pyegg)
