# Timetable project
# Intermediate Stage
from tkinter import*
from tkinter import ttk
import tkinter as tk
from unittest import case
from openpyxl import load_workbook,Workbook
import pandas as pd
import numpy as np
from tt_show_class_jan20 import TimeTable
import os
def create_excelsheet_orread(file_name,sheet_name):
    if os.path.exists(file_name):
        sheet_names_list = pd.ExcelFile(file_name).sheet_names
        if sheet_name not in sheet_names_list:
            df_init = pd.DataFrame(data_ref)
            with pd.ExcelWriter(file_name, mode='a', engine='openpyxl', if_sheet_exists='new') as writer:
                df_init.to_excel(writer,sheet_name=sheet_name,index=False,engine = "openpyxl")
            df = pd.read_excel(file_name,sheet_name=sheet_name,engine="openpyxl")
            return(df)
        else: 
            df = pd.read_excel(file_name,sheet_name=sheet_name,engine="openpyxl")
            return(df)
    else:
        df_init = pd.DataFrame(data_ref)
        df_init.to_excel(file_name,sheet_name,index=False,engine = "openpyxl")
        df = pd.read_excel(file_name,sheet_name=sheet_name,engine="openpyxl")
        return(df)   
def find_key(dictionary,value):
    for key,val in dictionary.items():
        if val == value:
            return(key)
    return None 
def parent_dept_selection(event):
    global df_dept
    reset_lf1_lf2()
    dept_emp_code.set('')
    df_dept = create_excelsheet_orread(file_name='faculty_data.xlsx',sheet_name=dept_code.get())
    dept_emp_code.config(values=df_dept.emp_code.tolist())
    text_box1.delete('1.0','end')
    text_box1.insert('1.0',f"Complete the slot allocation for the PRACTICAL classes to get the slots for Lectutre /Tutorial classes ..........  ")
    text_box1.insert('2.0',f"ENTER / REFRESH to continue with employee code")
def emp_code_selection(event):
    assign_dept_code.set('')
    assign_dept_code.config(values=("CE","ME","EE"))
    text_box1.delete('1.0','end')
    text_box1.insert('1.0',f"ENTER / REFRESH the department to which the class is assigned")
def dept_option_selection(event):
    odd_even_code.config(values=("ODD","EVEN"))
    text_box1.delete('1.0','end')
    text_box1.insert('1.0',f"ENTER / REFRESH the selection forsemester ODD or EVEN")
def odd_even_selection(event):
    odd_even = odd_even_code.get()
    if odd_even == 'ODD':
        odd_even_list = ['s1','s3','s5','s7']
    elif odd_even == 'EVEN':
        odd_even_list = ['s2','s4','s6','s8']
    else:
        pass
    semester_code.set('')
    semester_code.config(values=odd_even_list)
    text_box1.delete('1.0','end')
    text_box1.insert('1.0',f"ENTER / REFRESH to select the assigned semester")
def check_curi_filedata(file_name,sheet_name,ref_value):  #defined for use in semester option selection
    if os.path.exists(file_name):
        print(file_name,ref_value)
        sheet_names_list = pd.ExcelFile(file_name).sheet_names
        if sheet_name in sheet_names_list:
            df=pd.read_excel(file_name,sheet_name=sheet_name,engine="openpyxl")
            df_ref_value = df[df[ref_value] != 0]
            return df_ref_value
        else:
            text_box1.delete('1.0','end')
            text_box1.insert('1.0',f"{sheet_name} not available in the file {file_name}   .")
            text_box1.insert('2.0',f"Quit and create {sheet_name} sheet in file {file_name}")
            return False
    else:
        text_box1.delete('1.0','end')
        text_box1.insert('1.0',f"{file_name} not available in the system")
        text_box1.insert('2.0',f"Quit and create {file_name}")
        print("file does not exist")
        return False
def semester_option_selection(event):
    df_curi_lab = check_curi_filedata(f"curiculam_{assign_dept_code.get()}.xlsx",semester_code.get(),"P")
    if isinstance(df_curi_lab,bool):
        return
    df_sel = create_excelsheet_orread(f"faculty_assignment_{odd_even_code.get()}.xlsx",sheet_name=assign_dept_code.get())
    df_sel_lab = df_sel[["nick_name","P_code"]].copy()
    df_sel_lab.dropna(subset=['nick_name','P_code'],inplace=True) # remove rows with empty Name and Practical code
    code_lst_lab = []
    for i in range(len(df_sel_lab.nick_name.tolist())):
        if df_sel_lab.P_code.tolist()[i] != []:
            code_lst_lab.extend(df_sel_lab.P_code.tolist()[i].split(","))
    code_lst_lab = list(set(code_lst_lab))
    ltp_code.set('')
    print(len(df_curi_lab),len(code_lst_lab))
    # lab slots are to be identified first;check all the labs are selected, to get the lecture/tutorial slots
    if len(df_curi_lab) > len(code_lst_lab):
        ltp_code.config(values=("Practical"))
    else:
        ltp_code.config(values=("Lecture","Tutorial","Practical","Projects"))
        text_box1.delete('1.0','end')
        text_box1.insert('1.0',f"Complete the slot allocation for the PRACTICAL classes to get the slots for Lectutre /Tutorial classes ..........  ")
    text_box1.insert('2.0',f"ENTER / REFRESH to continue")
    sub_code.config(values=(''))
