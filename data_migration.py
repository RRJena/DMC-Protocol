# PROGRAM TO MIGRATE DATA FROM EXCEL TO POSTGRE SQL SERVER
import calendar
import datetime
from datetime import date,timedelta
import shutil
import os
import sqlite3
import time
import random
import numpy as np
import pandas as pd
import datetime
import psycopg2
#Timer Start NOW & DATE OF DATA MIGRATION
start_time = time.time()
today_date=datetime.date.today()
prev_date=today_date-datetime.timedelta(days=7)
#VARIABLES FOR EXCEl INDEX
start_index=0
total_column=0
total_row=0

#Function to LOG Process Details in LOG FILE
#MAKE LOG FILE EMPTY BEFORE PROCESSING
try:
    proces_file_log="DataMigration_Process_log/Data Migration_Check_process_log-"+str(today_date)+".txt"
    f = open(proces_file_log, "w")
    f.write("\n")
    f.close()
except IOError as e:
    print("IO ERROR"+str(e))
    errLog("err_type",str(e))

def processLog(process_data):
    try:
        f = open(proces_file_log, "a+")
        f.write(str(process_data+"\n"))
        f.close()
    except IOError as e:
        print("IO ERROR"+str(e))
        errLog("err_type",str(e))

#Function to LOG Error in Processing.
def errLog(err_type,err_data):
    try:
        log_time=datetime.datetime.now()
        log_date=log_time.strftime('%Y-%m-%d')
        err_file_name="DataMigration_Error_log/Error_log_data_migration-"+str(log_date)+".log"
        f = open(err_file_name, "a+")
        f.write(str(log_time)+",Error_Type: "+err_type+ ",Error_Data:" +err_data+"\n")
        f.close()
        #print (str(log_date)+ "    "+str(log_time))
    except IOError as e:
        print("IO ERROR"+str(e))
        processLog("ERROR LOG IO ERROR"+str(e))
#SELECT ALL EOL MODELS FROM DATABASE 
def migrate_status(data_mig_status,eol_loc):
    try:
        conn = sqlite3.connect('EOLDMCDATA.db')
        #q1="SELECT * FROM backup_info WHERE data_mig_status=null"
        q1="UPDATE backup_info SET data_mig_status="+data_mog_status+" WHERE loc='"+eol_loc+"'"
         #c=conn.cursor()
        result=conn.execute(q1)
        if result:
            print("File Location:"+file_loc+" : DATA MIG STATUS UPDATED TO :"+str(data_mig_status))
            processLog("File Location:"+file_loc+" : DATA MIG STATUS UPDATED TO :"+str(data_mig_status))
        else:
            print("Update Failed!")
            processLog("File Location:"+file_loc+" : DATA MIG STATUS FAILED!")
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        conn.close()
        errLog("DATABASE ERROR: ",str(e))

