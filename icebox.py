#!/usr/bin/env python2.7
import sys
import shutil
import time
import subprocess
import os
import json
from PyQt4 import QtCore, QtGui, uic


qtCreatorFile = "icebox.ui" #gui template
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

licenseIcebox='''
________________________________________________________________________________
  ICEBOX -- A Trivial GUI Front End for ICESTROM FPGA FLOW                                                                                                    
  Copyright (C) 2018- Andrew Albert                                                                                                                     
  Permission to use, copy, modify, and/or distribute this software for any  
  purpose with or without fee is hereby granted, provided that the above    
  copyright notice and this permission notice appear in all copies.         
                                                                            
  THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES  
  WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF          
  MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR   
  ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES    
  WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN     
  ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF   
  OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.            
                                                                            
  Yosys,Arachne-pnr,icestrom are trademarks & software designs of their     
  respective creators/owners.
_________________________________________________________________________________
'''

iceParts = [
'iCE40-LP1K-SWG16TR',
'iCE40-LP384-CM36',
'iCE40-LP1K-CM36',
'iCE40-LP384-CM49',
'iCE40-LP1K-CM49',
'iCE40-LP1K-CM81',
'iCE40-LP4K-CM81',
'iCE40-LP8K-CM81',
'iCE40-LP1K-CM121',
'iCE40-LP4K-CM121',
'iCE40-LP8K-CM121',
'iCE40-LP4K-CM225',
'iCE40-LP8K-CM225',
'iCE40-HX8K-CM225',
'iCE40-LP384-QN32',
'iCE40-LP1K-QN84',
'iCE40-LP1K-CB81',
'iCE40-LP1K-CB121',
'iCE40-HX1K-CB132',
'iCE40-HX4K-CB132',
'iCE40-HX8K-CB132',
'iCE40-HX1K-VQ100',
'iCE40-HX1K-TQ144',
'iCE40-HX4K-TQ144',
'iCE40-HX8K-CT256']

arachne_opts={
'iCE40-LP1K-SWG16TR':'-d 1k -P swg16tr',
'iCE40-LP384-CM36'  :'-d 384 -P cm36',
'iCE40-LP1K-CM36'   :'-d 1k -P cm36',
'iCE40-LP384-CM49'  :'-d 384 -P cm49',
'iCE40-LP1K-CM49'   :'-d 1k -P cm49',
'iCE40-LP1K-CM81'   :'-d 1k -P cm81',
'iCE40-LP4K-CM81'   :'-d 8k -P cm81:4k',
'iCE40-LP8K-CM81'   :'-d 8k -P cm81',
'iCE40-LP1K-CM121'  :'-d 1k -P cm121',
'iCE40-LP4K-CM121'  :'-d 8k -P cm121:4k',
'iCE40-LP8K-CM121'  :'-d 8k -P cm121',
'iCE40-LP4K-CM225'  :'-d 8k -P cm225:4k',
'iCE40-LP8K-CM225'  :'-d 8k -P cm225',
'iCE40-HX8K-CM225'  :'-d 8k -P cm225',
'iCE40-LP384-QN32'  :'-d 384 -P qn32',
'iCE40-LP1K-QN84'   :'-d 1k -P qn84',
'iCE40-LP1K-CB81'   :'-d 1k -P cb81',
'iCE40-LP1K-CB121'  :'-d 1k -P cb121',
'iCE40-HX1K-CB132'  :'-d 1k -P cb132',
'iCE40-HX4K-CB132'  :'-d 8k -P cb132:4k',
'iCE40-HX8K-CB132'  :'-d 8k -P cb132',
'iCE40-HX1K-VQ100'  :'-d 1k -P vq100',
'iCE40-HX1K-TQ144'  :'-d 1k -P tq144',
'iCE40-HX4K-TQ144'  :'-d 8k -P tq144:4k',
'iCE40-HX8K-CT256'  :'-d 8k -P ct256'}

