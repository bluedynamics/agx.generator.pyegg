Test agx.generator.pyegg
========================

Setup configuration and emulate main routine::

    >>> from zope.configuration.xmlconfig import XMLConfig

    >>> import agx.core
    >>> XMLConfig('configure.zcml', agx.core)()

    >>> from agx.core.main import parse_options

    >>> import os
    >>> modelpath = os.path.join(datadir, 'agx.testpackage.uml')
    >>> profilepath = os.path.join(datadir, '..', '..',
    ...                            'profiles', 'pyegg.profile.uml')
    >>> modelpaths = [modelpath, profilepath]
    >>> outdir = os.path.join(datadir, 'agx.testpackage')
    >>> controller = agx.core.Controller()
    >>> target = controller(modelpaths, outdir)
    >>> target
    <Directory object '/.../agx.generator.pyegg/src/agx/generator/pyegg/testing/data/agx.testpackage' at ...>

    >> target.printtree()
    <class 'node.ext.directory.directory.Directory'>: .../agx.testpackage
      <class 'node.ext.directory.directory.Directory'>: src
        <class 'node.ext.directory.directory.Directory'>: agx
          <class 'node.ext.python.nodes.Module'>: [1:2] - -1
            <class 'node.ext.python.nodes.Block'>: [2:2] - 0
          <class 'node.ext.directory.directory.Directory'>: testpackage
            <class 'node.ext.python.nodes.Module'>: [1:3] - -1
              <class 'node.ext.python.nodes.Block'>: [2:3] - 0
            <class 'node.ext.directory.directory.Directory'>: somepackage
              <class 'node.ext.python.nodes.Module'>: [1:3] - -1
                <class 'node.ext.python.nodes.Block'>: [2:3] - 0
              <class 'node.ext.python.nodes.Module'>: [1:25] - -1
                <class 'node.ext.python.nodes.Block'>: [2:3] - 0
                <class 'node.ext.python.nodes.Import'>: [5:5] - 0
                <class 'node.ext.python.nodes.Class'>: [7:25] - 0
                  <class 'node.ext.python.nodes.Attribute'>: [9:9] - 1
                  <class 'node.ext.python.nodes.Attribute'>: [10:10] - 1
                  <class 'node.ext.python.nodes.Function'>: [13:14] - 1
                    <class 'node.ext.python.nodes.Decorator'>: [12:12] - 1
                    <class 'node.ext.python.nodes.Block'>: [14:14] - 2
                  <class 'node.ext.python.nodes.Function'>: [17:18] - 1
                    <class 'node.ext.python.nodes.Decorator'>: [16:16] - 1
                    <class 'node.ext.python.nodes.Block'>: [18:18] - 2
                  <class 'node.ext.python.nodes.Function'>: [21:22] - 1
                    <class 'node.ext.python.nodes.Decorator'>: [20:20] - 1
                    <class 'node.ext.python.nodes.Block'>: [22:22] - 2
                  <class 'node.ext.python.nodes.Function'>: [24:25] - 1
                    <class 'node.ext.python.nodes.Block'>: [25:25] - 2
              <class 'node.ext.python.nodes.Module'>: [1:6] - -1
                <class 'node.ext.python.nodes.Block'>: [2:3] - 0
                <class 'node.ext.python.nodes.Function'>: [5:6] - 0
                  <class 'node.ext.python.nodes.Block'>: [6:6] - 1
            <class 'node.ext.python.nodes.Module'>: [1:21] - -1
              <class 'node.ext.python.nodes.Block'>: [2:3] - 0
              <class 'node.ext.python.nodes.Import'>: [5:5] - 0
              <class 'node.ext.python.nodes.Function'>: [7:8] - 0
                <class 'node.ext.python.nodes.Block'>: [8:8] - 1
              <class 'node.ext.python.nodes.Class'>: [10:11] - 0
                <class 'node.ext.python.nodes.Block'>: [11:11] - 1
              <class 'node.ext.python.nodes.Class'>: [13:14] - 0
                <class 'node.ext.python.nodes.Block'>: [14:14] - 1
              <class 'node.ext.python.nodes.Class'>: [16:17] - 0
                <class 'node.ext.python.nodes.Block'>: [17:17] - 1
              <class 'node.ext.python.nodes.Class'>: [19:21] - 0
                <class 'node.ext.python.nodes.Block'>: [21:21] - 1
                <class 'node.ext.python.nodes.Decorator'>: [?:?] - 0
      <class 'node.ext.template._api.JinjaTemplate'>: setup.py
