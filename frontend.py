from tkinter import *
from backend import *

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

        self.editNum = IntVar()             #New value for the device consumption rate or temperature
        self.consumptionRate = IntVar()             #New device's consumption rate
        self.deviceChoice = StringVar()             #Device that is going to be added
        self.addWidgets = []                #list of widgets on the "Add" Option
       
        self.stringList = []                #List of strings for the main menu
        for _ in range(len(self.smartHome.getDevices())):
            self.stringList.append(StringVar())


    def setText(self, device, string): 
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
            string.set(f"Plug: {status}, Consumption Rate: {device.consumptionRate}")
                
        elif isinstance(device, SmartOven):
            string.set(f"Oven: {status}, Temperature: {device.temperature}")
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
            self.setText(device, string)


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
            self.setText(device, string)


    def toggleDevice(self, device, string):
        ########################################
        #                                      #
        #  This turns specific devices on/off  #
        #                                      #
        ########################################

        device.toggleSwitch()
        self.setText(device, string)


    def editWindow(self, device, string):
        #################################################################
        #                                                               #
        #   This creates the window and widgets for the edit function   #
        #                                                               #
        #################################################################

        editWin = Toplevel(self.win)
        editWin.title("Edit Device")
        # print(device)

        if isinstance(device, SmartPlug):
            lblText = "Consumption Rate (0 - 150): "
        elif isinstance(device, SmartOven):
            lblText = "Temperature (0 - 260): "

        lblEdit = Label(editWin, text = lblText)
        lblEdit.grid(row=0, column = 0, sticky = W, pady=2) 

        entryEdit = Entry(editWin, width=20, textvariable = self.editNum)
        entryEdit.grid(row=0, column = 1, sticky = W, pady = 2)

        btnConfirm = Button(editWin, text= "Confirm", command = lambda: self.editStats(device, string, editWin))
        btnConfirm.grid(row = 1, column = 0, sticky= W, pady = 2)

        
    def editStats(self,device,string, editWin):
        ###################################################################
        #                                                                 #
        #   This changes the consumption rate or temperature for device   #
        #                                                                 #
        ###################################################################

        try:
            int(self.editNum.get())
        except TclError:
            self.errorWindow("Please make sure the input is a NUMBER")
            return None

        if isinstance(device, SmartPlug):
            if int(self.editNum.get()) > 150 or int(self.editNum.get()) < 0:
                self.errorWindow("Consumption rate must be a NUMBER between 0 - 150 ")
                return None
            device.setConsumptionRate(self.editNum.get())

        elif isinstance(device, SmartOven):
            if int(self.editNum.get()) > 260 or int(self.editNum.get()) < 0:
                self.errorWindow("Temperature must be a NUMBER between 0 - 260")
                return None
            device.setTemperature(self.editNum.get())
        
        editWin.destroy()
        self.setText(device, string)


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
        addDeviceChoice = OptionMenu(
            addWin,self.deviceChoice, 
            "Smart Plug", 
            "Smart Oven", 
            command=lambda device=self.deviceChoice: self.deviceSelection(addWin, device)
        )
        addDeviceChoice.grid(row=0, column=0, padx=10, pady=10)

    def deviceSelection(self, addWin, device):
        selectedOption = self.deviceChoice.get()
        self.consumptionRate.set(0)
        if selectedOption == "Smart Plug":
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

        entryAddDevice = Entry(addWin, width=20, textvariable = self.consumptionRate)
        entryAddDevice.grid(row=1, column = 1, sticky = W, pady = 2)
        self.addWidgets.append(entryAddDevice)

        btnAdd = Button(addWin, text="Add", command=lambda: self.addDevice(addWin))
        btnAdd.grid(row=2, column=0, pady=5)

        self.createWidgets()
        self.addWidgets.append(btnAdd)


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

        try:
            int(self.consumptionRate.get())
        except TclError:
            self.errorWindow("Please make sure input is a NUMBER")
            return None
        else:
            if int(self.consumptionRate.get()) > 150 or int(self.consumptionRate.get()) < 0:
                self.errorWindow("Consumption rate must be 0 - 150")
                return None

        if selectedOption.lower() == "smart plug":
            plug = SmartPlug(self.consumptionRate.get())
            self.smartHome.addDevice(plug)
        else:
            oven = SmartOven()
            self.smartHome.addDevice(oven)
   
        
        self.stringList.append(StringVar())
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
            
            self.setText(device, string)
            lblDevice = Label(self.mainFrame, textvariable = string)
            lblDevice.grid(row=row, column = 0, sticky = W, padx = padding, pady = padding) 

            btnToggle = Button(self.mainFrame, text= "Toggle", command = lambda index=i, device=device: self.toggleDevice(device, self.stringList[index]))
            btnToggle.grid(row = row, column = 2, sticky= W, padx = padding, pady = padding)

            btnEdit = Button(self.mainFrame, text="Edit", command=lambda index=i, device=device: self.editWindow(device, self.stringList[index]))
            btnEdit.grid(row = row, column = 3, sticky= W, padx = padding, pady = padding)

            btnDelete = Button(self.mainFrame, text= "Delete", command = lambda index=i: self.deleteDevice(index))
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

  