def data_migrate(start_date, end_date):
        try:
            conn = sqlite3.connect('EOLDMCDATA.db')
            q1="SELECT * FROM backup_info WHERE data_mig_status IS NULL AND empty_stat=0 AND gen_date BETWEEN '"+start_date+"' AND '"+end_date+"'"
            #q1="UPDATE backup_info SET data_mig_status="+data_mog_status+" WHERE loc='"+eol_loc+"'"
            #c=conn.cursor()
            result=conn.execute(q1)
            rows=conn.execute(q1)
            #Collecting All DATA AND STORE IN RESULT
            result=rows.fetchall()
            i=1
            #print(result)
            conn.close()
            count=0
            for row in result:
                file_loc=row[4]
                eol=row[7]
                empty_stat=row[8]
                cdate=row[5]
                data_mig_status=None
                file_size=row[2]
                if(eol=="EOL-YRA3"):
                    start_index=4
                    sheet_name="Data"
                    data=pd.read_excel(file_loc, sheet_name)
                    total_column=len(data.columns)
                    data_end=len(data)
                    total_cycle=data_end-start_index
                    total_row=data_end-1
                    row_index=4
                    while (row_index <= total_row):
                        try:
                            d1=data.iloc[row_index]
                            connection = psycopg2.connect(user="postgres",
                                      password="koki@123",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="EOL")
                            cursor = connection.cursor()
                            d1[35]=str(d1[35]).strip()
                            d1[36]=str(d1[36]).strip()
                            d1[37]=str(d1[37]).strip()
                            eol_time=d1[1].strftime("%H:%M:%S")
                            sql_select_query='SELECT * FROM public.yra3 WHERE eol_serial='+"'"+str(d1[0])+"' AND production_date="+"'"+str(cdate)+"' AND eol_check_time="+"'"+str(eol_time)+"';"
                            sql_insert_query = 'INSERT INTO public.yra3(eol_serial, production_date, eol_check_time, "M00", "M01", "M02", "M03", "M04", "M05", "M06", "M07", "M08", "M09", "M10", "M11", "M12", "M13", "M14", "M15", "M16", "M17", "M18", "M19", "M20", "M21", "M22", "M23", "M24", "M25", "M26", "M27", "M28", "M29", "M30", "M31", "M32", result, dmc, pinmark_no, "P1", "P2")  VALUES('+str(d1[0])+",'"+cdate+"','"+eol_time+"','"+str(d1[2])+"',"+str(d1[3])+","+str(d1[4])+","+str(d1[5])+","+str(d1[6])+","+str(d1[7])+","+str(d1[8])+","+str(d1[9])+","+str(d1[10])+","+str(d1[11])+","+str(d1[12])+","+str(d1[13])+","+str(d1[14])+","+str(d1[15])+","+str(d1[16])+","+str(d1[17])+","+str(d1[18])+","+str(d1[19])+","+str(d1[20])+","+str(d1[21])+","+str(d1[22])+","+str(d1[23])+","+str(d1[24])+","+str(d1[25])+","+str(d1[26])+","+str(d1[27])+","+str(d1[28])+","+str(d1[29])+","+str(d1[30])+","+str(d1[31])+","+str(d1[32])+","+str(d1[33])+","+str(d1[34])+",'"+str(d1[35])+"','"+str(d1[36])+"','"+str(d1[37])+"',"+str(d1[38])+","+str(d1[39])+");"
                            # executemany() to insert multiple rows rows
                            cursor.execute(sql_select_query)
                            if(cursor.rowcount>=1):
                                print("Already Data Exist in Database. Can't Insert Duplicate!")
                            else:
                                result = cursor.execute(sql_insert_query)
                                connection.commit()
                                print(cursor.rowcount, "Record inserted successfully into mobile table")
                        except (Exception, psycopg2.Error) as error:
                            print("Failed inserting record into mobile table {}".format(error))
                            errLog("PGSQL ERROR!:","Failed inserting record into mobile table {}".format(error))
                        finally:
                            # closing database connection.
                            if (connection):
                                cursor.close()
                                connection.close()
                                print("PostgreSQL connection is closed")
                        print(file_loc)
                        print("Check Date: "+cdate)
                        print("Total Cycle:"+str(total_cycle))
                        print("Total Colum:"+str(total_column))
                        row_index += 1
                    processLog(file_loc)
                    processLog("Check Date: "+cdate)
                    processLog("Total Cycle:"+str(total_cycle))
                    processLog("Total Colum:"+str(total_column))
                    count+=1
                    print("Total File Count: "+str(count))
                    processLog("Total File Count: "+str(count))
                elif(eol=="EOL-YRA2"):
                    start_index=7
                    sheet_name="Data"
                    data=pd.read_excel(file_loc, sheet_name)
                    total_column=len(data.columns)
                    data_end=len(data)
                    total_cycle=data_end-start_index
                    total_row=data_end-1
                    row_index=7
                    while (row_index <= total_row):
                        try:
                            d1=data.iloc[row_index]
                            connection = psycopg2.connect(user="postgres",
                                      password="koki@123",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="EOL")
                            cursor = connection.cursor()
                            d1[35]=str(d1[35]).strip()
                            d1[36]=str(d1[36]).strip()
                            d1[37]=str(d1[37]).strip()
                            eol_time=d1[1].strftime("%H:%M:%S")
                            sql_select_query='SELECT * FROM public.yra2 WHERE eol_serial='+"'"+str(d1[0])+"' AND production_date="+"'"+str(cdate)+"' AND eol_check_time="+"'"+str(eol_time)+"';"
                            sql_insert_query = 'INSERT INTO public.yra2(eol_serial, production_date, eol_check_time, "M00", "M01", "M02", "M03", "M04", "M05", "M06", "M07", "M08", "M09", "M10", "M11", "M12", "M13", "M14", "M15", "M16", "M17", "M18", "M19", "M20", "M21", "M22", "M23", "M24", "M25", "M26", "M27", "M28", "M29", "M30", "M31", "M32", result, dmc, pinmark_no, "P1", "P2")  VALUES('+str(d1[0])+",'"+cdate+"','"+eol_time+"','"+str(d1[2])+"',"+str(d1[3])+","+str(d1[4])+","+str(d1[5])+","+str(d1[6])+","+str(d1[7])+","+str(d1[8])+","+str(d1[9])+","+str(d1[10])+","+str(d1[11])+","+str(d1[12])+","+str(d1[13])+","+str(d1[14])+","+str(d1[15])+","+str(d1[16])+","+str(d1[17])+","+str(d1[18])+","+str(d1[19])+","+str(d1[20])+","+str(d1[21])+","+str(d1[22])+","+str(d1[23])+","+str(d1[24])+","+str(d1[25])+","+str(d1[26])+","+str(d1[27])+","+str(d1[28])+","+str(d1[29])+","+str(d1[30])+","+str(d1[31])+","+str(d1[32])+","+str(d1[33])+","+str(d1[34])+",'"+str(d1[35])+"','"+str(d1[36])+"','"+str(d1[37])+"',"+str(0)+","+str(0)+");"
                            # executemany() to insert multiple rows rows
                            cursor.execute(sql_select_query)
                            if(cursor.rowcount>=1):
                                print("Already Data Exist in Database. Can't Insert Duplicate!")
                            else:
                                result = cursor.execute(sql_insert_query)
                                connection.commit()
                                print(cursor.rowcount, "Record inserted successfully into mobile table")
                        except (Exception, psycopg2.Error) as error:
                            print("Failed inserting record into mobile table {}".format(error))
                            errLog("PGSQL ERROR!:","Failed inserting record into mobile table {}".format(error))
                        finally:
                            # closing database connection.
                            if (connection):
                                cursor.close()
                                connection.close()
                                print("PostgreSQL connection is closed")
                        print(file_loc)
                        print("Check Date: "+cdate)
                        print("Total Cycle:"+str(total_cycle))
                        print("Total Colum:"+str(total_column))
                        row_index += 1
                    processLog(file_loc)
                    processLog("Check Date: "+cdate)
                    processLog("Total Cycle:"+str(total_cycle))
                    processLog("Total Colum:"+str(total_column))
                    count+=1
                    print("Total File Count: "+str(count))
                    processLog("Total File Count: "+str(count))
                elif(eol=="EOL-YRA1"):
                    start_index=4
                    sheet_name="Data"
                    data=pd.read_excel(file_loc, sheet_name)
                    total_column=len(data.columns)
                    data_end=len(data)
                    total_cycle=data_end-start_index
                    total_row=data_end-1
                    row_index=4
                    while (row_index <= total_row):
                        try:
                            d1=data.iloc[row_index]
                            connection = psycopg2.connect(user="postgres",
                                      password="koki@123",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="EOL")
                            cursor = connection.cursor()
                            d1[33]=str(d1[33]).strip()
                            d1[34]=str(d1[34]).strip()
                            d1[35]=str(d1[35]).strip()
                            d1[36]=str(d1[36]).strip()
                            d1[37]=str(d1[37]).strip()
                            d1[38]=str(d1[38]).strip()
                            eol_time=d1[1].strftime("%H:%M:%S")
                            sql_select_query='SELECT * FROM public.yra1 WHERE eol_serial='+"'"+str(d1[0])+"' AND production_date="+"'"+str(cdate)+"' AND eol_check_time="+"'"+str(eol_time)+"';"
                            sql_insert_query = 'INSERT INTO public.yra1(eol_serial, production_date, eol_check_time, "M00", "M01", "M02", "M03", "M04", "M05", "M06", "M07", "M08", "M09", "M10", "M11", "M12", "M13", "M14", "M15", "M16", "M17", "M18", "M19", "M20", "M21", "M22", "M23", "M24", "M25", "M26", "M27", "M28", "M29", "M30", result,type,dmc, dmc_1, pinmark_no,dmc_readable, "P1", "P2")  VALUES('+str(d1[0])+",'"+cdate+"','"+eol_time+"','"+str(d1[2])+"',"+str(d1[3])+","+str(d1[4])+","+str(d1[5])+","+str(d1[6])+","+str(d1[7])+","+str(d1[8])+","+str(d1[9])+","+str(d1[10])+","+str(d1[11])+","+str(d1[12])+","+str(d1[13])+","+str(d1[14])+","+str(d1[15])+","+str(d1[16])+","+str(d1[17])+","+str(d1[18])+","+str(d1[19])+","+str(d1[20])+","+str(d1[21])+","+str(d1[22])+","+str(d1[23])+","+str(d1[24])+","+str(d1[25])+","+str(d1[26])+","+str(d1[27])+","+str(d1[28])+","+str(d1[29])+","+str(d1[30])+","+str(d1[31])+","+str(d1[32])+",'"+str(d1[33])+"','"+str(d1[34])+"','"+str(d1[36])+"','"+str(d1[37])+"','"+str(d1[35])+"','"+str(d1[38])+"',"+str(0)+","+str(0)+");"
                            # executemany() to insert multiple rows rows
                            cursor.execute(sql_select_query)
                            if(cursor.rowcount>=1):
                                print("Already Data Exist in Database. Can't Insert Duplicate!")
                            else:
                                result = cursor.execute(sql_insert_query)
                                connection.commit()
                                print(cursor.rowcount, "Record inserted successfully into mobile table")
                        except (Exception, psycopg2.Error) as error:
                            print("Failed inserting record into mobile table {}".format(error))
                            errLog("PGSQL ERROR!:","Failed inserting record into mobile table {}".format(error))
                        finally:
                            # closing database connection.
                            if (connection):
                                cursor.close()
                                connection.close()
                                print("PostgreSQL connection is closed")
                        print(file_loc)
                        print("Check Date: "+cdate)
                        print("Total Cycle:"+str(total_cycle))
                        print("Total Colum:"+str(total_column))
                        row_index += 1
                    processLog(file_loc)
                    processLog("Check Date: "+cdate)
                    processLog("Total Cycle:"+str(total_cycle))
                    processLog("Total Colum:"+str(total_column))
                    count+=1
                    print("Total File Count: "+str(count))
                    processLog("Total File Count: "+str(count))
                else:
                    print("EOL  NAME HAS NOT UPDATED IN PROGRAM!")
                
        except Exception as e:  
            print(e)
            conn.close()
            errLog("DATABASE ERROR: ",str(e))

