#updated Lululla 24/10/2018 Skin FHD
PANELVER = '0.1.1'
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.Standby import TryQuitMainloop
from Screens.Console import Console
from enigma import eTimer, loadPic, eDVBDB, eConsoleAppContainer
from xml.dom import Node, minidom
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Sources.List import List
from Components.ProgressBar import ProgressBar
from Components.ScrollLabel import ScrollLabel
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Components.config import config, ConfigDirectory, ConfigSubsection, ConfigSubList, ConfigEnableDisable, ConfigNumber, ConfigText, ConfigSelection, ConfigYesNo, ConfigPassword, getConfigListEntry, configfile
from Components.PluginComponent import plugins
from Components.Sources.StaticText import StaticText
from Components.Pixmap import Pixmap, MultiPixmap
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import fileExists, pathExists, createDir, resolveFilename, SCOPE_PLUGINS, SCOPE_CURRENT_SKIN
from os import popen, system, remove, listdir, chdir, getcwd, statvfs, mkdir, path, walk
import os
import sys
from Plugins.Plugin import PluginDescriptor
from Components.Sources.Progress import Progress
from Plugins.Extensions.NssPanel.CamEx import NSSCamsManager
from Tools import Notifications
from Tools.Directories import resolveFilename, pathExists, SCOPE_MEDIA, copyfile, fileExists
import xml.etree.cElementTree as x


#lululla
def ReloadBouquet():
    eDVBDB.getInstance().reloadServicelist()
    eDVBDB.getInstance().reloadBouquets() 
    

def GetSkinPath():
    myskinpath = resolveFilename(SCOPE_CURRENT_SKIN, '')
    myskinpath = '/usr/lib/enigma2/python/Plugins/Extensions/NssPanel/'
    return myskinpath


def getVarSpaceKb():
    try:
        s = statvfs('/')
    except OSError:
        return (0, 0)

    return (float(s.f_bfree * (s.f_bsize / 1024)), float(s.f_blocks * (s.f_bsize / 1024)))


class util:
    pluginIndex = -1
    pluginType = ''
    typeDownload = 'A'
    addonsName = ''
    filename = ''
    dir = ''
    size = 0
    check = 0

    def reloadSetting(self):
        print 'Reload settings'
        self.eDVBDB = eDVBDB.getInstance()
        self.eDVBDB.reloadServicelist()
        self.eDVBDB.reloadBouquets()


u = util()

class loadTmpDir:
    tmp_list = []

    def load(self):
        del self.tmp_list[:]
        pkgs = listdir('/tmp')
        count = 0
        for fil in pkgs:
            if fil.find('.ipk') != -1 or fil.find('.tar.gz') != -1 or fil.find('.zip') != -1:
                self.tmp_list.append([count, fil])
                count += 1


loadtmpdir = loadTmpDir()

class loadUniDir:
    uni_list = []

    def load(self):
        del self.uni_list[:]
        pkgs = listdir('/usr/uninstall')
        count = 0
        for fil in pkgs:
            if fil.find('_remove.sh') != -1:
                self.uni_list.append([count, fil])
                count += 1


loadunidir = loadUniDir()

class loadXml:
    tree_list = []
    plugin_list = []

    def load(self, filename):
        del self.tree_list[:]
        del self.plugin_list[:]
        tree = x.parse(filename)
        root = tree.getroot()
        c = 0
        for tag in root.getchildren():
            self.tree_list.append([c, tag.tag])
            c1 = 0
            for b in tree.find(tag.tag):
                self.plugin_list.append([c,
                 tag.tag,
                 b.find('Filename').text,
                 b.find('Descr').text,
                 b.find('Folder').text,
                 b.find('Size').text,
                 b.find('Check').text,
                 c1])
                c1 += 1

            c += 1


loadxml = loadXml()

def linkAddons():
    try:
        f = open('/var/etc/nssaddons.url', 'r')
        line = f.readline()
        f.close()
        return line[:-1]
    except:
        return 'http://nonsolosat.net/nsspannelopen/file/'


