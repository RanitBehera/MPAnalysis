import open3d,numpy,quaternion



def QuternionRotation(vectors,axis,angle):
    # Normalises axis to unit vector for direction
    axis=axis/numpy.linalg.norm(axis)

    # Rescale so that magnitude represents angle of rotation in radians
    axis*=angle

    # Get the quaternion
    q = quaternion.from_rotation_vector(axis)

    # Apply rotation
    vecs4 = numpy.zeros([vectors.shape[0],vectors.shape[1]+1])
    vecs4[:,1:] = vectors
    vecsq = quaternion.as_quat_array(vecs4)
    vecsq_rotated = q * vecsq * q.conjugate()

    return quaternion.as_float_array(vecsq_rotated)[:,1:]


# ====================================================================
# ====================================================================

class Basic:
    def __init__(self,title:str="Open3D",width:int=800,height:int=600):
        self.vis=open3d.visualization.VisualizerWithKeyCallback()
        self.vis.create_window(title,width,height)
        self.RegisterExtraKeyBindings()
        self.cloudlist=[]
    
    def Run(self):
        self.vis.run()
        self.vis.destroy_window()

    def SetBackgroundColor(self,bgcolor):
        self.vis.get_render_option().background_color = numpy.asarray(bgcolor) 

    def RegisterExtraKeyBindings(self):
        tranlate_amount=0.1
        rotate_amount=20

        def Key_E(vis):  # Forward Move
            vis.get_view_control().camera_local_translate(tranlate_amount,0,0)
        def Key_Q(vis):  # Backward Move
            vis.get_view_control().camera_local_translate(-tranlate_amount,0,0)
        def Key_D(vis):  # Look Right
            vis.get_view_control().camera_local_rotate(rotate_amount,0,0,0)
        def Key_A(vis):  # Look Left
            vis.get_view_control().camera_local_rotate(-rotate_amount,0,0,0)
        def Key_W(vis):  # Look Up
            vis.get_view_control().camera_local_rotate(0,-rotate_amount,0,0)
        def Key_S(vis):  # Look Down
            vis.get_view_control().camera_local_rotate(0,rotate_amount,0,0)

        self.vis.register_key_callback(ord('E'),Key_E)  # Move Forward
        self.vis.register_key_callback(ord('Q'),Key_Q)  # Move Backward
        self.vis.register_key_callback(ord('D'),Key_D)  # Look Right
        self.vis.register_key_callback(ord('A'),Key_A)  # Look Left
        self.vis.register_key_callback(ord('W'),Key_W)  # Look Up
        self.vis.register_key_callback(ord('S'),Key_S)  # Look Down


    # --- POINT CLOUD MANIPULATION

    def AddToPointCloudList(self,cloudname:str,points:list,colors:list):
        # VALIDATION : Avoid duplicate cloud name
        priorclouds=[cloud["Name"] for cloud in self.cloudlist]
        if cloudname in priorclouds:
            raise NameError("Cloud with same name already exist.")
        
        # VALIDATION : Color array.
        cdim=numpy.array(colors).shape
        lenp=len(points)
        if not cdim in ((),(3,),(lenp,),(lenp,3)):
            raise ValueError("Inconsistent color array length")
        if cdim==():colors=[colors,colors,colors]
        if cdim==(lenp,):colors=[[c,c,c] for c in colors]
        
        pcd= open3d.geometry.PointCloud()
        pcd.points=open3d.utility.Vector3dVector(points)
        if cdim in ((),(3,)):
            pcd.paint_uniform_color(colors)
        elif cdim in ((lenp,),(lenp,3)):
            pcd.colors=open3d.utility.Vector3dVector(colors)

        self.cloudlist.append({"Name":cloudname,"Object":pcd})
        self.vis.add_geometry(pcd)

    def ShowPointCloud(self,cloudname):
        if type(cloudname)==str:cloudname=[cloudname]
        for cloud in self.cloudlist:
            if cloud["Name"] in cloudname:
                self.vis.add_geometry(cloud["Object"],False)

    def HidePointCloud(self,cloudname):
        if type(cloudname)==str:cloudname=[cloudname]

        for cloud in self.cloudlist:
            if cloud["Name"] in cloudname:
                self.vis.remove_geometry(cloud["Object"],False)

    def ClearFromPointCloudList(self,cloudname): # Not working
        if type(cloudname)==str:cloudname=[cloudname]

        for cloud in self.cloudlist:
            if cloud["Name"] in cloudname:
                cloud["Object"].clear()
            self.cloudlist.remove(cloud)

    def ClearPointCloudList(self):
        self.vis.clear_geometries()
        self.cloudlist=[]
    

    # --- LINE SET MANIPULATION
    DEFAULT_LINE_COLOR=[1,1,1]

    def AddLine(self,p1:tuple,p2:tuple,color=DEFAULT_LINE_COLOR):
        line_set=open3d.geometry.LineSet()
        line_set.points=open3d.utility.Vector3dVector([p1,p2])
        line_set.lines=open3d.utility.Vector2iVector([[0,1]])
        line_set.colors=open3d.utility.Vector3dVector([color])
        line_set.line_width=5
        self.vis.add_geometry(line_set)

    def AddCurve(self,points,color=DEFAULT_LINE_COLOR,closed=False):
        vertices=numpy.array(points)
        edges=[]
        for i in range(len(vertices)-2):edges.append([i,i+1])
        if closed:edges.append([len(vertices)-1,0])
        edges=numpy.array(edges)

        edgecolor=numpy.outer(numpy.ones((len(edges),1)),color)
        line_set=open3d.geometry.LineSet()
        line_set.points=open3d.utility.Vector3dVector(vertices)
        line_set.lines=open3d.utility.Vector2iVector(edges)
        line_set.colors=open3d.utility.Vector3dVector(edgecolor)
        self.vis.add_geometry(line_set)




    def AddCircle(self,radius=1,location=[0,0,0],color=DEFAULT_LINE_COLOR,normal=[0,0,1],segments=32,start_ang=0,stop_ang=2*numpy.pi):
        # First create and orient circle at orgin and then shift to location
        seg_angles=numpy.linspace(start_ang,stop_ang,segments)
        vertices=numpy.zeros((segments,3))
        for i in range(segments):
            vertices[i][0]=radius*numpy.cos(seg_angles[i])
            vertices[i][1]=radius*numpy.sin(seg_angles[i])
            vertices[i][2]=0
        
        # Rotation axis is perpendicular to normal
        nx,ny,nz,nr=normal[0],normal[1],normal[2],numpy.linalg.norm(normal)
        rot_angle=numpy.arccos(nz/nr)
        rot_axis=[-ny,nx,0]
        vertices=QuternionRotation(vertices,rot_axis,rot_angle)

        # Shift to location
        vertices+=numpy.array(location)

        # Edges
        edges=[]
        for i in range(segments-1):edges.append([i,i+1])
        edges.append([segments-1,0])
        edges=numpy.array(edges)

        # Add it to window
        edgecolor=numpy.outer(numpy.ones((len(edges),1)),color)
        line_set=open3d.geometry.LineSet()
        line_set.points=open3d.utility.Vector3dVector(vertices)
        line_set.lines=open3d.utility.Vector2iVector(edges)
        line_set.colors=open3d.utility.Vector3dVector(edgecolor)
        self.vis.add_geometry(line_set)
        
        







