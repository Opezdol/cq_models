import cadquery as cq
import math

base_params = {
        'R' : 40,
        'R2' : 45,
        'H2' : 3,
        'H' : 30,
        'wall': 2,
        'name': 'Base'
        }

class Base():

    def __init__(self, params):
        if isinstance(params,dict):
            self.__dict__.update(params)
        else:
            raise AttributeError(f' Dict as params from {self}')
        self.path = self.makePath()

    def make(self):
        return (
                cq.Workplane()
                .circle(self.R2)
                .extrude(self.H2)
                .faces('>Z').workplane()
                .circle(self.R).extrude(self.H)
                .faces('<Z').workplane()
                .circle(self.R-self.wall).cutThruAll()
                # prepare for sweep and sweep
                .faces('>Z').workplane()
                .sketch().circle(self.R).circle(self.R-self.wall)
                .finalize()
                .sweep(
                    self.path,
                    isFrenet=True,
                    clean=True,
                    )
                )

    def makePath(self):

        def _makeParametricWire(x):
            return (x, self.H*3 * math.sin(x/self.R/2),0)

        return (
                cq.Workplane('XZ')
                .center(0,self.H+self.H2)
                .parametricCurve(
                    _makeParametricWire,
                    N=50,
                    start = 0,
                    stop = self.R*2*math.pi,
                    makeWire=True,
                    )
                )


def show(obj):
    show_object(obj.make(), name=obj.name)

res = Base(base_params)
path = res.path
show_object(path, name='path')
show(res)
