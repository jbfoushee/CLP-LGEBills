import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import os
import pandas as pd
import platform
import seaborn as sns


def GetKYGasCostData():

    # Data from:
    #   https://findenergy.com/ky/natural-gas/ (manually transferred)

    filepath = GetFile("KYGasPrices.xlsx")

    # ---------------------------------------------------------------------------
    # Project Requirement: Category 1a: Read more than one data file
    # --------------------------------------------------------------------------
    df_infile = pd.read_excel(filepath, header=0, skiprows=0, sheet_name="Sheet1")

    # Build an inner-join formatted value
    df_infile.insert(3,"Date_YYYYMM",1)
    df_infile["Date_YYYYMM"] = df_infile.apply(lambda row: str(row['Date'])[:7], axis = 1)

    del df_infile["Date"]

    return df_infile

def GetKYElecCostData():

    # Data from:
    #   https://findenergy.com/ky/ (manually transferred)

    filepath = GetFile("KYElecPrices.xlsx")

    # ---------------------------------------------------------------------------
    # Project Requirement: Category 1b: Read more than one data file
    # --------------------------------------------------------------------------
    df_infile = pd.read_excel(filepath, header=0, skiprows=0, sheet_name="Sheet1")

    # Build an inner-join formatted value
    df_infile.insert(3,"Date_YYYYMM",1)
    df_infile["Date_YYYYMM"] = df_infile.apply(lambda row: str(row['Date'])[:7], axis = 1)

    del df_infile["Date"]

    return df_infile

def GetBillingData():
    filepath = GetFile("LGEBills.xlsx")

    # ---------------------------------------------------------------------------
    # Project Requirement: Category 1c: Read more than one data file
    # --------------------------------------------------------------------------
    df_infile = pd.read_excel(filepath, header=0, skiprows=0, sheet_name="Bill Data")

    # Cleaning data: Remove Excel word-wrapping in column names
    for (columnName, columnData) in df_infile.items():
        mystr = str(columnName)
        if mystr.__contains__("\n"):
            df_infile.rename(columns = {mystr: mystr.replace("\n", "")}, inplace = True)

    # -------------------------------------------------------------------------------------------------------------
    # Project Requirement: Category 2a: Cleaning data -> Remove rows with at least column value with an NaN value...
    # -------------------------------------------------------------------------------------------------------------
    # Remove rows where the primary key ("Bill Due") or the pricing totals are missing
    df_infile.dropna(axis=0, subset=['Bill Due','Total $','Electric $','Gas $'], inplace=True)

    # Build an inner-join-friendly formatted value
    df_infile["Date_YYYYMM"] = df_infile.apply(lambda row: row["Bill Due"].strftime("%Y-%m"), axis = 1)


    return df_infile

def GetFile(what: str):
    print ("Looking for file '" + what + "'...")

    seperator = ""
    filepath = os.getcwd() 
    if platform.system() == "Windows":
        seperator = "\\"
    else:
        seperator = "/"
    filepath += seperator + what

    while os.path.exists(filepath) == False:
        filepath = input("Input file not found @ '" + filepath + "'. Where is it?\n")

        # User could enter "P:\ath", "P:\ath\", or "P:\ath\file.ext"
        # Normalize all three to "P:\ath\file.ext"
        if (filepath[::-1][0: len(what) + 1] != what[::-1] + seperator):
            filepath = (filepath + seperator + what).replace(seperator + seperator, seperator)

    return filepath

KYGASDATA = GetKYGasCostData()
KYELECDATA = GetKYElecCostData()
MYBILLING = GetBillingData()

def Report1():

    df_KYCost_Gas = KYGASDATA

    df_MyCost_Gas = MYBILLING[["Date_YYYYMM", "Gas $", "ccf Used", "Avg Temp"]]

    # ------------------------------------------------------------------------------------------
    # Project Requirement: Category 2b: ...and perform a pandas merge with your two datasets...
    # ------------------------------------------------------------------------------------------
    df_merged = pd.merge(df_MyCost_Gas, df_KYCost_Gas, how="left", on="Date_YYYYMM", suffixes=('_me', '_KY'))

    # -----------------------------------------------------------------------------------------------
    # Project Requirement: Category 2c: ...then calculate some new values based on the new dataset
    # -----------------------------------------------------------------------------------------------
    df_merged["Difference"] = df_merged["Gas $"] - df_merged["Average Bill per month"]

    plt.plot(df_merged["Date_YYYYMM"], df_merged["Gas $"])
    plt.plot(df_merged["Date_YYYYMM"], df_merged["Average Bill per month"])
    plt.legend(['My Gas Bill','Avg KY Gas Bill'])
    plt.xticks(np.arange(0, len(df_merged["Date_YYYYMM"])+1, 6))
    plt.xticks(rotation=90)
    formatx = ticker.StrMethodFormatter('${x:,.0f}')
    plt.gca().yaxis.set_major_formatter(formatx) 

    # ----------------------------------------------------------------------------------------------------------
    # Project Requirement: Category 3a: Visualize data in a graph, chart, or other visual representation of data.
    # ----------------------------------------------------------------------------------------------------------
    plt.show()

