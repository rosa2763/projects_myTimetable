# Timetable project
# Intermediate Stage
# Data Entry upto lf#1, lf#2 complete
from tkinter import*
from tkinter import ttk
import tkinter as tk
import pandas as pd
from tt_show_class_dec import TimeTable

def dic1_fun(key_col,val_col):
    keys = df1[key_col]
    values = df1[val_col]
    return(dict(zip(keys,values)))
def dic2_fun(key_col,val_col):
    keys = df2[key_col]
    values = df2[val_col]
    return(dict(zip(keys,values)))
def dic3_fun(key_col,val_col):
    keys = df3[key_col]
    values = df3[val_col]
    return(dict(zip(keys,values)))
def find_key(dictionary,value):
    for key,val in dictionary.items():
        if val == value:
            return(key)
    return None
#return[key for key,val in dictionary.items() if val == value]
def parent_dept_selection(event): 
    global df2,emp_dict,nick_name_dict
    data_tt["faculty_dept"] = dept_code.get()
    df2 = pd.read_excel("faculty_data.xlsx",sheet_name=data_tt["faculty_dept"])
    df2["ID2"] = df2.index
    #print(df2)
    emp_code.set('')
    emp_dict = dic2_fun("ID2","Emp_code")
    dept_dict = dic2_fun("ID2","Dept")
    nick_name_dict = dic2_fun("ID2","Nick_name")
    position_dict = dic2_fun("ID2","Position")  
    emp_list = list(emp_dict.values())
    emp_code.config(values=emp_list)
def emp_code_selection(event):
    global data_tt,emp_dict,nick_name_dict
    data_tt["faculty_code"] = emp_code.get()
    x_val = find_key(emp_dict,int(data_tt["faculty_code"]))
    my_data_tt["my_name"] = nick_name_dict[x_val]
    assign_dept_code.config(values=("CE","ME","EE"))
def dept_option_selection(event):
    data_tt["class_dept"] = assign_dept_code.get()
    my_data_tt["my_class"] = data_tt["class_dept"] 
    odd_even_code.config(values=("ODD","EVEN"))
def odd_even_selection(event):
    global odd_even
    odd_even = odd_even_code.get()
    if odd_even == 'ODD':
        odd_even_list = ['s1','s3','s5','s7']
    elif odd_even == 'EVEN':
        odd_even_list = ['s2','s4','s6','s8']
    else:
        pass
    semester_code.set('')
    semester_code.config(values=odd_even_list)
def semester_option_selection(event):
    global df1,odd_even
    data_tt["class_semester"] = semester_code.get()
    ltp_code.config(values=("Lecture","Tutorial","Practical","Projects"))
def ltp_option_selection(event):
    global class_x,df1,df3
    global weekday_dict,slot1_dict,slot2_dict,slot3_dict,slot4_dict
    global slot5_dict,slot6_dict
    df1 = pd.read_excel(f"curiculam_{data_tt['class_dept']}.xlsx",sheet_name=data_tt["class_semester"])
    df1["ID1"] = df1.index
    global code_dict,select_dict,class_count_dict
    global lec_dict,tut_dict,lab_dict,proj_dict
    global class_x,code_ref_lst,lec_ref_lst
    code_dict = dic1_fun("ID1","Code")
    select_dict = dic1_fun("ID1","Select")
    class_count_dict = dic1_fun("ID1","Number")
    lec_dict = dic1_fun("ID1","L")
    tut_dict = dic1_fun("ID1","T")
    lab_dict = dic1_fun("ID1","P")
    proj_dict = dic1_fun("ID1","R")
    select_lst = []
    for i in range(len(select_dict)):
        if select_dict[i] != 0:
            select_lst.append(select_dict[i])
        else:
            del code_dict[i]
            del lec_dict[i]
            del tut_dict[i]
            del lab_dict[i]
            del proj_dict[i]
            del class_count_dict[i]
