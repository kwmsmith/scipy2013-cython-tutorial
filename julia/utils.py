from subprocess import check_call

def compiler(setup_name):
    import sys, platform
    exe = sys.executable
    extras = []
    if platform.system() == 'Windows':
        extras = ['--compiler=mingw32']
    cmd = [exe, setup_name, 'build_ext', '--inplace'] + extras
    print cmd
    check_call(cmd)

def importer(module_name, function_name):
    for ending in ('.py', '.pyc', '.so', '.pyd'):
        module_name = module_name.rsplit(ending)[0]
    mod = __import__(module_name)
    try:
        return getattr(mod, function_name)
    except AttributeError:
        raise ImportError("cannot import name %s" % function_name)