# ====================================================================
# ====================================================================

class GADGET(Basic):
    DEFAULT_BG_COLOR        = [0,0,0]
    DEFAULT_WIREFRAME_COLOR = [1,1,1]
    DEFAULT_PART_COLOR      = [1,1,0]
    DEFAULT_DM_COLOR        = [1,0,1]
    DEFAULT_GAS_COLOR       = [0,1,1]
    DEFAULT_STAR_COLOR      = [1,1,0]
    DEFAULT_BH_COLOR        = [1,0,0]

    def __init__(self,title:str="Open3D",width:int=800,height:int=600):
        super().__init__(title,width,height)
        self.SetBackgroundColor(GADGET.DEFAULT_BG_COLOR)
        self.RegisterGADGETKeyBindings()
        self._dm=-1
        self._gas=-1
        self._star=-1
        self._bh=-1

    def RegisterGADGETKeyBindings(self):  
        def Key_0(vis):  # DM Toggle
            if self._dm<0: return
            if self._dm:self.HidePointCloud("DM")
            else:self.ShowPointCloud("DM")
            self._dm=not self._dm

        def Key_1(vis):  # Gas Toggle
            if self._gas<0: return
            if self._gas:self.HidePointCloud("Gas")
            else:self.ShowPointCloud("Gas")
            self._gas=not self._gas
        def Key_2(vis):  # Star Toggle
            if self._star<0: return
            if self._star:self.HidePointCloud("Star")
            else:self.ShowPointCloud("Star")
            self._star=not self._star
        def Key_3(vis):  # BH Toggle
            if self._bh<0: return
            if self._bh:self.HidePointCloud("BH")
            else:self.ShowPointCloud("BH")
            self._bh=not self._bh


        self.vis.register_key_callback(ord('0'),Key_0)  # DM Toggle 
        self.vis.register_key_callback(ord('1'),Key_1)  # Gas Toggle 
        self.vis.register_key_callback(ord('2'),Key_2)  # Star Toggle 
        self.vis.register_key_callback(ord('3'),Key_3)  # BH Toggle 

                
    def DarkMatter(self,points,colors=DEFAULT_DM_COLOR):  
        if self._dm>-1:self.ClearFromPointCloudList("DM")
        self.AddToPointCloudList("DM",points,colors)
        self._dm=1
        
    def Gas(self,points,colors=DEFAULT_GAS_COLOR):
        # if self._gas>-1:self.ClearFromPointCloudList("Gas")
        self.AddToPointCloudList("Gas",points,colors)
        self._gas=1

    def Star(self,points,colors=DEFAULT_STAR_COLOR):
        # if self._star>-1:self.ClearFromPointCloudList("Star")
        self.AddToPointCloudList("Star",points,colors)
        self._star=1

    def Blackhole(self,points,colors=DEFAULT_BH_COLOR):
        # if self._bh>-1:self.ClearFromPointCloudList("BH")
        self.AddToPointCloudList("BH",points,colors)
        self._bh=1

    def SurroundSpehere(self,radius,normal,location,color=DEFAULT_WIREFRAME_COLOR,resolution=16):
        ang=numpy.linspace(0,numpy.pi,resolution+2)
        rad=radius*numpy.sin(ang)
        zoff=radius*numpy.cos(ang)
        for i in range(len(ang)):
            direction=normal/numpy.linalg.norm(normal)
            diroffset=zoff[i]*direction
            self.AddCircle(rad[i],location+diroffset,normal=normal,color=color)
        