# Read the selected subject codes from the time table to avoid duplicate entry
    df3 = pd.read_excel(f"timeTable_{my_data_tt['my_class']}.xlsx",sheet_name=my_data_tt["my_sem"])
    df3["ID3"] = df3.index
    weekday_dict = dic3_fun("ID3","week_day")
    slot1_dict = dic3_fun("ID3","slot_1")
    slot2_dict = dic3_fun("ID3","slot_2")
    slot3_dict = dic3_fun("ID3","slot_3")
    slot4_dict = dic3_fun("ID3","slot_4")
    slot5_dict = dic3_fun("ID3","slot_5")
    slot6_dict = dic3_fun("ID3","slot_6")

    class_x=ltp_code.get()
    print(class_x)
    code_lst = list(code_dict.values())
    code_ref_lst = []
    class_count_lst = list(class_count_dict.values())
    class_count_ref_lst = []
    match class_x:
        case "Lecture":
            lec_lst = list(lec_dict.values())           
            lec_ref_lst = []
            for i in range(len(lec_lst)):
                if lec_lst[i] != 0:
                    lec_ref_lst.append(lec_lst[i])
                    code_ref_lst.append(code_lst[i])
        # avoid duplicate entry in Lecture
            code_lst = []
            x = len(lec_ref_lst)
            for j in range(x):
                L_count = lec_ref_lst[j]
                L_consumed = check_tt_space(code_ref_lst[j])
                if (L_count-L_consumed) > 0:
                    code_lst.append(code_ref_lst[j])
        case "Tutorial":
            tut_lst = list(tut_dict.values())
            for i in range(len(tut_lst)):
                if tut_lst[i] != 0:
                    class_count_ref_lst.append(class_count_lst[i])
                    code_ref_lst.append(code_lst[i])
        # avoid duplicate entry in tutorial
            code_lst = []
            T_count = 0
            x = len(class_count_ref_lst)
            for j in range(x):
                if class_count_ref_lst[j] <= 26:
                    T_count = 1
                elif class_count_ref_lst[j] <= 48:
                    T_count = 2
                else:
                    T_count = 3
                T_consumed = check_tt_space(code_ref_lst[j])
                if (T_count-T_consumed) > 0:
                    code_lst.append(code_ref_lst[j])
        case "Practical":
            lab_lst = list(lab_dict.values())           
            for i in range(len(lab_lst)):
                if lab_lst[i] != 0:
                    class_count_ref_lst.append(class_count_lst[i])
                    code_ref_lst.append(code_lst[i])
        # avoid duplicate entry in Practical
            code_lst = []
            P_count = 0
            x = len(class_count_ref_lst)
            for j in range(x):
                if class_count_ref_lst[j] <= 18:
                    P_count = 1
                elif class_count_ref_lst[j] <= 36:
                    P_count = 2
                elif class_count_ref_lst[j] <= 54:
                    P_count = 3
                else:
                    P_count = 4
                P_consumed = check_tt_space(code_ref_lst[j])
                if (P_count-P_consumed) > 0:
                    code_lst.append(code_ref_lst[j])
        case "Projects":
            proj_lst = list(proj_dict.values())           
            proj_ref_lst = []
            for i in range(len(proj_lst)):
                if proj_lst[i] != 0:
                    proj_ref_lst.append(proj_lst[i])
                    code_ref_lst.append(code_lst[i])
            code_lst = code_ref_lst
        case _:
            print("Who")
    sub_code.set('')
    sub_code.config(values=code_lst)

