import open3d,numpy

## --- WINDOW

class Open3DWindow:
    DEFAULT_BG_COLOR=[0,0,0]
    DEFAULT_WIREFRAME_COLOR=[1,1,1]
    def __init__(self,title:str="Open3D",width:int=800,height:int=600):
        self.vis=open3d.visualization.VisualizerWithKeyCallback()
        self.vis.create_window(title,width,height)
        self.RegisterExtraKeyBindings()
        self.SetBackgroundColor()
        self.dm={"Visibility":False,"Cloud":None}
        self.gas={"Visibility":False,"Cloud":None}
        self.star={"Visibility":False,"Cloud":None}
        self.bh={"Visibility":False,"Cloud":None}

    def RegisterExtraKeyBindings(self):
        self.tranlate_factor=0.1
        self.rotate_factor=20

        def KeyE(vis):  # Forward Move
            vis.get_view_control().camera_local_translate(self.tranlate_factor,0,0)
        def KeyQ(vis):  # Backward Move
            vis.get_view_control().camera_local_translate(-self.tranlate_factor,0,0)
        def KeyD(vis):  # Look Right
            vis.get_view_control().camera_local_rotate(self.rotate_factor,0,0,0)
        def KeyA(vis):  # Look Left
            vis.get_view_control().camera_local_rotate(-self.rotate_factor,0,0,0)
        def KeyW(vis):  # Look Up
            vis.get_view_control().camera_local_rotate(0,-self.rotate_factor,0,0)
        def KeyS(vis):  # Look Down
            vis.get_view_control().camera_local_rotate(0,self.rotate_factor,0,0)
        
        def Key0(vis):  # DM Toggle
            if self.dm["Cloud"]==None: return
            if self.dm["Visibility"]:self.vis.remove_geometry(self.dm["Cloud"],False)
            else:self.vis.add_geometry(self.dm["Cloud"],False)
            self.dm["Visibility"]=not self.dm["Visibility"]
        def Key1(vis):  # Gas Toggle
            if self.gas["Cloud"]==None: return
            if self.gas["Visibility"]:self.vis.remove_geometry(self.gas["Cloud"],False)
            else:self.vis.add_geometry(self.gas["Cloud"],False)
            self.gas["Visibility"]=not self.gas["Visibility"]
        def Key2(vis):  # Star Toggle
            if self.star["Cloud"]==None: return
            if self.star["Visibility"]:self.vis.remove_geometry(self.star["Cloud"],False)
            else:self.vis.add_geometry(self.star["Cloud"],False)
            self.star["Visibility"]=not self.star["Visibility"]
        def Key3(vis):  # BH Toggle
            if self.bh["Cloud"]==None: return
            if self.bh["Visibility"]:self.vis.remove_geometry(self.bh["Cloud"],False)
            else:self.vis.add_geometry(self.bh["Cloud"],False)
            self.bh["Visibility"]=not self.bh["Visibility"]

        self.vis.register_key_callback(ord('E'),KeyE)  # Move Forward
        self.vis.register_key_callback(ord('Q'),KeyQ)  # Move Backward
        self.vis.register_key_callback(ord('D'),KeyD)  # Look Right
        self.vis.register_key_callback(ord('A'),KeyA)  # Look Left
        self.vis.register_key_callback(ord('W'),KeyW)  # Look Up
        self.vis.register_key_callback(ord('S'),KeyS)  # Look Down 

        self.vis.register_key_callback(ord('0'),Key0)  # DM Toggle 
        self.vis.register_key_callback(ord('1'),Key1)  # Gas Toggle 
        self.vis.register_key_callback(ord('2'),Key2)  # Star Toggle 
        self.vis.register_key_callback(ord('3'),Key3)  # BH Toggle 
            
            





    def SetBackgroundColor(self,bgcolor=DEFAULT_BG_COLOR):
        self.vis.get_render_option().background_color = numpy.asarray(bgcolor)

    def SetLookAt(self,point):
        self.lookatpoint=point

    def Show(self):
        self.vis.run()
        self.vis.destroy_window()
        
    def GetPointCloud(self,points,colors):
        pcd= open3d.geometry.PointCloud()
        pcd.points=open3d.utility.Vector3dVector(points)
        if len(colors)==1:pcd.paint_uniform_color(colors[0])
        elif len(colors)==len(points): pcd.colors=open3d.utility.Vector3dVector(colors)
        else: raise(IndexError)
        return pcd

    def DarkMatter(self,points,colors):
        if not self.dm["Cloud"]==None:self.vis.clear_geometry(self.dm["Cloud"])
        self.dm["Visibility"]=True
        self.dm["Cloud"]=self.GetPointCloud(points,colors)
        self.vis.add_geometry(self.dm["Cloud"])

    def Gas(self,points,colors):
        if not self.gas["Cloud"]==None:self.vis.clear_geometry(self.gas["Cloud"])
        self.gas["Visibility"]=True
        self.gas["Cloud"]=self.GetPointCloud(points,colors)
        self.vis.add_geometry(self.gas["Cloud"])

    def Star(self,points,colors):
        if not self.star["Cloud"]==None:self.vis.clear_geometry(self.star["Cloud"])
        self.star["Visibility"]=True
        self.star["Cloud"]=self.GetPointCloud(points,colors)
        self.vis.add_geometry(self.star["Cloud"])

    def Blackhole(self,points,colors):
        if not self.bh["Cloud"]==None:self.vis.clear_geometry(self.bh["Cloud"])
        self.bh["Visibility"]=True
        self.bh["Cloud"]=self.GetPointCloud(points,colors)
        self.vis.add_geometry(self.bh["Cloud"])   


    def AddLine(self,p1:tuple,p2:tuple,color=DEFAULT_WIREFRAME_COLOR):
        line_set=open3d.geometry.LineSet()
        line_set.points=open3d.utility.Vector3dVector([p1,p2])
        line_set.lines=open3d.utility.Vector2iVector([[0,1]])
        line_set.colors=open3d.utility.Vector3dVector([color])
        self.vis.add_geometry(line_set)


    def AddWireframeBox(self,origin:tuple,dimensions:tuple,color=DEFAULT_WIREFRAME_COLOR):
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

        self.vis.add_geometry(line_set)

    def AddCircle(self,origin,radius,color=DEFAULT_WIREFRAME_COLOR,normal=[0,0,1]):
        res=32
        angles=numpy.linspace(0,2*numpy.pi,res)
        vertices=numpy.zeros((res,3))
        for i in range(len(angles)):
            vertices[i][0]=radius*numpy.cos(angles[i])+origin[0]
            vertices[i][1]=radius*numpy.sin(angles[i])+origin[1]
            vertices[i][2]=0+origin[2]

        edges=[]
        for i in range(res-1):
            edges.append([i,i+1])
        edges.append([res-1,0])

        edgecolor=numpy.outer(numpy.ones((len(edges),1)),color)
        line_set=open3d.geometry.LineSet()
        line_set.points=open3d.utility.Vector3dVector(vertices)
        line_set.lines=open3d.utility.Vector2iVector(edges)
        line_set.colors=open3d.utility.Vector3dVector(edgecolor)
        self.vis.add_geometry(line_set)



    # def AddWireframeSphere(self,origin=[0,0,0],radius=5,color=DEFAULT_WIREFRAME_COLOR):
