------------------------------------------------------------------------------
Tutorial Title
------------------------------------------------------------------------------

Cython: Speed up Python and NumPy, Pythonize C, C++, and Fortran.

Cython: combine the best of Python, NumPy, and C(++) for world domination

Cython: Python for comfort; C, C++, and Fortran for speed

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
Enthought's five-day intensive scientific Python training course.  He has
developed course material for high-performance and parallel computing with
Python, and taught the `"Efficient Parallel Python for High-Performance
Computing"<http://conference.scipy.org/scipy2012/tutorials.php#ti-77>`_
tutorial at the SciPy 2012 conference.

Contact Email
------------------------------------------------------------------------------
ksmith@enthought.com

Which Track
------------------------------------------------------------------------------
Intermediate / Advanced

Tutorial Description
------------------------------------------------------------------------------
.. A description of the tutorial, suitable for posting on the SciPy website
.. for attendees to view. It should include the target audience, the expected
.. level of knowledge prior to the class, and the goals of the class.

Target audience:

    Developers, researchers, scientists, and engineers who use Python and
    NumPy and who routinely hit performance bottlenecks and need better
    performance.

    C / C++ / Fortran users who would like their existing code to work with
    Python.

Expected level of knowledge:

    Use Python and NumPy daily, or have taken an introductory Python and NumPy
    course or tutorial (the introductory Python / NumPy tutorial is
    sufficient).

    Have some familiarity with C, C++, or Fortran.

Goals:

    Overall goal: Cython competence.

    Understand what Cython is, what benefit it brings, when it is appropriate
    to use.

    Know how to create and use a setup.py file that will create an extension
    module using cython.

    Know how to use Cython with the IPython notebook.

    Know how to add cython type declarations to Python code.

    Know how to create cdef and cpdef functions and cdef classes in Cython.

    Know how to use Cython's typed memoryviews to work with buffer objects and
    C / C++ / Fortran arrays.

    Know how to identify cython bottlenecks and speed them up.

    Know how to wrap external C / C++ / Fortran 90 code with Cython.

    Know how to apply Cython's OpenMP-based parallelism to straightforward
    nested loops for further performance.


Outline
------------------------------------------------------------------------------
.. A more detailed outline of the tutorial content, including the duration of
.. each part, and exercise sessions. Please include a description of how you
.. plan to make the tutorial hands-on.

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

Documentation
------------------------------------------------------------------------------
.. If available, URL links to tutorial notes, slides, exercise files, ipython
.. notebooks, that you already have, even if they are preliminary.