def check_tt_space(check_tt_list):
    global slot1_dict,slot2_dict,slot3_dict,slot4_dict
    global slot5_dict,slot6_dict    
    #print(check_tt_list)  
    count_used = 0
    slot1_list=list(slot1_dict.values())
    for i in range(len(slot1_list)):
        if slot1_list[i] == check_tt_list: 
            count_used = count_used +1
    slot2_list=list(slot2_dict.values())
    for i in range(len(slot2_list)):
        if slot2_list[i] == check_tt_list: 
            count_used = count_used +1
    slot3_list=list(slot3_dict.values())
    for i in range(len(slot3_list)):
        if slot3_list[i] == check_tt_list: 
            count_used = count_used +1
    slot4_list=list(slot4_dict.values())
    for i in range(len(slot4_list)):
        if slot4_list[i] == check_tt_list: 
            count_used = count_used +1
    slot5_list=list(slot5_dict.values())
    for i in range(len(slot5_list)):
        if slot5_list[i] == check_tt_list: 
            count_used = count_used +1
    slot6_list=list(slot6_dict.values())
    for i in range(len(slot6_list)):
        if slot6_list[i] == check_tt_list: 
            count_used = count_used +1
    return(count_used)   

def sub_option_selection(event):
    data_tt["sub_code"] = sub_code.get()
    action_code.config(values=("PROCEED","CLEAR"))
def action_option_selection(event):
    global class_x
    action_entry=action_code.get()
    #print(data_tt)
    if action_entry == "CLEAR":
        lf1_lf2_clear()
        pass
    elif action_entry == "PROCEED":
        tt_slot_entry(class_x,data_tt["sub_code"])
        TimeTable(root)
    else:
        pass
def tt_slot_entry(class_type,sub_selected):
    match class_type:
        case "Lecture":
            cb1.config(state='normal')
            cb2.config(state='normal')
            cb3.config(state='normal')
            cb4.config(state='normal')
            cb5.config(state='normal')
            cb6.config(state='normal')
            key_lec = find_key(code_dict,sub_selected)
            hr_count = lec_dict[key_lec]
            print(class_type,sub_selected,hr_count) 

    pass
def cancel_option_selection(event):
    lf1_lf2_clear()
    pass
def lf1_lf2_clear():
    emp_code.set('')
    emp_code['values']=()
    assign_dept_code.set('')
    odd_even_code.set('')
    semester_code.set('')
    ltp_code.set('')
    sub_code.set('')
    cancel_code.set('')

def common_for_cancel_options():
    pass

def clear_day_slot():
    text_box1.delete('1.0','end')
    text_box2.delete('1.0','end')
    sr0.set(0)
    sr1.set(0)
    sr2.set(0)
    sr3.set(0)
    sr4.set(0)
    sr5.set(0)
    sr6.set(0)

def week_click(week_value):
    day_slot["week_slot"]=r3.get()
    day_slot["time_slot0"]=sr0.get()
    day_slot["time_slot1"]=sr1.get()
    day_slot["time_slot2"]=sr2.get()
    day_slot["time_slot3"]=sr3.get()
    day_slot["time_slot4"]=sr4.get()
    day_slot["time_slot5"]=sr5.get()
    day_slot["time_slot6"]=sr6.get()
    print(day_slot)

def cancel_option(event):
    global clear_status
    cancel_entry = cancel_click.get()
    if cancel_entry == "Assigned Class":
        clear_status = 1
        common_for_cancel_options()
        text_box1.insert('1.0',"All the data entry under 1)Assigned for Dept./Topic 2)semester 3)Class Type 4)Subject Code will be reset for fresh entry.")    
    elif cancel_entry == "Day & Slot":
        clear_status = 2
        common_for_cancel_options()
        text_box1.insert('1.0',"All the data entry under 1)Assigned for Dept./Topic 2)semester 3)Class Type 4)Subject Code will be reset for fresh entry.")
    else:  
        clear_status = 3
        common_for_cancel_options()
        text_box1.insert('1.0',"All the data entry under 1)Assigned for Dept./Topic 2)semester 3)Class Type 4)Subject Code will be reset for fresh entry.")
