import cadquery as cq
params = {
	'H': 39,
	'W': 55,
	'h': 26,
	'w': 26,
    'fillet':9,
	}
class Fix ():
	def __init__(self, params:dict):
		self.__dict__.update(params)
	
	def __repr__(self):
		data = f'Fix\n'
		for key, value in self.__dict__.items():
			data += f'\t|{key}:{value}\n'
		return data
	
	def make(self):
		cut = ( cq.Sketch()
				.segment( (0,0),(0,-self.H))
				.segment( (self.w,-self.h))
				.segment( (self.W,- self.h))
				.segment( (self.W, 0))
				.close()
				.assemble()
				.reset()
				.vertices('<Y')
				.fillet(self.fillet)
				)
		res = (
			cq.Workplane()
			.box(60,45,2, centered = (False,False,False))
			.faces('>Z').workplane().center(5,39)
			.placeSketch(cut)
			.cutThruAll()
			)
		return res


class Plate():
	def __init__(self):
		self.pts = (
			(0,0),(0,55),(40,55),(40,0)
			)
		self.r = 2
	def make (self):
		res = (
			cq.Workplane()
			.pushPoints(self.pts)
			.circle(self.r)
			.extrude(10)
			)
		return res
"""
plate = Plate()
show_object(plate.make())
"""
fix = Fix(params)
show_object( fix.make())