def ltp_option_selection(event):
    global faculty_name,df_sel,df_curi_active,code_lst_lab,code_lst_tut
    action_code.set('')
    action_code.config(values=(''))
    faculty_name = df_dept.nick_name.tolist()[df_dept.emp_code.tolist().index(int(dept_emp_code.get()))]
    df_curi = create_excelsheet_orread(f"curiculam_{assign_dept_code.get()}.xlsx",semester_code.get())
    df_curi_active = df_curi[df_curi["Select"] != 0]
    df_sel = create_excelsheet_orread(f"faculty_assignment_{odd_even_code.get()}.xlsx",sheet_name=dept_code.get())
    print(df_sel)
    match ltp_code.get():
        case "Lecture":
            df_curi_lec = df_curi_active[df_curi_active["L"] != 0] 
            code_lst_temp = df_curi_lec.Code.tolist()
            df_sel_lec = df_sel[["nick_name","deptL_class","semL","L_code","L_class","L_hr"]].copy()
            df_sel_lec.dropna(subset=['nick_name','L_code'],inplace=True) # remove rows with empty nick_name,code
            if df_sel_lec.empty:
                code_lst = df_curi_lec.Code.tolist()
            else: 
                codesin_lec_lst = []
                deptin_lst_lec = []                    
                semin_lst_lec = []
                classin_lst_lec = []
                hrin_lst_lec = [] 
                for j in range(len(df_sel_lec)):  
                    code_lec_split = df_sel_lec.at[df_sel_lec.index.tolist()[j],"L_code"].split(",")
                    if len(code_lec_split) == 1:
                        classin_lst_lec.append(df_sel_lec.at[df_sel_lec.index.tolist()[j],"L_class"])
                        hrin_lst_lec.append(df_sel_lec.at[df_sel_lec.index.tolist()[j],"L_hr"])
                    else:
                        classin_lst_lec.extend(df_sel_lec.at[df_sel_lec.index.tolist()[j],"L_class"].split(","))
                        hrin_lst_lec.extend(df_sel_lec.at[df_sel_lec.index.tolist()[j],"L_hr"].split(","))
                    codesin_lec_lst.extend(code_lec_split)                     
                    deptin_lst_lec.extend(df_sel_lec.at[df_sel_lec.index.tolist()[j],"deptL_class"].split(","))
                    semin_lst_lec.extend(df_sel_lec.at[df_sel_lec.index.tolist()[j],"semL"].split(","))
                # remove codes with other department and semester
                codein_lec = []
                classin_lec = []
                hrin_lec = []
                for i in range(len(codesin_lec_lst)):
                    if codesin_lec_lst[i] in df_curi_lec.Code.tolist():
                        if assign_dept_code.get() == deptin_lst_lec[i] and semester_code.get() == semin_lst_lec[i]: 
                            codein_lec.append(codesin_lec_lst[i])
                            classin_lec.append(classin_lst_lec[i])
                            hrin_lec.append(hrin_lst_lec[i])
                # remove codes with full lecture hours from curriculam list
                print(codein_lec,classin_lec,hrin_lec)
                for i in range(len(codein_lec)):
                    if codein_lec[i] in df_curi_lec.Code.tolist():
                        if hrin_lec[i] == classin_lec[i]:
                            code_lst_temp.remove(codein_lec[i])
                # remove faculty_name code from the elemination list
                if faculty_name in df_sel_lec.nick_name.tolist():
                    df_sel_mylec = df_sel_lec[df_sel_lec["nick_name"] == faculty_name]
                    for i in range(len(df_sel_mylec.iloc[0]["L_code"].split(","))):
                        if df_sel_mylec.iloc[0]["L_code"].split(",")[i] in codein_lec:
                            codein_lec.remove(df_sel_mylec.iloc[0]["L_code"].split(",")[i])
                for i in range(len(codein_lec)):
                    if codein_lec[i] in code_lst_temp:
                        code_lst_temp.remove(codein_lec[i])
                code_lst = code_lst_temp                                          
        case "Tutorial":
            df_curi_tut = df_curi_active[df_curi_active["T"] != 0]
            df_sel_tut = df_sel[["nick_name","deptT_class","semT","T_code","T_hr"]].copy()
            df_sel_tut.dropna(subset=['nick_name','T_code'],inplace=True) # remove rows with empty tutorial code
            if df_sel_tut.empty:
                code_lst = df_curi_tut.Code.tolist()
                print(code_lst,"code list when sel empty")
            else:
                T_count = []
                for i in range(len(df_curi_tut)):
                    if list(df_curi_tut.Number)[i] <= 26:
                        T_need = 1
                    elif list(df_curi_tut.Number)[i] <= 48:
                        T_need = 2
                    else:
                        T_need = 3
                    T_count.append(T_need)
                code_lst_tut = df_curi_tut.Code.tolist()
                codesin_tut_lst = []
                deptin_lst_tut = []                    
                semin_lst_tut = []
                for j in range(len(df_sel_tut)):
                    codesin_tut_lst.extend(df_sel_tut.at[df_sel_tut.index.tolist()[j],"T_code"].split(","))
                    deptin_lst_tut.extend(df_sel_tut.at[df_sel_tut.index.tolist()[j],"deptT_class"].split(","))
                    semin_lst_tut.extend(df_sel_tut.at[df_sel_tut.index.tolist()[j],"semT"].split(","))
                codein_tut = []
                for i in range(len(codesin_tut_lst)):
                    if codesin_tut_lst[i] in df_curi_tut.Code.tolist():
                        if assign_dept_code.get() == deptin_lst_tut[i] and semester_code.get() == semin_lst_tut[i]:
                            codein_tut.append(codesin_tut_lst[i])
                T_used = [0]*len(df_curi_tut.Code.tolist())
                for i in range(len(df_curi_tut.Code.tolist())):
                    if df_curi_tut.Code.tolist()[i] in codein_tut:
                        T_used[i] += codein_tut.count(df_curi_tut.Code.tolist()[i])   
                print(T_used,T_count)
                for i in range(len(T_count)):
                    if T_used[i] >= T_count[i]:
                        if assign_dept_code.get() == deptin_lst_tut[i] and semester_code.get() == semin_lst_tut[i]:
                            code_lst_tut.remove(df_curi_tut.Code.tolist()[i])
                if df_sel_tut[df_sel_tut["nick_name"]==faculty_name].empty:
                    code_lst = code_lst_tut
                else:
                    df_mytut = df_sel_tut[df_sel_tut["nick_name"]==faculty_name]
                    my_tut_code = df_mytut.at[df_mytut.index.tolist()[0],"T_code"].split(",")
                    for i in range(len(my_tut_code)):
                        if my_tut_code[i] in code_lst_tut:
                            if assign_dept_code.get() == df_sel_tut.at[df_sel_tut.index.tolist()[0],"deptT_class"].split(",")[my_tut_code.index(my_tut_code[i])] and semester_code.get() == df_sel_tut.at[df_sel_tut.index.tolist()[0],"semT"].split(",")[my_tut_code.index(my_tut_code[i])]:
                                code_lst_tut.remove(my_tut_code[i])
                    code_lst = code_lst_tut     
        case "Practical":
            df_curi_lab = df_curi_active[df_curi_active["P"] != 0]
            df_sel_lab = df_sel[["nick_name","deptP_class","semP","P_code","P_hr"]].copy()
            df_sel_lab.dropna(subset=['nick_name','P_code'],inplace=True) # remove rows with empty Practical code
            if df_sel_lab.empty:
                code_lst = df_curi_lab.Code.tolist()          
            else:
                P_count = []
                for i in range(len(df_curi_lab)):
                    if list(df_curi_lab.Number)[i] <= 18:
                        P_need = 1
                    elif list(df_curi_lab.Number)[i] <= 32:
                        P_need = 2
                    elif list(df_curi_lab.Number)[i] <= 48:
                        P_need = 3
                    else:
                        P_need = 4                
                    P_count.append(P_need)                       
                code_lst_lab = df_curi_lab.Code.tolist()
                codesin_lab_lst = []
                deptin_lst_lab = []                    
                semin_lst_lab = []
                for j in range(len(df_sel_lab)):
                    codesin_lab_lst.extend(df_sel_lab.at[df_sel_lab.index.tolist()[j],"P_code"].split(","))
                    deptin_lst_lab.extend(df_sel_lab.at[df_sel_lab.index.tolist()[j],"deptP_class"].split(","))
                    semin_lst_lab.extend(df_sel_lab.at[df_sel_lab.index.tolist()[j],"semP"].split(","))
                print(codesin_lab_lst,deptin_lst_lab,semin_lst_lab)
                codein_lab = []
                for i in range(len(codesin_lab_lst)):
                    if codesin_lab_lst[i] in df_curi_lab.Code.tolist():
                        if assign_dept_code.get() == deptin_lst_lab[i] and semester_code.get() == semin_lst_lab[i]:
                            codein_lab.append(codesin_lab_lst[i])
                print(codein_lab)
                P_used = [0]*len(df_curi_lab.Code.tolist())
                print(P_count,P_used)
                for i in range(len(df_curi_lab.Code.tolist())):
                    if df_curi_lab.Code.tolist()[i] in codein_lab:
                        P_used[i] += codein_lab.count(df_curi_lab.Code.tolist()[i])   
                print(P_count,P_used)
                print(code_lst_lab)
                for i in range(len(P_count)):
                    if P_used[i] >= P_count[i]:
                        if assign_dept_code.get() == deptin_lst_lab[i] and semester_code.get() == semin_lst_lab[i]:
                            code_lst_lab.remove(df_curi_lab.Code.tolist()[i])
                print(code_lst_lab)
                if df_sel_lab[df_sel_lab["nick_name"]==faculty_name].empty:
                    code_lst = code_lst_lab
                else:
                    df_mylab = df_sel_lab[df_sel_lab["nick_name"]==faculty_name]
                    print(df_mylab)
                    print(df_mylab.at[df_mylab.index.tolist()[0],"P_code"])
                    my_lab_code = df_mylab.at[df_mylab.index.tolist()[0],"P_code"].split(",")
                    for i in range(len(my_lab_code)):
                        if my_lab_code[i] in code_lst_lab:
                            if assign_dept_code.get() == df_sel_lab.at[df_sel_lab.index.tolist()[0],"deptP_class"].split(",")[my_lab_code.index(my_lab_code[i])] and semester_code.get() == df_sel_lab.at[df_sel_lab.index.tolist()[0],"semP"].split(",")[my_lab_code.index(my_lab_code[i])]:
                                code_lst_lab.remove(my_lab_code[i])
                    code_lst = code_lst_lab           
        case "Projects":
            code_lst = ["Guide-4","Guide-8","Other HoD","other CT","Special"]
            faculty_in_guide_sel = df_sel[df_sel['nick_name'] == faculty_name]
            if list(faculty_in_guide_sel.R_code) != []:
                code_lst_l0 = code_lst
                code_lst = code_lst_l0
            for i in range(len(code_lst)):
                R_ref = [round(int(list(df_curi_active.Number)[i])/4),round(int(list(df_curi_active.Number)[i])/8),1,1,2]
        case _:
            print("Who")
    sub_code.set('')
    sub_code.config(values=code_lst)
