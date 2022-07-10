import os

import setuptools

# http://docs.cython.org/en/latest/src/userguide/source_files_and_compilation.html#distributing-cython-modules
extension = ".c"

if os.getenv("USE_CYTHON"):
    extension = ".pyx"

extensions = [
    setuptools.extension.Extension("pybmoore._bm", [f"pybmoore/_bm{extension}"])
]

if os.getenv("USE_CYTHON"):
    from Cython.Build import cythonize

    extensions = cythonize(
        extensions,
        annotate=True,
        compiler_directives={"language_level": 3},
    )

setuptools.setup(ext_modules=extensions)
