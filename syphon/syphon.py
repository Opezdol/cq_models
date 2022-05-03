import cadquery as cq

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

    def make(self):
        return (
                cq.Workplane()
                .circle(self.R)
                .extrude(self.H)
                )
def show(obj):
    show_object(obj.make(), name=obj.name)

res = Base(base_params)
show(res)
