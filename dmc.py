#CODE FOR DATA CLEANING , FILE ORGANISING DATE AND FOLDER WISE
import datetime 
import calendar 
from datetime import date
import shutil
import os
import sqlite3
import time
import random
#path_dir="G:\EOL\EOL-S101"
try:
    dmc_process_log="DMC_Process_log/dmc_process_log.txt"
    f = open(dmc_process_log, "w")
    f.write("\n")
    f.close()
except IOError as e:
    print("IO ERROR"+str(e))
    errLog("err_type",str(e))
    

def errLog(err_type,err_data):
    try:
        log_time=datetime.datetime.now()
        log_date=log_time.strftime('%Y-%m-%d')
        dmc_error_log_file_name="DMC_Error_log/Error_log_dmc_protocol-"+str(log_date)+".log"
        f = open(dmc_error_log_file_name, "a+")
        f.write(str(log_time)+",Error_Type: "+err_type+ ",Error_Data:" +err_data+"\n")
        f.close()
        #print (str(log_date)+ "    "+str(log_time))
    except IOError as e:
        print("IO ERROR"+str(e))
        processLog("ERROR LOG IO ERROR"+str(e))


def processLog(process_data):
    try:
        f = open(dmc_process_log, "a+")
        f.write(str(process_data+"\n"))
        f.close()
    except IOError as e:
        print("IO ERROR"+str(e))
        errLog("err_type",str(e))
    



def backup_log(file_name,file_type,file_loc,file_date,file_time,eol_name,file_size):
    try:
        conn = sqlite3.connect('EOLDMCDATA.db')
        #
        q1="SELECT * FROM backup_info WHERE loc='"+file_loc+"'"
         #c=conn.cursor()
        rows=conn.execute(q1)
        result=rows.fetchone()
        if result:
            print("Already Exist..No Need to Update")
            processLog("File Location:"+file_loc+" Already Exist..No Need to Update")
         
        else:
            print("No Record Found!")
            processLog("File Location:"+file_loc+"No Record Found!")
            conn.execute("INSERT INTO backup_info(file_name,file_size,type,loc,gen_date,gen_time,eol_name) VALUES(?,?,?,?,?,?,?)",(file_name,file_size,file_type,file_loc,file_date,file_time,eol_name))
            #conn.execute("INSERT INTO backup_info(file_name,file_size,type,loc,gen_date,gen_time,eol_name) VALUES(?,?,?,?,?,?,?)",("Hello",1234,"PDF","D://","11-11-2011","11:11:00","EOL1"))
            conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        errLog("DATABASE ERROR: ",str(e))
        

m=""
def get_cur_date():
    today = date.today()
    # dd/mm/YY
    d1 = today.strftime("%m%d%Y")
    return d1
# GET DATE FOR SQLITE
def get_cur_date2():
    d2=date.today()
    return d2
#Get day from Curent Date
def findDay(date):
    
    born = datetime.datetime.strptime(date, '%y%m%d').weekday() 
    return (str(calendar.day_name[born][0:3]))

EOL_DIR=""
EOL_DIR_PATH=""
EOL_DIR_BKP_PATH=""
EOL_DIR_BKP_FILE_PATH=""
EOL_FILE_LIST=""

try:
    dir_list=""
    start_time = time.time()
    base_path="E:\eol machine data"
    dir_list=os.listdir(base_path)
    EOL_DIR=""
    EOL_DIR_PATH=""
    EOL_DIR_BKP_PATH=""
    EOL_DIR_BKP_FILE_PATH=""
    EOL_FILE_LIST=""
except ConnectionError as e:
        print(str(e))
        errLog("Network Error: ", str(e))
        pass
except Exception as e:
        print(e)
        errLog("Error: ", str(e))
        
        pass    
except IOError as e:
        print(str(e))
        errLog("IO Error: ", str(e))
        pass
        
