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
			
		self.pluginPrefs["recordRequested"] = 0
			
		someVal = self.pluginPrefs["recordRequested"]
		indigo.server.log("Setting value of Now Showing Room to " + str(someVal))

	def shutdown(self):
		self.debugLog(u"shutdown called")
		
	def deviceStartComm(self, dev):			
		dev.stateListOrDisplayStateIdChanged()   

	########################################
	# Plugin Actions object callbacks 
	######################
	
	# ON OFF STATE OF DEVICE ON UI		
	def setRoomState(self, pluginAction, dev):
	#	self.debugLog(u"setHomestate Action called:\n" + str(pluginAction))
		dev.updateStateOnServer(key="roomState", value=str(pluginAction.props.get(u"roomStateField")))
		RoomStateValue = str(pluginAction.props.get(u"roomStateField"))
		if RoomStateValue == "On":
			dev.updateStateImageOnServer(indigo.kStateImageSel.SensorOn)	
		elif RoomStateValue == "Off":
			dev.updateStateImageOnServer(indigo.kStateImageSel.SensorOff)			
		else:
			dev.updateStateImageOnServer(indigo.kStateImageSel.SensorTripped)
		self.debugLog("Set Room State: " + str(pluginAction.props.get(u"roomStateField")) + " Entered.  State roomState set to: " + RoomStateValue)
		
	
			
	
	# EMAIL ADDRESS FIELDS (From MyPeople Plugin)
	def setEmail1Address(self, pluginAction, dev):
		substitutedTitle = self.substitute(pluginAction.props.get("email1AddressField", ""))
		dev.updateStateOnServer(key="email1Address", value=substitutedTitle)
		self.debugLog("Set Email 1 Address: " + str(pluginAction.props.get(u"email1AddressField")) + " Entered.  State email1Address set to: " + substitutedTitle)
		
	
	
	# UPDATE ALL STATES IN ONE ACTION (Not working yet... set up for My People Plugin still)
	def setAllStatesForPerson(self, pluginAction, dev):
	
		substitutedTitle1 = self.substitute(pluginAction.props.get("homeStateAllField", ""))
		if substitutedTitle1 == "Home":
			dev.updateStateImageOnServer(indigo.kStateImageSel.SensorOn)
			dev.updateStateOnServer(key="homeState", value="Home")
			newState ="Home"
			newSensor ="On"	
		elif substitutedTitle1 == "Away":
			dev.updateStateImageOnServer(indigo.kStateImageSel.SensorOff)
			dev.updateStateOnServer(key="homeState", value="Away")
			newState ="Away"
			newSensor ="Off"	
		elif substitutedTitle1 == "":
			dev.updateStateImageOnServer(indigo.kStateImageSel.SensorTripped)
			dev.updateStateOnServer(key="homeState", value="Unsure")
			newState ="Unsure"
			newSensor ="Tripped"		
		else:
			dev.updateStateImageOnServer(indigo.kStateImageSel.SensorTripped)
			dev.updateStateOnServer(key="homeState", value="Unsure")
			newState ="Unsure"	
			newSensor ="Tripped"		
		self.debugLog("01: " + str(pluginAction.props.get(u"homeStateAllField")) + " Entered.  State homeState set to: " + newState + ", Sensor: " + newSensor)
		

		substitutedTitle2 = self.substitute(pluginAction.props.get("userLocationAllField", ""))
		dev.updateStateOnServer(key="userLocation", value=substitutedTitle2)
		self.debugLog("02: " + str(pluginAction.props.get(u"userLocationAllField")) + " Entered.  State userLocation set to: " + substitutedTitle2)
		
		substitutedTitle3 = self.substitute(pluginAction.props.get("firstNameAllField", ""))
		dev.updateStateOnServer(key="firstName", value=substitutedTitle3)
		self.debugLog("03: " + str(pluginAction.props.get(u"firstNameAllField")) + " Entered.  " + "State firstName set to: " + substitutedTitle3)
		
		substitutedTitle4 = self.substitute(pluginAction.props.get("lastNameAllField", ""))
		self.debugLog("04: " + str(pluginAction.props.get(u"lastNameAllField")) + " Entered.  " + "State lastName set to: " + substitutedTitle4)
		dev.updateStateOnServer(key="lastName", value=substitutedTitle4)
			
		substitutedTitle5 = self.substitute(pluginAction.props.get("friendlyNameAllField", ""))
		self.debugLog("05: " + str(pluginAction.props.get(u"friendlyNameAllField")) + " Entered.  " + "State friendlyName set to: " + substitutedTitle5)
		dev.updateStateOnServer(key="friendlyName", value=substitutedTitle5)
		
		substitutedTitle6 = self.substitute(pluginAction.props.get("userIDNumberAllField", ""))
		self.debugLog("06: " + str(pluginAction.props.get(u"userIDNumberAllField")) + " Entered.  " + "State userIDNumber set to: " + substitutedTitle6)
		dev.updateStateOnServer(key="userIDNumber", value=substitutedTitle6)
		
		substitutedTitle7 = self.substitute(pluginAction.props.get("userPinNumberAllField", ""))
		self.debugLog("07: " + str(pluginAction.props.get(u"userPinNumberAllField")) + " Entered.  " + "State userPinNumber set to: " + substitutedTitle7)
		dev.updateStateOnServer(key="userPinNumber", value=substitutedTitle7)
		
		substitutedTitle8 = self.substitute(pluginAction.props.get("userPasswordAllField", ""))
		self.debugLog("08: " + str(pluginAction.props.get(u"userPasswordAllField")) + " Entered.  " + "State userPassword set to: " + substitutedTitle8)
		dev.updateStateOnServer(key="userPassword", value=substitutedTitle8)
		
		substitutedTitle9 = self.substitute(pluginAction.props.get("phone1NumberAllField", ""))
		self.debugLog("09: " + str(pluginAction.props.get(u"phone1NumberAllField")) + " Entered.  " + "State phone1Number set to: " + substitutedTitle9)
		dev.updateStateOnServer(key="phone1Number", value=substitutedTitle9)
	
		substitutedTitle10 = self.substitute(pluginAction.props.get("phone1SMSAllField", ""))
		self.debugLog("10: " + str(pluginAction.props.get(u"phone1SMSAllField")) + " Entered.  " + "State phone1SMS set to: " + substitutedTitle10)
		dev.updateStateOnServer(key="phone1SMS", value=substitutedTitle10)
	
		substitutedTitle11 = self.substitute(pluginAction.props.get("phone1MMSAllField", ""))
		self.debugLog("11: " + str(pluginAction.props.get(u"phone1MMSAllField")) + " Entered.  " + "State phone1MMS set to: " + substitutedTitle11)
		dev.updateStateOnServer(key="phone1MMS", value=substitutedTitle11)
		
		substitutedTitle12 = self.substitute(pluginAction.props.get("phone1IPAddressAllField", ""))
		self.debugLog("12: " + str(pluginAction.props.get(u"phone1IPAddressAllField")) + " Entered.  " + "State phone1IPAddress set to: " + substitutedTitle12)
		dev.updateStateOnServer(key="phone1IPAddress", value=substitutedTitle12)
	
		substitutedTitle13 = self.substitute(pluginAction.props.get("phone2NumberAllField", ""))
		self.debugLog("13: " + str(pluginAction.props.get(u"phone2NumberAllField")) + " Entered.  " + "State phone2Number set to: " + substitutedTitle13)
		dev.updateStateOnServer(key="phone2Number", value=substitutedTitle13)
	
		substitutedTitle14 = self.substitute(pluginAction.props.get("phone2SMSAllField", ""))
		self.debugLog("14: " + str(pluginAction.props.get(u"phone1SMSAllField")) + " Entered.  " + "State phone2SMS set to: " + substitutedTitle14)
		dev.updateStateOnServer(key="phone2SMS", value=substitutedTitle14)
	
		substitutedTitle15 = self.substitute(pluginAction.props.get("phone2MMSAllField", ""))
		self.debugLog("15: " + str(pluginAction.props.get(u"phone2MMSAllField")) + " Entered.  " + "State phone2MMS set to: " + substitutedTitle15)
		dev.updateStateOnServer(key="phone2MMS", value=substitutedTitle15)
		
		substitutedTitle16 = self.substitute(pluginAction.props.get("phone2IPAddressAllField", ""))
		self.debugLog("16: " + str(pluginAction.props.get(u"phone2IPAddressAllField")) + " Entered.  " + "State phone2IPAddress set to: " + substitutedTitle16)
		dev.updateStateOnServer(key="phone2IPAddress", value=substitutedTitle16)
		
		substitutedTitle17 = self.substitute(pluginAction.props.get("email1AddressAllField", ""))
		self.debugLog("17: " + str(pluginAction.props.get(u"email1AddressAllField")) + " Entered.  " + "State email1Address set to: " + substitutedTitle17)
		dev.updateStateOnServer(key="email1Address", value=substitutedTitle17)
	
		substitutedTitle18 = self.substitute(pluginAction.props.get("email2AddressAllField", ""))
		self.debugLog("18: " + str(pluginAction.props.get(u"email2AddressAllField")) + " Entered.  " + "State email2Address set to: " + substitutedTitle18)
		dev.updateStateOnServer(key="email2Address", value=substitutedTitle18)
		
		substitutedTitle19 = self.substitute(pluginAction.props.get("lastHomeAllField", ""))
		self.debugLog("19: " + str(pluginAction.props.get(u"lastHomeAllField")) + " Entered.  " + "State lastHome set to: " + substitutedTitle19)
		dev.updateStateOnServer(key="lastHome", value=substitutedTitle19)

		substitutedTitle20 = self.substitute(pluginAction.props.get("lastAwayAllField", ""))
		self.debugLog("20: " + str(pluginAction.props.get(u"lastAwayAllField")) + " Entered.  " + "State lastAway set to: " + substitutedTitle20)
		dev.updateStateOnServer(key="lastAway", value=substitutedTitle20)

		substitutedTitle21 = self.substitute(pluginAction.props.get("alertsOnAllField", ""))
		self.debugLog("21: " + str(pluginAction.props.get(u"alertsOnAllField")) + " Entered.  " + "State alertsOn set to: " + substitutedTitle21)
		dev.updateStateOnServer(key="alertsOn", value=substitutedTitle21)
		

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
	def nowShowingSpecific(self, pluginAction, dev):
		nowShowingRequest = self.substitute(pluginAction.props.get("nowShowingSpecificField", ""))
		roomCount = indigo.devices.len(filter="com.whmoorejr.my-rooms")-1
		nowShowingRequest = int(nowShowingRequest)
		recordRequested = 0
		
		### Verify Request is Within Range
		if nowShowingRequest > roomCount:
			self.debugLog("That Didn't Work: Can't get record# " + str(nowShowingRequest) + " out of " + str(roomCount) + " records")
			self.debugLog("Setting NowShowingRoom Back to First Record, Record #0")
			recordRequested = 0
			self.pluginPrefs["recordRequested"] = 0
		else:
			recordRequested = nowShowingRequest
			self.pluginPrefs["recordRequested"] = recordRequested
		
		recordCount = 0
		for dev in indigo.devices.iter(filter="com.whmoorejr.my-rooms"):
			if recordCount == recordRequested:
				roomName = dev.states["roomName"]
				roomState = dev.states["roomState"]
