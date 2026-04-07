from packaging.version import Version

from PyInstaller import compat
from PyInstaller.utils.hooks import collect_dynamic_libs, conda_support, get_installer


numpy_version = Version(compat.importlib_metadata.version("numpy")).release
numpy_installer = get_installer("numpy")

hiddenimports = []
datas = []
binaries = []

# NumPy 2.x imports some Python helpers from extension modules at runtime.
# Keeping the package available on the filesystem avoids mixed PYZ/filesystem
# lookup issues in frozen builds.
module_collection_mode = {"numpy": "pyz+py"}

# Collect numpy's bundled extension DLLs.
binaries += collect_dynamic_libs("numpy")

# Collect shared runtime dependencies from the active conda environment.
if numpy_installer == "conda":
    datas += conda_support.collect_dynamic_libs("numpy", dependencies=True)

# Submodules imported only from extension modules are not always visible to
# PyInstaller's module graph and must be listed explicitly.
if numpy_version >= (2, 0):
    hiddenimports += [
        "numpy._core._dtype_ctypes",
        "numpy._core._multiarray_tests",
    ]
else:
    hiddenimports += ["numpy.core._dtype_ctypes"]
    if numpy_version >= (1, 25):
        hiddenimports += ["numpy.core._multiarray_tests"]

if numpy_version >= (2, 3, 0):
    hiddenimports += ["numpy._core._exceptions"]

excludedimports = [
    "scipy",
    "pytest",
    "nose",
    "f2py",
    "setuptools",
]

if numpy_version < (1, 22, 0) or numpy_version > (1, 22, 1):
    excludedimports += [
        "distutils",
        "numpy.distutils",
    ]

if numpy_version < (2, 0):
    excludedimports += ["numpy.f2py"]