def Report2():

    df_KYCost_Elec = KYELECDATA
    
    df_MyCost_Elec = MYBILLING[["Date_YYYYMM", "Electric $", "kwh Used", "Avg Temp"]]

    # ------------------------------------------------------------------------------------------
    # Project Requirement: Category 2b: ...and perform a pandas merge with your two datasets...
    # ------------------------------------------------------------------------------------------
    df_merged = pd.merge(df_MyCost_Elec, df_KYCost_Elec, how="left", on="Date_YYYYMM", suffixes=('_me', '_KY'))

    plt.plot(df_merged["Date_YYYYMM"], df_merged["Electric $"])
    plt.plot(df_merged["Date_YYYYMM"], df_merged["Average Bill per month"])
    plt.legend(['My Electric Bill', 'Avg KY Electric Bill'])
    plt.xticks(np.arange(0, len(df_merged["Date_YYYYMM"])+1, 6))
    plt.xticks(rotation=90)
    formaty = ticker.StrMethodFormatter('${x:,.0f}')
    plt.gca().yaxis.set_major_formatter(formaty) 

    # ----------------------------------------------------------------------------------------------------------
    # Project Requirement: Category 3b: Visualize data in a graph, chart, or other visual representation of data.
    # ----------------------------------------------------------------------------------------------------------
    plt.show()

def Report3():

    df_MyCost_Gas = MYBILLING[["Date_YYYYMM", "Gas $", "ccf Used", "Avg ccf/d", "Avg Temp"]]
    
    sns.regplot(x="Avg Temp", y="Avg ccf/d", order=2, data=df_MyCost_Gas).set(title="My Avg gas usage per day vs Avg monthly temperature")
    formatx = ticker.StrMethodFormatter('{x:,.0f}°')
    plt.gca().xaxis.set_major_formatter(formatx) 
    
    # ----------------------------------------------------------------------------------------------------------
    # Project Requirement: Category 3c: Visualize data in a graph, chart, or other visual representation of data.
    # ----------------------------------------------------------------------------------------------------------
    plt.show()

def Report4():

    df_MyCost_Elec = MYBILLING[["Date_YYYYMM", "Electric $", "kwh Used", "Avg kwh/d", "Avg Temp"]]

    sns.regplot(x="Avg Temp", y="Avg kwh/d", order=2, data=df_MyCost_Elec).set(title="My Avg electric usage per day vs Avg monthly temperature")
    formatx = ticker.StrMethodFormatter('{x:,.0f}°')
    plt.gca().xaxis.set_major_formatter(formatx) 
    
    # ----------------------------------------------------------------------------------------------------------
    # Project Requirement: Category 3d: Visualize data in a graph, chart, or other visual representation of data.
    # ----------------------------------------------------------------------------------------------------------
    plt.show()

def Report5():

    df_MyCost = MYBILLING[["Date_YYYYMM", "Total $", "Avg Temp"]]

    sns.regplot(x="Avg Temp", y="Total $", order=2, data=df_MyCost).set(title="My Avg monthtly bill vs Avg monthly temperature")
    formatx = ticker.StrMethodFormatter('{x:,.0f}°')
    plt.gca().xaxis.set_major_formatter(formatx) 
    formaty = ticker.StrMethodFormatter('${x:,.0f}')
    plt.gca().yaxis.set_major_formatter(formaty)     
    
    # ----------------------------------------------------------------------------------------------------------
    # Project Requirement: Category 3e: Visualize data in a graph, chart, or other visual representation of data.
    # ----------------------------------------------------------------------------------------------------------
    plt.show()

def Report6():

    # Make a copy() to avoid SettingWithCopyWarning
    df_MyCost = MYBILLING[["Month", "Total $", "Electric $", "Gas $"]].copy()

    #Build new columns representing percentages of the facet to the overall price
    df_MyCost["ElecOfBill"] = df_MyCost["Electric $"] / df_MyCost["Total $"] * 100
    df_MyCost["GasOfBill"] = df_MyCost["Gas $"] / df_MyCost["Total $"] * 100

    df_MyCost.groupby(['Month']).mean()

    plt.bar(df_MyCost["Month"], df_MyCost["ElecOfBill"] + df_MyCost["GasOfBill"], label='Electric')
    plt.bar(df_MyCost["Month"], df_MyCost["GasOfBill"], label='Gas') 
   

    plt.xlabel('Month of year')
    plt.ylabel('Percentage of Total Bill')
    plt.title('Avg distribution of my bill between gas and electric, by month')
    plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        , ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        , rotation=20)
    formaty = ticker.StrMethodFormatter('{x}%')
    plt.gca().yaxis.set_major_formatter(formaty)         
    plt.legend(loc='upper left')

    # ----------------------------------------------------------------------------------------------------------
    # Project Requirement: Category 3f: Visualize data in a graph, chart, or other visual representation of data.
    # ----------------------------------------------------------------------------------------------------------
    plt.show()
    

def main():
    print (" ")

    menu_options = {
        1: "Report 1: My Gas bill vs the Avg KY Gas bill",
        2: "Report 2: My Electric bill vs the Avg KY Electric bill",
        3: "Report 3: My Avg gas usage per day vs Avg monthly temperature",
        4: "Report 4: My Avg electric usage per day vs Avg monthly temperature",
        5: "Report 5: My Avg monthly bill vs Avg monthly temperature",
        6: "Report 6: Avg Distribution of my bill between gas and electric, by month",
        0: "Quit",
    }
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )

    while (True):
        option = input('Enter your choice: ')
        
        badchoice = 1

        if (option.isnumeric() == True):
            option = int(option)
            badchoice = 0

            if (option > 0) & (option <= max(menu_options.keys())):
                print("Close the report to return to menu...")

            #Check what choice was entered and act accordingly
            if option == 1:
                Report1()
            elif option == 2:
                Report2()
            elif option == 3:
                Report3()
            elif option == 4:
                Report4()
            elif option == 5:
                Report5()                            
            elif option == 6:
                Report6()             
            elif option == 0:
                print('Quitting...')
                exit()
            else:
                badchoice = 1
        else:
            badchoice = 1

        if (badchoice == 1):
            print('Invalid option. Please enter a number between 0 and ' + str(max(menu_options.keys())) + '.')
main()