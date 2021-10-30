import os
from collections import OrderedDict

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# http://docs.cython.org/en/latest/src/userguide/source_files_and_compilation.html#distributing-cython-modules
cython_extension = ".c"
if os.getenv("USE_CYTHON"):
    print("USE_CYTHON enabled")
    cython_extension = ".pyx"

extensions = [
    setuptools.extension.Extension("pybmoore._bm", [f"pybmoore/_bm{cython_extension}"])
]

if os.getenv("USE_CYTHON"):
    from Cython.Build import cythonize

    extensions = cythonize(
        extensions,
        annotate=True,
        compiler_directives={"language_level": 3},
    )

with open("pybmoore/__version__.py", "r") as f:
    *_, __version__ = f.read().partition("=")
__version__ = __version__.strip(" \n'\"")


setuptools.setup(
    name="pybmoore",
    version=f"{__version__}",
    author="alexandre menezes",
    author_email="alexandre.fmenezes@gmail.com",
    description="Python/Cython Boyer-Moore string-search algorithm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache-2.0",
    url="https://github.com/amenezes/pybmoore",
    packages=setuptools.find_packages(include=["pybmoore", "pybmoore.*"]),
    python_requires=">=3.6.0",
    platforms=["macOS", "POSIX"],
    ext_modules=extensions,
    project_urls=OrderedDict(
        (
            ("Documentation", "https://github.com/amenezes/pybmoore"),
            ("Code", "https://github.com/amenezes/pybmoore"),
            ("Issue tracker", "https://github.com/amenezes/pybmoore/issues"),
        )
    ),
    tests_require=[
        "flake8",
        "pytest",
        "pytest-cov",
        "isort",
        "black",
        "mypy",
        "tox",
        "codecov",
        "safety",
        "Cython",
    ],
    setup_requires=["setuptools>=38.6.0"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Cython",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
