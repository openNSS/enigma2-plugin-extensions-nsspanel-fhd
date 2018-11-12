#updated Lululla 23/10/2018 Skin FHD
from Screens.Screen import Screen
from Components.ActionMap import ActionMap, NumberActionMap
from Components.MenuList import MenuList
from Components.Sources.List import List
from Screens.MessageBox import MessageBox
from Plugins.Plugin import PluginDescriptor
from Components.Pixmap import Pixmap
from Tools.Directories import fileExists, pathExists, SCOPE_SKIN_IMAGE, resolveFilename
from ServiceReference import ServiceReference
from Components.Button import Button
from Components.Label import Label
from Tools.LoadPixmap import LoadPixmap
import os
import urllib
from enigma import eTimer, RT_HALIGN_LEFT, RT_VALIGN_CENTER, eListboxPythonMultiContent, gFont, getDesktop
plugin_path = '/usr/lib/enigma2/python/Plugins/Extensions/NssPanel/'
cccaminfo = False

def main(session, **kwargs):
    session.open(NSSCamsManager)


# def DreamCCExtra(name, index, isActive = False):
    # res = [index]
    # res.append((eListboxPythonMultiContent.TYPE_TEXT,
     # 55,
     # 4,
     # 200,
     # 24,
     # 0,
     # RT_HALIGN_LEFT | RT_VALIGN_CENTER,
     # name))
    # if isActive:
        # png = LoadPixmap(plugin_path + 'buttons/green.png')
    # else:
        # png = LoadPixmap(plugin_path + 'buttons/red.png')
    # res.append((eListboxPythonMultiContent.TYPE_PIXMAP_ALPHATEST,
     # 5,
     # 4,
     # 40,
     # 24,
     # png))
    # return res

def DreamCCExtra(name, index, isActive = False):
    res = [index]
    res.append((eListboxPythonMultiContent.TYPE_TEXT,
     55,
     4,
     200,
     30,
     0,
     RT_HALIGN_LEFT | RT_VALIGN_CENTER,
     name))
    if isActive:
        png = LoadPixmap(plugin_path + 'buttons/green.png')
    else:
        png = LoadPixmap(plugin_path + 'buttons/red.png')
    res.append((eListboxPythonMultiContent.TYPE_PIXMAP_ALPHATEST,
     5,
     4,
     40,
     30,
     png))
    return res
    
class DCCMenu(MenuList):

    def __init__(self, list, selection = 0, enableWrapAround = True):
        MenuList.__init__(self, list, enableWrapAround, eListboxPythonMultiContent)
        self.l.setFont(0, gFont('Regular', 30))
        self.l.setItemHeight(50)
        self.selection = selection

    def postWidgetCreate(self, instance):
        MenuList.postWidgetCreate(self, instance)
        self.moveToIndex(self.selection)