def sub_option_selection(event):
    action_code.config(values=("PROCEED","CLEAR"))
def action_option_selection(event):
    global data_tt,data_faculty
    global class_x,data,ro_co_dict,row_val
    action_entry=action_code.get()
    if action_entry == "CLEAR":
        lf1_lf2_clear()
        pass
    elif action_entry == "PROCEED":
        TimeTable(root,f"timeTable_{assign_dept_code.get()}.xlsx",semester_code.get())
        week_click(None)
        refresh_button.config(bg="Yellow",fg="Black")
        text_box2.delete('1.0','end')
        text_box2.insert('1.0',f"Select weekday and one from available slot before REFRESH")
def block_lecslots_withnickname():
    dept_lst = ["CE","ME","EE"]
    odd_even = odd_even_code.get()
    if odd_even == 'ODD':
        semester_lst = ['s1','s3','s5','s7']
    elif odd_even == 'EVEN':
        semester_lst = ['s2','s4','s6','s8']
    for i in range(len(dept_lst)):
        for j in range(len(semester_lst)):
            df_tt_temp = pd.read_excel(f"timeTable_{dept_lst[i]}.xlsx",sheet_name=semester_lst[j],engine="openpyxl")
            for rows in range(len(df_tt_temp.index)):
                if faculty_name in df_tt_temp.iat[rows,1].split(","): 
                    if r3.get() == rows:
                        cb1.config(state='disabled')
                if faculty_name in df_tt_temp.iat[rows,2].split(","): 
                    if r3.get() == rows:
                        cb2.config(state='disabled')
                if faculty_name in df_tt_temp.iat[rows,3].split(","): 
                    if r3.get() == rows:
                        cb3.config(state='disabled')
                if faculty_name in df_tt_temp.iat[rows,4].split(","): 
                    if r3.get() == rows:
                        cb4.config(state='disabled')
                if faculty_name in df_tt_temp.iat[rows,5].split(","): 
                    if r3.get() == rows:
                        cb5.config(state='disabled')
                if faculty_name in df_tt_temp.iat[rows,6].split(","): 
                    if r3.get() == rows:
                        cb6.config(state='disabled')