def confirm_cancel():
    pass
    """
    cancel_check.config(text="Clear Data Entry",fg="black")
    cancel_button.config(text="Confirm CLEAR",bg="white",fg="black")
    #enter_action.config(bg="white")
    global clear_status
    if clear_status == 0:
        clear_lf1_2()
    elif clear_status == 1:
        clear_lf1_2()
    elif clear_status == 2:
        clear_day_slot()
    else:
        clear_ALL()
    """
def verify_ok():
    pass
def update_tt():
    print("123")
    TimeTable(root)

root=Tk()
root.title("Data entry by Faculty for TimeTable")
w_width = root.winfo_screenwidth()
w_height = root.winfo_screenheight()
dev_WIDTH = 700
dev_HEIGHT = 550
ref_s_WIDTH = 1920
ref_s_HEIGHT = 1080
s_width = int(dev_WIDTH*w_width/ref_s_WIDTH)
s_height = int(dev_HEIGHT*w_height/ref_s_HEIGHT)
#print(s_width,s_height)
root.geometry("700x550")
root.iconbitmap('Logo.ico')
root.columnconfigure(0,weight=1) #weight= 1 indicates scale of one
root.rowconfigure(0,weight=1)
frame=Frame(root)
frame.grid(row=0,column=0,padx=10,pady=5,sticky="nsew")
x = "Lecture"
global data_tt,my_data_tt,in_tt
data_tt={"faculty_dept":'CE',"faculty_code":1234,"class_dept":'CE',
    "class_semester":'S1',"class_type":'Lecture',"sub_code":'Maths'}
my_data_tt={"my_name":"ROSA","my_class":"CE","my_sem":"s1","my_sub":"sub_ref",
    "class_type":"Lecture","lect_count":1,"tut_count":1,"lab_count":1,
    "proj_guide":3,"room_no":"101","my_week":"Monday","my_slot":"1"}
in_tt={"week_day":" ","slot_1":[],"slot_2":[],"slot_3":[],
    "slot_4":[],"slot_5":[],"slot_6":[],"slot_x":[]}
odd_even="odd"
day_slot={"week_slot":3,"time_slot0":0,"time_slot1":1,"time_slot2":2,"time_slot3":3,
    "time_slot4":4,"time_slot5":5,"time_slot6":6}
