all:
	python setup.py build_ext --inplace

test: all
	python test_hello_world.py

clean:
	rm -r build cython_hello_world.{c,so}