def block_tutslots_withnickname():
    dept_lst = ["CE","ME","EE"]
    odd_even = odd_even_code.get()
    if odd_even == 'ODD':
        semester_lst = ['s1','s3','s5','s7']
    elif odd_even == 'EVEN':
        semester_lst = ['s2','s4','s6','s8']
    for i in range(len(dept_lst)):
        for j in range(len(semester_lst)):
            df_tt_temp = pd.read_excel(f"timeTable_{dept_lst[i]}.xlsx",sheet_name=semester_lst[j],engine="openpyxl")
            for rows in range(len(df_tt_temp.index)):
                if faculty_name in df_tt_temp.iat[rows,2].split(","): 
                    if r3.get() == rows:
                        cb2.config(state='disabled')
                if faculty_name in df_tt_temp.iat[rows,3].split(","): 
                    if r3.get() == rows:
                        cb3.config(state='disabled')
                if faculty_name in df_tt_temp.iat[rows,4].split(","): 
                    if r3.get() == rows:
                        cb4.config(state='disabled')
                if faculty_name in df_tt_temp.iat[rows,5].split(","): 
                    if r3.get() == rows:
                        cb5.config(state='disabled')
                if faculty_name in df_tt_temp.iat[rows,6].split(","): 
                    if r3.get() == rows:
                        cb6.config(state='disabled')       
def block_labslots_withnickname():
    dept_lst = ["CE","ME","EE"]
    odd_even = odd_even_code.get()
    if odd_even == 'ODD':
        semester_lst = ['s1','s3','s5','s7']
    elif odd_even == 'EVEN':
        semester_lst = ['s2','s4','s6','s8']
    for i in range(len(dept_lst)):
        for j in range(len(semester_lst)):
            df_tt_temp = pd.read_excel(f"timeTable_{dept_lst[i]}.xlsx",sheet_name=semester_lst[j],engine="openpyxl")
            for rows in range(len(df_tt_temp.index)):
                if faculty_name in df_tt_temp.iat[rows,4].split(","):
                    if r3.get() == rows:
                        cb3.config(state='disabled')
                if faculty_name in df_tt_temp.iat[rows,6].split(","):
                    if r3.get() == rows:
                        cb5.config(state='disabled')