def scan_path():
    global EOL_DIR
    global EOL_DIR_PATH
    global EOL_DIR_BKP_PATH
    global EOL_DIR_BKP_FILE_PATH
    global EOL_FILE_LIST
    try:
        for n in dir_list:
            if (n[0:3]=="EOL"):
                EOL_DIR+=n+","
        EOL_DIR=EOL_DIR.split(",")
        EOL_DIR.remove('')
        #print(EOL_DIR) 
        print("TOTAL EOL LIST ",len(EOL_DIR))
        processLog("TOTAL EOL LIST "+ str(len(EOL_DIR)))
        n=""
        for n in EOL_DIR:
            print("Base DIR:"+base_path)
            processLog("Base DIR"+ str(base_path))
            EOL_DIR_PATH += str(base_path+"/"+n+",")
            print("EOL DIR:"+EOL_DIR_PATH)
            processLog("EOL DIR LIST"+ str(EOL_DIR_PATH))
        EOL_DIR_PATH = EOL_DIR_PATH.split(",")
        EOL_DIR_PATH.remove('')
    except ConnectionError as e:
        print(str(e))
        errLog("Network Error: ", str(e))
        pass
    except Exception as e:
        print(e)   
        errLog("ERROR! :: ", str(e))
        pass 
    except IOError as e:
        print(str(e))
        errLog("IO Error: ", str(e))
        pass


        
#print(findDay(get_cur_date()))
#print((bkp_files_array[0]))
#Renaming The Files Folder Wise

