# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec file for Janken."""

import pkg_resources

block_cipher = None


def EntryPoint(dist, group, name, **kwargs):
    """Custom entry point "constructor" function to locate entry points."""

    # get toplevel packages of distribution from metadata
    def get_toplevel(dist):
        distribution = pkg_resources.get_distribution(dist)
        if distribution.has_metadata('top_level.txt'):
            return list(distribution.get_metadata('top_level.txt').split())
        else:
            return []

    kwargs.setdefault('hiddenimports', [])
    packages = []
    for distribution in kwargs['hiddenimports']:
        packages += get_toplevel(distribution)

    kwargs.setdefault('pathex', [])
    # get the entry point
    ep = pkg_resources.get_entry_info(dist, group, name)
    # insert path of the egg at the verify front of the search path
    kwargs['pathex'] = [ep.dist.location] + kwargs['pathex']
    # script name must not be a valid module name to avoid name clashes on
    # import
    script_path = os.path.join(workpath, name + '-script.py')
    print('creating script for entry point', dist, group, name)
    with open(script_path, 'w') as f:
        print('import', ep.module_name, file=f)
        print('{!s}.{!s}()'.format(ep.module_name, '.'.join(ep.attrs)), file=f)
        for package in packages:
            print("import", package, file=f)

    return Analysis([script_path] + kwargs.get('scripts', []), **kwargs)

a = EntryPoint(
    'janken', 'console_scripts', 'janken',
    datas=[(pkg_resources.resource_filename('janken', 'data'), 'janken/data')],
    hiddenimports=['tabulate'],
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='janken',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          icon='wrpsa.ico',
)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='janken'
)
