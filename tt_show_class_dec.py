from tkinter import*

class TimeTable(Toplevel):
	def __init__(self,parent):
		super().__init__(parent)
		self.title("Small Time Table")
		self.geometry("800x400")
		self.parent = parent
		self.iconbitmap('Logo.ico')
		#Basic timetable with 5 days and 6 slots
		self.columnconfigure(0,weight=1)
		self.rowconfigure(0,weight=1)
		self.tt=LabelFrame(self,text="  Class Time Table  ",fg="Blue",font="bold", border=5,borderwidth=5,padx=10,pady=10)
		self.tt.grid(row=0,column=0,padx=10,pady=5,sticky="nsew")
		self.tt.columnconfigure(0,weight=1)
		self.tt.rowconfigure(0,weight=1)
		self.class_label=Label(self.tt,text="CLASS",bg="red",font="bold",width=10,fg="white",border=5,borderwidth=2,bd=2,padx=5,pady=5)
		self.class_label.grid(row=0,column=0,padx=2,pady=2,sticky="nsew")
		
		self.row0=["SLOT1","SLOT2","SLOT3","SLOT4","SLOT5","SLOT6"]
		for i in range(6):
			self.tt.columnconfigure(i+1,weight=1)
			self.tt.rowconfigure(0,weight=1)
			self.lr0=Label(self.tt,text=self.row0[i],bg="grey",fg="white",font="bold",width=10,border=5,borderwidth=2,bd=2,padx=5,pady=5)
			self.lr0.grid(row=0,column=i+1,padx=2,pady=2,sticky="nsew")
		self.column0=["Monday","Tuesday","Wednesday","Thursday","Friday"]
		for i in range(5):
			self.tt.columnconfigure(0,weight=1)
			self.tt.rowconfigure(i+1,weight=1)
			self.lc0 = Label(self.tt,text=self.column0[i],width=10,bg="grey",fg="white",font="bold", border=5, borderwidth=2, bd=2, padx=5, pady=5)
			self.lc0.grid(row=i+1,column=0,padx=2,pady=2,sticky="nsew")
		self.days=[[["cMon1","fMon1"],["cMon2","fMon2"],["cMon3","fMon3"],["cMon4","fMon4"],["cMon5","fMon5"],["cMon6","fMon6"]],
    		[["cTue1","fTue1"],["cTue2","fTue2"],["cTue3","fTue3"],["cTue4","fTue4"],["cTue5","fTue5"],["cTue6","fTue6"]],
    		[["cWed1","fWed1"],["cWed2","fWed2"],["cWed3","fWed3"],["cWed4","fWed4"],["cWed5","fWed5"],["cWed6","fWed6"]],
    		[["cThu1","fThu1"],["cThu2","fThu2"],["cThu3","fThu3"],["cThu4","fThu4"],["cThu5","fThu5"],["cThu6","fThu6"]],
    		[["cFri1","fFri1"],["cFri2","fFri2"],["cFri3","fFri3"],["cFri4","fFri4"],["cFri5","fFri5"],["cFri6","fFri6"]]]
		for i in range(5):
			for j in range(6):
				self.tt.rowconfigure(i+1,weight=1)
				self.tt.columnconfigure(j+1,weight=1)
				self.lmn=Label(self.tt,text=f"{self.days[i][j][0]}\n{self.days[i][j][1]}",bg="lightblue",width=10,border=5,borderwidth=2,bd=2,padx=5,pady=5)
				self.lmn.grid(row=i+1,column=j+1,padx=2,pady=2,sticky="nsew")

		self.close_button = Button(self,text="Close Time Table Window",bg="Yellow",font="bold",command=self.destroy)
		self.close_button.grid(row=1,column=0,padx=10,pady=5,sticky="nsew")

class MainWindow(Tk):
	def __init__(self):
		super().__init__()
		self.title("Main window")
		self.geometry("500x400")
		self.iconbitmap('Logo.ico')
		self.open_tt_button = Button(self,text="Open",command=self.open_tt)
		self.open_tt_button.pack(pady=20)

	def open_tt(self):
		TimeTable(self)

if __name__ =="__main__":
	app = MainWindow()
	app.mainloop()