try:
    #INSERT TASK DETAILS IN PROCESS INFO DB
    d = datetime.datetime.now()
    db_start_date=str(d.year)+"-"+str(d.month)+"-"+str(d.day)
    db_start_time=str(d.hour)+":"+str(d.minute)+":"+str(d.second)
    conn = sqlite3.connect('process_info.db')
    conn.execute("INSERT INTO process_log(start_date,start_time,task_type) VALUES(?,?,?)",(str(db_start_date),str(db_start_time),"DATA-MIGRATION"))
    conn.commit()
    conn.close()
    processLog("TASK DETAILS ADDED SUCCESSFULLY IN PROCESS DB! THANK YOU")
except Exception as e:
    print(e)
    errLog("EOL DATA MIGRATION  DATABASE ERROR: ",str(e))
try:
    data_migrate(str(prev_date),str(today_date))
except Exception as e:
    print(e)
    errLog("EOL DATA MIGRATION FUNCTION CALL ERROR: ",str(e))
print("--- %s seconds ---" % (time.time() - start_time))
processLog("TOTAL TIME TAKEN FOR ALL PROCESS: "+str("--- %s seconds ---" % (time.time() - start_time)))

try:
    #UPDATE TASK DETAILS IN PROCESS INFO DB
    d = datetime.datetime.now() 
    db_end_date=str(d.year)+"-"+str(d.month)+"-"+str(d.day)
    db_end_time=str(d.hour)+":"+str(d.minute)+":"+str(d.second)
    end_time=time.time() - start_time
    conn = sqlite3.connect('process_info.db')
    #print("UPDATE process_log SET end_ date='"+str(db_end_date)+"',end_time="+str(db_end_date)+",time_taken="+str(int(end_time))+" WHERE start_date="+str(db_start_date)+" AND start_time="+str(db_start_time)+" AND task_type="+"DMC-LITE")
    conn.execute("UPDATE process_log SET end_date='"+str(db_end_date)+"',end_time='"+str(db_end_time)+"',time_taken="+str(int(end_time))+" WHERE start_date='"+str(db_start_date)+"' AND start_time='"+str(db_start_time)+"' AND task_type="+"'DATA-MIGRATION'")
    conn.commit()
    conn.close()
    processLog("TASK DETAILS UPDATED SUCCESSFULLY IN PROCESS DB! THANK YOU")
except Exception as e:
    print(e)
    errLog("EOL DATA MIGRATION DATABASE ERROR: ",str(e))
print("Thank You!")

