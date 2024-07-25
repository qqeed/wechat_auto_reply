import _thread
import uiautomation as uiauto
from wechat_pc import *
import wx
class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        self.dirname=''

        # A "-1" in the size parameter instructs wxWidgets to use the default size.
        # In this case, we select 200px width and the default height.
        wx.Frame.__init__(self, parent, title=title, size=(500,400))

        wx.StaticText(self, label="微信安装地址：")
        self.wx_install_path = wx.TextCtrl(self, value=r"C:\Program Files\Tencent\WeChat\WeChat.exe", size=(400, 25), pos=(100, 0))

        wx.StaticText(self,label="百度千帆大模型",pos=(0, 25))
        wx.StaticText(self, label="百度client_id：",pos=(0, 50))
        wx.StaticText(self, label="百度client_secret：", pos=(0, 75))
        wx.StaticText(self, label="百度模型地址：", pos=(0, 100))
        self.qf_client_id =wx.TextCtrl(self, value="", size=(400,25),pos=(100, 50))
        self.qf_client_secret = wx.TextCtrl(self, value="",size=(400,25), pos=(100, 75))
        self.qf_model_url = wx.TextCtrl(self, value="https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-3.5-8k-0205", size=(400, 25), pos=(100, 100))
        # self.control
        self.CreateStatusBar() # A Statusbar in the bottom of the window

        # Setting up the menu.
        filemenu= wx.Menu()
        menuOpen = filemenu.Append(wx.ID_OPEN, "&Open"," Open a file to edit")
        menuAbout= filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        menuExit = filemenu.Append(wx.ID_EXIT,"Exit"," Terminate the program")

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File")
        # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        # Events.
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)

        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.buttons = []
        self.buttons.append(wx.Button(self, -1,"开启自动回复",pos=(0, 130)))
        self.buttons.append(wx.Button(self, -1,"停止自动回复",pos=(100, 130)))
        self.Bind(wx.EVT_BUTTON, self.startReply, self.buttons[0])
        self.Bind(wx.EVT_BUTTON, self.endReply, self.buttons[1])
        self.sizer2.Add(self.buttons[0], 1, wx.EXPAND)
        self.sizer2.Add(self.buttons[1], 1, wx.EXPAND)

        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        # Use some sizers to see layout options
        # self.sizer = wx.BoxSizer(wx.VERTICAL)
        # self.sizer.Add(self.control, 1, wx.EXPAND)
        #self.sizer.Add(self.sizer2, 0, wx.EXPAND)

        # panel = wx.Panel(self)
        # self.quote = wx.StaticText(panel, label="Your quote: ", pos=(20, 30))



        #Layout sizers
        #self.SetSizer(self.sizer)
        #self.SetAutoLayout(1)
        #self.sizer2.Fit(self)
        self.Show()

    def OnAbout(self,e):
        # Create a message dialog box
        dlg = wx.MessageDialog(self, " A sample editor \n in wxPython", "About Sample Editor", wx.OK)
        dlg.ShowModal() # Shows it
        dlg.Destroy() # finally destroy it when finished.

    def OnExit(self,e):
        self.Close(True)  # Close the frame.

    def OnOpen(self,e):
        """ Open a file"""
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname, self.filename), 'r')
            self.control.SetValue(f.read())
            f.close()
            dlg.Destroy()
    def startReply(self,e):
        """ Open a file"""
        print("开启微信自动回复")

        try:
             wx_install_path = self.wx_install_path.GetValue();
             qf_client_id = self.qf_client_id.GetValue()
             qf_client_secret = self.qf_client_secret.GetValue()
             qf_model_url = self.qf_model_url.GetValue()
             print(f"qf_client_id="+qf_client_id)
             print(f"qf_client_secret="+qf_client_secret)
             print(f"qf_model_url="+qf_model_url)

             self.wechat = WechatAuto(wx_install_path,qf_client_id,qf_client_secret,qf_model_url)
             _thread.start_new_thread(open, ("Thread-1",self.wechat,))
        except Exception as e :
            dlg = wx.MessageDialog(self, "请先登录微信", "提示", wx.OK)
            dlg.ShowModal()  # Shows it
            dlg.Destroy()  # finally destroy it when finished.
            #wechat.openAutoReply()

    def endReply(self,e):
        """ Open a file"""
        print("结束微信自动回复")
        self.wechat.endAutoReply()
def open(name,wechat):

    wechat.openAutoReply()

if __name__ == "__main__":
    print("启动")
    app = wx.App(False)
    frame = MyFrame(None, "微信自动回复")
    frame.Show(True)
    app.MainLoop()



