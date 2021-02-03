#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
# A special Thank you to all the actual plugin developers on the Indigodomo forum that 
# assisted me almost daily with every bit of code that I struggled with. (which was most of it.)


import indigo

import os
import sys
import time

################################################################################
class Plugin(indigo.PluginBase):
	########################################
	def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
		super(Plugin, self).__init__(pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
		self.debug = True

	########################################
	def startup(self):

        #### Create Now Showing Room Device for Control Pages ####
		if "Now Showing Room" in indigo.devices:
			self.aRoomDev = indigo.devices["Now Showing Room"]
		else:
			indigo.server.log(u"Creating Now Showing Room Device for Control Pages")
			self.aRoomDev = indigo.device.create(indigo.kProtocol.Plugin, "Now Showing Room", "A template for control pages, do not delete, do not change address field", deviceTypeId="aRoom")
			self.aRoomDev.updateStateImageOnServer(indigo.kStateImageSel.SensorOn)
			self.aRoomDev.updateStateOnServer(key="roomState", value="On")
			
			newProps = aRoomDev.pluginProps  #Use pluginProps to save the value before substitution
			newProps["meta_roomState"] = "On"
		    	self.aRoomDev.replacePluginPropsOnServer(newProps)
			
		self.pluginPrefs["recordRequested"] = 0
		self.pluginPrefs["pollFreq"] = 10	
		someVal = self.pluginPrefs["pollFreq"]
		indigo.server.log("Polling Frequecny Reset to " + str(someVal)+" Seconds.  Use Plugin Config to change")
		# indigo.devices.subscribeToChanges()   <-- need to add more stuff to work properly
		# indigo.variables.subscribeToChanges()

	def shutdown(self):
		self.debugLog(u"shutdown called")
		
	def deviceStartComm(self, dev):			
		dev.stateListOrDisplayStateIdChanged()  
		
	def myLogTest(self):
		self.debugLog("experiment to see if invoking a function will work")
		
	def runConcurrentThread(self):
		
		try:
			while True:
				pollFreq = self.pluginPrefs["pollFreq"]
				self.sleep(pollFreq)
				
				for dev in indigo.devices.iter(filter="com.whmoorejr.my-rooms"):
				###### Identifier States	
					subRoomName = self.substitute(dev.pluginProps.get("meta_roomName","unknown"))
					subRoomState = self.substitute(dev.pluginProps.get("meta_roomState","Other"))
					subFloorLevel = self.substitute(dev.pluginProps.get("meta_floorLevel","unknown"))
					subBuilding = self.substitute(dev.pluginProps.get("meta_building","unknown"))
				###### Occupancy States	
					subIsOccupied = self.substitute(dev.pluginProps.get("meta_isOccupied","unknown"))
					subLastOccupied = self.substitute(dev.pluginProps.get("meta_lastOccupied","unknown"))
					subLastVacant = self.substitute(dev.pluginProps.get("meta_lastVacant","unknown"))
					subOccupiedBy1 = self.substitute(dev.pluginProps.get("meta_occupiedBy1","unknown"))
					subOccupiedBy2 = self.substitute(dev.pluginProps.get("meta_occupiedBy2","unknown"))
				###### Lighting Device States
					subMainLight = self.substitute(dev.pluginProps.get("meta_mainLight","unknown"))
					subAccentLight = self.substitute(dev.pluginProps.get("meta_accentLight","unknown"))
					subLuminescence = self.substitute(dev.pluginProps.get("meta_luminescence","unknown"))
					subWindowShades = self.substitute(dev.pluginProps.get("meta_windowShades","unknown"))
				###### Climate Device States
					subTemperature = self.substitute(dev.pluginProps.get("meta_temperature","unknown"))
					subHumidity = self.substitute(dev.pluginProps.get("meta_humidity","unknown"))
					subCeilingFan = self.substitute(dev.pluginProps.get("meta_ceilingFan","unknown"))
					
					
					#indigo.server.log("Sleep Test") # <-- for testing
					updatedStates = [
						{'key' : u'roomName', 'value' : subRoomName},
						{'key' : u'roomState', 'value' : subRoomState},
						{'key' : u'floorLevel', 'value' : subFloorLevel},
						{'key' : u'building', 'value' : subBuilding},
						{'key' : u'isOccupied', 'value' : subIsOccupied},
						{'key' : u'lastOccupied', 'value' : subLastOccupied},
						{'key' : u'lastVacant', 'value' : subLastVacant},
						{'key' : u'occupiedBy1', 'value' : subOccupiedBy1},
						{'key' : u'occupiedBy2', 'value' : subOccupiedBy2},
						{'key' : u'mainLight', 'value' : subMainLight},
						{'key' : u'accentLight', 'value' : subAccentLight},
						{'key' : u'luminescence', 'value' : subLuminescence},
						{'key' : u'windowShades', 'value' : subWindowShades},
						{'key' : u'temperature', 'value' : subTemperature},
						{'key' : u'humidity', 'value' : subHumidity},
						{'key' : u'ceilingFan', 'value' : subCeilingFan}
						]
					dev.updateStatesOnServer(updatedStates)
					if subRoomState == "On":
						dev.updateStateImageOnServer(indigo.kStateImageSel.SensorOn)
					elif subRoomState == "Off":
						dev.updateStateImageOnServer(indigo.kStateImageSel.SensorOff)
					else: 
						dev.updateStateImageOnServer(indigo.kStateImageSel.SensorTripped)	
				
		except self.StopThread:
			indigo.server.log(u"stop requested from indigo")
			
		return
	####################################
	# Plugin Config 
	####################################	
	def setPollFrequency(self, filter="", valuesDict=None, typeId="", targetID=0):
		listOptions = [
			(5,"5 Seconds"),(10,"10 Seconds"),(20,"20 Seconds"),
			(30,"30 Seconds"),(40,"40 Seconds"),(50,"50 Seconds"),
			(60,"1 Minute"),(180,"3 Minutes"),(300,"5 Minutes"),(600,"10 Minutes")
			]
		return listOptions
		
	def validatePrefsConfigUi(self, valuesDict):
		pollFreq = self.pluginPrefs["pollFreq"]
		pollFreqInt = int(pollFreq)
		if pollFreqInt > 0:
			self.pluginPrefs["pollFreq"] = pollFreqInt
			return (True, valuesDict)
		else:
			self.pluginPrefs["pollFreq"] = 10
			return (False, valuesDict)
	

	####################################
	# Plugin Actions object callbacks 
	####################################
	
	
	
	# ON OFF STATE OF DEVICE ON UI		
	def setRoomState(self, pluginAction, dev):
	#	self.debugLog(u"setHomestate Action called:\n" + str(pluginAction))
		
		RoomStateValue = str(pluginAction.props.get(u"roomStateField"))
		dev.updateStateOnServer(key="roomState", value=RoomStateValue)
		newProps = dev.pluginProps  #Use pluginProps to save the value before substitution
		thisRoom = dev.name	
		    	
		if RoomStateValue == "On":
			dev.updateStateImageOnServer(indigo.kStateImageSel.SensorOn)
			newProps["meta_roomState"] = "On"
			dev.replacePluginPropsOnServer(newProps)	
				
		elif RoomStateValue == "Off":
			dev.updateStateImageOnServer(indigo.kStateImageSel.SensorOff)
			newProps["meta_roomState"] = "Off"
			dev.replacePluginPropsOnServer(newProps)	
							
		else:
			dev.updateStateImageOnServer(indigo.kStateImageSel.SensorTripped)
			newProps["meta_roomState"] = "Other"
			dev.replacePluginPropsOnServer(newProps)
				
		metaMessage = dev.pluginProps["meta_roomState"]
		self.debugLog(thisRoom+" roomState set to: -" + RoomStateValue+"- .  meta_roomState set to: -"+metaMessage+"-")
		myLogTest(self)
	
			

	#### Now Showing Room scripts need to include the rest of the My Rooms states
	#### Need to re-work Specific Record to be able to select the room from a list of room devices.
	### Showing Next for control page use
	def nowShowingNext(self, pluginAction, dev):
	#	self.dev = indigo.devices["Now Showing"]
		recordRequested = self.pluginPrefs["recordRequested"]
		recordRequested = recordRequested + 1
		roomCount = indigo.devices.len(filter="com.whmoorejr.my-rooms")-1
		
		### Verify Requested Record is Within Range
		if recordRequested > roomCount:
			recordRequested = 0
			self.pluginPrefs["recordRequested"] = 0
		elif recordRequested < 0:
			recordRequested = roomCount
			self.pluginPrefs["recordRequested"] = roomCount
		else:
			self.pluginPrefs["recordRequested"] = recordRequested
		
		recordCount = 0
		for dev in indigo.devices.iter(filter="com.whmoorejr.my-rooms"):
			if recordCount == recordRequested:
				roomName = dev.states["roomName"]
				roomState = dev.states["roomState"]
###
############ Fill in the rest of the states ############
###
				aux05State = dev.states["aux05State"]
				break
			recordCount += 1
		
		indigo.server.log ("Now Showing Next Room \n " + "Record Requested is #: " + str(recordRequested) + ") " + roomName)
		self.aRoomDev = indigo.devices["Now Showing Room"]
		self.aRoomDev.updateStateOnServer(key="roomName", value=roomName)
		self.aRoomDev.updateStateOnServer(key="roomState", value=roomState)
###		
############ Fill in the rest of the states ############		
###						
		self.aRoomDev.updateStateOnServer(key="aux05State", value=aux05State)		
			
	
	### Showing Previous for control page use
	def nowShowingPrevious(self, pluginAction, dev):
		recordRequested = self.pluginPrefs["recordRequested"]
		recordRequested = recordRequested - 1
		roomCount = indigo.devices.len(filter="com.whmoorejr.my-rooms")-1
		
		### Verify Requested Record is Within Range
		if recordRequested > roomCount:
			recordRequested = 0
			self.pluginPrefs["recordRequested"] = 0
		elif recordRequested < 0:
			recordRequested = roomCount
			self.pluginPrefs["recordRequested"] = roomCount
		else:
			self.pluginPrefs["recordRequested"] = recordRequested
			
		recordCount = 0
		for dev in indigo.devices.iter(filter="com.whmoorejr.my-rooms"):
			if recordCount == recordRequested:
############ Fill in the rest of the states ############  (Copy from line 310 through...)
				break
			recordCount += 1
		
		indigo.server.log ("Now Showing Previous Room \n " + "Record Requested is #: " + str(recordRequested) + ") " + roomName)
		self.aRoomDev = indigo.devices["Now Showing Room"]
	#	self.aPersonDev.updateStateOnServer(key="firstName", value=firstName)
	#	self.aPersonDev.updateStateOnServer(key="lastName", value=lastName)				
	#	self.aPersonDev.updateStateOnServer(key="friendlyName", value=friendlyName)		
		
		
	### Showing First for control page use	
	def nowShowingFirst(self, pluginAction, dev):
		self.pluginPrefs["recordRequested"] = 0
		recordRequested = 0
		
		recordCount = 0
		for dev in indigo.devices.iter(filter="com.whmoorejr.my-rooms"):
			if recordCount == recordRequested:
############ Fill in the rest of the states ############  (Copy from line 310 through...)
				break
			recordCount += 1
		
		indigo.server.log ("Now Showing First Room \n " + "Record Requested is #: " + str(recordRequested) + " : " + roomName)
		self.aRoomDev = indigo.devices["Now Showing Room"]
		self.aRoomDev.updateStateOnServer(key="roomName", value=roomName)
		self.aPersonDev.updateStateOnServer(key="roomState", value=roomState)				
############ Fill in the rest of the states ############  (Copy from line 310 through...)
	
	### Showing Last for control page use
	def nowShowingLast(self, pluginAction, dev):
		roomCount = indigo.devices.len(filter="com.whmoorejr.my-rooms")-1
		recordRequested = roomCount
		self.pluginPrefs["recordRequested"] = roomCount
			
		recordCount = 0
		for dev in indigo.devices.iter(filter="com.whmoorejr.my-rooms"):
			if recordCount == recordRequested:
############ Fill in the rest of the states ############  (Copy from line 310 through...)
			
				break
			recordCount += 1
		
		indigo.server.log ("Now Showing Previous Room \n " + "Record Requested is #: " + str(recordRequested) + ") " + roomName)
		self.aRoomDev = indigo.devices["Now Showing Room"]
		self.aRoomDev.updateStateOnServer(key="roomName", value=roomName)
		self.aRoomDev.updateStateOnServer(key="roomState", value=roomState)				
############ Fill in the rest of the states ############  (Copy from line 310 through...)

	
	### Showing Specific Record for control page use
	def nowShowingSpecific(self, pluginAction, dev, valuesDict):
		requestedDev = str(pluginAction.props.get(u"setRequestedDevice"))
		sourceDev = indigo.devices[int(requestedDev)]
		sourceDevName = sourceDev.name
		sourceDevID = sourceDev.id
		

		meta_roomName = sourceDev.pluginProps.get("meta_roomName","unknown")
		meta_roomState = sourceDev.pluginProps.get("meta_roomState","Other")
		meta_floorLevel = sourceDev.pluginProps.get("meta_floorLevel","unknown")
		meta_building = sourceDev.pluginProps.get("meta_building","unknown")
		meta_isOccupied = sourceDev.pluginProps.get("meta_isOccupied","unknown")
		meta_lastOccupied = sourceDev.pluginProps.get("meta_lastVacant","unknown")
		meta_lastVacant = sourceDev.pluginProps.get("meta_floorLevel","unknown")
		meta_occupedBy1 = sourceDev.pluginProps.get("meta_occupedBy1","unknown")
		meta_occupedBy2 = sourceDev.pluginProps.get("meta_occupedBy2","unknown")
		meta_mainLight = sourceDev.pluginProps.get("meta_mainLight","unknown")
		meta_accentLight = sourceDev.pluginProps.get("meta_accentLight","unknown")
		meta_luminescence = sourceDev.pluginProps.get("meta_luminescence","unknown")
		meta_windowShades = sourceDev.pluginProps.get("meta_windowShades","unknown")
		meta_temperature = sourceDev.pluginProps.get("meta_temperature","unknown")
		meta_humidity = sourceDev.pluginProps.get("meta_humidity","unknown")
		meta_ceilingFan = sourceDev.pluginProps.get("meta_ceilingFan","unknown")
		
		
	
		thisRoomDev = indigo.devices["Now Showing Room"]
		newProps = thisRoomDev.pluginProps	
		newProps["meta_roomName"] = meta_roomName
		newProps["meta_roomState"] = meta_roomState
		newProps["meta_floorLevel"] = meta_floorLevel
		newProps["meta_building"] = meta_building
		newProps["meta_isOccupied"] = meta_isOccupied
		newProps["meta_occupedBy1"] = meta_occupedBy1
		newProps["meta_occupedBy2"] = meta_occupedBy2
		newProps["meta_mainLight"] = meta_mainLight
		newProps["meta_accentLight"] = meta_accentLight
		newProps["meta_luminescence"] = meta_luminescence
		newProps["meta_windowShades"] = meta_windowShades
		newProps["meta_temperature"] = meta_temperature
		newProps["meta_humidity"] = meta_humidity
		newProps["meta_ceilingFan"] = meta_ceilingFan
		newProps["address"] = sourceDevName # shows which device the Now Showing Room is displaying in the Address field of the GUI
		thisRoomDev.replacePluginPropsOnServer(newProps)		
	
		recordCount = 0
		for dev in indigo.devices.iter(filter="com.whmoorejr.my-rooms"):
			if dev.name == sourceDevName:
				break
			recordCount += 1
		self.pluginPrefs["recordRequested"] = recordCount	
		thisRecord = str(recordCount)
		indigo.server.log(u"Record Requested is #: " + thisRecord + ") " + sourceDevName )
				
	def filterDevicesNS(self, filter, valuesDict, typeId, targetId):
		xList =[]
		for dev in indigo.devices.iter(filter="com.whmoorejr.my-rooms"):
			if dev.name != "Now Showing Room":  
				xList.append(( unicode(dev.id),dev.name))
		return xList		
		
############ Fill in the rest of the states ############  (Copy from line 310 through...)	


#### SET ANY STATE TEXT INPUT	
	
	def setAnyStateFT(self, pluginAction, dev):
	
		requestedDev = str(pluginAction.props.get(u"setADeviceField"))
		requestedState = str(pluginAction.props.get(u"setAnyStateField"))
		newValue = str(pluginAction.props.get(u"newStateValueField"))
		subNewValue = self.substitute(pluginAction.props.get("newStateValueField", ""))
		thisRoomDev = indigo.devices[int(requestedDev)]
		thisDevName = thisRoomDev.name
		thisRoomDev.updateStateOnServer(key=requestedState, value=subNewValue)
		newProps = thisRoomDev.pluginProps  #Use pluginProps to save the value before substitution
		metaDataItem = "meta_"+requestedState
		newProps[metaDataItem] = newValue
		thisRoomDev.replacePluginPropsOnServer(newProps)
		self.debugLog(newValue + " Entered, " + thisDevName + " : " + requestedState + "has been changed to: " + subNewValue)
		self.debugLog("Saved as metadate porperty" + metaDataItem + " with value "+ newValue)
	
	def filterDevices(self, filter, valuesDict, typeId, targetId):
		xList =[]
		for dev in indigo.devices.iter(filter="com.whmoorejr.my-rooms"):
			if dev.name != "Now Showing Room":
				xList.append(( unicode(dev.id),dev.name))
		return xList
		
	def buttonConfirmDevice(self, valuesDict, typeID, devId):
		return valuesDict

	def filterDevStates(self, filter, valuesDict, typeId, targetId):
		xList =[]
		if len(valuesDict) < 2:                         return [("0","")]
		if "setADeviceField" not in valuesDict:       return [("0","")]
		if valuesDict["setADeviceField"] in ["0",""]: return [("0","")]
		dev = indigo.devices[int(valuesDict["setADeviceField"])]
		for state in dev.states:
			if state !="roomState":
				if state!="roomState.On": 
					if state!="roomState.Off":
						if state!="roomState.Other":
							xList.append((state,state+"   ; currentV: "+unicode(dev.states[state]) ))
		return xList	
		
	def buttonConfirmNewValue(self, valuesDict, typeId, devId): 
		self.debugLog("I Pushed the Confirm Button")
		requestedDev = valuesDict["setADeviceField"]
		requestedState = valuesDict["setAnyStateField"]
		newValue = valuesDict["newStateValueField"]
		subNewValue = self.substitute(valuesDict["newStateValueField"])
		thisRoomDev = indigo.devices[int(requestedDev)]
		thisDevName = thisRoomDev.name
		thisRoomDev.updateStateOnServer(key=requestedState, value=subNewValue)
		self.debugLog(u"The Device -"+thisDevName+":"+requestedState+"- value set to: -" + subNewValue + "- From Entered Text: -" +newValue+"-")
		
		newProps = thisRoomDev.pluginProps
		metaDataItem = "meta_"+requestedState
		newProps[metaDataItem] = newValue
		thisRoomDev.replacePluginPropsOnServer(newProps)
		self.debugLog("metadata added to " + thisDevName + " key= " + metaDataItem + " with value: " + newValue)
		return valuesDict


#### SET ANY STATE FROM SOURCE STATE
	def setAnyStateFS(self, pluginAction, dev):
		requestedDev = str(pluginAction.props.get(u"setADeviceFieldFS"))
		requestedState = str(pluginAction.props.get(u"setAnyStateFieldFS"))  
		sourceDevID = str(pluginAction.props.get(u"setSourceDeviceField")) 
		sourceState = str(pluginAction.props.get(u"setSourceStateField")) 
		newValue = (u"%%d:"+sourceDevID+":"+sourceState+"%%")
		subNewValue = self.substitute(newValue)
		sourceDevice = indigo.devices[int(sourceDevID)]
		sourceDeviceName = sourceDevice.name
		thisRoomDev = indigo.devices[int(requestedDev)]
		thisDevName = thisRoomDev.name
		thisRoomDev.updateStateOnServer(key=requestedState, value=subNewValue)
		self.debugLog(u"The Device -"+thisDevName+":"+requestedState+"- value set to: -" + subNewValue + "- From Source: -" +sourceDeviceName+ ":"+sourceState+"-")
		
		newProps = thisRoomDev.pluginProps
		metaDataItem = "meta_"+requestedState
		newProps[metaDataItem] = newValue
		thisRoomDev.replacePluginPropsOnServer(newProps)
		self.debugLog("metadata added to " + thisDevName + ". key= " + metaDataItem + " with value: " + newValue)
		
	def filterDevicesFS(self, filter, valuesDict, typeId, targetId):
		xList =[]
		for dev in indigo.devices.iter(filter="com.whmoorejr.my-rooms"):
			if dev.name != "Now Showing Room":
				xList.append(( unicode(dev.id),dev.name))
		return xList
		
	def buttonConfirmDeviceFS(self, valuesDict, typeID, devId):
		return valuesDict

	def filterDevStatesFS(self, filter, valuesDict, typeId, targetId):
		xList =[]
		if len(valuesDict) < 2:                         return [("0","")]
		if "setADeviceFieldFS" not in valuesDict:       return [("0","")]
		if valuesDict["setADeviceFieldFS"] in ["0",""]: return [("0","")]
		dev = indigo.devices[int(valuesDict["setADeviceFieldFS"])]
		for state in dev.states:
			if state !="roomState":
				if state!="roomState.On": 
					if state!="roomState.Off":
						if state!="roomState.Other":
							xList.append((state,state+"   ; currentV: "+unicode(dev.states[state]) ))
		#xList.append(("0","==== off, do not use ===="))
		return xList	
	
	def filterAllDevices(self, filter, valuesDict, typeId, targetId):
		xList =[]
		for dev in indigo.devices:
			if dev.name !="Now Showing Room":
				xList.append(( unicode(dev.id),dev.name))
		return xList
	
	def buttonConfirmSourceFS(self, valuesDict, typeID, devID):
		return valuesDict
	
	def filterSourceDevStates(self, filter, valuesDict, typeId, targetId):
		xList =[]
		if len(valuesDict) < 2:                         return [("0","")]
		if "setSourceDeviceField" not in valuesDict:       return [("0","")]
		if valuesDict["setSourceDeviceField"] in ["0",""]: return [("0","")]
		dev = indigo.devices[int(valuesDict["setSourceDeviceField"])]
		for state in dev.states:
			xList.append((state,state+"   ; currentV: "+unicode(dev.states[state]) ))
		return xList
			
	def buttonConfirmNewValueFS(self, valuesDict, typeId, devId): 
		self.debugLog("I Pushed the Confirm Button")
		requestedDev = valuesDict["setADeviceFieldFS"]
		requestedState = valuesDict["setAnyStateFieldFS"]
		sourceDevID = valuesDict["setSourceDeviceField"]
		sourceState = valuesDict["setSourceStateField"]
		newValue = (u"%%d:"+sourceDevID+":"+sourceState+"%%")
		subNewValue = self.substitute(newValue)
		sourceDevice = indigo.devices[int(sourceDevID)]
		sourceDeviceName = sourceDevice.name
		thisRoomDev = indigo.devices[int(requestedDev)]
		thisDevName = thisRoomDev.name
		thisRoomDev.updateStateOnServer(key=requestedState, value=subNewValue)
		self.debugLog(u"The Device -"+thisDevName+":"+requestedState+"- value set to: -" + subNewValue + "- From Source: -" +sourceDeviceName+ ":"+sourceState+"-")
		
		newProps = thisRoomDev.pluginProps
		metaDataItem = "meta_"+requestedState
		newProps[metaDataItem] = newValue
		thisRoomDev.replacePluginPropsOnServer(newProps)
		self.debugLog("metadata added to " + thisDevName + ". key= " + metaDataItem + " with value: " + newValue)
		return valuesDict
		
#### SET ANY STATE FROM VARIABLE
	def setAnyStateFV(self, pluginAction, dev):
		requestedDev = str(pluginAction.props.get(u"setADeviceFieldFV"))
		requestedState = str(pluginAction.props.get(u"setAnyStateFieldFV"))  
		sourceVarID = str(pluginAction.props.get(u"setSourceVariableField")) 
		newValue = (u"%%v:"+sourceVarID+"%%")
		subNewValue = self.substitute(newValue)
		sourceVariable = indigo.variables[int(sourceVarID)]
		sourceVariableName = sourceVariable.name
		thisRoomDev = indigo.devices[int(requestedDev)]
		thisDevName = thisRoomDev.name
		thisRoomDev.updateStateOnServer(key=requestedState, value=subNewValue)
		self.debugLog(u"The Device -"+thisDevName+":"+requestedState+"- value set to: -" + subNewValue + "- From Variable: -" +sourceVariableName+ ":"+sourceVarID+"-")
		
		newProps = thisRoomDev.pluginProps
		metaDataItem = "meta_"+requestedState
		newProps[metaDataItem] = newValue
		thisRoomDev.replacePluginPropsOnServer(newProps)
		self.debugLog("metadata added to " + thisDevName + ". key= " + metaDataItem + " with value: " + newValue)
		
	def filterDevicesFV(self, filter, valuesDict, typeId, targetId):
		xList =[]
		for dev in indigo.devices.iter(filter="com.whmoorejr.my-rooms"):
			if dev.name != "Now Showing Room":
				xList.append(( unicode(dev.id),dev.name))
		return xList
		
	def buttonConfirmDeviceFV(self, valuesDict, typeID, devId):
		return valuesDict

	def filterDevStatesFV(self, filter, valuesDict, typeId, targetId):
		xList =[]
		if len(valuesDict) < 2:                         return [("0","")]
		if "setADeviceFieldFV" not in valuesDict:       return [("0","")]
		if valuesDict["setADeviceFieldFV"] in ["0",""]: return [("0","")]
		dev = indigo.devices[int(valuesDict["setADeviceFieldFV"])]
		for state in dev.states:
			if state !="roomState":
				if state!="roomState.On": 
					if state!="roomState.Off":
						if state!="roomState.Other":
							xList.append((state,state+"   ; currentV: "+unicode(dev.states[state]) ))
		return xList	
	
	def filterAllVariables(self, filter, valuesDict, typeId, targetId):
		vList =[]
		for var in indigo.variables:
			vList.append(( unicode(var.id),var.name))
		return vList 
			
	def buttonConfirmNewValueFV(self, valuesDict, typeId, devId): 
		self.debugLog("I Pushed the Confirm Button")
		requestedDev = valuesDict["setADeviceFieldFV"]
		requestedState = valuesDict["setAnyStateFieldFV"]
		sourceVarID = valuesDict["setSourceVariableField"]
		newValue = (u"%%v:"+sourceVarID+"%%")
		subNewValue = self.substitute(newValue)
		sourceVariable = indigo.variables[int(sourceVarID)]
		sourceVariableName = sourceVariable.name
		thisRoomDev = indigo.devices[int(requestedDev)]
		thisDevName = thisRoomDev.name
		thisRoomDev.updateStateOnServer(key=requestedState, value=subNewValue)
		self.debugLog(u"The Device -"+thisDevName+":"+requestedState+"- value set to: -" + subNewValue + "- From Variable: -" +sourceVariableName+ ":"+sourceVarID+"-")
		
		newProps = thisRoomDev.pluginProps
		metaDataItem = "meta_"+requestedState
		newProps[metaDataItem] = newValue
		thisRoomDev.replacePluginPropsOnServer(newProps)
		self.debugLog("metadata added to " + thisDevName + ". key= " + metaDataItem + " with value: " + newValue)
		return valuesDict
	