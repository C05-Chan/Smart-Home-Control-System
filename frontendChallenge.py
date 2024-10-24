from tkinter import *
from backendChallenge import *

def setUpHome():
    ######################################################
    #                                                    #
    #     This is inital set up for smart home system    #
    #       - User can enter 5 devices in the shell      #
    #                                                    #
    ######################################################

    home = SmartHome()
    amount = 0

    while amount != 5:
        device = input("What device would you like to add to your smart home? (Plug or Oven) ")
        if device.lower() == "plug":
            while True:
                consumptionRate = input("What is the consumption rate? ")
                try:
                    consumptionRate = int(consumptionRate)
                    if 0 <= consumptionRate <= 150:
                        break
                    else:
                        print("Consumption rate must be between 0 and 150")

                except ValueError:
                    print("Consumption rate must be a valid number")

            plug = SmartPlug(consumptionRate)
            home.addDevice(plug)
            amount += 1

        elif device.lower() == "oven":
            oven = SmartOven()
            home.addDevice(oven)
            amount += 1
        
        else:
            print("Device is not available")

    return home


class SmartHomeSystem():

    def __init__(self, smartHome): #Constructor
        self.win = Tk()
        self.win.title("Smart Home System")

        self.mainFrame = Frame(self.win)
        self.mainFrame.pack(padx=10, pady=10)

        self.smartHome = smartHome              #Smart home class

        self.consumptionRate = IntVar()             #New device's consumption rate
        self.deviceChoice = StringVar()             #Device that is going to be added

        self.addWidgets = []                #List of widgets on the "Add" Option
        self.editList = []           #List of new values for the device consumption rate or temperature
        self.stringList = []                #List of strings for the main menu
        self.imageList = []  

        self.bin = PhotoImage(file='bin.png')
        self.binImage= self.bin.subsample(5,5) #this changes the size of the image

        self.power = PhotoImage(file='powerButton.png')
        self.powerImage= self.power.subsample(6,6)

        self.plug = PhotoImage(file='Plug.png')
        self.plugImage= self.plug.subsample(4,4)
    
        self.oven = PhotoImage(file='oven.png')
        self.ovenImage= self.oven.subsample(4,4)

        for _ in range(len(self.smartHome.getDevices())):
            self.stringList.append(StringVar())
            self.imageList.append(StringVar())
            self.editList.append(IntVar())


    def setText(self, device, string, indexedImage): 
        ############################################################
        #                                                          #
        #   This is sets the string for the device on main menu    #
        #                                                          #
        ############################################################

        if device.switchedOn:
            status = "On"
        else:
            status = "Off"

        if isinstance(device, SmartPlug):
            image = self.plugImage
            string.set(f"Plug: {status}, Consumption Rate: {device.consumptionRate}")
            indexedImage.set(image)
            return image
                
        elif isinstance(device, SmartOven):
            image = self.ovenImage
            string.set(f"Oven: {status}, Temperature: {device.temperature}")
            indexedImage.set(image)
            return image
        else:
            string.set("")

    def turnAllOnPress(self):
        ####################################
        #                                  #
        #  This turns all the devices ON   #
        #                                  #
        ####################################

        self.smartHome.turnOnAll()
        for i, device in enumerate(self.smartHome.getDevices()):
            #print(device)
            string = self.stringList[i]
            image = self.imageList[i]
            self.setText(device, string, image)


    def turnAllOffPress(self):
        #####################################
        #                                   #
        #  This turns all the devices OFF   #
        #                                   #
        #####################################

        self.smartHome.turnOffAll()
        for i, device in enumerate(self.smartHome.getDevices()):
            #print(device)
            string = self.stringList[i]
            image = self.imageList[i]
            self.setText(device, string, image)


    def toggleDevice(self, device, string, image):
        ########################################
        #                                      #
        #  This turns specific devices on/off  #
        #                                      #
        ########################################

        device.toggleSwitch()
        self.setText(device, string,image)



        
    def editStats(self,device,string, image, value):
        ###################################################################
        #                                                                 #
        #   This changes the consumption rate or temperature for device   #
        #                                                                 #
        ###################################################################
        amount = int(value)

        if isinstance(device, SmartPlug):

            device.setConsumptionRate(amount)

        elif isinstance(device, SmartOven):

            device.setTemperature(amount)
        
        #editWin.destroy()
        self.setText(device, string, image)

    def refreshWidgets(self):
        ################################################################
        #                                                              #
        #   This refreshes the main menu with new or deleted devices   #
        #                                                              #
        ################################################################

        for widget in self.mainFrame.winfo_children():
            widget.destroy()

        self.createWidgets()

    def deleteDevice(self,index):
        #############################################
        #                                           #
        #   This removes a device from smart home   #
        #                                           #
        #############################################

        self.smartHome.removeDevice(index)
        # self.setText(None,index)
        del self.stringList[index]
        del self.imageList[index]
        del self.editList[index]
        self.refreshWidgets()

    def addWindow(self):
        ################################################################
        #                                                              #
        #   This creates the window and widgets for the add function   #
        #                                                              #
        ################################################################

        addWin = Toplevel(self.win)
        addWin.title("Add Device")
        

        self.addPlugWidgets(addWin)

        self.deviceChoice.set("Smart Plug")
        addDeviceChoice = OptionMenu(addWin, self.deviceChoice, "Smart Plug", "Smart Oven", command=lambda device=self.deviceChoice: self.deviceSelection(addWin, device))
        addDeviceChoice.grid(row=0, column=0, padx=10, pady=10)
        
    def deviceSelection(self, addWin, device):
        ################################################################
        #                                                              #
        #   This changes the window depending on the device seleceted  #
        #                                                              #
        ################################################################

        self.consumptionRate.set(0)
        if device == "Smart Plug":
            self.addPlugWidgets(addWin)
        else:
            self.addOvenWidgets(addWin)


    def addPlugWidgets(self, addWin):
        ###############################################################################
        #                                                                             #
        #   This creates the consumption entry box for smart plug for add function    #
        #                                                                             #
        ###############################################################################

        lblConsumptionRate = Label(addWin, text ="Add a Consumption Rate (0 - 150): ")
        lblConsumptionRate.grid(row=1, column = 0, sticky = W, pady = 2) 
        self.addWidgets.append(lblConsumptionRate)

        spindboxAddConsumption = Spinbox(addWin, textvariable=self.consumptionRate, from_=0, to=150, width=10, state="readonly")
        spindboxAddConsumption.grid(row=1, column = 1, sticky = W, pady = 2)
        self.addWidgets.append(spindboxAddConsumption)

        btnAdd = Button(addWin, text="Add", command=lambda: self.addDevice(addWin))
        btnAdd.grid(row=2, column=0, pady=5)
        self.addWidgets.append(btnAdd)

        self.createWidgets()



    def addOvenWidgets(self, addWin):
        #################################################################
        #                                                               #
        #   This removes the widgets for smart oven for add function    #
        #                                                               #
        #################################################################

        self.deleteAddWidgets()
        btnAdd = Button(addWin, text="Add", command=lambda: self.addDevice(addWin))
        btnAdd.grid(row=2, column=0, pady=5)

        self.addWidgets.append(btnAdd)


    def addDevice(self, addWin):
        #########################################################
        #                                                       #
        #   This adds the device to the system and main menu    #
        #                                                       #
        #########################################################

        selectedOption = self.deviceChoice.get()
        consumptionRate = int(self.consumptionRate.get())
    

        if selectedOption.lower() == "smart plug":
            plug = SmartPlug(consumptionRate)
            self.smartHome.addDevice(plug)
        else:
            oven = SmartOven()
            self.smartHome.addDevice(oven)
   
        
        self.stringList.append(StringVar())
        self.imageList.append(StringVar())
        self.editList.append(IntVar())
        addWin.destroy()
        self.refreshWidgets()

    def deleteAddWidgets(self):
        ###################################################
        #                                                 #
        #   This deletes the widgets on the add window    #
        #                                                 #
        ###################################################

        for widget in self.addWidgets:
            widget.destroy()

        self.addWidgets = []


    def errorWindow(self, string):
        ##################################################################
        #                                                                #
        #   This creates a error window to let the user know the issue   #
        #                                                                #
        ##################################################################
    
        errorWin = Toplevel(self.win)
        lblConsumptionRate = Label(errorWin, text = string)
        lblConsumptionRate.pack(padx =10, pady = 10) 

        btnOkError = Button(errorWin, text="Ok", command=errorWin.destroy)
        btnOkError.pack()

    def createWidgets(self):
        #########################################
        #                                       #
        #   This creates widgets on main menu   #
        #                                       #
        #########################################
        padding = 2

        btnTurnOn = Button(self.mainFrame, text= "Turn On All", command = self.turnAllOnPress)
        btnTurnOn.grid(row = 0, column = 0, sticky= W, padx = padding, pady = padding)

        btnTurnOff = Button(self.mainFrame, text= "Turn Off All", command = self.turnAllOffPress)
        btnTurnOff.grid(row = 0, column = 3, sticky = E, padx = padding, pady = padding, columnspan=2)

        row = 1
        for i, device in enumerate(self.smartHome.getDevices()):
            string = self.stringList[i]
            indexImage = self.imageList[i]
            
            currentImage = self.setText(device, string, indexImage)
            lblDevice = Label(self.mainFrame, textvariable = string, image=currentImage, compound=LEFT)
            lblDevice.grid(row=row, column = 0, sticky = W, padx = padding, pady = padding) 

            btnToggle = Button(self.mainFrame, text= "Toggle",image=self.powerImage, command = lambda index=i, device=device : self.toggleDevice(device, self.stringList[index], self.imageList[index]))
            btnToggle.grid(row = row, column = 2, sticky= W, padx = padding, pady = padding)


            if isinstance(device, SmartPlug):
                max = 150
                startValue = device.getConsumptionRate()
            elif isinstance(device, SmartOven):
                max = 260
                startValue = device.getTemperature()

            editScale = Scale(
                self.mainFrame, 
                variable=self.editList[i],
                command=lambda value, index = i, device=device: self.editStats(device, self.stringList[index], self.imageList[index], value), 
                orient=HORIZONTAL, 
                length=200, 
                from_=0, 
                to=max
            )

            editScale.set(startValue)
            editScale.grid(row=row, column=3, sticky=W, pady=padding)

            btnDelete = Button(self.mainFrame, text= "Delete", image=self.binImage, command = lambda index=i: self.deleteDevice(index))
            btnDelete.grid(row = row, column = 4, sticky= W, padx = padding, pady = padding)

            row += 1

        btnAdd = Button(self.mainFrame, text= "Add", command = self.addWindow)
        btnAdd.grid(row = row, column = 0, sticky = W, padx = padding, pady = padding)


    def run(self):
        self.createWidgets()
        self.win.mainloop()

def main():
    smartHome = setUpHome()
    app = SmartHomeSystem(smartHome)
    app.run()

main()

  