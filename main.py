#!/usr/bin/python
# coding: utf-8
#
# @module GUI_Ciligou
#
# @author: Zengming Deng
#
# @description:
#
# @since: 2020-04-17 15:23:06
# -------------------------------

import wx
from ciligou import SearchCiligou as search
from thunder import down as StartDownTask


class gui_main(wx.Frame):
    def __init__(self, parent=None):
        super(gui_main, self).__init__(parent)
        self.SetTitle("磁力狗搜索桌面版")
        self.items_cnt = 0
        self.itemdict_lists = []
        self.InitUI()
        self.Centre()

    def InitStatusBar(self):
        # *创建一个状态栏，在底部，双栏
        self.statusbar = self.CreateStatusBar()
        #将状态栏分割为3个区域,比例为1:2:3
        self.statusbar.SetFieldsCount(2)
        self.statusbar.SetStatusWidths([-2, -1])
        self.statusbar.SetStatusText("共搜索到%d个条目" % (self.items_cnt), 0)
        #设置状态栏2内容
        self.statusbar.SetStatusText("等待输入搜索信息", 1)

    def InitUI(self):
        self.panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.InitStatusBar()
        self.text_info = wx.StaticText(self.panel, label="请输入需要搜索的电影或者车牌！")
        font2 = wx.Font(14, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        self.text_info.SetFont(font2)
        self.tc_input = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.tc_input.Bind(wx.EVT_TEXT_ENTER, self.ClickToSearch)
        self.btn_enter = wx.Button(self.panel, label="搜索", size=(70, 30))
        self.btn_enter.Bind(wx.EVT_BUTTON, self.ClickToSearch)
        self.listct = wx.ListCtrl(self.panel, -1, style=wx.LC_REPORT, size=(-1, 250))
        self.listct.InsertColumn(0, '资源名', wx.LIST_FORMAT_CENTER, width=280)
        self.listct.InsertColumn(1, '大小', wx.LIST_FORMAT_CENTER, width=80)
        self.listct.InsertColumn(2, '链接', wx.LIST_FORMAT_CENTER, width=300)
        self.listct.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnDouClick)
        vbox.Add(self.text_info, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        vbox.Add(self.tc_input, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        vbox.Add(self.btn_enter, flag=wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        vbox.Add(self.listct, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        self.panel.SetSizer(vbox)
        self.SetSize(700, 500)
    
    def ClickToSearch(self, e):
        if self.tc_input.GetValue() == '':
            return
        self.statusbar.SetStatusText("开始搜索磁力狗链接, 请稍后", 1)
        search(word=self.tc_input.GetValue(), updateItem=self.UpdateMoiveItem)
        wx.MessageDialog(None, '搜索完成', 'Message', wx.OK | wx.ICON_HAND)
        self.statusbar.SetStatusText("搜索磁力狗链接结束", 1)
        pass

    def OnDouClick(self, e):
        # 双击条目可以启动下载
        itemID = e.GetEventObject().GetFirstSelected()
        magnet_ = self.itemdict_lists[itemID]['url']
        format_ = self.itemdict_lists[itemID]['format']
        name_ = self.itemdict_lists[itemID]['title']
        StartDownTask(url=magnet_, name=name_, format_=format_)

    def UpdateMoiveItem(self, dict_={}):
        if dict_ is None:
            wx.MessageDialog(None, '网络异常', 'Message', wx.OK | wx.ICON_ERROR)
        self.items_cnt += 1
        self.UpdateStatusBar1()
        print(dict_)
        index = self.listct.InsertItem(self.items_cnt, dict_['title'])
        self.listct.SetItem(index, 1, dict_['storage'])
        self.listct.SetItem(index, 2, dict_['url'])
        self.itemdict_lists.append(dict_)
        self.listct.Update()
        
    def UpdateStatusBar1(self):
        self.statusbar.SetStatusText("共搜索到%d个条目, 双击可以启动迅雷下载！" % (self.items_cnt), 0)

if __name__ == '__main__':
    app = wx.App()
    gui_main().Show()
    app.MainLoop()
