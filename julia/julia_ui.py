# --- Imports
import numpy as np

from traits.api import HasTraits, Float, Instance, Array, on_trait_change, DelegatesTo, Property, Int
from traitsui.api import View, Item, RangeEditor, Controller
from chaco.api import Plot, ArrayPlotData, jet, OrRd
from enable.api import ComponentEditor

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
    module_name = module_name.rsplit('.py')[0]
    return getattr(__import__(module_name), function_name)

# --- Traits classes.

class Julia(HasTraits):

    runtime = Float()
    cr = Float(-0.1)
    ci = Float(0.651)
    resolution = Int(100)
    julia = Array()
    
    @on_trait_change('cr, ci, resolution')
    def update_julia(self):
        self.julia = self.compute()
        
    def _julia_default(self):
        return self.compute()
    
    def compute(self):
        julia, self.runtime = compute_julia(self.cr, self.ci, self.resolution, lim=4., cutoff=1e4)
        return np.log(julia)


class JuliaUI(Controller):
    
    model = Instance(Julia)
    runtime = Property(depends_on=['model.runtime'])
    plot = Instance(Plot)
    
    traits_view = View(Item('controller.plot', editor=ComponentEditor(), show_label=False),
                       Item('resolution', editor=RangeEditor(low=100, high=1000, mode='slider')),
                       Item('cr', editor=RangeEditor(low=-2.0, high=2.0)),
                       Item('ci', editor=RangeEditor(low=-2.0, high=2.0)),
                       Item('controller.runtime', style='readonly', show_label=False),
                       width=800, height=900, resizable=True,
                       title="Julia Set Explorer")
    
    @on_trait_change('model.runtime')
    def _get_runtime(self):
        return "Compute time: {:d} ms".format(int(round(self.model.runtime * 1000)))
    
    @on_trait_change('model.julia')
    def update_julia(self):
        self.plot.data.set_data('julia', self.model.julia)
    
    def _plot_default(self):
        julia = self.model.julia
        apd = ArrayPlotData(julia=julia[:-1,:-1])
        grid = np.linspace(-2, 2, self.model.resolution-1)
        X, Y = np.meshgrid(grid, grid)
        plot = Plot(apd)
        plot.aspect_ratio = 1.0
        plot.img_plot("julia", xbounds=X, ybounds=Y, colormap=OrRd, interpolation='bicubic')
        return plot
        
if __name__ == '__main__':
    from argparse import ArgumentParser
    compiler('setup.py')
    compute_julia = importer('julia_cython_solution', 'compute_julia_opt')
    julia = Julia()
    jui = JuliaUI(model=julia)
    jui.configure_traits()