def org_docs(path):
    empty_dir_count=0
    bkp_files_path=os.listdir(path)
    m=""
    fold=0
    other_file=0
    xls_file=0
    for n in bkp_files_path:
        new_file=""
        new_path=""
        fold+=1
        f_date=n[(len(n)-10):len(n)]
        f_date=f_date.split(".")
        #f1_date=str(f_date[2][2:]+f_date[0]+f_date[1])
        #print ("f1_date=", f1_date)
        print(f_date)
        processLog("FILES ON DATE DATE : "+ str(f_date))
        #FILE LIST AND PATH                                                                                                             
        eol_file_dir=str(path+"/"+n)
        bkp_files_array=os.listdir(eol_file_dir)
        if(len(bkp_files_array)==0):
            try:
                os.rmdir(eol_file_dir)
            except Exception as e:
                print(e)
                errLog("EOL BACKUP EMPTY DIR REMOVE ERROR: ",str(e))
            empty_dir_count+=1
            print("Empty Folder Deleted!")
            processLog("Log: Empty Folder Got Deleted")
        for m in bkp_files_array:
            print("M:=",m)
            processLog("File Name: "+str(m))
            f_type=m[(len(m)-3):len(m)]
            print(f_type)
            processLog("File Type: "+str(f_type))
            #file_loc=str(eol_file_dir+"/"+m)
            #print("File_Name:"+str(eol_file_dir)+"/"+m)
            if (f_type!="xls" and f_type!="txt" and f_type!="lsx"):
                print("not xls")
                processLog("File Type: "+str("NOT XLS/XLSX/TXT FILE!"))
                other_file+=1
                math_date=""
                high=0
                low=0
                file_type="OTHER"
            elif (f_type=="xls"):
                #print("XLS:",xls_file)
                xls_file+=1
                low=len(m)-15
                high=len(m)
                math_date=m[low:(low+6)]
                file_type="XLS"
                processLog("File Type: "+str("XLS  FILE!"))
            elif (f_type=="lsx"):
                #print("XLS:",xls_file)
                xls_file+=1
                low=len(m)-16
                high=len(m)
                math_date=m[low:(low+6)]
                file_type="XLSX"
                processLog("File Type: "+str("XLSX FILE!"))
            #print("Math_date",math_date)
            if(str(math_date).isnumeric()):
                new_file=str(path+"/Evening "+findDay(math_date)+" "+m[(low+2):(low+4)]+"."+m[(low+4):(low+6)]+".20"+m[low:(low+2)]+"/"+m)
                new_path=str(path+"/Evening "+findDay(math_date)+" "+m[(low+2):(low+4)]+"."+m[(low+4):(low+6)]+".20"+m[low:(low+2)])
            else:
                new_file=str(path+"/Evening "+"OTHER FILES"+"/"+m)
                new_path=str(path+"/Evening "+"OTHER FILES")
            #os.mkdir(new_path)
            print(new_path)
            processLog("File New DIR Path "+str(new_path))
            eol_name=path.split("/")
            eol_name=eol_name[1]
            print("Path:"+str(eol_name))
            processLog("EOL Name: "+str(eol_name))
            new_file_name=str(path+"/"+n+"/"+m[low:high])
            old_file_name=str(path+"/"+n+"/"+m)
            file_stat=os.stat(old_file_name)
            st_mtime=file_stat.st_mtime
            file_size=file_stat.st_size
            file_loc=new_file
            file_name=m
            file_date=datetime.datetime.fromtimestamp(st_mtime).strftime('%Y-%m-%d')    
            file_time=datetime.datetime.fromtimestamp(st_mtime).strftime('%H:%M')    
            print("Last Modified Time : ",file_date,"Time:",file_time )
            processLog("Last Modified Date and Time: "+str(file_date + file_time))
            print("NEW FILE NAME:"+new_file_name)
            processLog("NEW FILE NAME: "+str(new_file_name))
            print("OLD FILE NAME:"+old_file_name)
            processLog("OLD FILE NAME: "+str(old_file_name))
            print("NEW FILE PTAH:"+new_path)
            print("NEW MOVE FILE NAME:"+new_file)
            processLog("New Move File Name: "+str(new_file))
            #ADDING FILE INFO DATA INTO SQLITE DATABASE
            backup_log(file_name,file_type,file_loc,file_date,file_time,eol_name,file_size)
            if(new_file==old_file_name):
                print("NO NEED TO MOVE. IT IS IN RIGHT FOLDER!")
                processLog("NO NEED TO MOVE. IT IS IN RIGHT FOLDER!")
            else:
                if(os.path.isdir(new_path)):
                    print("Path Exist")
                    processLog("Path Exist")
                    if(os.path.isfile(new_file)):
                        print("FILE ALSO EXIST!")
                        processLog("FILE ALSO EXIST!")
                        #checking File Size , if new file size is greater than old file then replace old file with new file else remove new file.
                        file_stat_new = os.stat(old_file_name)
                        file_stat_old = os.stat(new_file)
                        old_file_size=file_stat_old.st_size
                        new_file_size=file_stat_new.st_size
                        print("OLD FILE SIZE: "+str(old_file_size))
                        print("NEW FILE SIZE: "+str(new_file_size))
                        processLog("OLD FILE SIZE:"+str(old_file_size)+", NEW FILE SIZE: "+str(new_file_size)+"\n")
                        if(old_file_size <= new_file_size):
                            try:
                                shutil.move(old_file_name,new_file)
                            except Exception as e:
                                print(e)
                                errLog("EOL BACKUP FILE REMOVE ERROR: ",str(e))
                        else:
                            try:
                                os.remove(old_file_name)
                            except Exception as e:
                                print(e)
                                errLog("EOL BACKUP FILE REMOVE ERROR: ",str(e))
                    else:
                        try:
                            shutil.move(old_file_name,new_file)
                        except Exception as e:
                            print(e)
                            errLog("EOL BACKUP  FILE MOVE ERROR: ",str(e))
                else:
                    print("Not Exist")
                    processLog("FILE NOT EXIST!")
                    os.mkdir(new_path)
                    if(os.path.isfile(new_file)):
                        print("FILE ALSO EXIST!")
                        processLog("FILE ALSO EXIST!")
                        try:
                            os.remove(old_file_name)
                        except Exception as e:
                            print(e)
                            errLog("EOL BACKUP DUPLICATE FILE REMOVAL ERROR: ",str(e))
                    else:
                        try:
                            shutil.move(old_file_name,new_file)
                            processLog("FILE REPLACED")
                            #shutil.copyfile(old_file_name,new_file)
                            #shutil.move(old_file_name,new_path)
                            #os.rename(old_file_name, new_file_name)
                        except Exception as e:
                            print(e)
                            errLog("EOL BACKUP FILE REPLACEMENT ERROR: ",str(e))
    print("TOTAL NO OF FOLDERS:")
    print(fold)   
    processLog("TOTAL NO. OF FOLDERS IN THIS EOL: "+str(fold))
    print("TOTAL NO OF OTHER FILES:")            
    print(other_file)
    processLog("TOTAL NO. OF OTHER FILES IN THIS EOL: "+str(other_file))
    print("Total No. of XLS Files:")
    print(xls_file)
    processLog("TOTAL NO. OF EXCEL FILES IN THIS EOL: "+str(xls_file))
    print("Total No. DELETED EMPTY FOLDERS:")
    print(empty_dir_count)
    processLog("TOTAL NO. OF DELETED FOLDERS IN THIS EOL: "+str(empty_dir_count))
    try:
        conn = sqlite3.connect('EOLDMCDATA.db')
        conn.execute("INSERT INTO EOLBACKUPDETAILS(DIRNAME,NDIR,NEF,NOF,DELFOLDER,DATE) VALUES(?,?,?,?,?,?)",(path,fold,xls_file,other_file,empty_dir_count,str(get_cur_date2())))
        conn.commit()
        conn.close()
        processLog("EOL Process DONE! For this EOL and  UPDATED In BACKUP INFO")
    except Exception as e:
        print(e)
        errLog("EOL BACKUP  DATABASE ERROR: ",str(e))
    
   

