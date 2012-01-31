from agx.core import (
    handler,
    token,
)
from agx.core.util import (
    read_target_node,
    dotted_path,
)
from agx.generator.pyegg.utils import class_base_name
from node.ext.uml.utils import (
    TaggedValues,
    UNSET,
)
from node.ext.directory.interfaces import IDirectory
from node.ext.directory import Directory
from node.ext.template import JinjaTemplate
from node.ext import python
from node.ext.python.utils import Imports
from agx.generator.pyegg.utils import (
    templatepath,
    set_copyright,
)


@handler('eggdocuments', 'uml2fs', 'hierarchygenerator',
         'pythonegg', order=10)
def eggdocuments(self, source, target):
    """Create egg default documents.
    """
    target = target.anchor
    if not 'src' in target:
        target['src'] = Directory()


@handler('eggsetup', 'uml2fs', 'hierarchygenerator',
         'pythonegg', order=10)
def eggsetup(self, source, target):
    """Create egg ``setup.py``.
    """
    root = target.anchor
    root.factories['setup.py'] = JinjaTemplate
    
    tgv = TaggedValues(source)
    version = tgv.direct('version', 'pyegg:pyegg', '1.0')
    project = source.name
    
    cp = tgv.direct('copyright', 'pyegg:pyegg', '')
    cp = cp.split(',')
    cp = [line.strip() for line in cp]
    
    description = tgv.direct('description', 'pyegg:pyegg', '')
    
    classifiers = tgv.direct('classifiers', 'pyegg:pyegg', '')
    classifiers = classifiers.split(',')
    classifiers = [cla.strip() for cla in classifiers]
    
    keywords = tgv.direct('keywords', 'pyegg:pyegg', '')
    
    author = tgv.direct('author', 'pyegg:pyegg', '')
    author_email = tgv.direct('email', 'pyegg:pyegg', '')
    
    url = tgv.direct('url', 'pyegg:pyegg', '')
    
    license_name = tgv.direct('license', 'pyegg:pyegg', '')
    
    namespace = project.split('.')
    namespace_packages = list()
    if len(namespace) > 1:
        for i in range(len(namespace) - 1):
            namespace_packages.append('"%s"' % '.'.join(namespace[:i + 1]))
    namespace_packages = ', '.join(namespace_packages)
    
    zip_safe = tgv.direct('zipsafe', 'pyegg:pyegg', 'False')
    
    if 'setup.py' in root:
        setup = root['setup.py']
    else:
        setup = JinjaTemplate()
    
    setup.template = templatepath('setup.py.jinja')
    setup.params = {'cp': cp,
                    'version': version,
                    'project': project,
                    'description': description,
                    'classifiers': classifiers,
                    'keywords': keywords,
                    'author': author,
                    'author_email': author_email,
                    'url': url,
                    'license_name': license_name,
                    'namespace_packages': namespace_packages,
                    'zip_safe': zip_safe,}
    
    if 'README.rst' in root:
        readme = root['README.rst']
    else:
        readme = JinjaTemplate()
    
    readme.template = templatepath('README.rst.jinja')
    #give it the same params as setup.py
    readme.params = setup.params
    root['README.rst'] = readme


@handler('eggdirectories', 'uml2fs', 'hierarchygenerator',
         'pythonegg', order=20)
def eggdirectories(self, source, target):
    """Create egg directory structure and corresponding ``__init__.py`` files.
    """
    package = target.anchor['src']
    names = source.name.split('.')    
    for i in range(len(names)):
        if not names[i] in package:
            package[names[i]] = Directory()
        package = package[names[i]]
        module = python.Module()
        package['__init__.py'] = module
        if i < len(names) - 1:
            if not module.blocks():
                block = python.Block()
                block.text = u"__import__('pkg_resources')" + \
                             u".declare_namespace(__name__)"
                module['ns_dec'] = block
        else:
            set_copyright(source, module)
    
    #store all pyeggs in a token
    eggtok = token('pyeggs', True, packages=set(), directories=set())
    eggtok.packages.add(source)
    eggtok.directories.add(package)
    target.finalize(source, package)