class NssMenu(Screen):
    __module__ = __name__
    #skin = '\n\t<screen name="NSS Panel" position="center,center" size="800,600" title="NSS Panel">\n\t  <widget source="list" render="Listbox" position="15,80" size="730,500" scrollbarMode="showOnDemand">\n\t    <convert type="TemplatedMultiContent">\n\t\t\t\t\t\t{"template": [\n\t\t\t\t\t\t\t\tMultiContentEntryText(pos = (90, 5), size = (300, 30), font=0, flags = RT_HALIGN_LEFT | RT_HALIGN_LEFT, text = 1),\n\t\t\t\t\t\t\t\tMultiContentEntryText(pos = (110, 30), size = (640, 50), font=0, flags = RT_VALIGN_TOP, text = 2),\n\t\t\t\t\t\t\t\tMultiContentEntryPixmapAlphaTest(pos=(5, 1), size=(72, 72), png = 3),\n\t\t\t\t\t\t\t\t],\n\t\t\t\t\t\t"fonts": [gFont("Regular", 20)],\n\t\t\t\t\t\t"itemHeight": 80\n\t\t\t\t\t\t}\n\t\t\t\t</convert>\n\t  </widget>\n\t  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NssPanel/icons/logo.png" position="30,0" size="711,76" alphatest="on" />\t\n\t  <widget source="conn" render="Label" position="15,540" size="730,35" font="Regular;20" halign="center" valign="center" transparent="1" />\n\t</screen>'

    skin = '''
    <screen name="NSS Panel" position="center,center" size="1280,720" title="NSS Panel">
    <widget source="list" render="Listbox" position="333,104" size="554,493" scrollbarMode="showOnDemand">
    <convert type="TemplatedMultiContent">
        {"template": [
        MultiContentEntryText(pos = (90, 5), size = (300, 30), font=0, flags = RT_HALIGN_LEFT | RT_HALIGN_LEFT, text = 1),
        MultiContentEntryText(pos = (110, 30), size = (640, 50), font=0, flags = RT_VALIGN_TOP, text = 2),
        MultiContentEntryPixmapAlphaTest(pos=(5, 1), size=(72, 72), png = 3),
        ],
        "fonts": [gFont("Regular", 30)],
        "itemHeight": 80
        }
    </convert>
    </widget>
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NssPanel/icons/logo.png" position="245,0" size="711,76" alphatest="on" />
    <widget source="conn" render="Label" position="247,600" size="812,35" font="Regular;30" halign="center" valign="center" transparent="1" />
    </screen>
    '''    
    
    
    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self['conn'] = StaticText('')
        self['spaceused'] = ProgressBar()
        self.container = eConsoleAppContainer()
        self.container.appClosed.append(self.runFinished)
        self.containerExtra = eConsoleAppContainer()
        self.containerExtra.appClosed.append(self.runFinishedExtra)
        self.readUrl = linkAddons()
        self.MenuList = [('CamEx',
          'Cam Manager',
          'Imposta Cam',
          'icons/cam.png',
          True),
         ('DownAdd',
          'Download Addons',
          'Scarica plugin',
          'icons/downloads.png',
          True),
         ('ManInstall',
          'Manual Install',
          'Installa Manuale',
          'icons/manual.png',
          True),
         ('RemAddons',
          'Remove addons',
          'Disinstalla plugin',
          'icons/remove.png',
          True),
         ('ScriptEx',
          'Script Executer',
          'Esegui Script',
          'icons/script.png',
          True),
         ('RebBox',
          'Restart',
          'Riavvia',
          'icons/reboot.png',
          True)]
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.cancel,
         'back': self.cancel})
        self.onLayoutFinish.append(self.updateList)
        self.onShown.append(self.setWindowTitle)

    def ConvertSize(self, size):
        size = int(size)
        if size >= 1073741824:
            Size = '%0.2f TB' % (size / 1073741824.0)
        elif size >= 1048576:
            Size = '%0.2f GB' % (size / 1048576.0)
        elif size >= 1024:
            Size = '%0.2f MB' % (size / 1024.0)
        else:
            Size = '%0.2f KB' % size
        return str(Size)

    def setWindowTitle(self):
        diskSpace = getVarSpaceKb()
        percFree = int(diskSpace[0] / diskSpace[1] * 100)
        percUsed = int((diskSpace[1] - diskSpace[0]) / diskSpace[1] * 100)
        self.setTitle('%s - %s: %s (%d%%)' % (_('NSS Addons'),
         _('Free'),
         self.ConvertSize(int(diskSpace[0])),
         percFree))
        self['spaceused'].setValue(percUsed)

    def KeyOk(self):
        self['conn'].text = ''
        if not self.container.running():
            sel = self['list'].getCurrent()[0]
            if sel == 'CamEx':
                self.session.open(NSSCamsManager)
            elif sel == 'DownAdd':
                self['conn'].text = _('Connetting to addons server. Please wait...')
                if self.readUrl != None:
                    self.containerExtra.execute('wget ' + self.readUrl + 'nsspanelset/tmp.tmp -O /tmp/tmp.tmp')
                else:
                    self['conn'].text = _('Server not found!\nPlease check internet connection.')
            elif sel == 'ManInstall':
                self.session.open(ManualInstall)
            elif sel == 'RemAddons':
                self.session.open(RemoveAddons)
            elif sel == 'ScriptEx':
                self.session.open(ScriptExecuter)
            elif sel == 'RebBox':
                msg = _('Do you want reboot now?')
                box = self.session.openWithCallback(self.rebootBox, MessageBox, msg, MessageBox.TYPE_YESNO)
                box.setTitle(_('Restart Decoder'))
        return

    def runFinishedExtra(self, retval):
        if fileExists('/tmp/tmp.tmp'):
            try:
                f = open('/tmp/tmp.tmp', 'r')
                line = f.readline()[:-1]
                f.close()
                self.container.execute('wget ' + self.readUrl + 'nsspanelset/' + line + ' -O /tmp/addons.xml')
            except:
                self['conn'].text = _('Server not found! Please check internet connection.')

        else:
            self['conn'].text = _('Server not found! Please check internet connection.')

    def runFinished(self, retval):
        if fileExists('/tmp/addons.xml'):
            try:
                loadxml.load('/tmp/addons.xml')
                remove('/tmp/addons.xml')
                self['conn'].text = ''
                self.session.open(ListaFile)
            except:
                self['conn'].text = _('File xml is not correctly formatted!')

        else:
            self['conn'].text = _('Server not found! Please check internet connection.')

    def cancel(self):
        if not self.container.running() and not self.containerExtra.running():
            del self.container.appClosed[:]
            del self.container
            del self.containerExtra.appClosed[:]
            del self.containerExtra
            self.close()
        else:
            if self.container.running():
                self.container.kill()
            if self.containerExtra.running():
                self.containerExtra.kill()
            if fileExists('/tmp/addons.xml'):
                remove('/tmp/addons.xml')
            if fileExists('/tmp/tmp.tmp'):
                remove('/tmp/tmp.tmp')
            self['conn'].text = _('Process Killed by user. Server Not Connected!')

    def updateList(self):
        del self.list[:]
        skin_path = GetSkinPath()
        for i in self.MenuList:
            if i[4]:
                self.list.append((i[0],
                 i[1],
                 i[2],
                 LoadPixmap(skin_path + i[3])))

        self['list'].setList(self.list)

    def PluginDownloadBrowserClosed(self):
        self.updateList()

    def rebootBox(self, answer):
        if answer is True:
            system('reboot')


