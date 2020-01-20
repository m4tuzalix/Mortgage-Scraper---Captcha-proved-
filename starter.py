from gui import Main 
from psutil import process_iter
from os import system
to_kill = ["chromedriver", "python", "chrome"]
for x in to_kill:
    system(f"taskkill /f /im {x}.exe")
app = Main()
app.mainloop()