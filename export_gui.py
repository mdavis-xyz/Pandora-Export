#!/usr/bin/env python3

# gui wrapper around the pandora export script by Matthew Davis (July 2017).
# Copyright for the export code and the pandora library 
# are held by their respective creators. This file is placed in the public
# domain to the extent possible.

import tkinter as tk       
from tkinter import Frame, Button, Listbox, Entry, Label, filedialog, \
                    StringVar
import sys
import export 
import os.path

# Possibly useful links:
#
# - reddit discussion of export scripts:
#     https://www.reddit.com/r/Pandora/comments/6og294/pandora_australia_users_i_wrote_a_script_to/
#     https://www.reddit.com/r/Pandora/comments/6ne7n5/i_wrote_a_python_script_for_exporting_your_likes/
# - github repo for Matthew Davis' script:
#     https://github.com/mlda065/Pandora-Export
# - Unofficial Pandora HTTP API (used under the hood):
#     https://6xq.net/pandora-apidoc/json/methods/

# freezing tools: use pyInstaller
#   http://python-guide-pt-br.readthedocs.io/en/latest/shipping/freezing/
#   https://pyinstaller.readthedocs.io/en/stable/

# muse - feeling good
# https://www.youtube.com/watch?v=CmwRQqJsegw

# mock exporter for testing
class FakeLogic(object):
  def __init__(self):
    object.__init__(self)
    print("logic inited")

  def login(self, userid, password):
    print("do fk login")

  def getLikes(self):
    print("do fk getLikes")

  def save(self, fullFileName='full.json', neatFileName = 'neat.json'):
    print("do fk save")


class Application(Frame):              
    def __init__(self, master=None):
        Frame.__init__(self, master, width=800, height=500)
        self.createWidgets()
        self.exporter = export.Exporter()
        #self.exporter = FakeLogic()

    def createWidgets(self):
        # top menu bar

        self.topBar = Frame(self.master)#,height=10) #,width=50)
        topBar = self.topBar
        topBar.config(bd=3, relief=tk.GROOVE)

        self.quitBtn = Button(topBar, text='Quit',
            command=self.quit)
        self.quitBtn.pack(side="right")

        topBar.pack(side=tk.TOP,fill=tk.X)

        self.mainFrame = Frame(self.master) #,height=60) #,width=50)
        mainFrame = self.mainFrame
        mainFrame.pack(side=tk.TOP,fill=tk.BOTH, expand=1)

        self.loginFrame()

    def loginFrame(self):
      self.loginFrm = Frame(self.mainFrame, height=150, width=450)
      loginFrm = self.loginFrm 
      loginFrm.config(bd=3, relief=tk.GROOVE)

      Label(loginFrm, text="userid (e.g. email address)").grid(row=0)
      Label(loginFrm, text="password").grid(row=1)

      loginFrm.userid = Entry(loginFrm, width=40)
      loginFrm.password = Entry(loginFrm, show='*', width=20)

      def doLogin():
        userid   = loginFrm.userid.get()
        password = loginFrm.password.get()
        self.exporter.login(userid, password)
        self.loginFrm.destroy()
        self.downloadFrame()

      loginFrm.loginBtn = Button(loginFrm,text='Login', command=doLogin)

      loginFrm.userid.grid(row=0, column=1)
      loginFrm.password.grid(row=1, column=1)
      loginFrm.loginBtn.grid(row=2, column=0, columnspan=2, pady=5)

      loginFrm.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def downloadFrame(self):
      self.downloadFrm = Frame(self.mainFrame, height=150, width=450)
      downloadFrm = self.downloadFrm 
      downloadFrm.config(bd=3, relief=tk.GROOVE)

      def doDownload():
        self.exporter.getLikes()
        print("download done")
        self.downloadFrm.destroy()
        self.saveFrame()

      downloadFrm.loginBtn = Button(downloadFrm,text='Download thumbed tracks', command=doDownload )
      downloadFrm.loginBtn.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

      downloadFrm.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def saveFrame(self):
      self.saveFrm = Frame(self.mainFrame, height=150, width=450)
      saveFrm = self.saveFrm
      saveLocn = StringVar()

      def doChooseDir():
        saveLocn_ = filedialog.askdirectory(parent=self.saveFrm, 
                      initialdir=".",title='Please select a directory')
        if len(saveLocn_) > 0:
          saveLocn.set(saveLocn_)
          saveFrm.saveLocLbl.config(textvariable=saveLocn)
          saveFrm.saveBtn.config(state=tk.ACTIVE)

      def doSave():
        fullFileName = os.path.join(saveLocn.get(), "full.json")
        neatFileName = os.path.join(saveLocn.get(), "neat.json")
        self.exporter.save(fullFileName, neatFileName)

      Label(saveFrm, text="Save data to:").grid(row=0)
      saveFrm.saveLocBtn = Button(saveFrm,text='Choose directory', command=doChooseDir)
      saveFrm.saveLocBtn.grid(row=0,column=1)
      saveFrm.saveLocLbl = Label(saveFrm, text="No directory chosen")
      saveFrm.saveLocLbl.grid(row=0,column=2)

      saveFrm.saveBtn = Button(saveFrm,text='Save', command=doSave, state=tk.DISABLED)
      saveFrm.saveBtn.grid(row=1,column=1)

      saveFrm.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

 
def main():
  print("main...")
  
  app = Application()
  print("made app...")
  app.master.title('Pandora exporter')
  app.master.geometry('{}x{}'.format(500, 350))
  app.mainloop()   

MAIN="__main__" 
#MAIN=None

if __name__ == MAIN:
  main()

