from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files, copy_metadata, get_package_paths, is_module_satisfies


# Astropy needs bundled data files at runtime. The stock contrib hook uses
# collect_submodules('astropy'), but that isolated scan crashes in this conda
# environment. Enumerate submodules from the package directory instead.
datas = collect_data_files('astropy')

ply_files = []
for path, target in collect_data_files('astropy', include_py_files=True):
    if path.endswith(('_parsetab.py', '_lextab.py')):
        ply_files.append((path, target))

datas += ply_files

if is_module_satisfies('astropy >= 5.0'):
    datas += copy_metadata('astropy')
    datas += copy_metadata('numpy')

_pkg_base, pkg_dir_str = get_package_paths('astropy')
pkg_dir = Path(pkg_dir_str)

hiddenimports = []
for file_path in pkg_dir.rglob('*'):
    if '__pycache__' in file_path.parts:
        continue
    if file_path.suffix not in {'.py', '.pyd'}:
        continue

    relative = file_path.relative_to(pkg_dir)
    if file_path.name == '__init__.py':
        module_name = '.'.join(('astropy',) + relative.parent.parts)
    elif file_path.suffix == '.py':
        module_name = '.'.join(('astropy',) + relative.with_suffix('').parts)
    else:
        module_name = '.'.join(('astropy',) + tuple(relative.stem.split('.')))

    if module_name and module_name not in hiddenimports:
        hiddenimports.append(module_name)

if 'numpy.lib.recfunctions' not in hiddenimports:
    hiddenimports.append('numpy.lib.recfunctions')
if 'astropy_iers_data' not in hiddenimports:
    hiddenimports.append('astropy_iers_data')
if 'yaml' not in hiddenimports:
    hiddenimports.append('yaml')