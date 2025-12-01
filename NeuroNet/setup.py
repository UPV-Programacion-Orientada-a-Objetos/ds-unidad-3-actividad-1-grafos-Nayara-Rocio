from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy

extensions = [
    Extension(
        "neuronet",
        sources=["neuronet.pyx", "sparse_graph.cpp"],
        language="c++",
        extra_compile_args=["-std=c++11", "-O3", "-march=native"],
        extra_link_args=["-std=c++11"],
        include_dirs=[numpy.get_include(), "."]
    )
]

setup(
    name="neuronet",
    ext_modules=cythonize(extensions, compiler_directives={'language_level': 3}),
    zip_safe=False,
)