------------------------------------------------------------------------------
Tutorial Title
------------------------------------------------------------------------------

Cython: Speed up Python and NumPy, Pythonize C, C++, and Fortran.

Author
------------------------------------------------------------------------------
Smith, Kurt, Enthought, Inc.

Bio
------------------------------------------------------------------------------
.. A short bio of the presenter or team members, containing a description of
.. past experiences as a trainer/teacher/speaker, and (ideally) links to
.. videos of these experiences if available.

Dr. Smith has been using Python in scientific computing for nearly ten years,
and has developed tools to simplify the integration of performance-oriented
languages with Python.  He has contributed to the Cython project, implementing
the initial version of the typed memoryviews and native cython arrays.  He
uses Cython extensively in his consulting work at Enthought.  He received his
B.S. in physics and applied mathematics from the University of Dallas, and his
Ph.D. in physics from the University of Wisconsin-Madison.  His doctoral
research focused on the application of fluid plasma models to astrophysical
systems, involving the composition of high-performance parallel simulations of
plasma turbulence.

Dr. Smith has trained hundreds of scientists, engineers, and researchers in
Python, NumPy, Cython, and parallel and high-performance computing as part of
Enthought's five-day scientific Python training course.  He has developed
course material for high-performance and parallel computing with Python, and
taught the `"Efficient Parallel Python for High-Performance
Computing"<http://conference.scipy.org/scipy2012/tutorials.php#ti-77>`_
tutorial at the SciPy 2012 conference.

Contact Email
------------------------------------------------------------------------------
ksmith@enthought.com

Which Track
------------------------------------------------------------------------------
Advanced

Tutorial Description
------------------------------------------------------------------------------
.. A description of the tutorial, suitable for posting on the SciPy website
.. for attendees to view. It should include the target audience, the expected
.. level of knowledge prior to the class, and the goals of the class.

Cython is a flexible and multi-faceted tool that brings down the barrier
between Python and other languages.  With cython, you can add type information
to your Python code to yield dramatic performance improvements.  Cython also
allows you to wrap C, C++ and Fortran libraries to work with Python and NumPy.
It is used extensively in research environments and in end-user applications.

This hands-on tutorial will cover Cython from the ground up, and will include
the newest Cython features, including typed memoryviews.

Target audience:

    Developers, researchers, scientists, and engineers who use Python and
    NumPy and who routinely hit bottlenecks and need improved performance.

    C / C++ / Fortran users who would like their existing code to work with
    Python.

Expected level of knowledge:

    Intermediate and / or regular user of Python and NumPy.  Have used
    Python's decorators, exceptions, and classes.  Knowledge of NumPy arrays,
    array views, fancy indexing, and NumPy dtypes.  Have programmed in at
    least one of C, C++, or Fortran.
    
    Some familiarity with the Python or NumPy C-API a plus.  Familiarity with
    memoryviews and buffers a plus.  Familiarity with OpenMP a plus.
    Array-based inter-language programming between Python and C, C++, or
    Fortran a plus.

Goals:

    Overall goal: Cython familiarity for newcomers, Cython competence for
    those with some experience.

    Understand what Cython is, what benefit it brings, when it is appropriate
    to use.

    Know how to create and use a setup.py file that will create an extension
    module using cython.

    Know how to use Cython from within the IPython notebook.

    Know how and why to add cython type declarations to Python code.

    Know how to create cdef and cpdef functions and cdef classes in Cython.

    Know how to use Cython's typed memoryviews to work with buffer objects and
    C / C++ / Fortran arrays.

    Know how to identify cython bottlenecks and speed them up.

    Know how to wrap external C / C++ / Fortran 90 code with Cython.

    Know how to handle inter-language error states with Cython.

    Know how to apply Cython's OpenMP-based parallelism to straightforward
    nested loops for further performance.


Outline
------------------------------------------------------------------------------
.. A more detailed outline of the tutorial content, including the duration of
.. each part, and exercise sessions. Please include a description of how you
.. plan to make the tutorial hands-on.

Cython overview, basic usage / workflow (30 minutes)

    Simple example (compiling the `sinc` function or similar); .pyx files;
    setup.py files; Python extension modules; pure Python mode; crossing the
    py2 - py3 divide with cython; Cython within IPython / IPython notebook.

    Exercise: get `add(a,b)` function to compile with Cython using .pyx and
    setup.py and from within an IPython notebook.

Adding type information (30 minutes)

    def, cdef, cpdef functions; cdef variables; cython generated source code;
    performance difference between Cython & Python; tradeoffs with using typed
    variables.

    Exercise: cythonize `sinc()` function by adding type information, and
    vectorize it with numpy's `vectorize` decorator.  Compare performance to
    pure-python `sinc()` kernel.

Wrapping external C libraries (30 minutes)

    `cdef extern from` block, declaring external functions and typedefs;
    wrapping external functions; declaring external structures; dealing with
    "const"; 

    Exercise: create `get_date()` function that wraps `time()` and
    `localtime()` from "time.h".

    Alternative exercise: wrap simple 1D interpolation routine from GSL.

cdef classes / extension types (20 minutes)

    Difference between "class Foo" and "cdef class Foo" in Cython; extension
    type data / attributes, how different from regular class attributes;
    `__cinit__()` and `__dealloc__()`; extension type inheritance limitations.

    Demo of creating a particle `cdef class` in Cython.

Wrapping C++ classes (30 minutes)

    Simple example -- wrap shape C++ class; `cdef cppclass` declarations;
    creating a `cdef class` wrapper around a C++ class; using a thisptr;
    memory management.

    Exercise: wrap a simple C++ shape class with a `cdef class` extension
    type, using `__cinit__`, `__dealloc__` and an internal thisptr.

typed memoryviews, fused types (30 minutes)

    Python buffers and memoryviews, NumPy arrays; Cython's typed memoryviews,
    syntax and basic example; different declarations -- C / Fortran
    contiguous, direct, indirect, strided, generic, etc; interop with NumPy
    arrays and C / C++ / Fortran arrays; supported operations, performance;
    cython built-in arrays (Fused types will be covered if time permitting.)

    Demo: Implement distance matrix (matrix of "distances" between pairs of
    points) calculation using typed memoryviews.

Capstone exercise: Compute Julia sets (50 minutes)

    `$ cython -a foo.pyx` -- annotations and how to use them; pure python code
    for computing Julia set; pure python performance; first step: add type
    information to scalars; second step: def -> cdef; third step: type arrays
    as memoryviews; fourth step: add cython decorators; fifth step: use
    prange.

Package List
------------------------------------------------------------------------------
.. A list of Python packages that attendees will need to have installed prior
.. to the class to follow along. Please mention if any packages are not cross
.. platform. Installation instructions or links to installation documentation
.. should be provided for packages that are not available through
.. easy_install, pip, EPD, Anaconda, etc., or that require third party
.. libraries.

All necessary packages are available with an academic / full EPD installation,
Anaconda, easy_install, or pip.

Users must have Cython >= 0.16 for the course.

The tutorial material (slides, exercises & demos) will be available for
download and on USB drives.

Documentation
------------------------------------------------------------------------------
.. If available, URL links to tutorial notes, slides, exercise files, ipython
.. notebooks, that you already have, even if they are preliminary.

Basic slide content is based on Enthought's Cython training slides.  These
slides will be reworked significantly for this tutorial.  In particular, the
NumPy buffer declarations will be taken out and replaced with the typed
memoryview content listed in the outline.  Other content (an IPython notebook
with the start of the capstone project) is available as well::

    http://www.enthought.com/~public_content/ksmith/scipy2013_cython
