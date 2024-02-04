import numpy as np
import open3d as o3d
import open3d.visualization.gui as gui
import open3d.visualization.rendering as rendering
import open3d.visualization as vis



class Viewer3D(object):
    MENU_QUIT = 0
    UIBAR_YOFFSET = 20
    UIBAR_HEIGHT = 20

    def __init__(self, title="Viewer 3D",width=1600,height=900):
        app = o3d.visualization.gui.Application.instance
        app.initialize()
        self.window=app.create_window(title,width,height)
        self.InitialiseUI()
        app.run()

    def InitialiseUI(self):
        self.em = em = self.window.theme.font_size
        
        # Menu Bar
        o3d.visualization.gui.Application.instance.menubar=self.MenuBar()
        
        # UI Bar
        uibar = gui.Vert(0, gui.Margins(0*em, 0.0*em, 0.0*em, 0.0*em))
        uibar.frame=gui.Rect(self.window.content_rect.x, self.window.content_rect.y + Viewer3D.UIBAR_YOFFSET,self.window.content_rect.width, Viewer3D.UIBAR_HEIGHT)

        # UI Tiles
        uitiles=gui.Horiz(0,gui.Margins(0*em, 0.0*em, 0.0*em, 0.0*em))
        uibar.add_child(uitiles)

        # test
        uitiles.add_child(gui.Label("Root Halo : "))
        combo = gui.Combobox()
        self.FillRootCombo(combo)
        combo.set_on_selection_changed(self.OnRootComboSlectionChanged)
        uitiles.add_child(combo)

        # filedlgbutton = gui.Button("...")
        # filedlgbutton.horizontal_padding_em = 0.5
        # filedlgbutton.vertical_padding_em = 0
        # # filedlgbutton.set_on_clicked(self._on_filedlg_button)


        # fileedit_layout = gui.Horiz()
        # fileedit_layout.add_child(gui.Label("Model file"))
        # fileedit_layout.add_child(self.fileedit)
        # fileedit_layout.add_fixed(0.25 * em)
        # fileedit_layout.add_child(filedlgbutton)

        # root_form.add_child(fileedit_layout)


        # Scene Widget
        scene=gui.SceneWidget()
        scene.scene = rendering.Open3DScene(self.window.renderer)
        scene.set_view_controls(gui.SceneWidget.Controls.ROTATE_CAMERA)
        scene.frame=gui.Rect(self.window.content_rect.x, self.window.content_rect.y+40,self.window.content_rect.width, self.window.content_rect.height-40)




        self.window.add_child(uibar)
        self.window.add_child(scene)


    def MenuBar(self):
        gui=o3d.visualization.gui
        menubar=gui.Menu()
        menubar_tab1=gui.Menu()
        menubar_tab1.add_item("Open ...",1)
        menubar_tab1.add_separator()
        menubar_tab1.add_item("Quit",Viewer3D.MENU_QUIT)
        menubar_tab2=gui.Menu()
        menubar_tab3=gui.Menu()
        menubar.add_menu("File",menubar_tab1)
        menubar.add_menu("Settings",menubar_tab2)
        menubar.add_menu("Help",menubar_tab3)
        self.AttachMenuItemsEventListeners()
        return menubar
    
    def AttachMenuItemsEventListeners(self):
        w=self.window
        w.set_on_menu_item_activated(Viewer3D.MENU_QUIT,self.OnQuit)
    
    def FillRootCombo(self,combo):
        combo.add_item("Halo-0")
        combo.add_item("Halo-1")
        combo.add_item("Halo-2")
        combo.add_item("Halo-356")

    #-----------------------------------------------Events
    def OnQuit(self):
        self.window.close()
        # gui.Application.instance.quit()

    def OnResize(self):
        print("window resized")

    def OnRootComboSlectionChanged(self,a,b):
        print("root-changed",a,b)

    



viewer3d = Viewer3D("Halo Visualizer")