class ListaFile(Screen):
    __module__ = __name__
    #skin = '\n\t<screen name="DownloadsList" position="center,center" size="800,600" title="Downloads Lista">\n\t  <widget source="list" render="Listbox" position="12,6" size="750,480" scrollbarMode="showOnDemand">\n\t    <convert type="TemplatedMultiContent">\n\t\t\t\t\t\t{"template": [\n\t\t\t\t\t\t\t\tMultiContentEntryText(pos = (5, 5), size = (700, 30), font=0, flags = RT_HALIGN_LEFT | RT_HALIGN_LEFT, text = 1),\n\t\t\t\t\t\t\t\t],\n\t\t\t\t\t\t"fonts": [gFont("Regular", 20)],\n\t\t\t\t\t\t"itemHeight": 36\n\t\t\t\t\t\t}\n\t\t\t\t</convert>\n\t  </widget>\n\t  <ePixmap position="136,532" size="34,47" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NssPanel/buttons/key_red.png" alphatest="on" />\n\t  <ePixmap position="422,532" size="32,47" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NssPanel/buttons/key_green.png" alphatest="on" />\n\t  <widget name="key_red" position="177,535" zPosition="1" size="209,40" font="Regular;20" halign="center" valign="center" backgroundColor="#009f1313" transparent="1" />\n\t  <widget name="key_green" position="453,535" zPosition="1" size="209,40" font="Regular;20" halign="center" valign="center" backgroundColor="#009f1313" transparent="1" />\n\t</screen>'

    skin = '''
    <screen name="DownloadsList" position="center,center" size="1280,720" title="Downloads">
    <widget source="list" render="Listbox" position="125,80" size="905,447" zPosition="2" scrollbarMode="showOnDemand" transparent="1">
    <convert type="TemplatedMultiContent">
           {"template": [
           MultiContentEntryText(pos = (5, 5), size = (720, 34), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 1),
           ],
           "fonts": [gFont("Regular", 30)],
           "itemHeight": 45
           }
    </convert>
    </widget>

    <widget source="conn" render="Label" position="125,582" size="930,70" font="Regular;30" halign="center" valign="center" transparent="1" />
    <ePixmap position="116,532" size="34,47" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NssPanel/buttons/key_red.png" alphatest="on" />
    <ePixmap position="342,532" size="32,47" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NssPanel/buttons/key_green.png" alphatest="on" />
    <widget name="key_red" position="147,535" zPosition="1" size="209,40" font="Regular;30" halign="center" valign="center" backgroundColor="#009f1313" transparent="1" />
    <widget name="key_green" position="373,535" zPosition="1" size="209,40" font="Regular;30" halign="center" valign="center" backgroundColor="#009f1313" transparent="1" />
    </screen>
    '''
    
    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self['key_red'] = Label(_('Cancel'))
        self['key_green'] = Label(_('Continue'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'back': self.close,
         'red': self.close,
         'green': self.KeyOk})
        self.onLayoutFinish.append(self.loadData)
        self.onShown.append(self.setWindowTitle)

    def setWindowTitle(self):
        self.setTitle(self.title)

    def KeyOk(self):
        u.pluginType = self['list'].getCurrent()[0]
        u.pluginIndex = self['list'].getIndex()
        self.session.open(DownloadFile)

    def loadData(self):
        del self.list[:]
        for tag in loadxml.tree_list:
            self.list.append((tag[1], tag[1]))

        self['list'].setList(self.list)


class DownloadFile(Screen):
    __module__ = __name__
    #skin = '\n\t<screen name="DownloadsList" position="center,center" size="800,600" title="Downloads">\n\t  <widget source="list" render="Listbox" position="12,6" size="750,470" zPosition="2" scrollbarMode="showOnDemand" transparent="1">\n\t    <convert type="TemplatedMultiContent">\n\t           {"template": [\n\t           MultiContentEntryText(pos = (5, 5), size = (720, 34), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 1),\n\t           ],\n\t           "fonts": [gFont("Regular", 20)],\n\t           "itemHeight": 45\n\t          }\n\t        </convert>\n\t  </widget>\n\t  <ePixmap position="136,532" size="34,47" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NssPanel/buttons/key_red.png" alphatest="on" />\n\t  <ePixmap position="422,532" size="32,47" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NssPanel/buttons/key_green.png" alphatest="on" />\n\t  <widget source="conn" render="Label" position="137,476" size="540,48" font="Regular;20" halign="center" valign="center" transparent="1" />\n\t  <widget name="key_red" position="169,535" zPosition="1" size="209,40" font="Regular;20" halign="center" valign="center" backgroundColor="#009f1313" transparent="1" />\n\t  <widget name="key_green" position="453,535" zPosition="1" size="209,40" font="Regular;20" halign="center" valign="center" backgroundColor="#009f1313" transparent="1" />\n\t</screen>'

    skin = '''
    <screen name="DownloadsList" position="center,center" size="1280,720" title="Downloads">
    <widget source="list" render="Listbox" position="125,80" size="905,447" zPosition="2" scrollbarMode="showOnDemand" transparent="1">
    <convert type="TemplatedMultiContent">
        {"template": [
        MultiContentEntryText(pos = (5, 5), size = (720, 34), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 1),
        ],
        "fonts": [gFont("Regular", 30)],
        "itemHeight": 45
        }
    </convert>
    </widget>

    <widget source="conn" render="Label" position="125,582" size="930,70" font="Regular;30" halign="center" valign="center" transparent="1" />
    
    <ePixmap position="116,532" size="34,47" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NssPanel/buttons/key_red.png" alphatest="on" />
    <ePixmap position="342,532" size="32,47" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NssPanel/buttons/key_green.png" alphatest="on" />
    <widget name="key_red" position="147,535" zPosition="1" size="209,40" font="Regular;30" halign="center" valign="center" backgroundColor="#009f1313" transparent="1" />
    <widget name="key_green" position="373,535" zPosition="1" size="209,40" font="Regular;30" halign="center" valign="center" backgroundColor="#009f1313" transparent="1" />
    </screen>
    '''    
    
    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self['conn'] = StaticText(_('Loading elements.\nPlease wait...'))
        self['type'] = Label('')
        self['key_red'] = Label(_('Cancel'))
        self['key_green'] = Label(_('Continue'))
        self.container = eConsoleAppContainer()
        self.container.appClosed.append(self.runFinished)
        self['type'].setText(_('Download ') + str(u.pluginType))
        self.readUrl = linkAddons()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'back': self.cancel,
         'red': self.cancel,
         'green': self.KeyOk})
        self.onLayoutFinish.append(self.loadPlugin)
        self.onShown.append(self.setWindowTitle)

    def setWindowTitle(self):
        self.setTitle(_('Download ') + str(u.pluginType))

    def KeyOk(self):
        if not self.container.running():
            self.sel = self['list'].getIndex()
            for tag in loadxml.plugin_list:
                if tag[0] == u.pluginIndex:
                    if tag[7] == self.sel:
                        u.addonsName = tag[3]
                        self.downloadAddons()
                        return

            self.close()

    def loadPlugin(self):
        del self.list[:]
        for tag in loadxml.plugin_list:
            if tag[0] == u.pluginIndex:
                self.list.append((tag[3], tag[3]))

        self['list'].setList(self.list)
        self['conn'].text = _('Elements Loaded!. Please select one to install.')

    def downloadAddons(self):
        self.getAddonsPar()
        if int(u.size) > int(getVarSpaceKb()[0]) and int(u.check) != 0:
            msg = _('Not enough space!\nPlease delete addons before install new.')
            self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
            return
        url = self.readUrl + u.dir + '/' + u.filename
        self.session.openWithCallback(self.executedScript, NssDownloader, url, '/tmp/', u.filename)

    def executedScript(self, *answer):
        if answer[0] == NssConsole.EVENT_DONE:
            if fileExists('/tmp/' + u.filename):
                msg = _('Do you want install the addon:\n%s?') % u.addonsName
                box = self.session.openWithCallback(self.installAddons, MessageBox, msg, MessageBox.TYPE_YESNO)
                box.setTitle(_('Install Addon'))
            else:
                msg = _('File: %s not found!\nPlease check your internet connection.') % u.filename
                self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
        elif answer[0] == NssConsole.EVENT_KILLED:
            self['conn'].text = _('Process Killed by user!\nAddon not downloaded.')

    def installAddons(self, answer):
        if answer is True:
            if u.filename.find('.ipk') != -1:
                dest = '/tmp/' + u.filename
                mydir = getcwd()
                chdir('/')
                cmd = 'opkg install --force-overwrite --force-reinstall ' + dest
                cmd2 = 'rm -f ' + dest
                self.session.open(Console, title=_('Ipk Package Installation'), cmdlist=[cmd, cmd2])
                chdir(mydir)
                self['conn'].text = _('Addon installed succesfully!')
            elif u.filename.find('.tar.gz') != -1:
                self.container.execute('tar -xzvf /tmp/' + u.filename + ' -C /')
                self['conn'].text = _('Please wait..Installing!')
                
                
                
                
            else:
                self['conn'].text = _('File: %s\nis not a valid package!') % u.filename
        elif fileExists('/tmp/' + u.filename):
            remove('/tmp/' + u.filename)

    def runFinished(self, retval):
        if fileExists('/tmp/' + u.filename):
            remove('/tmp/' + u.filename)
        self['conn'].text = _('Addon installed succesfully!')
        if u.pluginType.find('Setting') != -1:
            u.reloadSetting()
            print 'Settings reloaded succesfully!'
            self['conn'].text = _('Settings reloaded succesfully!')
        else:
            self['conn'].text = _('Reload Plugins list\nPlease Wait...')
            plugins.readPluginList(resolveFilename(SCOPE_PLUGINS))
            self['conn'].text = _('Addon installed succesfully!')

    def cancel(self):
        if not self.container.running():
            del self.container.appClosed[:]
            del self.container
            self.close()
        else:
            self.container.kill()
            self['conn'].text = _('Process Killed by user.\nAddon not installed correctly!')

    def restartEnigma2(self, answer):
        if answer is True:
            system('killall -9 enigma2')

    def getAddonsPar(self):
        for tag in loadxml.plugin_list:
            if tag[0] == u.pluginIndex:
                if tag[3] == u.addonsName:
                    u.filename = tag[2]
                    u.dir = tag[4]
                    u.size = tag[5]
                    u.check = tag[6]


