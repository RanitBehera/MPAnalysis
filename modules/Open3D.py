import open3d,numpy

def DrawLine(vis,p1:tuple,p2:tuple,color=[0.5,0.5,0.5]):
    line_set=open3d.geometry.LineSet()
    line_set.points=open3d.utility.Vector3dVector([p1,p2])
    line_set.lines=open3d.utility.Vector2iVector([[0,1]])
    line_set.colors=open3d.utility.Vector3dVector([color])
    vis.add_geometry(line_set)


def DrawBox(vis,origin:tuple,dimensions:tuple,color=[0.5,0.5,0.5]):
    Ox,Oy,Oz=origin[0],origin[1],origin[2]
    dx,dy,dz=dimensions[0],dimensions[1],dimensions[2]

    p0=[Ox,Oy,Oz]
    p1=[Ox+dx,Oy,Oz]
    p2=[Ox+dx,Oy+dy,Oz]
    p3=[Ox,Oy+dy,Oz]
    p4=[Ox,Oy,Oz+dz]
    p5=[Ox+dx,Oy,Oz+dz]
    p6=[Ox+dx,Oy+dy,Oz+dz]
    p7=[Ox,Oy+dy,Oz+dz]

    vertices=[p0,p1,p2,p3,p4,p5,p6,p7]
    edges=[[0,1],[1,2],[2,3],[3,0],[0,4],[4,5],[5,6],[6,7],[7,4],[1,5],[2,6],[3,7]]
    edgecolor=numpy.outer(numpy.ones((len(edges),1)),color)

    line_set=open3d.geometry.LineSet()
    line_set.points=open3d.utility.Vector3dVector(vertices)
    line_set.lines=open3d.utility.Vector2iVector(edges)
    line_set.colors=open3d.utility.Vector3dVector(edgecolor)

    vis.add_geometry(line_set)