@handler('pypackage', 'uml2fs', 'hierarchygenerator', 'pypackage', order=30)
def pypackage(self, source, target):
    """Create python packages.
    """
    if not len(target.anchor):
        raise Exception(u"Invalid egg structure. Is ``pyegg`` stereotype "
                        u"applied on root package in UML model?")
    if not source.name in target.anchor:
        target.anchor[source.name] = Directory()
    package = target.anchor[source.name]
    module = python.Module()
    package['__init__.py'] = module
    set_copyright(source, module)
    target.finalize(source, package)


@handler('pymodule', 'uml2fs', 'hierarchygenerator', 'pymodule', order=30)
def pymodule(self, source, target):
    """Create python modules.
    """
    module = python.Module()
    container = target.anchor
    container['%s.py' % source.name] = module
    set_copyright(source, module)
    #store all pymodules in a token
    modtok = token('pymodules', True, modules=set())
    modtok.modules.add(module)
    target.finalize(source, module)


@handler('pyclass', 'uml2fs', 'hierarchygenerator', 'pyclass', order=30)
def pyclass(self, source, target):
    """Create python classes.
    """
    if source.stereotype('pyegg:stub') is not None:
        return
    name = source.name
    module = target.anchor
    set_copyright(source, module)
    if module.classes(name):
        class_ = module.classes(name)[0]
        target.finalize(source, class_)
        return
    class_ = python.Class(name)
    module[str(class_.uuid)] = class_
    if not source.stereotype('pyegg:function') \
      and not source.parent.stereotype('pyegg:pymodule'):
        imp = Imports(module.parent['__init__.py'])
        imp.set(class_base_name(class_), [[class_.classname, None]])
    target.finalize(source, class_)


@handler('pyfunction', 'uml2fs', 'hierarchygenerator', 'pyfunction', order=30)
def pyfunction(self, source, target):
    """Create python functions.
    """
    def set_args_kwargs(source, function):
        tgv = TaggedValues(source)
        _args = tgv.direct('args', 'pyegg:function')
        _kwargs = tgv.direct('kwargs', 'pyegg:function')
        if _args is not UNSET:
            function.s_args = _args
        if _kwargs is not UNSET:
            function.s_kwargs = _kwargs
    name = source.name
    container = target.anchor
    if container.functions(name):
        function = container.functions(name)[0]
        set_args_kwargs(source, function)
        target.finalize(source, function)
        return
    function = python.Function(name)
    container[str(function.uuid)] = function
    set_args_kwargs(source, function)
    target.finalize(source, function)


@handler('pydecorator', 'uml2fs', 'hierarchygenerator', 'pydecorator', order=40)
def pydecorator(self, source, target):
    """Create Decorator.
    """
    tgv = TaggedValues(source)
    name = tgv.direct('name', 'pyegg:decorator')
    args = tgv.direct('args', 'pyegg:decorator', None)
    kwargs = tgv.direct('kwargs', 'pyegg:decorator', None)
    container = read_target_node(source, target.target)
    if container.decorators(name):
        decorator = container.decorators(name)[0]
    else:
        decorator = python.Decorator(name)
        container[str(decorator.uuid)] = decorator
    if args is not None:
        decorator.s_args = args
    if kwargs is not None:
        decorator.s_kwargs = kwargs


@handler('pyattribute', 'uml2fs', 'hierarchygenerator', 'pyattribute', order=40)
def pyattribute(self, source, target):
    """Create Attribute.
    """
    expression = None
    tgv = TaggedValues(source)
    expression = tgv.direct('expression', 'pyegg:expression', None)
    name = source.name
    container = target.anchor
    if container.attributes(name):
        attribute = container.attributes(name)[0]
        if expression is not None:
            attribute.value = expression
        target.finalize(source, attribute)
        return
    value = expression is not None and expression or 'None' 
    attribute = python.Attribute([name], value=value)
    container[str(attribute.uuid)] = attribute
    target.finalize(source, attribute)