class ManualInstall(Screen):
    __module__ = __name__
    # skin = '\n\t<screen name="ManualInstall" position="center,center" size="800,600" title="Manual Install">\n\t  <widget source="list" render="Listbox" position="12,6" size="772,476" scrollbarMode="showOnDemand">\n\t    <convert type="TemplatedMultiContent">\n\t\t\t\t\t\t{"template": [\n\t\t\t\t\t\t\t\tMultiContentEntryText(pos = (50, 5), size = (700, 30), font=0, flags = RT_HALIGN_LEFT | RT_HALIGN_LEFT, text = 1),\n\t\t\t\t\t\t\t\t],\n\t\t\t\t\t\t"fonts": [gFont("Regular", 20)],\n\t\t\t\t\t\t"itemHeight": 40\n\t\t\t\t\t\t}\n\t\t\t\t</convert>\n\t  </widget>\n\t  <widget source="conn" render="Label" position="104,485" size="608,48" font="Regular;20" halign="center" valign="center" transparent="1" />\n\t  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NssPanel/buttons/key_red.png" position="37,539" size="34,47" alphatest="on" />\n\t  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NssPanel/buttons/key_green.png" position="285,537" size="34,47" alphatest="on" />\n\t  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NssPanel/buttons/key_yellow.png" position="532,539" size="34,47" alphatest="on" />\n\t  <widget name="key_red" position="71,540" zPosition="1" size="209,40" font="Regular;20" halign="center" valign="center" backgroundColor="#009f1313" transparent="1" />\n\t  <widget name="key_yellow" position="565,540" zPosition="1" size="209,40" font="Regular;20" halign="center" valign="center" backgroundColor="#00a08500" transparent="1" />\n\t  <widget name="key_green" position="319,540" zPosition="1" size="209,40" font="Regular;20" halign="center" valign="center" backgroundColor="#00a08500" transparent="1" />\n\t</screen>'

    skin = '''
    <screen name="ManualInstall" position="center,center" size="1280,720" title="Manual Install">
    <widget source="list" render="Listbox" position="125,80" size="905,447" scrollbarMode="showOnDemand">
    <convert type="TemplatedMultiContent">
        {"template": [
        MultiContentEntryText(pos = (50, 5), size = (700, 30), font=0, flags = RT_HALIGN_LEFT | RT_HALIGN_LEFT, text = 1),
        ],
        "fonts": [gFont("Regular", 30)],
        "itemHeight": 40
        }
    </convert>
    </widget>
    <widget source="conn" render="Label" position="125,582" size="930,70" font="Regular;30" halign="center" valign="center" transparent="1" />
    <ePixmap position="116,532" size="34,47" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NssPanel/buttons/key_red.png" alphatest="on" />
    <ePixmap position="342,532" size="32,47" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NssPanel/buttons/key_green.png" alphatest="on" />
    <ePixmap position="572,532" size="34,47" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NssPanel/buttons/key_yellow.png" alphatest="on" />
    <ePixmap position="807,532" size="34,47" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NssPanel/buttons/key_blue.png" alphatest="on" />
    <widget name="key_red" position="147,535" zPosition="1" size="209,40" font="Regular;30" halign="center" valign="center" backgroundColor="#009f1313" transparent="1" />
    <widget name="key_green" position="373,535" zPosition="1" size="209,40" font="Regular;30" halign="center" valign="center" backgroundColor="#009f1313" transparent="1" />
    <widget name="key_yellow" position="605,535" zPosition="1" size="209,40" font="Regular;30" halign="center" valign="center" backgroundColor="#00a08500" transparent="1" />
    <widget name="key_blue" position="835,535" zPosition="1" size="209,40" font="Regular;30" halign="center" valign="center" backgroundColor="#00a08500" transparent="1" />
    
    </screen>
    '''
    
    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self['conn'] = StaticText('Put your file .tar.gz or .ipk or file setting .zip via FTP in /tmp.')
        self['key_red'] = Label(_('Cancel'))
        self['key_yellow'] = Label(_('Reload /tmp'))
        self['key_green'] = Label(_('Restart E2'))
        self['key_blue'] = Label(_('Remove'))
        
        self.container = eConsoleAppContainer()
        self.container.appClosed.append(self.runFinished)
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'yellow': self.readTmp,
         'red': self.cancel,
         'back': self.cancel,
         'blue':self.clean,
         'green': self.restartE2})
        self.onLayoutFinish.append(self.readTmp)

    def readTmp(self):
        del self.list[:]
        loadtmpdir.load()
        if len(loadtmpdir.tmp_list) > 0:
            for fil in loadtmpdir.tmp_list:
                self.list.append((fil[1], fil[1]))

        else:
            self['conn'].text = _('Put your file .tar.gz or .ipk or file settings.zip via FTP in /tmp.')
        self['list'].setList(self.list)

    def KeyOk(self):
        if not self.container.running():
            if len(loadtmpdir.tmp_list) > 0:
                self.sel = self['list'].getIndex()
                for p in loadtmpdir.tmp_list:
                    if p[0] == self.sel:
                        u.filename = p[1]

                msg = _('Do you want install the addon:\n%s?') % u.filename
                box = self.session.openWithCallback(self.installAddons, MessageBox, msg, MessageBox.TYPE_YESNO)
                box.setTitle(_('Install Addon'))
            else:
                self.close()
                
    def clean(self):
        if not self.container.running():
            if len(loadtmpdir.tmp_list) > 0:
                self.sel = self['list'].getIndex()
                for p in loadtmpdir.tmp_list:
                    if p[0] == self.sel:
                        u.filename = p[1]

                msg = _('Do you want remove:\n%s?') % u.filename
                box = self.session.openWithCallback(self.removeAddons, MessageBox, msg, MessageBox.TYPE_YESNO)
                box.setTitle(_('Remove - Clean /tmp'))
            else:
                self.close()                
                
    def removeAddons(self, answer):
        if answer is True:  
            if u.filename.find('.ipk') != -1 or u.filename.find('.tar.gz') != -1 or u.filename.find('.tgz') != -1 or u.filename.find('.tar') != -1 or u.filename.find('.zip') != -1:
                dest = '/tmp/' + u.filename
                mydir = getcwd()
                cmd = 'rm -f ' + dest
                self.session.open(Console, title='Remove - Clean /tmp', cmdlist=[cmd])
                chdir(mydir)            
                self['conn'].text = _('File: %s\nremoved succesfully!') % u.filename
                self.readTmp()
        
            else:
                self['conn'].text = _('File: %s\nis not a valid package!') % u.filename
        

    def installAddons(self, answer):
        if answer is True:
            self['conn'].text = _(' %s Installed!! RestartE2.') % u.filename
            if u.filename.find('.ipk') != -1:
                dest = '/tmp/' + u.filename
                mydir = getcwd()
                chdir('/')
                cmd = 'opkg install --force-overwrite --force-reinstall ' + dest
                cmd2 = 'rm -f ' + dest
                self.session.open(Console, title='Ipk Package Installation', cmdlist=[cmd, cmd2])
                chdir(mydir)
            elif u.filename.find('.tar.gz') != -1 or u.filename.find('.tgz') != -1:
                self.container.execute('tar -xzvf /tmp/' + u.filename + ' -C /')
                
            #lululla only settings.zip named files that contain non-folder settings - 
            elif u.filename.find('settings.zip') != -1 : #or u.filename.find('setting') != -1:
                dest = '/tmp/' + u.filename
                print 'Dest= ', dest
                os.system('rm -rf /etc/enigma2/lamedb')
                os.system('rm -rf /etc/enigma2/*.radio')
                os.system('rm -rf /etc/enigma2/*.tv')
                if not os.path.exists("/tmp/settings"):
                    os.makedirs("/tmp/settings")
                fdest1 = "/tmp/settings" 
                fdest2 = "/etc/enigma2"
                cmd1 = ("unzip -o -q %s -d %s") % (dest,fdest1)
                print "cmd1 =", cmd1
                cmd2 = ("cp -rf %s/* %s") % (fdest1,fdest2)
                print "cmd2 =", cmd2
                cmd3 = "wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &"
                cmd4 = "rm -rf %s" % fdest1
                cmd5 = "rm -rf /tmp/settings.zip"                
                cmd = []
                cmd.append(cmd1)
                cmd.append(cmd2)
                cmd.append(cmd3)
                cmd.append(cmd4)
                cmd.append(cmd5)                
                title = _("Installo i Settings")          
                self.session.open(Console,_(title),cmd,finishedCallback=self.readTmp, closeOnSuccess=True)
                
            #lululla end        
                
            else:
                self['conn'].text = _('File: %s\nis not a valid package!') % u.filename
             
            
    def runFinished(self, retval):
        plugins.readPluginList(resolveFilename(SCOPE_PLUGINS))
        remove('/tmp/' + u.filename)
        self['conn'].text = _('Addon: %s\ninstalled succesfully!') % u.filename
        self.readTmp()
        msg = _('Enigma2 will be now hard restarted to complete package installation.\nDo You want restart enigma2 now?')
        box = self.session.openWithCallback(self.restartEnigma2, MessageBox, msg, MessageBox.TYPE_YESNO)
        box.setTitle(_('Restart enigma'))

    def cancel(self):
        if not self.container.running():
            del self.container.appClosed[:]
            del self.container
            self.close()
        else:
            self.container.kill()
            self['conn'].text = _('Process Killed by user.\nAddon not installed correctly!')

    def restartEnigma2(self, answer):
        if answer is True:
            system('killall -9 enigma2')

    def restartE2(self):
        system('killall -9 enigma2')


