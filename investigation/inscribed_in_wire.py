import cadquery as cq

# Create the wire to investigate
wire_under_investigation = (
    cq.Sketch()
    .arc((0, 0), 1.0, 0.0, 360.0)
    .arc((1, 1.5), 0.5, 0.0, 360.0)
    .segment((0.0, 2), (-1, 3.0))
    .hull()
    ._faces.Faces()[0]
).outerWire()
print(wire_under_investigation.Length())
#print (wire_under_investigation.paramAt(5))

dataPnts = [1,4,6,7,8,9,10 ]
pnts = wire_under_investigation.positions(dataPnts,mode='parameter')
nrmls = [wire_under_investigation.tangentAt(loc,mode='parameter') for loc in dataPnts]

for pnt, nrml in zip(pnts,nrmls):
    print(f'Point: {pnt}, Normal {nrml}')
    circle = cq.Sketch().circle(0.2)
    show_object(circle.moved(cq.Location(pnt)))

show_object(wire_under_investigation)