#     def AddWireframeBox(self,origin:tuple,dimensions:tuple,color=DEFAULT_WIREFRAME_COLOR):
#         Ox,Oy,Oz=origin[0],origin[1],origin[2]
#         dx,dy,dz=dimensions[0],dimensions[1],dimensions[2]

#         p0=[Ox,Oy,Oz]
#         p1=[Ox+dx,Oy,Oz]
#         p2=[Ox+dx,Oy+dy,Oz]
#         p3=[Ox,Oy+dy,Oz]
#         p4=[Ox,Oy,Oz+dz]
#         p5=[Ox+dx,Oy,Oz+dz]
#         p6=[Ox+dx,Oy+dy,Oz+dz]
#         p7=[Ox,Oy+dy,Oz+dz]

#         vertices=[p0,p1,p2,p3,p4,p5,p6,p7]
#         edges=[[0,1],[1,2],[2,3],[3,0],[0,4],[4,5],[5,6],[6,7],[7,4],[1,5],[2,6],[3,7]]
#         edgecolor=numpy.outer(numpy.ones((len(edges),1)),color)

#         line_set=open3d.geometry.LineSet()
#         line_set.points=open3d.utility.Vector3dVector(vertices)
#         line_set.lines=open3d.utility.Vector2iVector(edges)
#         line_set.colors=open3d.utility.Vector3dVector(edgecolor)

#         self.vis.add_geometry(line_set)

  