class RemoveAddons(Screen):
    __module__ = __name__
    # skin = '\n\t<screen name="Remove Addons" position="center,center" size="800,600" title="Remove Addons">\n\t  <widget source="list" render="Listbox" position="12,6" size="611,481" scrollbarMode="showOnDemand">\n\t    <convert type="TemplatedMultiContent">\n\t\t\t\t\t\t{"template": [\n\t\t\t\t\t\t\t\tMultiContentEntryText(pos = (50, 5), size = (300, 30), font=0, flags = RT_HALIGN_LEFT | RT_HALIGN_LEFT, text = 1),\n\t\t\t\t\t\t\t\t],\n\t\t\t\t\t\t"fonts": [gFont("Regular", 20)],\n\t\t\t\t\t\t"itemHeight": 40\n\t\t\t\t\t\t}\n\t\t\t\t</convert>\n\t  </widget>\n\t  <widget source="conn" render="Label" position="105,500" size="608,45" font="Regular;20" halign="center" valign="center" transparent="1" />\n\t  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NssPanel/buttons/key_red.png" position="275,550" size="34,47" alphatest="on" />\n\t  <widget name="key_red" position="311,553" zPosition="1" size="209,40" font="Regular;20" halign="center" valign="center" backgroundColor="#009f1313" transparent="1" />\n\t</screen>'

    skin = '''
    <screen name="Remove Addons" position="center,center" size="1280,720" title="Remove Addons">
    <widget source="list" render="Listbox" position="125,80" size="905,448" scrollbarMode="showOnDemand">
    <convert type="TemplatedMultiContent">
        {"template": [
        MultiContentEntryText(pos = (50, 5), size = (300, 30), font=0, flags = RT_HALIGN_LEFT | RT_HALIGN_LEFT, text = 1),
        ],
        "fonts": [gFont("Regular", 30)],
        "itemHeight": 40
        }
        </convert>
    </widget>
    <widget source="conn" render="Label" position="125,582" size="930,70" font="Regular;30" halign="center" valign="center" transparent="1" />
    <ePixmap position="116,532" size="34,47" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NssPanel/buttons/key_red.png" alphatest="on" />
    <widget name="key_red" position="147,535" zPosition="1" size="209,40" font="Regular;30" halign="center" valign="center" backgroundColor="#009f1313" transparent="1" />
    </screen>
    '''
    
    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self['conn'] = StaticText('')
        self['key_red'] = Label(_('Remove'))
        self.container = eConsoleAppContainer()
        self.container.appClosed.append(self.runFinished)
        try:
            if not path.exists('/usr/uninstall'):
                mkdir('/usr/uninstall', 493)
        except:
            pass

        for fileinv in listdir('/usr/uninstall'):
            if fileinv.startswith('._'):
                remove(fileinv)

        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'back': self.cancel,
         'red': self.KeyOk})
        self.onLayoutFinish.append(self.readTmp)

    def PluginDownloadBrowserClosed(self):
        self.readTmp()

    def readTmp(self):
        loadunidir.load()
        del self.list[:]
        if len(loadunidir.uni_list) > 0:
            for fil in loadunidir.uni_list:
                self.list.append((fil[1], fil[1][:-10]))

        else:
            self['conn'].text = _('Nothing to uninstall!')
        self['list'].setList(self.list)

    def KeyOk(self):
        if not self.container.running():
            if len(loadunidir.uni_list) > 0:
                self.sel = self['list'].getIndex()
                for p in loadunidir.uni_list:
                    if p[0] == self.sel:
                        u.filename = p[1]

                msg = _('Are you sure you want remove the Package:\n%s?') % u.filename[:-10]
                box = self.session.openWithCallback(self.removeAddons, MessageBox, msg, MessageBox.TYPE_YESNO)
                box.setTitle(_('Remove Addon'))
            else:
                self.close()

    def removeAddons(self, answer):
        if answer is True:
            self['conn'].text = _('Removing: %s.\nPlease wait...') % u.filename[:-10]
            self.container.execute('/usr/uninstall/' + u.filename)

    def runFinished(self, retval):
        plugins.readPluginList(resolveFilename(SCOPE_PLUGINS))
        self.readTmp()
        self['conn'].text = _('Addons:\n %s \nPackege removed successfully.') % u.filename[:-10]
        msg = _('Enigma2 will be now hard restarted to complete package remove.\nDo You want restart enigma2 now?')
        box = self.session.openWithCallback(self.restartEnigma2, MessageBox, msg, MessageBox.TYPE_YESNO)
        box.setTitle(_('Restart enigma'))

    def cancel(self):
        if not self.container.running():
            del self.container.appClosed[:]
            del self.container
            self.close()
        else:
            self.container.kill()
            self['conn'].text = _('Process Killed by user.\nAddon not removed completly!')

    def restartEnigma2(self, answer):
        if answer is True:
            system('killall -9 enigma2')