sr=IntVar()
#LBELFRAME lf1
frame.columnconfigure(0,weight=1) #weight= 1 indicates scale of one
frame.rowconfigure((0,1,2,3),weight=1)
lf1=LabelFrame(frame,text="Employ Code: Parent Dept: Faculty Initial: Assigned Dept.",padx=5,pady=2,fg="Blue")
lf1.grid(row=0,column=0,padx=10,pady=5,sticky="nsew")
lf1.columnconfigure((0,1,2,3),weight=1,uniform="a") #weight= 1 indicates scale of one
lf1.rowconfigure((0,1),weight=1)
dept_emp_code=Label(lf1,text="Parent Dept.& Emp.Code",width=15)
dept_emp_code.grid(row=0,column=0,columnspan=2,padx=2,pady=2,sticky="nsew")
dept_class=Label(lf1,text="Assigned Department/Semester",width=15)
dept_class.grid(row=0,column=2,columnspan=2,padx=2,pady=2,sticky="nsew")
#lf1 entries
dept_options=StringVar()
dept_code=ttk.Combobox(lf1,textvariable=dept_options,state='raedonly')
dept_code.grid(row=1,column=0,padx=10,pady=2,sticky="nsew")
dept_code['values']=("CE","ME","EE")
dept_code.current()
dept_code.bind("<<ComboboxSelected>>",parent_dept_selection)
emp_options=StringVar()
emp_code=ttk.Combobox(lf1,textvariable=emp_options,state='raedonly')
emp_code.grid(row=1,column=1,padx=10,pady=2,sticky="nsew")
emp_code['values']=()
emp_code.current()
emp_code.bind("<<ComboboxSelected>>",emp_code_selection)
assign_dept_options=StringVar()
assign_dept_code=ttk.Combobox(lf1,textvariable=assign_dept_options,state='raedonly')
assign_dept_code.grid(row=1,column=2,padx=10,pady=2,sticky="nsew")
assign_dept_code['values']=()
assign_dept_code.current()
assign_dept_code.bind("<<ComboboxSelected>>",dept_option_selection)
odd_even_options=StringVar()
odd_even_code=ttk.Combobox(lf1,textvariable=odd_even_options,state='raedonly')
odd_even_code.grid(row=1,column=3,padx=10,pady=2,sticky="nsew")
odd_even_code['values']=()
odd_even_code.current()
odd_even_code.bind("<<ComboboxSelected>>",odd_even_selection)
#LBELFRAME lf2
lf2=LabelFrame(frame,text="Selecting Assigned Classes",padx=5,pady=2,fg="Blue")
lf2.grid(row=1,column=0,padx=10,pady=5,sticky="nsew")
#lf2 options
global semester_options
#lf2 labels
lf2.columnconfigure((0,1,2,3),weight=1,uniform="a") #weight= 1 indicates scale of one
lf2.rowconfigure((0,1,2),weight=1)
text_box1=Text(lf2, width=60,height=3,fg="red",font=("Ariel",11))
text_box1.grid(row=0, column=0,columnspan=4,padx=10,pady=5,sticky="nsew")
semester_class=Label(lf2,text="Semester",width=15)
semester_class.grid(row=1,column=0,padx=2,pady=2,sticky="nsew")
ltp_type=Label(lf2,text="Class type",width=15)
ltp_type.grid(row=1,column=1,padx=2,pady=2,sticky="nsew")
sub_code=Label(lf2,text="Subject Code",width=15)
sub_code.grid(row=1,column=2,padx=2,pady=2,sticky="nsew")
sub_check=Label(lf2,text="ACTION",width=15)
sub_check.grid(row=1,column=3,padx=2,pady=2,sticky="nsew")
#lf2 entries
semester_options=StringVar()
semester_code=ttk.Combobox(lf2,textvariable=semester_options,state='raedonly')
semester_code.grid(row=2,column=0,padx=10,pady=2,sticky="nsew")
semester_code['values']=()
semester_code.current()
semester_code.bind("<<ComboboxSelected>>",semester_option_selection)
ltp_options=StringVar()
ltp_code=ttk.Combobox(lf2,textvariable=ltp_options,state='raedonly')
ltp_code.grid(row=2,column=1,padx=10,pady=2,sticky="nsew")
ltp_code['values']=()
ltp_code.current()
ltp_code.bind("<<ComboboxSelected>>",ltp_option_selection)
sub_options=StringVar()
sub_code=ttk.Combobox(lf2,textvariable=sub_options,state='raedonly')
sub_code.grid(row=2,column=2,padx=10,pady=2,sticky="nsew")
sub_code['values']=()
sub_code.current()
sub_code.bind("<<ComboboxSelected>>",sub_option_selection)
action_options=StringVar()
action_code=ttk.Combobox(lf2,textvariable=action_options,state='raedonly')
action_code.grid(row=2,column=3,padx=10,pady=2,sticky="nsew")
action_code['values']=("CLEAR")
action_code.current()
action_code.bind("<<ComboboxSelected>>",action_option_selection)
#LBELFRAME lf3
lf3=LabelFrame(frame,text="Timetable Weekday and Slot selection",padx=5,pady=2,fg="Blue")
lf3.grid(row=2,column=0,padx=10,pady=5,sticky="nsew")
lf3.columnconfigure((0,1,2,3,4,5,6),weight=1,uniform="a") #weight= 1 indicates scale of one
lf3.rowconfigure((0,1,2),weight=1)
r3=IntVar()
week_day=["Monday","Tuesday","Wednesday","Thursday","Friday"]
for i in range(len(week_day)):
    week=(Radiobutton(lf3,text=week_day[i],variable=r3,value=i,command=lambda:week_click(r3.get())))
    week.grid(row=0,column=i+1,padx=10,pady=2,sticky="nsew")