''' 
try:
    scan_path()
    path_dir=""
    for path_dir in EOL_DIR_PATH:
        org_docs(str(path_dir))
        time.sleep(1)
except ConnectionError as e:
    print(str(e))
except Exception as e:
    print(e)    
except IOError as e:
    print(str(e))
    
  '''
try:
    #INSERT TASK DETAILS IN PROCESS INFO DB
    d = datetime.datetime.now()
    db_start_date=str(d.year)+"-"+str(d.month)+"-"+str(d.day)
    db_start_time=str(d.hour)+":"+str(d.minute)+":"+str(d.second)
    conn = sqlite3.connect('process_info.db')
    conn.execute("INSERT INTO process_log(start_date,start_time,task_type) VALUES(?,?,?)",(str(db_start_date),str(db_start_time),"DMC"))
    conn.commit()
    conn.close()
    processLog("TASK DETAILS ADDED SUCCESSFULLY IN PROCESS DB! THANK YOU")
except Exception as e:
    print(e)
    errLog("EOL BACKUP  DATABASE ERROR: ",str(e))
#SCAN ALL DIR AND PATH
try:
    scan_path()
except Exception as e:
    print(e)
    errLog("EOL BACKUP  DATABASE ERROR: ",str(e))
#START DMC PROCESS
processLog("\n ------------------------DMC PROCESS STARTED AT: "+str(datetime.date)+str(start_time)+"---------------------------------------- \n")
for path_dir in EOL_DIR_PATH:
    try:
        org_docs(path_dir)
    except Exception as e:
        print(e)
        errLog("DMC FUNCTION CALL ERROR: ",str(e))
print("--- %s seconds ---" % (time.time() - start_time))
processLog("TOTAL TIME TAKEN FOR ALL PROCESS: "+str("--- %s seconds ---" % (time.time() - start_time)))
processLog("\n ------------------------DMC PROCESS COMPLETED AT: "+str(datetime.date)+str(start_time)+"---------------------------------------- \n")
try:
    #UPDATE TASK DETAILS IN PROCESS INFO DB
    d = datetime.datetime.now() 
    db_end_date=str(d.year)+"-"+str(d.month)+"-"+str(d.day)
    db_end_time=str(d.hour)+":"+str(d.minute)+":"+str(d.second)
    end_time=time.time() - start_time
    conn = sqlite3.connect('process_info.db')
    #print("UPDATE process_log SET end_ date='"+str(db_end_date)+"',end_time="+str(db_end_date)+",time_taken="+str(int(end_time))+" WHERE start_date="+str(db_start_date)+" AND start_time="+str(db_start_time)+" AND task_type="+"DMC-LITE")
    conn.execute("UPDATE process_log SET end_date='"+str(db_end_date)+"',end_time='"+str(db_end_time)+"',time_taken="+str(int(end_time))+" WHERE start_date='"+str(db_start_date)+"' AND start_time='"+str(db_start_time)+"' AND task_type="+"'DMC'")
    conn.commit()
    conn.close()
    processLog("TASK DETAILS UPDATED SUCCESSFULLY IN PROCESS DB! THANK YOU")
except Exception as e:
    print(e)
    errLog("EOL BACKUP  DATABASE ERROR: ",str(e))
print("Thank You!")
    