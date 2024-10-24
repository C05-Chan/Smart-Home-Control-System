class SmartDevice:
    def __init__(self):
        self.switchedOn = False

    def toggleSwitch(self):
        if not self.switchedOn: 
            self.switchedOn = True
        else:
            self.switchedOn = False
    
    def getSwitchedOn(self):
        return self.switchedOn
    
class SmartPlug(SmartDevice):
    def __init__(self, consumptionRate):
        super().__init__()
        self.consumptionRate = consumptionRate
        
    def setConsumptionRate(self, rate):
        if rate >= 0 and rate <= 150:
            self.consumptionRate = rate

    def getConsumptionRate(self):
        return self.consumptionRate
    
    def __str__(self):
        if self.switchedOn:
            switchStatus = "On"
        else:
            switchStatus = "Off"

        output = f"Your Plug is currently {switchStatus} " #change the switch so that rather than it say false it will say off
        output += f"and your consumption rate is: {self.consumptionRate}"
        return output
    

def testSmartPlug():
    plug = SmartPlug(45)
    plug.toggleSwitch()
    plug.getSwitchedOn
    print(plug.switchedOn)
    print(plug.consumptionRate)
    print(plug)

    plug.setConsumptionRate(150)
    print(plug.consumptionRate)
    plug.setConsumptionRate(0)
    print(plug.consumptionRate)
    plug.setConsumptionRate(151)
    print(plug.consumptionRate)

    print(plug)


###########################################################
class SmartOven(SmartDevice):
    def __init__(self):
        super().__init__()
        self.temperature = 0

    def setTemperature(self, temperature):
        if temperature >= 0 and temperature <= 260:
            self.temperature = temperature


    def getTemperature(self):
        return self.temperature


    def __str__(self):
        if self.switchedOn:
            ovenStatus = "On"
        else:
            ovenStatus = "Off"

        output = f"Your Oven is currently {ovenStatus} " #change the switch so that rather than it say false it will say off
        output += f"and your temperature is: {self.temperature}"
        return output
    
def testSmartOven():
    oven = SmartOven()
    oven.toggleSwitch()
    oven.getSwitchedOn
    print("Oven Status:", oven.switchedOn)
    print("Oven Temp:", oven.temperature)

    oven.setTemperature(260)
    print("Oven Temp:", oven.temperature)
    oven.setTemperature(0)
    print("Oven Temp:", oven.temperature)
    oven.setTemperature(261)
    print("Oven Temp:", oven.temperature)

    print(oven)

###########################################################

class SmartHome:
    def __init__(self):
        self.devices = []

    def getDevices(self):
        return self.devices
    
    def getDeviceAt(self, index):
        if index < len(self.devices)-1:
            output = self.devices[index]
        return output
    
    def removeDevice(self,index):
        if index <= len(self.devices)-1:
            device = self.devices[index]
            self.devices.remove(device)


    def addDevice(self,device):
        #if device not in self.devices:
        self.devices.append(device)
        
    def toggleSwitch(self, index):
        if index <= len(self.devices)-1:
            device = self.devices[index]
            device.toggleSwitch()

    def turnOnAll(self):
        for device in self.devices:
            if device.switchedOn == False:
                device.toggleSwitch()

    def turnOffAll(self):
        for device in self.devices:
            if device.switchedOn == True:
                device.toggleSwitch()

    def __str__(self):
        output = "Your Smart Home contains:\n"
        for device in self.devices:
            output += str(device) + "\n"
        return output

def testSmartHome():
    home = SmartHome()

    plug1 = SmartPlug(45)
    plug1.toggleSwitch()
    plug1.setConsumptionRate(150)

    plug2 = SmartPlug(45)
    plug2.setConsumptionRate(25)

    oven = SmartOven()
    oven.setTemperature(10)

    home.addDevice(plug1)
    home.addDevice(plug2)
    home.addDevice(oven)

    home.toggleSwitch(2)
    print(home)

    home.turnOnAll()
    print(home)

    home.removeDevice(1)
    print(home)



################################################################
def main():
    #testSmartPlug()
    #testSmartOven()
    testSmartHome()


#main()