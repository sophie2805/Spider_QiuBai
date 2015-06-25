#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Sophie2805'

import wx
import wx.grid
from mail import *
from QiuBai import *

class Frame(wx.Frame):
    QiuBai = None
    content = None
    m = SMail()
    def __init__(self, parent=None, title='Get the Hottest QiuBai!',size=(450, 630),
                 style=wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER |wx.MAXIMIZE_BOX)):
        wx.Frame.__init__(self, parent=parent,  title=title, size=size,style = style)
        self.Centre()
        panel = wx.Panel(self,-1)

        self.text_Email = wx.StaticText(panel,1, "You want it too? Add your email below. Using ';' between multiple emails. Existing emails will not be added again.")
        self.input_Email = wx.TextCtrl(panel,2)
        self.button_Email = wx.Button(panel,3,label='+')

        '''Bind with function'''
        self.button_Email.Bind(wx.EVT_BUTTON,self.add)

        self.text_DeleteEmail = wx.StaticText(panel,4, "Existing receivers are listed below. You can delete by double clicking them and clicking on '-' button. Please note that it can hold 20 emails at most one time.")

        '''grid'''
        self.grid = wx.grid.Grid(panel,5)
        self.grid.CreateGrid(20,1)
        self.grid.EnableEditing(False)
        self.grid.SetColSize(0,200)
        self.grid.SetColLabelValue(0,'Emails')
        for i in range(len(self.m.receiver)):
                self.grid.SetCellBackgroundColour(i,0,"grey")
                self.grid.SetCellValue(i,0,self.m.receiver[i])

        self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK,self.grid_change_color)

        self.button_DeleteEmail = wx.Button(panel,6,label='-')
        self.button_Send = wx.Button(panel,7,label='send')

        '''Bind with function'''
        self.button_Send.Bind(wx.EVT_BUTTON,self.sendmail)
        self.button_DeleteEmail.Bind(wx.EVT_BUTTON,self.d_emails)

        '''BoxSizer'''
        '''================================================================'''
        add_Email = wx.BoxSizer() #input box and add button
        add_Email.Add(self.input_Email,proportion=4,flag = wx.LEFT, border = 5)
        add_Email.Add(self.button_Email,proportion=1,flag=wx.LEFT,border=15)

        ae = wx.BoxSizer(wx.VERTICAL)
        ae.Add(self.text_Email,proportion =4, flag=wx.ALL, border=5)
        ae.Add(add_Email,proportion=2, flag=wx.LEFT|wx.BOTTOM|wx.RIGHT, border=5)

        h_b = wx.BoxSizer()#send button and delete button
        h_b.Add(self.button_Send,flag=wx.LEFT,border=5)
        h_b.Add(self.button_DeleteEmail,flag=wx.LEFT,border=250)

        de = wx.BoxSizer(wx.VERTICAL)
        de.Add(self.text_DeleteEmail,proportion=2,flag=wx.ALL, border=5)
        de.Add(self.grid,proportion = 4,flag=wx.LEFT, border=80)
        de.Add(h_b,proportion=1,flag=wx.TOP, border=10)

        vBoxSizer = wx.BoxSizer(wx.VERTICAL)
        vBoxSizer.Add(ae,proportion=2,flag=wx.ALL,border=5)
        vBoxSizer.Add(de,proportion=4,flag=wx.LEFT|wx.BOTTOM|wx.RIGHT,border=5)
        panel.SetSizer(vBoxSizer)

    #delete the emails that cell bk color changed to yellow
    def d_emails(self,evt):
        count_yellow = 0
        for i in range(len(self.m.receiver)):
            if self.grid.GetCellBackgroundColour(i,0)==(255, 255, 0, 255): # yellow
                count_yellow += 1

        if count_yellow == 0:
            wx.MessageBox('Wake up!\nSelect then delete!')

        else:
            l = len(self.m.receiver)
            self.m.receiver=[]
            for i in range(l):
                if self.grid.GetCellBackgroundColour(i,0)==(128, 128, 128, 255):#grey
                    self.m.receiver.append(self.grid.GetCellValue(i,0))
                self.grid.SetCellValue(i,0,'')#clear the cell's value
                self.grid.SetCellBackgroundColour(i,0,'white')

            for i in range(len(self.m.receiver)):
                self.grid.SetCellBackgroundColour(i,0,"grey")
                self.grid.SetCellValue(i,0,self.m.receiver[i])
            self.grid.ForceRefresh()

    #change cell bk color when double click the cell. The cell without value will not be changed
    def grid_change_color(self,evt):
        if self.grid.GetCellValue(self.grid.GridCursorRow,self.grid.GridCursorCol) != '':
            if self.grid.GetCellBackgroundColour(self.grid.GridCursorRow,self.grid.GridCursorCol)==(128, 128, 128, 255):#grey
                self.grid.SetCellBackgroundColour(self.grid.GridCursorRow,self.grid.GridCursorCol,'yellow')
            else:
                self.grid.SetCellBackgroundColour(self.grid.GridCursorRow,self.grid.GridCursorCol,'grey')
        self.grid.ForceRefresh()

    #add the emails that user input
    def add(self,evt):
        x = str(self.input_Email.GetValue().encode('utf-8'))
        if len(x) == 0:
            wx.MessageBox('Hey dude, input something first!')
        elif len(x) != len(x.decode('utf-8')):#non ASCII character contained
            wx.MessageBox('Hey dude, please input English character only!')
        else:
            x = x.split(';')
            tag = 0
            for i in range(len(x)):
                if len(x[i]) != 0:
                    if x[i] in self.m.receiver:
                        x[i]=''#existing emails, set to ''
                    elif self.validate_email(x[i]) == None:
                        wx.MessageBox('Hey dude, eyes wide open! \nPlease input like this: xxx@xxx.com;eee@eee.org')
                        tag = 1
                        break
            if tag == 0: # all emails are valid
                for item in x:
                    if len(item) != 0:
                        self.m.receiver.append(item)
                for i in range(len(self.m.receiver)):
                    self.grid.SetCellBackgroundColour(i,0,"grey")
                    self.grid.SetCellValue(i,0,self.m.receiver[i])
                self.input_Email.Clear()
                self.grid.ForceRefresh()

    #validate the emails user input
    def validate_email(self,s):
        pattern = "^[a-zA-Z0-9\._-]+@([a-zA-Z0-9_-]+\.)+([a-zA-Z]{2,3})$"
        p = re.compile(pattern)
        return p.match(s)

    def sendmail(self,evt):
        if len(self.m.receiver) == 0:
            wx.MessageBox('Are you kidding me?\n Add some receivers then send!')
        else:
            self.QiuBai = FetchData('http://www.qiushibaike.com/text','http://www.qiushibaike.com/',
                                '<div class="content">[\n\s]+.+[\n\s]','[<div class="content"><br/>\n]')
            self.content = self.QiuBai.getData(self.QiuBai.getHtml())
            msg = '\n\n'.join(self.content)
            result = self.m.send_mail(msg)
            if result == '1':
                wx.MessageBox('The hottest QiuBai had been sent.\n Enjoy it ^_^ !')
            else:
                wx.MessageBox('Some exception occurred :-(\nTry again later...\n'+result)
class GetQiuBaiApp(wx.App):
    def OnInit(self):
        frame = Frame()
        frame.Show()
        return True

if __name__ == "__main__":
    app = GetQiuBaiApp()
    app.MainLoop()