class NSSCamsManager(Screen):
    global HD_Res
    try:
        sz_w = getDesktop(0).size().width()
        if sz_w == 1280:
            HD_Res = True
        else:
            HD_Res = True
    except:
        HD_Res = False

    if HD_Res == True:
        # skin = '<screen name="NSSCamsManager" position="center,center" size="920,600" title="" flags="wfNoBorder">\n\t\t<widget name="list" position="60,50" size="800,401" scrollbarMode="showOnDemand" transparent="1" zPosition="2" />\n\t\t<ePixmap name="red" position="150,530" zPosition="2" size="34,47" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NssPanel/buttons/key_red.png" transparent="1" alphatest="on" />\n\t\t<ePixmap name="green" position="534,530" zPosition="2" size="34,47" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NssPanel/buttons/key_green.png" transparent="1" alphatest="on" />\n\t\t<widget name="key_red" position="188,534" size="209,40" valign="center" halign="center" zPosition="4" foregroundColor="white" font="Regular;20" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" />\n\t\t<widget name="key_green" position="572,534" size="209,40" valign="center" halign="center" zPosition="4" foregroundColor="white" font="Regular;20" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" />\n\t\t</screen>'

        skin = '''
        <screen name="NSSCamsManager" position="center,center" size="1280,720" title="" flags="wfNoBorder">
        <widget name="list" position="125,80" size="905,448" scrollbarMode="showOnDemand" transparent="1" zPosition="2" />
        <ePixmap name="red" position="116,532" zPosition="2" size="34,47" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NssPanel/buttons/key_red.png" transparent="1" alphatest="on" />
        <ePixmap name="green" position="342,532" zPosition="2" size="34,47" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NssPanel/buttons/key_green.png" transparent="1" alphatest="on" />
        <widget name="key_red" position="147,535" size="209,40" valign="center" halign="center" zPosition="4" foregroundColor="white" font="Regular;30" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" />
        <widget name="key_green" position="373,535" size="209,40" valign="center" halign="center" zPosition="4" foregroundColor="white" font="Regular;30" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" />
        </screen>
        '''
        
    def __init__(self, session, args = 0):
        self.session = session
        Screen.__init__(self, session)
        self.skin = NSSCamsManager.skin
        self.index = 0
        self.sclist = []
        self.namelist = []
        self.lastCam = ''
        self.oldService = self.session.nav.getCurrentlyPlayingServiceReference()
        self['actions'] = ActionMap(['OkCancelActions', 'ColorActions'], {'ok': self.action,
         'cancel': self.close,
         'green': self.action,
         'red': self.stop})
        self.CCcam = False
        self['key_red'] = Button(_('Stop'))
        self['key_green'] = Button(_('Start/Restart'))
        os.system('ln -sf /usr/keys /var/keys')
        self.lastCam = self.readCurrent()
        self.softcamlist = []
        self['info'] = Label()
        self['list'] = DCCMenu(self.softcamlist)
        self.readScripts()
        title = 'CamsManager'
        self.setTitle(title)
        self['pixmap'] = Pixmap()
        self.onShown.append(self.openCCcamInfo)

    def refresh(self):
        self.index = 0
        self.sclist = []
        self.namelist = []
        self.oldService = self.session.nav.getCurrentlyPlayingServiceReference()
        self.softcamlist = []
        self['list'].setList(self.softcamlist)
        self.readScripts()
        self.lastCam = self.readCurrent()
        title = 'CamsManager'
        self.setTitle(title)
        self.openCCcamInfo()

    def showcccaminfo(self):
        try:
            if 'cccam' in self.lastCam.lower():
                self.session.openWithCallback(CCcamInfoMain)
        except:
            pass

    def openCCcamInfo(self):
        try:
            if 'cccam' in self.lastCam.lower():
                self.CCcam = True
            else:
                self.CCcam = False
        except:
            self.CCcam = False

    def openTest(self):
        pass

    def getLastIndex(self):
        a = 0
        if len(self.namelist) > 0:
            for x in self.namelist:
                if x == self.lastCam:
                    return a
                a += 1

        else:
            return -1
        return -1

    def action(self):
        self.session.nav.playService(None)
        last = self.getLastIndex()
        var = self['list'].getSelectionIndex()
        try:
            os.remove('/tmp/ecm.info')
        except:
            pass

        self['info'].setText('')
        if last > -1:
            if last == var:
                self.cmd1 = '/usr/script/cam/' + self.sclist[var] + ' cam_res &'
                os.system(self.cmd1)
                os.system('sleep 3')
            else:
                self.cmd1 = '/usr/script/cam/' + self.sclist[last] + ' cam_down &'
                os.system(self.cmd1)
                os.system('sleep 2')
                self.cmd1 = '/usr/script/cam/' + self.sclist[var] + ' cam_up &'
                os.system(self.cmd1)
        else:
            try:
                self.cmd1 = '/usr/script/cam/' + self.sclist[var] + ' cam_up &'
                os.system(self.cmd1)
                os.system('sleep 3')
            except:
                self.refresh
                return

        if last != var:
            try:
                self.lastCam = self['list'].l.getCurrentSelection()[1][7]
                self.writeFile()
            except:
                self.refresh
                return

        print self.cmd1
        self.readScripts()
        self.session.nav.playService(self.oldService)
        self.refresh
        return

    def writeFile(self):
        if self.lastCam is not None:
            clist = open('/etc/clist.list', 'w')
            clist.write(self.lastCam)
            clist.close()
        stcam = open('/etc/startcam.sh', 'w')
        stcam.write('#!/bin/sh\n' + self.cmd1)
        stcam.close()
        self.cmd2 = 'chmod 755 /etc/startcam.sh &'
        os.system(self.cmd2)
        return

    def stop(self):
        self.session.nav.playService(None)
        last = self.getLastIndex()
        if last > -1:
            self.cmd1 = '/usr/script/cam/' + self.sclist[last] + ' cam_down &'
            os.system(self.cmd1)
        else:
            return
        self.lastCam = 'no'
        self.writeFile()
        os.system('sleep 4')
        self.readScripts()
        self['info'].setText(' ')
        self.session.nav.playService(self.oldService)
        return

    def readScripts(self):
        self.index = 0
        scriptliste = []
        pliste = []
        path = '/usr/script/cam/'
        for root, dirs, files in os.walk(path):
            for name in files:
                scriptliste.append(name)

        self.sclist = scriptliste
        i = len(self.softcamlist)
        del self.softcamlist[0:i]
        for lines in scriptliste:
            dat = path + lines
            sfile = open(dat, 'r')
            for line in sfile:
                if line[0:3] == 'OSD':
                    nam = line[5:len(line) - 2]
                    if self.lastCam is not None:
                        if nam == self.lastCam:
                            self.softcamlist.append(DreamCCExtra(name=nam, index=self.index, isActive=True))
                        else:
                            self.softcamlist.append(DreamCCExtra(name=nam, index=self.index, isActive=False))
                        self.index += 1
                    else:
                        self.softcamlist.append(DreamCCExtra(name=nam, index=self.index, isActive=False))
                        self.index += 1
                    pliste.append(nam)

            sfile.close()
            self['list'].setList(self.softcamlist)
            self.namelist = pliste

        return

    def readCurrent(self):
        lastcam = ''
        try:
            clist = open('/etc/clist.list', 'r')
        except:
            return

        if clist is not None:
            for line in clist:
                lastcam = line

            clist.close()
        return lastcam

    def autocam(self):
        current = None
        try:
            clist = open('/etc/clist.list', 'r')
            print 'found list'
        except:
            return

        if clist is not None:
            for line in clist:
                current = line

            clist.close()
        print 'current =', current
        if os.path.isfile('/etc/autocam.txt') is False:
            alist = open('/etc/autocam.txt', 'w')
            alist.close()
        self.cleanauto()
        alist = open('/etc/autocam.txt', 'a')
        alist.write(self.oldService.toString() + '\n')
        last = self.getLastIndex()
        alist.write(current + '\n')
        alist.close()
        self.session.openWithCallback(self.callback, MessageBox, _('Autocam assigned to the current channel'), type=1, timeout=10)
        return

    def cleanauto(self):
        delemu = 'no'
        if os.path.isfile('/etc/autocam.txt') is False:
            return
        myfile = open('/etc/autocam.txt', 'r')
        myfile2 = open('/etc/autocam2.txt', 'w')
        icount = 0
        for line in myfile.readlines():
            if line[:-1] == self.oldService.toString():
                delemu = 'yes'
                icount = icount + 1
                continue
            if delemu == 'yes':
                delemu = 'no'
                icount = icount + 1
                continue
            myfile2.write(line)
            icount = icount + 1

        myfile.close()
        myfile2.close()
        os.system('rm /etc/autocam.txt')
        os.system('cp /etc/autocam2.txt /etc/autocam.txt')