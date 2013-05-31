

all:
	python setup.py build_ext --inplace
	python setup_tmpl.py build_ext --inplace

clean:
	rm -rf build *.so wrap_particle{,_tmpl}.{c,cpp}