class NssDownloader(Screen):
    __module__ = __name__
    # skin = '\n\t<screen name="NSS Downloader" position="center,center" size="607,185" title="Remove Addons">\n\t  <widget source="fname" render="Label" position="19,7" size="580,75" font="Regular;18" halign="center" valign="center" foregroundColor="blue" backgroundColor="black" transparent="1" />\n\t  <widget source="progressbar" render="Progress" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NssPanel/icons/progress.png" position="19,86" size="580,12" zPosition="2" transparent="1" />\n\t  <widget source="status" render="Label" position="19,102" zPosition="3" size="580,75" font="Regular;22" halign="center" backgroundColor="blue" transparent="1" />\n\t</screen>'
    skin = '''
    <screen name="NSS Downloader" position="center,center" size="607,185" title="Remove Addons">
    <widget source="fname" render="Label" position="19,7" size="580,75" font="Regular;30" halign="center" valign="center" foregroundColor="blue" backgroundColor="black" transparent="1" />
    <widget source="progressbar" render="Progress" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NssPanel/icons/progress.png" position="19,86" size="580,12" zPosition="2" transparent="1" />
    <widget source="status" render="Label" position="19,102" zPosition="3" size="580,75" font="Regular;30" halign="center" backgroundColor="blue" transparent="1" />
    </screen>
    '''
    
    
    EVENT_DONE = 10
    EVENT_KILLED = 5
    EVENT_CURR = 0

    def __init__(self, session, url, folder, filename):
        Screen.__init__(self, session)
        self.url = url
        self.filename = filename
        self.dstfilename = folder + filename
        self['oktext'] = Label(_('OK'))
        self['canceltext'] = Label(_('Cancel'))
        self['fname'] = StaticText('')
        self['status'] = StaticText('')
        self['progressbar'] = Progress()
        self['progressbar'].range = 1000
        self['progressbar'].value = 0
        self['actions'] = ActionMap(['WizardActions', 'DirectionActions', 'ColorActions'], {'ok': self.cancel,
         'back': self.cancel,
         'red': self.stop,
         'green': self.cancel}, -1)
        self.autoCloseTimer = eTimer()
        self.autoCloseTimer.timeout.get().append(self.cancel)
        self.startDownloadTimer = eTimer()
        self.startDownloadTimer.timeout.get().append(self.fileDownload)
        self.download = None
        self.downloading(False)
        self.onShown.append(self.setWindowTitle)
        self.onLayoutFinish.append(self.startDownload)
        return

    def setWindowTitle(self):
        self.setTitle(_('Downloading...'))

    def startDownload(self):
        self['progressbar'].value = 0
        self.startDownloadTimer.start(250, True)

    def downloading(self, state = True):
        if state:
            self['canceltext'].show()
            self['oktext'].hide()
        else:
            self.download = None
            self['canceltext'].hide()
            self['oktext'].show()
        return

    def fileDownload(self):
        from Tools.Downloader import downloadWithProgress
        print '[download] downloading %s to %s' % (self.url, self.dstfilename)
        self.download = downloadWithProgress(self.url, self.dstfilename)
        self.download.addProgress(self.progress)
        self.download.start().addCallback(self.finished).addErrback(self.failed)
        self.downloading(True)
        self['fname'].text = _('Downloading file: %s ...') % self.filename

    def progress(self, recvbytes, totalbytes):
        if self.download:
            self['progressbar'].value = int(1000 * recvbytes / float(totalbytes))
            self['status'].text = '%d of %d kBytes (%.2f%%)' % (recvbytes / 1024, totalbytes / 1024, 100 * recvbytes / float(totalbytes))

    def failed(self, failure_instance = None, error_message = ''):
        if error_message == '' and failure_instance is not None:
            error_message = failure_instance.getErrorMessage()
        print '[Download_failed] ' + error_message
        if fileExists(self.dstfilename):
            remove(self.dstfilename)
        self['fname'].text = _('Download file %s failed!') % self.filename
        self['status'].text = error_message
        self.EVENT_CURR = self.EVENT_KILLED
        self.downloading(False)
        return

    def finished(self, string = ''):
        if self.download:
            print '[Download_finished] ' + str(string)
            self.EVENT_CURR = self.EVENT_DONE
            self.downloading(False)
            self['oktext'].hide()
            self['fname'].text = _('Download file %s finished!') % self.filename
            self['status'].text = ''
            self.autoCloseTimer.start(200)

    def stop(self):
        if self.download:
            self.download.stop()
            self.downloading(False)
            if fileExists(self.dstfilename):
                remove(self.dstfilename)
            self.EVENT_CURR = self.EVENT_KILLED
            self['fname'].text = _('Downloading killed by user!')
            self['status'].text = _('Press OK to close window.')

    def cancel(self):
        if self.download == None:
            self.close(self.EVENT_CURR)
        return