def week_click(week_value:any):
    global code_lst_lab,code_lst_tut,faculty_name
    df_tt = pd.read_excel(f"timeTable_{assign_dept_code.get()}.xlsx",sheet_name=semester_code.get(),engine="openpyxl")
    print(df_tt)
    match ltp_code.get():
        case "Lecture":
            reset_lf3()
            if df_tt.at[r3.get(),"slot_1"] == "FREE":
                cb1.config(state='normal')
            if df_tt.at[r3.get(),"slot_2"] == "FREE":
                cb2.config(state='normal')
            if df_tt.at[r3.get(),"slot_3"] == "FREE":
                cb3.config(state='normal')
            if df_tt.at[r3.get(),"slot_4"] == "FREE":
                cb4.config(state='normal')
            if df_tt.at[r3.get(),"slot_5"] == "FREE":
                cb5.config(state='normal')
            if df_tt.at[r3.get(),"slot_6"] == "FREE":
                cb6.config(state='normal')
            #if df_tt.at[r3.get(),"slot_x"] == "FREE":
            #   cb7.config(state='normal')
            else:
                print("NOT blank")
                text_box2.delete('1.0','end')
                text_box2.insert('1.0',f"!! WARNING !! First complete the entry in LAB slots to get all slots for the LECTURE")
                if df_tt.at[r3.get(),"slot_1"] == "FREE":
                    cb1.config(state='normal')
                if df_tt.at[r3.get(),"slot_2"] == "FREE":
                    cb2.config(state='normal')  
            block_lecslots_withnickname()                    
        case "Tutorial":
            reset_lf3()
            print(len(df_tt.index),len(df_tt.columns))
            codein_status = 0
            for rows in range(len(df_tt.index)):
                for cols in range(1,len(df_tt.columns)-1):
                    if f"{sub_code.get()}(T)" in df_tt.iat[rows,cols]:
                        print(rows,cols)
                        codein_status = 1
                        r3.set(rows)
                        match cols:
                            case 1:                        
                                cb1.config(state='normal')
                            case 2:                        
                                cb2.config(state='normal')
                            case 3:                        
                                cb3.config(state='normal')
                            case 4:
                                cb4.config(state='normal')
                            case 5:
                                cb5.config(state='normal')
                            case 6:
                                cb6.config(state='normal') 
            if codein_status == 0:
                if df_tt.at[r3.get(),"slot_2"] == "FREE":
                    cb2.config(state='normal')
                if df_tt.at[r3.get(),"slot_3"] == "FREE":
                    cb3.config(state='normal')
                if df_tt.at[r3.get(),"slot_4"] == "FREE":
                    cb4.config(state='normal')
                if df_tt.at[r3.get(),"slot_5"] == "FREE":
                    cb5.config(state='normal')
                if df_tt.at[r3.get(),"slot_6"] == "FREE":
                    cb6.config(state='normal')
                #if df_tt.at[r3.get(),"slot_x"] == "FREE":
                #   cb7.config(state='normal')
            block_tutslots_withnickname()
        case "Practical":
            reset_lf3()
            nprows,npcols = np.where(df_tt == f"{sub_code.get()}(P)")
            print(nprows,npcols,f"{sub_code.get()}(P)")
            if nprows.size == 0:
                if df_tt.at[r3.get(),"slot_3"] == "FREE":
                    cb3.config(state='normal')
                if df_tt.at[r3.get(),"slot_5"] == "FREE":
                    cb5.config(state='normal')             
            else:
                r3.set(nprows[0])
                match npcols[0]:
                    case 3:                        
                        cb3.config(state='normal')
                    case 5:
                        cb5.config(state='normal')                            
            block_labslots_withnickname()
    verify_ok()
    verify_button.config(bg="white",fg="black")
def refresh_weekslots():
    global ro_co_lst,df_tt
    ro_co_lst = [sr0.get(),sr1.get(),sr2.get(),sr3.get(),sr4.get(),sr5.get(),sr6.get()]
    if 1 not in ro_co_lst:
        text_box2.insert('1.0',f"!!WARNING!! Select weekday and one from available slot before REFRESH...................")
        refresh_button.config(bg="Red",fg="White")
        return
    if sr2.get() == 1 and ltp_code.get() == "Practical":
        sr3.set(1)
        sr4.set(0)
    elif sr4.get() == 1 and ltp_code.get() == "Practical":
        sr3.set(0)
        sr5.set(1)
        sr6.set(1)
    refresh_button.config(bg="yellow",fg="black")
    verify_button.config(bg="Blue",fg="white")
    update_button.config(bg="white",fg="black")
    text_box2.delete('1.0','end')
    text_box2.insert('1.0',f"Confirm your choice {ltp_code.get()} : for the subject {sub_code.get()} for {semester_code.get()} in {assign_dept_code.get()} .... ")
def verify_ok():
    update_button.config(bg="Blue",fg="white")
    verify_button.config(bg="white",fg="black")
    refresh_button.config(bg="white",fg="black")
    text_box2.delete('1.0','end')
    text_box2.insert('1.0',f"Confirm and SAVE to Time Table")
    cancel_button.config(text="CANCEL",bg="yellow",fg="black")
    disable_lf1_lf2()
