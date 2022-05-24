from cadquery import Workplane, Vector, Face, Plane

class Part():
    """
    class Part describes interaction between two parts
    all parameters of the part during creation available as attributes

    """
    def __init__(self, params = {}: dict):
        if params isinstance(params, dict):
            for key,value in params.items():
                # add key: value to self class 
                # nocheck for key as str
                # TODO convertion key from params to string 
                self.__dict__.update(params)
        else:
            raise ValueError('Params of model should be passed as dict')

    def test(self):
        for key, value in self.__dict__.items():
            print(f'{key}--\t->{value}')

class PlateAdhesive(Part):
    """ std plate for goPro mount """
    params = {
        "width":36,
        "length": 47,
        "heigth": 13,
        "c_height": 2,
        "c_width": 4,
        "c_length": 34,
        }
    def __init__(self):
        super().__init(params = PlateAdhesive.params)