class NssConsole(Screen):
    EVENT_DONE = 10
    EVENT_KILLED = 5
    EVENT_CURR = 0

    def __init__(self, session, cmd, Wtitle, large = False):
        Screen.__init__(self, session)
        if large:
            self.skinName = 'NssConsoleL'
        lang = config.osd.language.getText()
        self.cmd = cmd
        self.Wtitle = Wtitle
        self.callbackList = []
        self['text'] = ScrollLabel('')
        self['oktext'] = Label(_('OK'))
        self['canceltext'] = Label(_('Cancel'))
        self['actions'] = ActionMap(['WizardActions', 'DirectionActions', 'ColorActions'], {'ok': self.cancel,
         'back': self.cancel,
         'up': self['text'].pageUp,
         'down': self['text'].pageDown,
         'red': self.stop,
         'green': self.cancel}, -1)
        self['oktext'].hide()
        self.autoCloseTimer = eTimer()
        self.autoCloseTimer.timeout.get().append(self.cancel)
        self.container = eConsoleAppContainer()
        self.container.appClosed.append(self.runFinished)
        self.container.dataAvail.append(self.dataAvail)
        self.onLayoutFinish.append(self.startRun)
        self.onShown.append(self.setWindowTitle)

    def setWindowTitle(self):
        self.setTitle(self.Wtitle)

    def startRun(self):
        if self.container.execute(self.cmd):
            self.runFinished(-1)

    def runFinished(self, retval):
        self.EVENT_CURR = self.EVENT_DONE
        self['text'].setText(self['text'].getText() + _('Done') + '\n')
        self['canceltext'].hide()
        if config.nss.autocloseconsole.value:
            if int(config.nss.autocloseconsoledelay.value) != 0:
                self.autoCloseTimer.startLongTimer(int(config.nss.autocloseconsoledelay.value))
            else:
                self.cancel()
        else:
            self['text'].setText(self['text'].getText() + _('Please Press OK Button to close windows!') + '\n')
            self['oktext'].show()

    def stop(self):
        if self.isRunning():
            self.EVENT_CURR = self.EVENT_KILLED
            self['text'].setText(self['text'].getText() + _('Action killed by user') + '\n')
            self.container.kill()
            self['canceltext'].hide()
            if config.nss.autocloseconsole.value:
                if int(config.nss.autocloseconsoledelay.value) != 0:
                    self.autoCloseTimer.startLongTimer(int(config.nss.autocloseconsoledelay.value))
                else:
                    self.cancel()
            else:
                self['text'].setText(self['text'].getText() + _('Please Press OK Button to close windows!') + '\n')
                self['oktext'].show()

    def cancel(self):
        if not self.isRunning():
            if self.autoCloseTimer.isActive():
                self.autoCloseTimer.stop()
            del self.autoCloseTimer
            self.container.appClosed.remove(self.runFinished)
            self.container.dataAvail.remove(self.dataAvail)
            del self.container.dataAvail[:]
            del self.container.appClosed[:]
            del self.container
            self.close(self.EVENT_CURR)

    def dataAvail(self, str):
        self['text'].setText(self['text'].getText() + str)

    def isRunning(self):
        return self.container.running()