def update_tt():
    global faculty_name,df_sel,df_curi_active
    global ro_co_lst,df_tt
    activate_lf1_lf2()
    update_button.config(bg="white",fg="black")
    cancel_button.config(text="Confirm CANCEL",bg="white",fg="black")
    print(df_sel)
    match ltp_code.get():
        case "Lecture":
            df_curi_lec = df_curi_active[df_curi_active["L"] != 0]
            lec_class_hr = df_curi_lec.L.tolist()[df_curi_lec.Code.tolist().index(sub_code.get())]
            df_sel_lec = df_sel[["nick_name","deptL_class","semL","L_code","L_class","L_hr"]].copy()
            if faculty_name in df_sel_lec.nick_name.tolist():
                index_row = df_sel_lec.index[df_sel_lec['nick_name'] == faculty_name].tolist()[0]
                df_sel_mylec = df_sel_lec[df_sel_lec["nick_name"]==faculty_name]
                if df_sel_mylec.L_code.any():
                    code_lst = df_sel_mylec.at[df_sel_mylec.index.tolist()[0],"L_code"].split(",")
                    if sub_code.get() in code_lst:
                        if len(code_lst)==1:
                            #code_lst_selected = code_lst[0]
                            #class_lst_selected = df_sel_mylec.at[df_sel_mylec.index.tolist()[0],"L_class"]
                            hr_lst = df_sel_mylec.at[df_sel_mylec.index.tolist()[0],"L_hr"]
                            hr_lst += 1
                        else:               
                            hr_lst = df_sel_mylec.at[df_sel_mylec.index.tolist()[0],"L_hr"].split(",")
                            for j in range(len(code_lst)):
                                if code_lst[j]==sub_code.get():
                                    hr_lst[j]=int(float(hr_lst[j])) + 1
                        df_sel.loc[index_row,"L_hr"] = hr_lst if len(code_lst)==1 else ",".join(str(x) for x in hr_lst)
                    else:
                        df_sel.loc[index_row,"deptL_class"] = f"{df_sel_lec.at[index_row,"deptL_class"]},{assign_dept_code.get()}"
                        df_sel.loc[index_row,"semL"] = f"{df_sel_lec.at[index_row,"semL"]},{semester_code.get()}"
                        df_sel.loc[index_row,"L_code"] = f"{df_sel_lec.at[index_row,"L_code"]},{sub_code.get()}"
                        df_sel.loc[index_row,"L_class"] = f"{df_sel_lec.at[index_row,"L_class"]},{lec_class_hr}"
                        df_sel.loc[index_row,"L_hr"] = f"{df_sel_lec.at[index_row,"L_hr"]},{1}"         
                else:
                    df_sel.loc[index_row,"deptL_class"] = assign_dept_code.get()
                    df_sel.loc[index_row,"semL"] = semester_code.get()
                    df_sel.loc[index_row,"L_code"] = sub_code.get()
                    df_sel.loc[index_row,"L_class"] = lec_class_hr
                    df_sel.loc[index_row,"L_hr"] = f"{1}"                                 
            else:
                new_record = pd.DataFrame([{'nick_name':faculty_name,'emp_code':dept_emp_code.get(),'dept_origin':dept_code.get(),
                    'deptL_class':assign_dept_code.get(),'semL':semester_code.get(),'L_code':sub_code.get(),'L_class':lec_class_hr,"L_hr":1}])
                df_sel = pd.concat([df_sel,new_record],ignore_index=True)
            with pd.ExcelWriter(f"faculty_assignment_{odd_even_code.get()}.xlsx",engine="openpyxl",mode='a',if_sheet_exists='replace') as writer:
                df_sel.to_excel(writer,sheet_name=dept_code.get(),index=False)
            #df_sel.to_excel(f"faculty_assignment_{odd_even_code.get()}.xlsx",dept_code.get(),index=False,engine="openpyxl")
            df_tt = pd.read_excel(f"timeTable_{assign_dept_code.get()}.xlsx",semester_code.get(),engine="openpyxl")
            df_tt.iloc[r3.get(),ro_co_lst.index(1)+1] = f"{faculty_name},{dept_code.get()},{sub_code.get()},(L)"
            with pd.ExcelWriter(f"timeTable_{assign_dept_code.get()}.xlsx",engine="openpyxl",mode='a',if_sheet_exists='replace') as writer:
                df_tt.to_excel(writer,sheet_name=semester_code.get(),index=False)
            #df_tt.to_excel(f"timeTable_{assign_dept_code.get()}.xlsx",semester_code.get(),index=False,engine="openpyxl")
        case "Tutorial":
            df_sel_tut = df_sel[["nick_name","deptT_class","semT","T_code","T_hr"]].copy()
            if faculty_name in list(df_sel_tut.nick_name):
                df_sel_mytut = df_sel_tut[df_sel_tut["nick_name"]==faculty_name]
                index_row = df_sel_tut.nick_name.tolist().index(faculty_name)
                if df_sel_mytut.T_code.any():
                    df_sel.loc[index_row,"deptT_class"] = f"{df_sel_tut.at[index_row,"deptT_class"]},{assign_dept_code.get()}"
                    df_sel.loc[index_row,"semT"] = f"{df_sel_tut.at[index_row,"semT"]},{semester_code.get()}"
                    df_sel.loc[index_row,"T_code"] = f"{df_sel_tut.at[index_row,"T_code"]},{sub_code.get()}"
                    df_sel.loc[index_row,"T_hr"] = f"{df_sel_tut.at[index_row,"T_hr"]},{1}"
                else:
                    df_sel.loc[index_row,"deptT_class"] = f"{assign_dept_code.get()}"
                    df_sel.loc[index_row,"semT"] = f"{semester_code.get()}"
                    df_sel.loc[index_row,"T_code"] = f"{sub_code.get()}"
                    df_sel.loc[index_row,"T_hr"] = f"{1}"           
            else:        
                new_record = pd.DataFrame([{'nick_name':faculty_name,'emp_code':dept_emp_code.get(),'dept_origin':dept_code.get(),
                    'deptT_class':assign_dept_code.get(),'semT':semester_code.get(),'T_code':sub_code.get(),"T_hr":1}])
                df_sel = pd.concat([df_sel,new_record],ignore_index=True)
            with pd.ExcelWriter(f"faculty_assignment_{odd_even_code.get()}.xlsx",engine="openpyxl",mode='a',if_sheet_exists='replace') as writer:
                df_sel.to_excel(writer,sheet_name=dept_code.get(),index=False)         
            df_tt = pd.read_excel(f"timeTable_{assign_dept_code.get()}.xlsx",semester_code.get(),engine="openpyxl")
            if df_tt.iat[r3.get(),ro_co_lst.index(1)+1] == 'FREE':
                names_plusT = f"{sub_code.get()}(T),{faculty_name}"
            else:
                names_plusT = df_tt.iat[r3.get(),ro_co_lst.index(1)+1] + f",{faculty_name}"
            df_tt.iloc[r3.get(),ro_co_lst.index(1)+1] = names_plusT
            with pd.ExcelWriter(f"timeTable_{assign_dept_code.get()}.xlsx",engine="openpyxl",mode='a',if_sheet_exists='replace') as writer:
                df_tt.to_excel(writer,sheet_name=semester_code.get(),index=False)
        case "Practical":
            df_sel_lab = df_sel[["nick_name","deptP_class","semP","P_code","P_hr"]].copy()
            if faculty_name in list(df_sel_lab.nick_name):
                df_sel_mylab = df_sel_lab[df_sel_lab["nick_name"]==faculty_name]
                index_row = df_sel_lab.nick_name.tolist().index(faculty_name)
                if df_sel_mylab.P_code.any():
                    df_sel.loc[index_row,"deptP_class"] = f"{df_sel_lab.at[index_row,"deptP_class"]},{assign_dept_code.get()}"
                    df_sel.loc[index_row,"semP"] = f"{df_sel_lab.at[index_row,"semP"]},{semester_code.get()}"
                    df_sel.loc[index_row,"P_code"] = f"{df_sel_lab.at[index_row,"P_code"]},{sub_code.get()}"
                    df_sel.loc[index_row,"P_hr"] = f"{df_sel_lab.at[index_row,"P_hr"]},{str(1)}"
                else:
                    df_sel.loc[index_row,"deptP_class"] = assign_dept_code.get()
                    df_sel.loc[index_row,"semP"] = semester_code.get()
                    df_sel.loc[index_row,"P_code"] = sub_code.get()
                    df_sel.loc[index_row,"P_hr"] = str(1)             
            else:
                new_record = pd.DataFrame([{'nick_name':faculty_name,'emp_code':dept_emp_code.get(),'dept_origin':dept_code.get(),
                    'deptP_class':assign_dept_code.get(),'semP':semester_code.get(),'P_code':sub_code.get(),"P_hr":1}])
                df_sel = pd.concat([df_sel,new_record],ignore_index=True) 
            with pd.ExcelWriter(f"faculty_assignment_{odd_even_code.get()}.xlsx",engine="openpyxl",mode='a',if_sheet_exists='replace') as writer:
                df_sel.to_excel(writer,sheet_name=dept_code.get(),index=False)
            df_tt = pd.read_excel(f"timeTable_{assign_dept_code.get()}.xlsx",semester_code.get(),engine="openpyxl")
            if df_tt.iat[r3.get(),ro_co_lst.index(1)+2] == 'FREE':
                names_plus = df_tt.iat[r3.get(),ro_co_lst.index(1)+2] = faculty_name
                df_tt.iloc[r3.get(),ro_co_lst.index(1)+1] = f"{sub_code.get()}(P)"
            else:
                names_plus = df_tt.iat[r3.get(),ro_co_lst.index(1)+2] + f",{faculty_name}"
            df_tt.iloc[r3.get(),ro_co_lst.index(1)+2] = names_plus
            with pd.ExcelWriter(f"timeTable_{assign_dept_code.get()}.xlsx",engine="openpyxl",mode='a',if_sheet_exists='replace') as writer:
                df_tt.to_excel(writer,sheet_name=semester_code.get(),index=False)
    activate_lf1_lf2()
    reset_lf1_lf2()
    reset_lf3()
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
def lf1_lf2_clear():
    dept_emp_code.set('')
    dept_emp_code['values']=()
    assign_dept_code.set('')
    odd_even_code.set('')
    semester_code.set('')
    ltp_code.set('')
    sub_code.set('')
    cancel_code.set('')
