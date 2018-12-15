'''
CREATED BY: Gregory Nikol
Contains and tests the TwelveTone class
imports from copy to create a deepcopy in the _expand method
'''
from copy import deepcopy
from time import sleep

class TwelveTone:
    '''
    Stores and operates on the musical composition tool, twelve tone matrix
    TODO: Add ability to playback sound in relation to note
          Function to output matrix to a printable file
    '''
    ALPHANUM_REP = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 't', 'e']
    FLAT_ALPHA_REP = ['C', 'D♭', 'D', 'E♭', 'E', 'F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B']
    SHARP_ALPHA_REP = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    DEFAULT = "default"
    EXPAND = "expand"

    def __init__(self):
        '''
        Initializes an empty twelve tone matrix
        '''
        self.matrix = [[" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                       [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                       [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                       [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                       [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                       [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                       [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                       [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                       [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                       [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                       [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                       [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]]

    def __str__(self):
        '''
        INPUT: The twelve tone matrix used throughout the script
        OUTPUT: A visual, formatted representation of the twelve tone matrix
        '''
        ret_str = ""

        print("\n"*50)
        ret_str += "      I0  I1  I2  I3  I4  I5  I6  I7  I8  I9 I10 I11\n"
        ret_str += "    /-----------------------------------------------\\\n"
        for row in range(12):
            #Populate a string with the content of one row
            row_string = ""
            for col in range(12):
                #Handles formatting for numbers with two-three digits
                if len(str(self.matrix[row][col])) == 3:
                    row_string += f"{self.matrix[row][col]}|"
                elif len(str(self.matrix[row][col])) == 2:
                    row_string += f" {self.matrix[row][col]}|"
                else:
                    row_string += f" {self.matrix[row][col]} |"

            #Handles formatting for row numbers with two digits
            if row >= 10:
                ret_str += f" P{row}|{row_string}\n"
            else:
                ret_str += f" P{row} |{row_string}\n"

            #Handles different board design for the end of the board
            if row == 11:
                ret_str += "    \\-----------------------------------------------/"
            else:
                ret_str += "    |-----------------------------------------------|\n"
        return ret_str
    
    def clear(self):
        self.__init__()

    def _get_input(self, current_index):
        '''
        INPUT: a list object and the index you're trying to fill
            EXPECTED: the first list (or prime row) of the twelve tone matrix
        OUTPUT: a user input that's been checked for validity
        '''
        user_input = ""

        #Starts infinite loop that can only be left through a return statement
        while True:
            #Handles phrasing difference for index numbers
            print(self.__str__())

            if current_index+1 in [4, 5, 6, 7, 8, 9, 10, 11, 12]:
                user_input = int(input(f"Enter the {current_index+1}th value of your prime row: "))
            elif current_index+1 == 3:
                user_input = int(input(f"Enter the {current_index+1}rd value of your prime row: "))
            elif current_index+1 == 2:
                user_input = int(input(f"Enter the {current_index+1}nd value of your prime row: "))
            elif current_index+1 == 1:
                user_input = int(input(f"Enter the {current_index+1}st value of your prime row: "))

            #Ensures the user's input is a number and that it is unique to the current pattern
            if user_input in self.matrix[0]:
                print("You've already used that value! Try a new number!")
                input()
                continue
            elif user_input not in range(12):
                print("Your value should be a valid number between 0 and 11.\n")
                input()
                continue
            break
        return user_input

    def _fill(self):
        '''
        INPUT: the current matrix
        EXPECTS: the current matrix should be 12x12 with the first row filled with unique values
        OUTPUT: returns a filled matrix corresponding to the algorithm
        '''
        intervals = [(self.matrix[0][x] - self.matrix[0][x-1]) % 12 for x in range(1, 12) if self.matrix[0][x] != " "]

        for row in range(1, len(intervals)+1):
            for col in range(len(intervals)+1):
                self.matrix[row][col] = (self.matrix[row-1][col] - intervals[row-1]) % 12

    def _expand(self):
        '''
        INPUT: the twelve tone matrix
        OUTPUT: returns a matrix showing the musical distance between notes
        '''
        #deepcopy makes a non reference copy of the given matrix
        original_matrix = deepcopy(self.matrix)

        for row in range(12):
            #these variables keep track of the number of regressions in each row and column
            horizontal_twelves = 0
            vertical_twelves = 0

            for col in range(12):
                #skips an iteration for the matrix's diagonal
                if row == col:
                    continue
                #applies to every value outside the diagonal
                elif col > row:
                    #adds 12 to every value that regresses in the original row it's referencing
                    if original_matrix[row][col] < original_matrix[row][col-1]:
                        horizontal_twelves += 1
                    self.matrix[row][col] += (12 * horizontal_twelves)
                    #adds 12 to every value that regresses in the original column it's referencing
                    if original_matrix[col][row] < original_matrix[col-1][row]:
                        vertical_twelves += 1
                    self.matrix[col][row] += (12 * vertical_twelves)

    def _contract(self):
        '''
        INPUT: the twelve tone matrix affected by the expand_tt function
        OUTPUT: the original twelve tone matrix
        '''
        for row in range(12):
            for col in range(12):
                self.matrix[row][col] = self.matrix[row][col] % 12

    def _flip_back(self, rep):
        '''
        INPUT: 2-dimensional matrix, and the list representation currently active
        OUTPUT: prints out the original version of the matrix and returns it
        '''
        for row in range(12):
            for col in range(12):
                self.matrix[row][col] = rep.index(self.matrix[row][col])

    def build_matrix(self):
        '''
        INPUT: the twelve tone matrix
        FUNCTIONS USED: fill_remaining and get_input
        OUTPUT: a fully filled out twelve tone matrix
        '''
        #Get user input for the prime row of the twelve tone matrix
        for index in range(13):
            if index > 0:
                self._fill()
            if index < 12:
                self.matrix[0][index] = self._get_input(index)

    def flip_representation(self, rep):
        '''
        POSSIBLE REPRESENTATIONS: ALPHANUM_REP, FLAT_ALPHA_REP, SHARP_ALPHA_REP, EXPAND

        INPUT: 2-dimensional matrix, and a new list representation
        OUTPUT: prints out the converted version of the matrix and returns it
        '''
        #If the matrix is in numeral representation proceed to flip to new rep
        if set(self.matrix[0]) == set(range(12)) and rep != TwelveTone.DEFAULT:
            if rep == TwelveTone.EXPAND:
                self._expand()

            else:
                #Iterate through the entire matrix, altering representation
                for row in range(12):
                    for col in range(12):
                        self.matrix[row][col] = str(rep[self.matrix[row][col]])
        #If the matrix isn't in numeral representation flip back to it then proceed
        else:
            if set(self.matrix[0]) == set(TwelveTone.ALPHANUM_REP):
                self._flip_back(TwelveTone.ALPHANUM_REP)
            elif set(self.matrix[0]) == set(TwelveTone.FLAT_ALPHA_REP):
                self._flip_back(TwelveTone.FLAT_ALPHA_REP)
            elif set(self.matrix[0]) == set(TwelveTone.SHARP_ALPHA_REP):
                self._flip_back(TwelveTone.SHARP_ALPHA_REP)
            else:
                try:
                    self._contract()
                except:
                    print("ERROR ENCOUNTERED WHILE TRYING TO CONTRACT")
            if rep != TwelveTone.DEFAULT:
                self.flip_representation(rep)

def _print_menu(is_first_show=False):
    '''
    Display the menu options for testing TwelveTone
    '''
    print("TWELVE TONE CALCULATOR OPTIONS")
    print("------------------------------")
    print("\n1. Build a new matrix")
    if not is_first_show:
        print("2. Expand matrix")
        print("3. Convert to alpha-numeric")
        print("4. Convert to flat alphabetic")
        print("5. Convert to sharp alphabetic")
        print("6. Convert to default representation")
        print("7. Clear the matrix")
        print("8. Save the matrix")
    print("9. Exit the program\n")

def _get_integer(is_first_show=False):
    usr_in = ""
    while True:
        try:
            if is_first_show:
                usr_in = int(input("Choose an item 1 or 9: "))
            else:
                usr_in = int(input("Choose an item 1 -> 9: "))
        except ValueError:
            print("[VALUE ERROR]: Please enter an integer")
            continue
        except TypeError:
            print("[TYPE ERROR]: Please enter an integer")
            continue
        else:
            if usr_in < 1 or usr_in > 9:
                print("[OUT OF RANGE ERROR]: Only numbers between 1 and 8 are accepted")
        break
    return usr_in

def main():
    '''
    This code runs if this script is being run directly.
    This code is meant to test the functions of the TwelveTone class
    '''
    my_matrix = TwelveTone()
    status = 0
    is_first_show = True

    while True:
        _print_menu(is_first_show)
        status = _get_integer()

        if status == 1:
            if is_first_show:
                my_matrix.build_matrix()
                print(my_matrix)
                is_first_show = False
            else:
                print("You have to clear your matrix first!\n")
        elif status == 2 and not is_first_show:
            my_matrix.flip_representation(my_matrix.EXPAND)
            print(my_matrix)
            input("Press [Enter] to continue.....\n")
        elif status == 3 and not is_first_show:
            my_matrix.flip_representation(my_matrix.ALPHANUM_REP)
            print(my_matrix)
            input("Press [Enter] to continue.....\n")
        elif status == 4 and not is_first_show:
            my_matrix.flip_representation(my_matrix.FLAT_ALPHA_REP)
            print(my_matrix)
            input("Press [Enter] to continue.....\n")
        elif status == 5 and not is_first_show:
            my_matrix.flip_representation(my_matrix.SHARP_ALPHA_REP)
            print(my_matrix)
            input("Press [Enter] to continue.....\n")
        elif status == 6 and not is_first_show:
            my_matrix.flip_representation(TwelveTone.DEFAULT)
            print(my_matrix)
            input("Press [Enter] to continue.....\n")
        elif status == 7 and not is_first_show:
            my_matrix.clear()
            is_first_show = True
        elif status == 8 and not is_first_show:
            file_name = input("Enter a file name: ")
            matrix_file = open(str(file_name)+".txt", 'w', encoding='utf-8')
            matrix_file.write(str(my_matrix))
            matrix_file.close()
        elif status == 9:
            break
        else:
            continue

if __name__ == "__main__":
    main()