############ Fill in the rest of the states ############  (Copy from line 310 through...)
				
				break
			recordCount += 1
		
		indigo.server.log ("Now Showing Room #: " + str(recordRequested) + ") " + roomName)
		self.aRoomDev = indigo.devices["Now Showing Room"]
		self.aRoomDev.updateStateOnServer(key="roomName", value=roomName)
		self.aRoomDev.updateStateOnServer(key="roomState", value=roomState)				
############ Fill in the rest of the states ############  (Copy from line 310 through...)	


#### Combo State Experiment
	
	
	def setAnyState(self, pluginAction, dev):
	
		requestedDev = str(pluginAction.props.get(u"setADeviceField"))
		requestedState = str(pluginAction.props.get(u"setAnyStateField"))
		newValue = str(pluginAction.props.get(u"setStateValueField"))
		subNewValue = self.substitute(pluginAction.props.get("newStateValueField", ""))
		thisRoomDev = indigo.devices[int(requestedDev)]
		thisDevName = thisRoomDev.name
		thisRoomDev.updateStateOnServer(key=requestedState, value=subNewValue)
		newProps = thisRoomDev.pluginProps  #Use pluginProps to save the value before substitution
		metaDataItem = "meta_"+requestedState
		newProps[metaDataItem] = newValue
		thisRoomDev.replacePluginPropsOnServer(newProps)
		self.debugLog(newValue + " Entered, " + thisDevName + " : " + requestedState + "has been changed to: " + subNewValue)
		self.debugLog(metaDataItem)
	
		
	def filterDevices(self, filter, valuesDict, typeId, targetId):
		xList =[]
		for dev in indigo.devices.iter(filter="com.whmoorejr.my-rooms"):
			xList.append(( unicode(dev.id),dev.name))
		#xList.append(("0","==== off, do not use ===="))
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
			xList.append((state,state+"   ; currentV: "+unicode(dev.states[state]) ))
		#xList.append(("0","==== off, do not use ===="))
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
		self.debugLog(newValue + " Entered, " + thisDevName + " : " +  requestedState + " has been changed to: " + subNewValue)
		self.debugLog("subNewValue: " + subNewValue)
		return valuesDict
		