icetime_opts={
'iCE40-LP1K-SWG16TR':'-d lp1k',
'iCE40-LP384-CM36'  :'-d lp384',
'iCE40-LP1K-CM36'   :'-d lp1k',
'iCE40-LP384-CM49'  :'-d lp384',
'iCE40-LP1K-CM49'   :'-d lp1k',
'iCE40-LP1K-CM81'   :'-d lp1k',
'iCE40-LP4K-CM81'   :'-d lp8k',
'iCE40-LP8K-CM81'   :'-d lp8k',
'iCE40-LP1K-CM121'  :'-d lp1k',
'iCE40-LP4K-CM121'  :'-d lp8k',
'iCE40-LP8K-CM121'  :'-d lp8k',
'iCE40-LP4K-CM225'  :'-d lp8k',
'iCE40-LP8K-CM225'  :'-d lp8k',
'iCE40-HX8K-CM225'  :'-d hx8k',
'iCE40-LP384-QN32'  :'-d lp384',
'iCE40-LP1K-QN84'   :'-d lp1k',
'iCE40-LP1K-CB81'   :'-d lp1k',
'iCE40-LP1K-CB121'  :'-d lp1k',
'iCE40-HX1K-CB132'  :'-d hx1k',
'iCE40-HX4K-CB132'  :'-d hx8k',
'iCE40-HX8K-CB132'  :'-d hx8k',
'iCE40-HX1K-VQ100'  :'-d hx1k',
'iCE40-HX1K-TQ144'  :'-d hx1k',
'iCE40-HX4K-TQ144'  :'-d hx8k',
'iCE40-HX8K-CT256'  :'-d hx8k'	
}

documentation='''
______________________________________________________________________________
**TABs**
  INSTALL 
	* Select all of IceStorm, Arachne-PNR, Yosys 
	* Provide the password to install all software into your machine 
	* Only need to install these software once 
	* Ignore this option if you've installed the software by any other method
	* Software installation may take a while to finish

  PROJECT 
	* Name your project [stop_clock, Led_on_off etc...]
	* Add/Remove pcf file as required 
	* pcf file provides the place and route tool with pin location
  
  RTL 
	* Add/Remove RTL files that will be synthesized for this project 
	* Currently only Verilog HDL is supported
	* provide the name of the top level module 
  
  GENERATE
	* Select your FPGA package from the drop-down list 
	* Press "Generate FPGA Image" button to go through the flow
	* It will also generate a project file, so this project can be re-loaded

**MENU**
  LOAD_PROJECT 
	* Load a previously created project (.json)

  CLEAR_PROJECT
	* Clear The currently loaded project
_______________________________________________________________________________
'''
 
