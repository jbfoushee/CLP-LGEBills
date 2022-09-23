import pandas as pd
import numpy as np
import os
import platform
import matplotlib.pyplot as plt
import seaborn as sns


def GetKYGasCostData():

    #https://findenergy.com/ky/
    #https://findenergy.com/ky/natural-gas/
    #https://www.eia.gov/dnav/ng/hist/n3010ky3m.htm

    filepath = LocateBillingFile("KYGasPrices.xlsx")

    df_infile = pd.read_excel(filepath, header=0, skiprows=0, sheet_name="Sheet1")

    df_infile.insert(3,"Date_YYYYMM",1)
    df_infile["Date_YYYYMM"] = df_infile.apply(lambda row: str(row['Date'])[:7], axis = 1)

    del df_infile["Date"]

    return df_infile

def GetKYElecCostData():

    #https://findenergy.com/ky/

    filepath = LocateBillingFile("KYElecPrices.xlsx")

    df_infile = pd.read_excel(filepath, header=0, skiprows=0, sheet_name="Sheet1")

    df_infile.insert(3,"Date_YYYYMM",1)
    df_infile["Date_YYYYMM"] = df_infile.apply(lambda row: str(row['Date'])[:7], axis = 1)

    del df_infile["Date"]

    return df_infile

def GetBillingData():
    filepath = LocateBillingFile("LGEBills.xlsx")

    df_infile = pd.read_excel(filepath, header=0, skiprows=0, sheet_name="Bill Data")

    #Remove Excel word-wrapping in column names
    for (columnName, columnData) in df_infile.iteritems():
        mystr = str(columnName)
        if mystr.__contains__("\n"):
            df_infile.rename(columns = {mystr: mystr.replace("\n", "")}, inplace = True)

    df_infile["Date_YYYYMM"] = df_infile.apply(lambda row: row["Bill Due"].strftime("%Y-%m"), axis = 1)

    return df_infile

def LocateBillingFile(what):
    print ("Looking for data...")

    filepath = os.getcwd() 
    if platform.system() == "Windows":
        filepath += "\\"
    else:
        filepath += "/"
    filepath += what

    while os.path.exists(filepath) == False:
        filepath = input("Input file not found. Where is it?\n")
    return filepath

KYGASDATA = GetKYGasCostData()
KYELECDATA = GetKYElecCostData()
MYBILLING = GetBillingData()

def Report1():

    df_KYCost_Gas = KYGASDATA

    df_MyCost_Gas = MYBILLING[["Date_YYYYMM", "Gas $", "ccf Used", "$ / ccf", "Avg Temp"]]

    df_merged = pd.merge(df_MyCost_Gas, df_KYCost_Gas, how="left", on="Date_YYYYMM", suffixes=('_me', '_KY'))

    plt.plot(df_merged["Date_YYYYMM"], df_merged["Gas $"])
    plt.plot(df_merged["Date_YYYYMM"], df_merged["Average Bill per month"])
    plt.legend(['My Gas Bill','Avg KY Gas Bill'])
    plt.show()

def Report2():

    df_KYCost_Elec = KYELECDATA
    
    df_MyCost_Elec = MYBILLING[["Date_YYYYMM", "Electric $", "kwh Used", "$ / kwh", "Avg Temp"]]

    df_merged = pd.merge(df_MyCost_Elec, df_KYCost_Elec, how="left", on="Date_YYYYMM", suffixes=('_me', '_KY'))

    plt.plot(df_merged["Date_YYYYMM"], df_merged["Electric $"])
    plt.plot(df_merged["Date_YYYYMM"], df_merged["Average Bill per month"])
    plt.legend(['My Electric Bill', 'Avg KY Electric Bill'])
    plt.show()

def Report3():

    df_MyCost_Gas = MYBILLING[["Date_YYYYMM", "Gas $", "ccf Used", "Avg ccf/d", "Avg Temp"]]

    sns.regplot(x="Avg Temp", y="Avg ccf/d", order=2, data=df_MyCost_Gas).set(title="Avg gas usage per day vs Avg monthly temperature")
    plt.show()

def Report4():

    df_MyCost_Elec = MYBILLING[["Date_YYYYMM", "Electric $", "kwh Used", "Avg kwh/d", "Avg Temp"]]

    sns.regplot(x="Avg Temp", y="Avg kwh/d", order=2, data=df_MyCost_Elec).set(title="Avg electric usage per day vs Avg monthly temperature")
    plt.show()

def main():
    menu_options = {
        1: "Report 1",
        2: "Report 2",
        3: "Report 3",
        4: "Report 4",
        0: "Quit",
    }
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )

    while (True):
        option = int(input('Enter your choice: '))
                
        #Check what choice was entered and act accordingly
        if option == 1:
            Report1()
        elif option == 2:
            Report2()
        elif option == 3:
            Report3()
        elif option == 4:
            Report4()            
        elif option == 0:
            print('Thanks message before exiting')
            exit()
        else:
            print('Invalid option. Please enter a number between 0 and ' + str(max(menu_options.keys())) + '.')

main()