#print(week.r3)
show_msg=Label(lf3,text="-----------Slot 1 to Slot 6 for Lecture & Tutorial and Slot X optional-------------",fg="Blue")
show_msg.grid(row=1, column=0, columnspan=7,padx=2,pady=2,sticky="nsew")
slots=["Slot 1","Slot 2","Slot 3","Slot 4","Slot 5","Slot 6","Slot X"]
sr0 = IntVar()
sr1 = IntVar()
sr2 = IntVar()
sr3 = IntVar()
sr4 = IntVar()
sr5 = IntVar()
sr6 = IntVar()
global cb1
cb1=Checkbutton(lf3, text=slots[0], variable=sr0,state='disabled')
cb1.grid(row=3, column=0,sticky="nsew")
cb2=Checkbutton(lf3, text=slots[1], variable=sr1,state='disabled')
cb2.grid(row=3, column=1,sticky="nsew")
cb3=Checkbutton(lf3, text=slots[2], variable=sr2,state='disabled')
cb3.grid(row=3, column=2,sticky="nsew")
cb4=Checkbutton(lf3, text=slots[3], variable=sr3,state='disabled')
cb4.grid(row=3, column=3,sticky="nsew")
cb5=Checkbutton(lf3, text=slots[4], variable=sr4,state='disabled')
cb5.grid(row=3, column=4,sticky="nsew")
cb6=Checkbutton(lf3, text=slots[5], variable=sr5,state='disabled')
cb6.grid(row=3, column=5,sticky="nsew")
cb7=Checkbutton(lf3, text=slots[6], variable=sr6,state='disabled')
cb7.grid(row=3, column=6,sticky="nsew")
#LBELFRAME lf4
#lf4 options
lf4=LabelFrame(frame,text="Timetable Data Entry Commands",padx=5,pady=2,fg="Blue")
lf4.grid(row=3,column=0,padx=10,pady=5,sticky="nsew")
lf4.columnconfigure((0,1,2,3),weight=1,uniform="a") #weight= 1 indicates scale of one
lf4.rowconfigure((0,1),weight=1)
text_box2=Text(lf4, width=60,height=3,fg="red",font=("Ariel",11))
text_box2.grid(row=0,column=0,columnspan=4,padx=10,pady=5,sticky="nsew")
cancel_check=Label(lf4,text="Cancel Data Entry",width=15)
cancel_check.grid(row=1,column=0,columnspan=2, padx=2,pady=2,sticky="nsew")
cancel_options=StringVar()
cancel_code=ttk.Combobox(lf4,textvariable=cancel_options,state='raedonly')
cancel_code.grid(row=2,column=0,padx=10,pady=2,sticky="nsew")
cancel_code['values']=("Clear Day & Slot ","Clear All Data","Clear Data from Time Table")
cancel_code.current()
cancel_code.bind("<<ComboboxSelected>>",cancel_option_selection)

cancel_button=Button(lf4,text="Confirm CANCEL",bg="white",command=confirm_cancel)
cancel_button.grid(row=2,column=1,padx=2,pady=2,sticky="nsew")
verify_data=Label(lf4,text="Verify & Update TimeTable",width=15)
verify_data.grid(row=1,column=2,columnspan=2, padx=2,pady=2,sticky="nsew")
verify_button=Button(lf4,text="Verified OK",bg="white",command=verify_ok)
verify_button.grid(row=2,column=2,padx=2,pady=2,sticky="nsew")
update_button=Button(lf4,text="Update TimeTable",bg="white",command=update_tt)
update_button.grid(row=2,column=3,padx=2,pady=2,sticky="nsew")
root.mainloop()