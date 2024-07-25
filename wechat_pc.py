import uiautomation as uiauto
import os
from time import sleep
import pyautogui
import http.client
import json
import requests
import re
class WechatAuto:

    def __init__(self, wechat_locate: str,qf_client_id:str,qf_client_secret:str,qf_model_url:str):
        """
        启动微信，定位基本元素
        :param wechat_locate: 微信安装绝对路径.exe
        """
        # os.system(rf'start {wechat_locate}')

        self.qf_client_id=qf_client_id ;
        self.qf_client_secret=qf_client_secret ;
        self.qf_model_url=qf_model_url ;
        # 找到微信窗口
        self.wechat_window = uiauto.WindowControl(searchDepth=1, ClassName='WeChatMainWndForPC')
        # 选择微信窗口
        self.wechat_window.SwitchToThisWindow()
        # 窗口控制栏,固定,最大小化,退出
        # self.window_control = self.wechat_window.ToolBarControl(searchDepth=5, LocalizedControlType="工具栏")
        # self.wechat_window.ButtonControl(searchDepth=6, Name='置顶').Click()

        # 用户导航：用户,聊天,通讯录,收藏……
        self.guide_tool = self.wechat_window.ToolBarControl(searchDepth=4, Name='导航')
        # 会话列表
        self.chat_list = self.wechat_window.ListControl(searchDepth=8, Name='会话')
        # 当前聊天对象消息列表窗口,聊天内容
        self.chat_massage = self.wechat_window.ListControl(searchDepth=12, Name='消息')
        # 聊天界面搜索框
        self.chat_search = self.wechat_window.EditControl(searchDepth=7, Name='搜索')
        # 先清除搜索框再输入内容
        self.chat_search_clear = self.wechat_window.ButtonControl(searchDepth=7, Name='清空')
        # 搜索结果
        self.search_result = self.wechat_window.ListControl(searchDepth=8, Name="@str:IDS_FAV_SEARCH_RESULT:3780",
                                                            LocalizedControlType="列表")
        # 发送按钮
        self.send_button = self.wechat_window.ButtonControl(searchDepth=15, Name="发送(S)")

        self.chat_name: str = ""

        self.baiduToken =self.getBaiDuToken()

        self.status = True

        print(f"token = ",self.baiduToken)
    def input_content(self, name: str):
        return self.wechat_window.EditControl(searchDepth=14, LocalizedControlType="编辑", Name=name)

    def getBaiDuToken(self):

        url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id="+self.qf_client_id+"&client_secret="+self.qf_client_secret

        print(url)
        response = requests.request("GET", url)
        reqResult = response.text
        print(reqResult)
        print(json.loads(reqResult))
        return json.loads(reqResult)["access_token"];

    def getAIAnswer(self,query):

        #url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-3.5-8k-0205?access_token=" + self.baiduToken
        url = self.qf_model_url+"?access_token=" + self.baiduToken
        headers = {
            'Authorization': 'Bearer app-FEKJAQOdVPKJf40znr5IIbUd',
            'Content-Type': 'application/json'
        }
        payload = json.dumps({
            "messages": [{"role": "user", "content": query}],
            "system": "你是个人做诗助手，根据用户的输入内容，做一首诗回复。"
        })

        print(payload)
        response = requests.request("POST", url, headers=headers, data=payload)

        reqResult = response.text
        print(reqResult)
        return json.loads(reqResult)["result"]

    def openAutoReply(self):

        while self.status:
            sleep(2)
            for chat in self.chat_list.GetChildren():
                # print(chat)
                # mnprint(chat.TextControl(searchDepth=5, foundIndex=1))
                if chat.Name.find("新消息") != -1:
                    chat.Click()
                    msg = self.chat_massage
                    print(msg)
                    msg_children = msg.GetChildren()
                    if len(msg_children) > 0:
                        last_xiaoxi = msg_children[-1]
                    else:
                        continue
                    print(f""+last_xiaoxi.Name)
                    if last_xiaoxi.Name == "[图片]":
                       last_xiaoxi.CaptureToImage(savePath="c:\\Users\\endym\\Desktop\\1.png", x=90,width=160)
                       my_content = "嘻嘻"
                    else:
                        print("last_xiaoxi.Name=",last_xiaoxi.Name)

                        massage = self.getAIAnswer(last_xiaoxi.Name)
                        content = self.input_content(chat.TextControl(searchDepth=5, foundIndex=1).Name)
                        content.Click()
                        result = massage.replace("Observation: ", "")
                        if result!="":
                            content.SendKeys(text=result, waitTime=0.2)
                            self.send_button.Click()
    def endAutoReply(self):
        self.status = False