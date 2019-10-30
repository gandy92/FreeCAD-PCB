# -*- coding: utf8 -*-
#****************************************************************************
#*                                                                          *
#*   Printed Circuit Board Workbench for FreeCAD             PCB            *
#*   Flexible Printed Circuit Board Workbench for FreeCAD    FPCB           *
#*   Copyright (c) 2013, 2014, 2015                                         *
#*   marmni <marmni@onet.eu>                                                *
#*                                                                          *
#*                                                                          *
#*   This program is free software; you can redistribute it and/or modify   *
#*   it under the terms of the GNU Lesser General Public License (LGPL)     *
#*   as published by the Free Software Foundation; either version 2 of      *
#*   the License, or (at your option) any later version.                    *
#*   for detail see the LICENCE text file.                                  *
#*                                                                          *
#*   This program is distributed in the hope that it will be useful,        *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of         *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          *
#*   GNU Library General Public License for more details.                   *
#*                                                                          *
#*   You should have received a copy of the GNU Library General Public      *
#*   License along with this program; if not, write to the Free Software    *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307   *
#*   USA                                                                    *
#*                                                                          *
#****************************************************************************
import FreeCAD
from PySide import QtCore, QtGui
import sys

__scriptVersion__ = 5.0
__dataBaseVersion__ = 2.0
__pythonVersion__ = 3.6
__requiredFreeCADVersion__ = (0.18, 0.18)  # (min, max)


def currentFreeCADVersion():
    data = FreeCAD.Version()
    print("currentFreeCADVersion():", data)
    return float(data[0] + '.' + data[1].split('.')[0])


def checkPythonVesion():
    currentVersion = float(sys.version_info[0] + '.' + sys.version_info[1])
    if currentVersion < __pythonVersion__:
        return False
    else:
        return [True]

def checkCompatibility():
    ''' InitGui -> Initialize() '''
    currentFCVersion = currentFreeCADVersion()
    
    if currentFCVersion >= __requiredFreeCADVersion__[0] and currentFCVersion <= __requiredFreeCADVersion__[1]:
        print("Python version:", sys.version_info)
        if float("{0}.{1}".format(sys.version_info[0], sys.version_info[1])) < __pythonVersion__:
            return [False, "Error. Minimum required Python version: {0}.".format(__pythonVersion__)]
        else:
            return [True]
    else:
        return [False, "Error. Incompatible FreeCAD version. Supported FreeCAD versions: {0}-{1}.\n".format(__requiredFreeCADVersion__[0], __requiredFreeCADVersion__[1])]


def checkdataBaseVersion():
    ''' PCBdataBase -> checkVersion() '''
    version = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/PCB").GetFloat("dataBaseVersion", 0.0)
        
    if float(version) < __dataBaseVersion__:
        dial = QtGui.QMessageBox()
        dial.setText(u"Old database format detected - upgrading database format is required. This may take several seconds.")
        dial.setWindowTitle("Caution!")
        dial.setIcon(QtGui.QMessageBox.Question)
        rewT = dial.addButton('Ok', QtGui.QMessageBox.YesRole)
        dial.exec_()
        
        return False
    else:
        return True


def setDefaultValues():
    ''' InitGui -> Initialize() '''
    data = {
        "dataBaseVersion" : ['f', __dataBaseVersion__],
        "scriptVersion" : ['f', __scriptVersion__]
    }

    for i,j in data.items():
        if j[0] == 'f' and FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/PCB").GetFloat(i, 0.0) == 0.0:
            FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/PCB").SetFloat(i, float(j[1]))

