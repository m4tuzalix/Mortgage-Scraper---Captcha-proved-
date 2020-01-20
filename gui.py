from tkinter import *
from mortgage import Mortgage
from data import get_data
from datetime import datetime
from threading import Thread
from os import _exit
from psutil import process_iter

class Main(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.configure(bg='yellow')
        self.current_path = []
        
        def env_cleaner():
            to_kill = ["python", "chromedriver"]
            for process in process_iter():
                for to_be_killed in to_kill:
                    if to_be_killed in process.name():
                        process.kill()
                        break
            
            _exit(0)

        Tk.protocol(self,'WM_DELETE_WINDOW', lambda:env_cleaner()) #// stops evertyhing after gui has been closed
        

        ClickFrame = Frame(self, bd=1, width=330, height=50, padx=1, pady=1, bg='green', relief=RIDGE) #//// buttons space
        ClickFrame.pack(side=BOTTOM)

        Data = Frame(self, bd=1, width=300, height=400, padx=5, pady=5, relief=RIDGE, bg='green') #////// content space
        Data.pack(side=BOTTOM)
        
        DataLeft = LabelFrame(Data, bd=1, width=200, height=300, padx=5, pady=5, relief=RIDGE, bg='yellow', font=('arial', 20, 'bold'))
        DataLeft.pack(side=LEFT)

        

        self.path_mortgage = Label(DataLeft, text='Mortgage data file')
        self.path_mortgage.grid(row=1, column=0, sticky=W)
        self.entry_mortgage = Entry(DataLeft, width=30)
        self.entry_mortgage.grid(row=1, column=1)

        self.path_raport = Label(DataLeft, text='New raport')
        self.path_raport.grid(row=3, column=0, sticky=W)
        self.entry_raport = Entry(DataLeft, width=30)
        self.entry_raport.grid(row=3, column=1)


        self.labels = {self.path_raport, self.path_mortgage}
        for label in self.labels:
            label.configure(bg='red', font=('times new roman', 10, 'bold'))
        
        a = 2
        for row in range(3):
            self.space = Label(DataLeft, text="", bg='yellow')
            self.space.grid(row=a, column=1)
            a = a + 2

        
        self.send = Button(ClickFrame, text='Proceed', bg='red', width=30, command=self.assign_mechanism_to_new_thread)
        self.send.pack(anchor=CENTER)
    
    def assign_mechanism_to_new_thread(self):
        self.second_thread = Thread(target=self.mechanism)
        self.second_thread.daemon = True
        self.second_thread.start()
    
    def mechanism(self):
        self.send.config(state="disabled") #// disables button after click
        path_to_mortgage = str(self.entry_mortgage.get())
        path_to_raport = str(self.entry_raport.get())

        if '"' in path_to_mortgage: #// gets rid of quotes
            path_to_mortgage = path_to_mortgage[1:len(path_to_mortgage)-1]
            
        #/// containers for paths and names
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        raport_name = "RaportKW"
        data_path = f'{path_to_mortgage}'
        raport_path = f'{path_to_raport}'

        #/// main mechanism
        all_data = get_data(data_path) #// class object
        for single in all_data.gather_data(): #// function returns array of credentials
            print("Processing: "+single[0]+"/"+single[1]+"/"+single[2])
            mechanism = Mortgage(single[0],single[1],single[2])
            if mechanism.mortgage() != False: #// if mortgage data provided is correct, then get the content
                content = mechanism.read_content()
                if content != False:
                    for x in content:
                        print(x)
                else:
                    all_data.save_fails(f"{single[0]}/{single[1]}/{single[2]}", "Time exceeded", raport_name, path_to_raport) #// 1.id   2.reason of fail   3. name of raport(!!Do not include extension!!)
                    continue
            else:
                all_data.save_fails(f"{single[0]}/{single[1]}/{single[2]}", "Wrong number", raport_name, path_to_raport) #// 1.id   2.reason of fail   3. name of raport(!!Do not include extension!!)
                continue

app = Main()
app.mainloop()
