from jinja2 import Template

result = Template(open('wrap_particle_tmpl.pyx.in').read()).render(floatings='double float'.split())
# result = Template(open('wrap_particle_tmpl.pyx.in').read()).render()
print result
open('wrap_particle_tmpl_jinja.pyx', 'w').write(result)