class ScriptExecuter(Screen):
    # skin = '\n\t<screen name="Script Panel" position="center,center" size="800,600">\n\t\t\t<widget source="list" render="Listbox" position="14,10" size="770,491" scrollbarMode="showOnDemand">\n\t\t\t\t<convert type="StringList" />\n\t\t\t</widget>\n\t\t\t<widget name="labstatus" position="14,510" size="800,30" font="Regular;21" valign="center" noWrap="1" backgroundColor="#333f3f3f" foregroundColor="#FFC000" shadowOffset="-2,-2" shadowColor="black" transparent="1" />\n\t  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NssPanel/buttons/key_red.png" position="275,550" size="34,47" alphatest="on" />\n\t  <widget name="key_red" position="311,553" zPosition="1" size="209,40" font="Regular;20" halign="center" valign="center" backgroundColor="#009f1313" transparent="1" />\n\t</screen>'

    skin = '''
    <screen name="Script Panel" position="center,center" size="1280,720">
    
    <widget source="list" render="Listbox" font="Regular;30" itemHeight="40" position="125,80" size="905,447" scrollbarMode="showOnDemand">
    <convert type="StringList" />
    </widget>
    
    <widget name="labstatus" position="136,582" size="895,48" font="Regular;30" valign="center" noWrap="1" backgroundColor="#333f3f3f" foregroundColor="#FFC000" shadowOffset="-2,-2" shadowColor="black" transparent="1" />
    <ePixmap position="116,532" size="34,47" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NssPanel/buttons/key_red.png" alphatest="on" />
    <widget name="key_red" position="147,535" zPosition="1" size="209,40" font="Regular;30" halign="center" valign="center" backgroundColor="#009f1313" transparent="1" />
    </screen>
    '''
    
    
    def __init__(self, session):
        Screen.__init__(self, session)
        self['labstatus'] = Label(_('NO SCRIPT FOUND'))
        self['key_red'] = Label(_('Execute'))
        self.mlist = []
        self.populateScript()
        self['list'] = List(self.mlist)
        self['list'].onSelectionChanged.append(self.schanged)
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.startScript,
         'back': self.close,
         'red': self.startScript})
        self.onLayoutFinish.append(self.script_sel)
        self.onShown.append(self.setWindowTitle)

    def setWindowTitle(self):
        self.setTitle(_('Script Panel'))

    def script_sel(self):
        self['list'].index = 1
        self['list'].index = 0

    def populateScript(self):
        try:
            if not path.exists('/usr/script'):
                mkdir('/usr/script', 493)
        except:
            pass

        myscripts = listdir('/usr/script')
        for fil in myscripts:
            if fil.find('.sh') != -1:
                fil2 = fil[:-3]
                desc = 'N/A'
                f = open('/usr/script/' + fil, 'r')
                for line in f.readlines():
                    if line.find('#DESCRIPTION=') != -1:
                        line = line.strip()
                        desc = line[13:]

                f.close()
                res = (fil2, desc)
                self.mlist.append(res)

    def schanged(self):
        mysel = self['list'].getCurrent()
        if mysel:
            mytext = ' ' + mysel[1]
            self['labstatus'].setText(mytext)

    def startScript(self):
        mysel = self['list'].getCurrent()
        if mysel:
            mysel = mysel[0]
            mysel2 = '/usr/script/' + mysel + '.sh'
            mytitle = 'NonSoloSat Script: ' + mysel
            self.session.open(Console, title=mytitle, cmdlist=[mysel2])


class DreamCCAuto:

    def __init__(self):
        self.readCurrent()

    def readCurrent(self):
        current = None
        try:
            clist = open('/etc/clist.list', 'r')
        except:
            return

        if clist is not None:
            for line in clist:
                current = line

            clist.close()
        scriptliste = []
        path = '/usr/script/cam/'
        for root, dirs, files in os.walk(path):
            for name in files:
                scriptliste.append(name)

        for lines in scriptliste:
            dat = path + lines
            datei = open(dat, 'r')
            for line in datei:
                if line[0:3] == 'OSD':
                    nam = line[5:len(line) - 2]
                    if current == nam:
                        if fileExists('/etc/init.d/dccamd'):
                            os.system('mv /etc/init.d/dccamd /etc/init.d/dccamdOrig &')
                        os.system('ln -sf /usr/bin /var/bin')
                        os.system('ln -sf /usr/keys /var/keys')
                        os.system('ln -sf /usr/scce /var/scce')
                        os.system('ln -sf /usr/script /var/script')
                        os.system('sleep 2')
                        os.system(dat + ' cam_startup &')

            datei.close()

        return


def autostartsoftcam(reason, session = None, **kwargs):
    global DreamCC_auto
    if reason == 0:
        try:
            if fileExists('/etc/init.d/dccamd'):
                os.system('mv /etc/init.d/dccamd /etc/init.d/dccamdOrig &')
            DreamCC_auto = DreamCCAuto()
        except:
            pass


def main(session, **kwargs):
    session.open(NssMenu)


def menu(menuid, **kwargs):
    if menuid == 'mainmenu':
        return [(_('NonSoloSat Panel'),
          main,
          'NonSoloSat_mainmenu',
          44)]
    return []


def Plugins(**kwargs):
    list = []
    list.append(PluginDescriptor(icon='icons/icon.png', name='NonSoloSat Panel', description='NonSoloSat Panel', where=PluginDescriptor.WHERE_MENU, fnc=menu))
    list.append(PluginDescriptor(icon='icons/icon.png', name='NonSoloSat Panel', description='Everything in one panel', where=PluginDescriptor.WHERE_PLUGINMENU, fnc=main))
    list.append(PluginDescriptor(where=[PluginDescriptor.WHERE_AUTOSTART], fnc=autostartsoftcam))
    return list