def disable_lf1_lf2():
    dept_emp_code.config(state="disabled")
    assign_dept_code.config(state="disabled")
    odd_even_code.config(state="disabled")
    semester_code.config(state="disabled")
    ltp_code.config(state="disabled")
    sub_code.config(state="disabled")
    action_code.config(state="disabled")
def activate_lf1_lf2():
    dept_emp_code.config(state="readonly")
    assign_dept_code.config(state="readonly")
    odd_even_code.config(state="readonly")
    semester_code.config(state="readonly")
    ltp_code.config(state="readonly")
    sub_code.config(state="readonly")
    action_code.config(state="readonly")
def reset_lf1_lf2():
    #dept_emp_code['values']=()
    #dept_emp_code.set('')
    assign_dept_code.config(values=(''))
    assign_dept_code.set('')
    #odd_even_code['values']=()
    #odd_even_code.set('')
    semester_code.config(values=(''))
    semester_code.set('')
    ltp_code.config(values=(''))
    ltp_code.set('')
    sub_code.config(values=(''))
    sub_code.set('')
    action_code.config(values=(''))
    action_code.set('') 
def reset_lf3():
    cb1.config(state='disabled')
    cb2.config(state='disabled')
    cb3.config(state='disabled')
    cb4.config(state='disabled')
    cb5.config(state='disabled')
    cb6.config(state='disabled')
    cb7.config(state='disabled')
    sr0.set(0)
    sr1.set(0)
    sr2.set(0)
    sr3.set(0)
    sr4.set(0)
    sr5.set(0)
    sr6.set(0)
