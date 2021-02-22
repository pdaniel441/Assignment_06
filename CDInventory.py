#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with classes and functions to modify CDInventory Program.
# Change Log: Patrick Danielson, 2021-Feb-21, Modified Starter Script
# DBiesinger, 2030-Jan-01, Created File
# PDanielson, 2021-Feb-21, Modified Starter Script
#------------------------------------------#
import os.path

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
lstRow = []  # list of data row
strFileName = 'CDInventory.txt'  # data storage file
objFile = None  # file object

# Check if Inventory File Exists in Directory, Create if file not found.
if os.path.exists(strFileName): 
    pass
else:
    objFile = open(strFileName,'w')
    objFile.close()


# -- PROCESSING -- #
class DataProcessor:
    """Processing Functions on Inventory Data"""
    
    @staticmethod
    def add_entry(entry,table):
        """Function to operate on user input list and append list to data table
        
        Args:
            entry (list): list of stings containing entry ID, Title, and Artist for inventory
            table (list of dict): 2D data structure (list of dicts) that holds the inventory data during runtime
            
        Returns:
            None.
        
        """
        intID = int(entry[0])
        dicRow = {'ID': intID, 'Title': entry[1], 'Artist': entry[2]}
        table.append(dicRow)
    
    @staticmethod
    def remove_entry(entryID, table):
        """Function to operate on data table to remove row based on user input.
        
        Args:
            entryID (int): Integer value of CDInventory ID
            
        Returns:
            None.
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == entryID:
                del table[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')

class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        table.clear()  # this clears existing data and allows to load data from file
        objFile = open(file_name, 'r')
        for line in objFile:
            data = line.strip().split(',')
            dicRow = {'ID': int(data[0]), 'Title': data[1], 'Artist': data[2]}
            table.append(dicRow)
        objFile.close()
        
        print('Local Variable \'table\' now stores entries from Text File.')

    @staticmethod
    def write_file(file_name, table):
        """Function to save data table stored in runtime to a *.txt file
        
        Args:
            file_name (string): name of file to write data to
            table (list of dict): 2D data structure (list of dicts) that holds data during runtime
        
        Returns:
            None.
        """
        objFile = open(file_name, 'w')
        for row in lstTbl:
            lstValues = list(row.values())
            lstValues[0] = str(lstValues[0])
            objFile.write(','.join(lstValues) + '\n')
        objFile.close()


# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    @staticmethod
    def get_new_entry():
        """Get information from user for new CD Entry and return list of 
        strings containing the entries.
        
        Args:
            None.
            
        Returns:
            strID (string): User input string for the entry ID
            strTitle (string): User input string for the entry CD Title
            strArtist (string): User input string for the entry CD Artist
                
        """
        strID = input('Enter ID: ').strip()
        strTitle = input('What is the CD\'s title? ').strip()
        strArtist = input('What is the Artist\'s name? ').strip()
        return [strID, strTitle, strArtist]
        

# -- MAIN PROGRAM -- #

# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(strFileName, lstTbl)

# 2. Start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled: ')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
        
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        lstRow = IO.get_new_entry()  # Store returned list of return values from IO function

        # 3.3.2 Add item to the table
        DataProcessor.add_entry(lstRow, lstTbl)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
        
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
        
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        intIDDel = int(input('Which ID would you like to delete? ').strip())
        
        # 3.5.2 search thru table and delete CD
        DataProcessor.remove_entry(intIDDel,lstTbl)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')