class MyApp(QtGui.QMainWindow, Ui_MainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)
		
		##define some fancy colors 
		self.blue  = QtGui.QColor(0,0,255)
		self.red   = QtGui.QColor(255,0,0)
		self.green = QtGui.QColor(0,128,0)
		self.black = QtGui.QColor(0,0,0)

		#set default transcript text color to blue
		self.statusEdit.setTextColor(self.blue)

		#print welcome message
		self.statusEdit.setText("Welcome to IceBox...")

		#move cursor to the end
		self.statusEdit.moveCursor(QtGui.QTextCursor.End)

		#set project tab as the default tab
		self.iceBoxTab.setCurrentIndex(1)

		#tab-1 => install 
		#set password input to secret mode
		self.lineEditPassword.setEchoMode(QtGui.QLineEdit.Password)
		#install software
		self.pushButtonInstall.clicked.connect(self.installSoftware)

		#tab-2 => project
		#add pcf
		self.pushButtonAddPcf.clicked.connect(self.addPcf)
		#remove pcf
		self.pushButtonRemovePcf.clicked.connect(self.removePcf)

		#tab-3 => RTL
		#add verilog
		self.pushButtonAddVerilog.clicked.connect(self.addVerilog)
		#remove verilog
		self.pushButtonRemoveVerilog.clicked.connect(self.removeVerilog)

		#tab-4 => Run
		#populate the fpga part numbers
		self.comboBoxFpgaPart.addItems(iceParts)
		#register the fpga part
		self.comboBoxFpgaPart.activated.connect(self.selectFPGA)
		#generate fpga image
		self.pushButtonGenerateFPGA.clicked.connect(self.generateFPGAImage)

		#menu actions
		#menu->project
		#menu->project->LoadProject
		self.actionLoadProject.triggered.connect(self.loadProject)
		self.actionClearProject.triggered.connect(self.clearProject)
		self.actionQuit.triggered.connect(QtCore.QCoreApplication.instance().quit)
		#menu->Help->About
		self.actionAbout.triggered.connect(self.about)
		self.actionDocumentation.triggered.connect(self.doc)

		
		
		#software address in a dict
		self.swAddr = 	{
							'icestorm'   :'https://github.com/cliffordwolf/icestorm.git',
							'arachne-pnr':'https://github.com/cseed/arachne-pnr.git',
							'yosys'      :'https://github.com/cliffordwolf/yosys.git'
						}		

		#set default workspace at $HOME+/icebox 
		self.workspace = os.environ['HOME']+"/icebox"
		self.homeDir   = os.environ['HOME']
		
		if not(os.path.isdir(self.workspace)):
			os.mkdir(self.workspace)
		self.statusEdit.append("workspace is set to "+self.workspace)
		
		self.icestormInstallDir = self.homeDir+"/icestorm"		
		self.arachneInstallDir  = self.homeDir+"/arachne"
		self.yosysInstallDir    = self.homeDir+"/yosys"
		
		##index for auto gen files 
		self.pcfTreeWidgetIndex     = 0
		self.verilogTreeWidgetIndex = 1
		self.yosysTreeWidgetIndex   = 2
		self.arachneTreeWidgetIndex = 3
		self.icepackTreeWidgetIndex = 4
		self.icetimeTreeWidgetIndex = 5
 
		#files
		self.pcfFile =""
		self.verilogFiles=[]
		self.yosysFile = "" 
		self.arachneFile = ""
		self.icepackFile = ""
		self.icetimeFile = ""

		self.buildTreeView()
		#when one of the files are clicked/selected 
		self.treeWidgetIceBox.itemActivated.connect(self.readHandler)
		
	def readHandler(self):
		
		getItems = self.treeWidgetIceBox.selectedItems()
    	
		baseNode = getItems[0]
		getChildNode = baseNode.text(0)
		
		if "/" in getChildNode:
			dir = str(getChildNode).split("/")[:-1]  #get file name
			dir = "/".join(dir)
			self.runCmdStdOut(["xdg-open "+dir])
	
	def doc(self):
		self.statusEdit.setTextColor(self.black)
		self.statusEdit.append(documentation)
		self.statusEdit.setTextColor(self.blue)

	def about(self):
		#print license information
		self.statusEdit.setTextColor(self.black)
		self.statusEdit.append(licenseIcebox)
		self.statusEdit.setTextColor(self.blue)
	
	def printSuccess(self,msg):
		#print success message in green !
		self.statusEdit.setTextColor(self.green)
		self.statusEdit.append(msg)
		self.statusEdit.setTextColor(self.blue)
	
	def printFail(self,msg):
		self.statusEdit.setTextColor(self.red)
		self.statusEdit.append(msg)
		self.statusEdit.setTextColor(self.blue)
	
	def gitClone(self,swName,installDir):
		self.statusEdit.append("Cloning "+swName+" from github")
		time.sleep(1)
		os.mkdir(installDir,0777)
		cloneResult=self.runCmdStdErr(["git clone --progress "+self.swAddr[swName]+" "+installDir])
		
		if cloneResult > 0 :
			self.printFail("Cloning of "+swName+" was unsuccessful")
		else:			
			self.printSuccess("Cloning of "+swName+" was successful")
		
		return cloneResult


	def rmSwFolder(self,swName):
		self.statusEdit.append("Removing Any Previous "+swName+" Installation...")
		shutil.rmtree(swName,ignore_errors=True)
		
	
	def makeSw(self,swName,installDir):
		self.statusEdit.append("making "+swName)
		self.statusEdit.append("this may take a while!")
		time.sleep(10)
		os.chdir(installDir)
		makeResult=self.runCmdStdOut(["make"])
		if (makeResult==0):
			self.printSuccess("Finished making "+swName+" successfully")
		else:
			self.printFail("Making of "+swName+" was unsuccessful")
		os.chdir(self.homeDir)
		return makeResult
	
	def makeInstall(self,swName,installDir,password):
		self.statusEdit.append("installing "+swName)
		self.statusEdit.append("this may take a while!")
		time.sleep(10)
		os.chdir(installDir)
		installResult=self.runCmdStdOut(['echo '+password+' | sudo -kS make install'])
		if (installResult==0):
			self.printSuccess("Installed "+swName+" successfully")
		else:
			self.printFail("Installation of "+swName+" was unsuccessful")
			
		os.chdir(self.homeDir)
		return installResult

	def incProgressBar(self,inc):
		value  = self.progressBarInstall.value()
		value += inc
		self.progressBarInstall.setValue(value)

	def installSoftware(self):
		
		self.progressBarInstall.setValue(0)	
		password = self.lineEditPassword.text()
		incValueEnable  = 11
		incValueDisable = 33
		installStateMachine = "check_password"

		installDone    = False 
		icestormResult = 0 
		arachneResult  = 0 
		yosysResult    = 0
		passwordEmpty  = False 

		while not(installDone):
			self.statusEdit.append(installStateMachine)
			if installStateMachine == "check_password":
				if password == "":
					self.printFail("password is empty, cannot install software!")
					passwordEmpty = True
					installStateMachine = "exit_installer"
				else:	
					self.statusEdit.append("Going to install software...")
					installStateMachine = "check_icestorm"

			#######################################################
			###install icestorm
			######################################################		
			elif installStateMachine == "check_icestorm":
				#run icestorm installation
				icestormResult = 0 

				if (self.checkBoxIceStrom.isChecked()):				
					self.statusEdit.append("Will install IceStrom...")				
					self.rmSwFolder(self.icestormInstallDir)
					time.sleep(0.1)			
					installStateMachine = "clone_icestorm"
				else:
					self.incProgressBar(incValueDisable)
					self.statusEdit.append("Not Installing Icestorm")
					installStateMachine = "check_arachne_pnr"
			
			elif installStateMachine == "clone_icestorm":

				if self.gitClone('icestorm',self.icestormInstallDir) == 0: #0 = cloning worked				
					self.incProgressBar(incValueEnable)
					installStateMachine = "make_icestorm"		
				else:
					#cloning failed
					icestormResult += 1
					installStateMachine = "check_arachne_pnr"
				
			elif installStateMachine == "make_icestorm":

				if self.makeSw('icestorm',self.icestormInstallDir) == 0: #icestorm make passed 
					self.incProgressBar(incValueEnable)
					installStateMachine = "install_icestorm"
				else:
					#making failed
					icestormResult += 1
					installStateMachine = "check_arachne_pnr"

			elif installStateMachine == "install_icestorm":
				
				if self.makeInstall('icestorm',self.icestormInstallDir,password)==0:
					self.incProgressBar(incValueEnable)				
				else:
					icestormResult += 1

				installStateMachine = "check_arachne_pnr"		

			#####################
			#install arachne-pnr
			elif installStateMachine == "check_arachne_pnr":
				arachneResult = 0
				if (self.checkBoxArachne.isChecked()):
					self.statusEdit.append("Will install Arachne-Pnr...")
					self.rmSwFolder(self.arachneInstallDir)
					installStateMachine = "clone_arachne_pnr"			
				else:
					self.incProgressBar(incValueDisable)
					self.statusEdit.append("Not Installing Arachne")
					installStateMachine = "check_yosys"
					
			elif installStateMachine == "clone_arachne_pnr":
				if self.gitClone('arachne-pnr',self.arachneInstallDir) == 0:					
					self.incProgressBar(incValueEnable)	
					installStateMachine = "make_arachne_pnr"
				else:
					arachneResult += 1 
					installStateMachine = "check_yosys"
			
			elif installStateMachine == "make_arachne_pnr":
				
				if self.makeSw('arachne-pnr',self.arachneInstallDir) == 0:						
					self.incProgressBar(incValueEnable)
					installStateMachine = "install_arachne_pnr"
				else:
					arachneResult += 1
					installStateMachine = "check_yosys"
			
			elif installStateMachine == "install_arachne_pnr":
							
				if self.makeInstall('arachne-pnr',self.arachneInstallDir,password) == 0:
								
					self.incProgressBar(incValueEnable)
							
				else:
					arachneResult += 1
				
				installStateMachine = "check_yosys"

			##############################################################
			#install yosys
			##############################################################
			#phase 1 
			
			elif installStateMachine == "check_yosys":
				yosysResult = 0 
				#check if yosys is supposed to be installed
				if (self.checkBoxYosys.isChecked()):
					self.statusEdit.append("Will install Yosys...")
					#remove any directories called yosys
					self.rmSwFolder(self.yosysInstallDir)
					
					installStateMachine = "clone_yosys"
				else:
					self.statusEdit.append("Not Installing Yosys!")
					self.incProgressBar(incValueDisable)
					installStateMachine = "exit_installer"				
			
			elif installStateMachine == "clone_yosys":
				if self.gitClone('yosys',self.yosysInstallDir) == 0:			
					self.incProgressBar(incValueEnable)
					installStateMachine = "make_yosys"
				else:
					yosysResult += 1
					installStateMachine = "exit_installer"
			
			elif installStateMachine == "make_yosys":

				if self.makeSw('yosys',self.yosysInstallDir) == 0:
					self.incProgressBar(incValueEnable)
					installStateMachine = "install_yosys"
				else:
					yosysResult += 1
					installStateMachine = "exit_installer"
					
							
			elif installStateMachine == "install_yosys":
							
				if self.makeInstall('yosys',self.yosysInstallDir,password) == 0:
					self.incProgressBar(incValueEnable)
				else:			
					yosysResult +=1
				
				installStateMachine = "exit_installer"

			elif installStateMachine == "exit_installer":
				result = 0
				if ((icestormResult > 0) or (arachneResult > 0 ) or (yosysResult > 0 )):
					result = 1 
				else:
					result = 0 

				if not(passwordEmpty):
					if result == 0 :
						self.progressBarInstall.setValue(100)
						self.printSuccess("Software installation Successful")
					else:
						self.printFail("Software installation failed")
						if (icestormResult > 0):
							self.printFail("icestorm installation failed")
						
						if (arachneResult > 0):
							self.printFail("arachne-pnr installation failed")
						
						if (yosysResult > 0):
							self.printFail("yosys installation failed")
					
					
				password = ""
				installDone = True

	def clearProject(self):
		self.pcfFile =""
		self.verilogFiles=[]
		self.yosysFile = "" 
		self.arachneFile = ""
		self.icepackFile = ""
		self.icetimeFile = ""
		self.lineEditProjectName.setText("")
		self.lineEditTopModule.setText("")
		self.comboBoxFpgaPart.setCurrentIndex(0)
		
		
		self.buildTreeView()
		self.iceBoxTab.setCurrentIndex(1)
		self.printSuccess("clearing the project was successful")

	def loadProject(self):
		self.projectFile = str(QtGui.QFileDialog.getOpenFileName(self, 'load .json project file',filter="*.json"))

		try:
			with open(self.projectFile) as json_data:
				project= json.load(json_data)

				self.pcfFile      = self.workspace+"/"+project['project']+"/"+project['pcf']
				
				self.verilogFiles = []
				for rtlFile in project['rtl']:
					self.verilogFiles.append(self.workspace+"/"+project['project']+"/"+rtlFile)

				self.yosysFile = "" 
				self.arachneFile = ""
				self.icepackFile = ""
				self.icetimeFile = ""
				
				self.lineEditProjectName.setText(project['project'])
				self.lineEditTopModule.setText(project['top_module'])
				index = self.comboBoxFpgaPart.findText(project['fpga'])
				self.comboBoxFpgaPart.setCurrentIndex(index)
				self.buildTreeView()
				#view run tab
				self.iceBoxTab.setCurrentIndex(3)
				self.printSuccess("Loading project "+self.projectFile+" Successful")
		except:
			self.printFail("project file does not exist")
		

	
	def readVerilogCmd(self):
		
		read_verilog = ""
		
		for v in self.verilogFiles:
			read_verilog = read_verilog+' read_verilog '+v+';'
		
		return read_verilog	
	
	#get file name from absolute file path/file_name.extension
	def getFileName(self,absFilePath):

		return os.path.basename(absFilePath)
	
	def verilogFileNameArray(self):
		vFileNameArray = [] 

		for v in self.verilogFiles:
			vFileNameArray.append(self.getFileName(v))

		return vFileNameArray

	
	def generateFPGAImage(self):
		
		self.projectName = str(self.lineEditProjectName.text())
		
		self.topName     = self.lineEditTopModule.text()
		self.progressBarGenerateFPGA.setValue(0)

		generateStateMachine = "check_project_name"
		generationFinished   = False

		self.yosysFile = "" 
		self.arachneFile = ""
		self.icepackFile = ""
		self.icetimeFile = ""

		while not(generationFinished):
			
			if (generateStateMachine=="check_project_name"):
				
				if self.projectName == "":
					self.printFail("Project name is empty : Not generating FPGA Image ") 
					self.printFail("Provide project name in Project Tab")
					generateStateMachine = "exit_generator"
				else:
					self.projectLocation = self.workspace+'/'+self.projectName
					
					#create project directory if it does not exist
					if not(os.path.isdir(self.projectLocation)):
						try:
							os.mkdir(self.projectLocation)
						except:
							self.printFail("Not able to create directory at "+self.projectLocation)
							generateStateMachine = "exit_generator"
					try:	
						os.chdir(self.projectLocation)
					except:
						self.printFail("Not able to change directory to "+self.projectLocation)
						generateStateMachine = "exit_generator"
						
					generateStateMachine = "check_top_name"
			
			elif (generateStateMachine=="check_top_name"):

				if self.topName == "": 
					self.printFail("Top module name is empty : Not generating FPGA Image ") 
					self.printFail("Provide top module name in RTL Tab")
					generateStateMachine = "exit_generator"
				else:
					generateStateMachine = "copy_rtl_files"
			
			
			elif (generateStateMachine=="copy_rtl_files"):
				
				tmp_verilog_files = []
				#check if verilog files are not empty
				if self.verilogFiles:
					#copy rtl files to the project folder
					for v in self.verilogFiles:
						
						rtlInProjectDirectory = self.projectLocation+"/"+self.getFileName(v)
						#check if verilog file is in the project folder
						if v != rtlInProjectDirectory:
							#verilog file does not exist in project folder, so copy
							try:
								shutil.copyfile(v,rtlInProjectDirectory)
							except:
								self.printFail("could not copy "+v+" to project directory")
								generateStateMachine = "exit_generator"
								
						tmp_verilog_files.append(self.projectLocation+"/"+self.getFileName(v))
					
					self.verilogFiles = tmp_verilog_files

					self.buildTreeView()

					generateStateMachine = "run_synthesis"
				
				else:					
					self.printFail("No verilog RTL Files added : Not generating FPGA Image ") 
					self.printFail("Provide RTL files in RTL Tab")
					generateStateMachine = "exit_generator"

			elif (generateStateMachine == "run_synthesis"):			
				
				self.yosysFile = self.projectLocation+'/'+self.projectName+'.blif'
				yosysCmd       = 'yosys -p \"'+self.readVerilogCmd()+' hierarchy -check -top '+self.topName+'; synth_ice40 -blif '+self.yosysFile+'\"'
				yosysStat      = self.runCmdStdOut([yosysCmd])

				if yosysStat== 0:
					self.printSuccess("RTL Synthesis Passed")
					self.progressBarGenerateFPGA.setValue(33)
					generateStateMachine = "copy_pcf_file"
				else:
					#yosys failed! clear the yosys out file
					self.yosysFile = "" 
					self.printSuccess("RTL Synthesis Failed : Not generating FPGA Image")
					generateStateMachine = "exit_generator"				
				
			elif (generateStateMachine=="copy_pcf_file"):
				if self.pcfFile == "":
					self.printFail("No .pcf constraints added to the project : Not generating FPGA Image ")
					self.printFail("Provide PCF file in project Tab")
					self.progressBarGenerateFPGA.setValue(0)
					generateStateMachine = "exit_generator"
				else:
					if self.pcfFile != self.projectLocation+"/"+self.getFileName(self.pcfFile):
						shutil.copyfile(self.pcfFile,self.projectLocation+"/"+self.getFileName(self.pcfFile))

					self.pcfFile = self.projectLocation+"/"+self.getFileName(self.pcfFile)

					self.buildTreeView()
					generateStateMachine="run_pnr"


			elif (generateStateMachine=="run_pnr"):
				self.FPGAPart = self.comboBoxFpgaPart.currentText()
				self.printSuccess("Selected FPGA Part => "+self.FPGAPart)	
				opts = arachne_opts[str(self.FPGAPart)]
				
				arachneStat=self.runCmdStdErr(['arachne-pnr '
												+opts+
												' -p '+self.pcfFile+
												' -o '+self.projectLocation+'/'+self.projectName+'.txt '
												+self.projectLocation+'/'+self.projectName+'.blif'])
					
				if arachneStat==0:

					self.arachneFile = self.projectLocation+'/'+self.projectName+'.txt'

					self.printSuccess("Place & Route Successful")
					self.progressBarGenerateFPGA.setValue(66)
					generateStateMachine = "generate_image"
				else:
					self.printSuccess("Place & Route Failed")
					self.progressBarGenerateFPGA.setValue(0)
					generateStateMachine = "exit_generator"
			
			elif (generateStateMachine=="generate_image"):
				
				icepackStat=self.runCmdStdErr(['icepack -v '+self.projectLocation+'/'+self.projectName+'.txt '+self.projectLocation+'/'+self.projectName+'.bin'])
						
				if (icepackStat==0):

					self.icepackFile = self.projectLocation+'/'+self.projectName+'.bin'

					self.printSuccess("FPGA Image Generation Successful")
					generateStateMachine = "generate_timing_info"
				else:
					self.printSuccess("FPGA Image Generation unsuccessful")
					generateStateMachine = "exit_generator"

			elif (generateStateMachine=="generate_timing_info"):
				
				opts = icetime_opts[str(self.FPGAPart)]
				self.runCmdStdOut(['icetime -tm '+opts+' '+self.projectLocation+'/'+self.projectName+'.txt --'])
				self.runCmdStdOut(['icetime -tm '+opts+' '+self.projectLocation+'/'+self.projectName+'.txt >> '+self.projectLocation+'/'+self.projectName+'_timing.txt'])

				self.icetimeFile = self.projectLocation+'/'+self.projectName+'_timing.txt'
				generateStateMachine = "generate_project_file"

			elif (generateStateMachine=="generate_project_file"):
				
				self.progressBarGenerateFPGA.setValue(100)
							
				############################################
				#create project file
				project = {
							'project'   : str(self.projectName), 
							'fpga'      : str(self.FPGAPart),
							'pcf'       : str(self.getFileName(self.pcfFile)),
							'top_module': str(self.topName),
							'rtl'       : self.verilogFileNameArray()
						  }
				with open(self.projectLocation+"/"+self.projectName+'.json', 'w') as outfile:  
					json.dump(project, outfile)
				self.printSuccess("Project file generation done")
				
				generateStateMachine = "exit_generator"
			
			elif (generateStateMachine=="exit_generator"):

				self.buildTreeView()			
				generationFinished=True
	
	def viewSingleFile(self,title,index,fileName):
		
		parent = QtGui.QTreeWidgetItem([title])

		if fileName is not(""):			
			parent.addChild(QtGui.QTreeWidgetItem([fileName]))
		
		self.treeWidgetIceBox.insertTopLevelItem(index,parent)
	
	def buildTreeView(self):
		#build for pcf files

		items = self.treeWidgetIceBox.topLevelItemCount()
		#remove all items at qtreewidget
		for i in range(0,items):
			self.treeWidgetIceBox.takeTopLevelItem(0)

		###pcf view
		self.viewSingleFile("PCF",self.pcfTreeWidgetIndex,self.pcfFile)
		
		#verilog
		self.verilogParent = QtGui.QTreeWidgetItem(['VERILOG RTL'])
		
		if self.verilogFiles:
			for v in self.verilogFiles:			
				self.verilogParent.addChild(QtGui.QTreeWidgetItem([v]))
		
		self.treeWidgetIceBox.insertTopLevelItem(1,self.verilogParent)

		self.viewSingleFile("YOSYS",self.yosysTreeWidgetIndex,self.yosysFile)
		
		self.viewSingleFile("ARACHNE-PNR",self.arachneTreeWidgetIndex,self.arachneFile)

		self.viewSingleFile("ICEPACK",self.icepackTreeWidgetIndex,self.icepackFile)

		self.viewSingleFile("ICETIME",self.icetimeTreeWidgetIndex,self.icetimeFile)
		
		self.treeWidgetIceBox.expandAll()

		self.treeWidgetIceBox.setAutoScroll(True)
		
	
	def addPcf(self):		
		if self.pcfFile is (""):
			self.pcfFile = str(QtGui.QFileDialog.getOpenFileName(self, 'Add .pcf File',filter="*.pcf"))
			if self.pcfFile is "":
				self.printFail(".pcf file was not added")
			else:
				self.printSuccess("added "+self.pcfFile+" project")
			self.buildTreeView()			
		else:
			self.printFail("Remove "+self.pcfFile+" before adding")
	
	def removePcf(self):
		if self.pcfFile is not(""):
			self.printSuccess("removed "+self.pcfFile+" from project")
			self.pcfFile = ""
			self.buildTreeView()
		else:
			self.printFail("Add .pcf file before removing")
	
	
	def addVerilog(self):		
		self.treeWidgetIceBox.takeTopLevelItem(1)
		vfiles=QtGui.QFileDialog.getOpenFileNames(self, 'add .verilog file(s)',filter="*.v")
			
		for vfile in vfiles:
			if vfile in self.verilogFiles:
				self.printFail("not adding "+vfile+" since it's already in the project")
			else:
				self.verilogFiles.append(str(vfile))
				self.printSuccess("adding "+vfile+" to the project")
			
		self.buildTreeView()


	def removeVerilog(self):
		if not self.verilogFiles:
			self.printFail("No verilog files to be removed...")
		else:
		
			verilogFilesToBeRemoved=QtGui.QFileDialog.getOpenFileNames(self, 'remove .verilog file(s)',filter="*.v")
			
			verilogFilesToBeRemovedJustFileName = []

			for verilogFile in verilogFilesToBeRemoved:
				verilogFilesToBeRemovedJustFileName.append(self.getFileName(str(verilogFile)))
			
			removeSuccess = False
			for verilogFileToRemove in verilogFilesToBeRemovedJustFileName:
				removeSuccess = False
				for verilogFileInProject in self.verilogFiles:
					if verilogFileToRemove in verilogFileInProject:
					
						self.verilogFiles.remove(verilogFileInProject) 
						self.printSuccess("Removed "+verilogFileToRemove+" from project")
						removeSuccess = True

				if not(removeSuccess):
					self.printFail("cannot remove "+verilogFileToRemove+" from project, since it was not added first!")
				
							
			self.buildTreeView()
			
			
	def selectFPGA(self):
		self.FPGAPart = self.comboBoxFpgaPart.currentText()
		self.printSuccess("Selected FPGA Part => "+self.FPGAPart)
	
	
	def runCmdStdErr(self,command):
		
		process = subprocess.Popen(command,shell=True,stderr=subprocess.PIPE)
		while True:
			output = process.stderr.readline()
			if output == '' and process.poll() is not None:
				break
			if output:
				self.statusEdit.append(output.strip())
		rc = process.poll()
		return rc

	def runCmdStdOut(self,command):
		
		process = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
		while True:
			output = process.stdout.readline()
			if output == '' and process.poll() is not None:
				break
			if output:
				self.statusEdit.append(output.strip())
		rc = process.poll()
		return rc	
	

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	window = MyApp()
	window.show()
	sys.exit(app.exec_())