def normalset_lf3():
    cb1.config(state='normal')
    cb2.config(state='normal')
    cb3.config(state='normal')
    cb4.config(state='normal')
    cb5.config(state='normal')
    cb6.config(state='normal')
    cb7.config(state='normal')
    sr0.set(0)
    sr1.set(0)
    sr2.set(0)
    sr3.set(0)
    sr4.set(0)
    sr5.set(0)
    sr6.set(0) 
def cancel_option_selection(event):
    lf1_lf2_clear()
    cancel_entry = cancel_code.get()
    if cancel_entry == "Clear Day & Slot":
        print("clear day and slot")
        clear_day_slot()
        text_box1.insert('1.0',"All the data entry under 1)Assigned for Dept./Topic 2)semester 3)Class Type 4)Subject Code will be reset for fresh entry.")
    elif cancel_entry == "Clear All data":
        print("clear all data")
        text_box1.insert('1.0',"All the data entry under 1)Assigned for Dept./Topic 2)semester 3)Class Type 4)Subject Code will be reset for fresh entry.")
    else:
        print("clear data from Time Table")
    pass
def common_for_cancel_options():
    pass
def confirm_cancel():
    update_button.config(bg="white",fg="black")
    cancel_button.config(text="Confirm CANCEL",bg="white",fg="black")
    activate_lf1_lf2()
    reset_lf1_lf2()
    reset_lf3()
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
global table_tt
table_tt=[{"week_day":" ","slot_1":" ","slot_2":" ","slot_3":" ",
    "slot_4":" ","slot_5":" ","slot_6":" ","slot_x":" "}]
global code_lst_lab
code_lst_lab = []
odd_even="odd"
day_slot={"week_slot":3,"time_slot0":0,"time_slot1":1,"time_slot2":2,"time_slot3":3,
    "time_slot4":4,"time_slot5":5,"time_slot6":6}
sr=IntVar()
#Storage file for manipulation
data_ref = [{'nick_name':'','emp_code':'','dept_origin':'','deptL_class':'','semL':'','L_code':'','L_class':'',"L_hr":'',
    'deptT_class':'','semT':'','T_code':'',"T_hr":'','deptP_class':'','semP':'','P_code':'',"P_hr":'',
    'deptR_class':'','semR':'','R_code':'',"R_hr":''}]
#Storage file on departments
dept_data = [{'emp_code':'','dept':'','grade':'','nick_name':'','pay_band':''}]
#Storage file on curiculam
curi_data = [{'Code':'','Subject':'','Select':'','Number':'','L':'','T':'','P':'','R':''}]
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
sub_lec_faculty = {}
sub_tut_faculty = {}
sub_lab_faculty = {}
sub_proj_faculty = {}
#lf1 entries
dept_options=StringVar()
dept_code=ttk.Combobox(lf1,textvariable=dept_options,state='raedonly')
dept_code.grid(row=1,column=0,padx=10,pady=2,sticky="nsew")
dept_code['values']=("CE","ME","EE")
dept_code.current()
dept_code.bind("<<ComboboxSelected>>",parent_dept_selection)
dept_emp_options=StringVar()
dept_emp_code=ttk.Combobox(lf1,textvariable=dept_emp_options,state='raedonly')
dept_emp_code.grid(row=1,column=1,padx=10,pady=2,sticky="nsew")
dept_emp_code['values']=()
dept_emp_code.current()
dept_emp_code.bind("<<ComboboxSelected>>",emp_code_selection)
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
text_box1=Text(lf2, width=60,height=3,fg="Blue",font=("Ariel",11))
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
refresh_button = Button(lf3,text="REFRESH",command=refresh_weekslots)
refresh_button.grid(row=0,column=6,padx=2,pady=2,sticky="nsew")
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