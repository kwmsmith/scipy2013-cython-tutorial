# --- Imports
from time import time as clock_time

import numpy as np

from traits.api import HasTraits, Float, Instance, Array, on_trait_change, DelegatesTo, Property
from traitsui.api import View, Item, RangeEditor, HGroup
from chaco.api import Plot, ArrayPlotData
from enable.api import ComponentEditor

from harmonograph import compute

# --- Traits classes.

class Oscillator(HasTraits):

    amp = Float(1.0)
    freq = Float(5.0)
    phase = Float(0.0)
    damping = Float(0.01)
    
    traits_view = View(
            Item('amp', editor=RangeEditor(low=1.0, high=5.0, low_label='', high_label='', mode='slider'), show_label=False),
            Item('freq', editor=RangeEditor(low=10.0, high=10.5, low_label='', high_label='', mode='slider'), show_label=False),
            Item('phase', editor=RangeEditor(low=0.0, high=2. * np.pi, low_label='', high_label='', mode='slider'), show_label=False),
            Item('damping', editor=RangeEditor(low=0.0, high=0.1, low_label='', high_label='', mode='slider'), show_label=False),
            )
    
oscs = '[osc0, osc1, osc2, osc3]'
attrs = 'amp freq phase damping'.split()
depon = ', '.join('%s.%s' % (oscs, attr) for attr in attrs)

class Harmonograph(HasTraits):

    runtime = Float()
    time = Array()
    xy = Property(depends_on=['time, ' + depon])
    osc0 = Instance(Oscillator, args=())
    osc1 = Instance(Oscillator, args=())
    osc2 = Instance(Oscillator, args=())
    osc3 = Instance(Oscillator, args=())
    
    def _time_default(self):
        return np.linspace(0, 10, 1000)
    
    def _get_xy(self):
        return self.compute()
    
    def compute(self):
        t0 = clock_time()
        oscs = [self.osc0, self.osc1, self.osc2, self.osc3]
        amps = [o.amp for o in oscs]
        fs = [o.freq for o in oscs]
        phs = [o.phase for o in oscs]
        ds = [o.damping for o in oscs]
        xy = compute(self.time, amps, fs, phs, ds)
        t1 = clock_time() - t0
        self.runtime = t1
        return xy
    
    @on_trait_change(depon)
    def update(self):
        self.xy = self.compute()


class HarmonographUI(HasTraits):
    
    DELTA = Float(0.01)

    model = Instance(Harmonograph)
    runtime = Property(depends_on=['model.runtime'])
    framerate = Property(depends_on=['model.runtime'])
    xy = DelegatesTo('model')
    osc0 = DelegatesTo('model')
    osc1 = DelegatesTo('model')
    osc2 = DelegatesTo('model')
    osc3 = DelegatesTo('model')
    plot = Instance(Plot)
    totaltime = Float(20.)
    starttime = Float(0.0)
    
    traits_view = View(Item('plot', editor=ComponentEditor(), show_label=False),
            Item('starttime', editor=RangeEditor(low=0.0, high=50, mode='slider')),
            Item('totaltime', editor=RangeEditor(low=10, high=50, mode='slider')),
            HGroup(
                Item('osc0', style='custom', show_label=False),
                Item('osc1', style='custom', show_label=False),
                Item('osc2', style='custom', show_label=False),
                Item('osc3', style='custom', show_label=False),
                ),
            Item('framerate', style='readonly'),
            width=800,
            height=600,
            resizable=True)
    
    def _get_framerate(self):
        return "{:d} FPS".format(int(1. / (self.model.runtime)))
    
    @on_trait_change('starttime, totaltime')
    def update(self):
        self.model.time = np.linspace(self.starttime, self.starttime + self.totaltime, int(self.totaltime / self.DELTA))
        
    def _xy_changed(self):
        self.plot.data.set_data('x', self.xy[0])
        self.plot.data.set_data('y', self.xy[1])
    
    def _plot_default(self):
        x, y = self.xy
        apd = ArrayPlotData(x=x, y=y)
        plot = Plot(apd)
        plot.plot(('x', 'y'))
        return plot
        
if __name__ == '__main__':
    hg = Harmonograph()
    hui = HarmonographUI(model=hg)
    hui.configure_traits()
