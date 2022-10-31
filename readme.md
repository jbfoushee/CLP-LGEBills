# Code Louisville - Data 2
# LGE Bills Analysis

The objecive of this project is to compare my household's utility bills to the Kentucky average.

Data is pulled from 
- 20 years-worth of Louisville Gas & Electric (LGE) bills
- Kentucky residential gas- and electric data from [findenergy.com](https://findenergy.com/ky/)

## Requirements
- Python 3.10.0
- Requirement packages are outlined in requirements.txt, installed during Install instructions

## Install:

1. Clone the repository:
```
| Linux/Mac/Windows                                         |
|-----------------------------------------------------------|
| git clone https://github.com/jbfoushee/CLP-LGEBills.git   |
```
2. Create the virtual environment from the cloned directory:
```
| Linux/Mac                | Windows                        |
|--------------------------|--------------------------------|
| python3 -m venv venv     | python -m venv venv            |
```
3. Activate the virtual environment :
```
| Linux/Mac                | Windows (run one)              |
|--------------------------|--------------------------------|
| source venv/bin/activate | source venv/Scripts/activate   |
|                          | .\venv\Scripts\Activate.ps1    |
```
4. Install requirements:
```
| Linux/Mac/Windows                                         |
|-----------------------------------------------------------|
| pip install -r requirements.txt                           |
```
5. Execute main.py
```
| Linux/Mac                | Windows                        |
|--------------------------|--------------------------------|
| python3 main.py          | python main.py                 |
```

## Running
In the terminal, run
```
| Linux/Mac                | Windows                        |
|--------------------------|--------------------------------|
| python3 main.py          | python main.py                 |
```
The program will load the data files, and prompt which report you would like to display.
Close the report, and either view another or exit the program.


## Project Requirements
### Category 1: Loading Data:

Read 2+ data files (JSON, CSV, Excel, etc.)

The LGE bills were manually transferred into an Excel document.

The Kentucky gas- and electric cost data were found within charts found at [findenergy.com](https://findenergy.com/ky/).
Research was taken to locate the underlying .json through internet developer tools, but the source filename randomizes.
I could not take the chance the project reviewer would receive an error attempting to locate the file.
The data were transferred manually into Excel documents.

See main.py for areas labeled "Category 1" in comments.

### Category 2: Clean and operate on data:

Clean your data and perform a pandas merge with your two data sets, then calculate some new values based on the new data set.
This was accomplished by removing NaN values on the joining values between the data sets.

See main.py for areas labeled "Category 2" in comments.

### Category 3: Visualize / Present

Visualize data in a graph, chart, or other visual representation of data.

The Python script, once fully loaded, allows the user to review 6 reports out of matplotlib or seaborn displays:

Report 1: My Gas bill vs the Avg KY Gas bill

Report 2: My Electric bill vs the Avg KY Electric bill
(Note: Report does not distinguish between Kentucky households that use electricity or gas as primary heating)
(Note: Data on Average KY cost goes back to 2017.)

Report 3: My Avg gas usage per day vs Avg monthly temperature

Report 4: My Avg electric usage per day vs Avg monthly temperature
(Note: Report does not distinguish between Kentucky households that use electricity or gas as primary heating)

Report 5: My Avg monthly bill vs Avg monthly temperature
(Note: Report does not distinguish between Kentucky households that use electricity or gas as primary heating)

Report 6: Avg distribution of my bill between gas and electric, by month

### Category 4: Best Practices

The program should utilize a virtual environment and document library dependencies in a requirements.txt file.
See readme for requirements.txt