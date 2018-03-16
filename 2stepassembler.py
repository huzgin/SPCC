# This is an implementation of 2 step assembler for IBM 360/370 PC.
# The input is being read from input.txt file
# Please make sure that if there is a blank space, just a single space is used to signify it.
# Make sure that all the words are separated by single spaces

# TODO Location Counter and storing output code for pass2


# *********************************************************************************************
# Symbol Table Format:
# ID    Symbol  Value   Length  R/A

def add_literal_value(index_value):
    global location_counter
    if (location_counter % 8) != 0:
        location_counter = location_counter + (8 - (location_counter % 8))
    for x in range(0, len(literal_table)):
        literal_table[x].append(str(location_counter))
        location_counter = location_counter+4

    return

def check_for_symbol(sym, loc, index):

    if sym == 'END':  # Checking if end of code found
        print("END statement found.")
        output_pass_1.append(sym)
        return 2
    else:
        if sym == '':  # If the input to this function is blank, it has no symbol to store
            return 0
        if assembly_code_tokenized_by_word[index][1] != 'START':  # So program name  doesn't end up in symbol table
            id_string = '#ID' + str(len(symbol_table) + 1)  # Get length of symbol table+1 for ID
            # str function converts int to string, to reverse use int()
            data_to_append = [id_string, sym, loc, 'R']
            symbol_table.append(data_to_append)
        output_pass_1.append(sym)
        return 1


def pot_get(index_value, pocode):
    global location_counter
    if pocode == 'START':
        global program_name
        program_name = assembly_code_tokenized_by_word[index_value][0]
        location_counter = int(assembly_code_tokenized_by_word[index_value][2])

        for x in range(0, (len(symbol_table))):
            if assembly_code_tokenized_by_word[index_value][0] in symbol_table[x][1]:
                symbol_table[x][2] = location_counter
        output_pass_1.append('START')
        output_pass_1.append(assembly_code_tokenized_by_word[index_value][2])
    if pocode == 'LTORG':
        add_literal_value(index_value)


    if pocode in pseudo_opcode_table_pass1:  # Checking if value available in pot table

        if pocode in ['DS', 'DC']:
            operand_og = assembly_code_tokenized_by_word[index_value][2]
            if (location_counter % 4) != 0:
                location_counter = location_counter + (4 - (location_counter % 4))
                # Alignment for DC,DS commands

            if operand_og.find('F') == 0:  # Eg: F'34'
                location_counter = location_counter+4

            elif operand_og.endswith('F'):  # Eg: 10F
                operand = operand_og.split('F')
                location_counter = location_counter + 4*int(operand[0])

        elif pocode in ['EQU']:
            for x in range(0, (len(symbol_table))):
                if assembly_code_tokenized_by_word[index_value][0] in symbol_table[x][1]:
                    symbol_table[x][2] = assembly_code_tokenized_by_word[index_value][2]
                    symbol_table[x].append('A')
                    # updating value in symbol table

        elif pocode in ['USING', 'END']:
            if pocode == 'USING':
                operand_og = assembly_code_tokenized_by_word[index_value][2]
                operand = operand_og.split(',')
                global base_table
                if operand[0] == '*':
                    base_table.append([operand[1], location_counter])



        output_pass_1.append(pocode)
        return 0

    else:

        return 1


def mot_get(mocode, index):
    for j in range(0, (len(machine_opcode_table_pass1))-1):
        if mocode in machine_opcode_table_pass1[j][0]:  # Checking if value available in mot table
            # print(mocode+' found in mot table')
            # l = machine_opcode_table_pass1[j][1]
            output_pass_1.append(mocode)
            output_pass_1.append(str(assembly_code_tokenized_by_word[index][2]))

            return int(machine_opcode_table_pass1[j][1])
    else:
        return 0


def literal_check(litcode):
    try:
        if litcode[2]:
            if '=' in litcode[2]:
                litval = litcode[2].split('=')
                id_string = '#LT' + str(len(literal_table) + 1)  # Get length of literal table+1 for ID
                literal = '='+litval[1]
                data_to_append = [id_string, literal]
                literal_table.append(data_to_append)
                output_pass_1.append(id_string)
    except IndexError:
        return 0


# Functions Above This
# *********************************************************************************************
# Main Below This


# File Reading
assembly_code = open('input.txt', "r").read()  # Reading File Data
# print('This is the input code: \n' + assembly_code)  # For User Verification

# Tokenizing File
assembly_code_tokenized_by_line = assembly_code.split('\n')  # Token by line
assembly_code_tokenized_by_word = assembly_code_tokenized_by_line  # Declaring array for for loop

for i in range(0, (len(assembly_code_tokenized_by_line) - 1)):  # Looping through list
    assembly_code_tokenized_by_word[i] = assembly_code_tokenized_by_word[i].split(' ')
    # ^Splitting each internal list on blank space
# print(assembly_code_tokenized_by_word)  # Temp for debugging

# Tables for Pass 1
machine_opcode_table_pass1 = [['SR', 2], ['LA', 4], ['L', 4], ['AR', 2], ['A', 4], ['ST', 4], ['C', 4],
                              ['BNE', 4], ['LR', 2], ['BR', 2]]
# ^Table for pass1 has only 2 values to figure out size

pseudo_opcode_table_pass1 = ['USING', 'DROP', 'EQU', 'DS', 'DC', 'END']
# ^Table for pass1 has only names, rest is handled in POTtype function

literal_table = []
# ^Literal table to store values of all literals

symbol_table = []
# ^Symbol table to store values of all symbols

base_table = []
# ^ base table

output_pass_1 = []
# ^output of pass 1

final_output_pass_1 = []
location_counter = 0  # Location Counter initialize

# TODO  Main Loop Starts here:
for i in range(0, (len(assembly_code_tokenized_by_word) - 1)):
# Working on element 0
    if assembly_code_tokenized_by_word[i][0] != ' ':
        flag = check_for_symbol(assembly_code_tokenized_by_word[i][0], location_counter, i)  # Just Sending to different function


# Working on element 1
    if assembly_code_tokenized_by_word[i][0] != 'END':  # To avoid list index out of range for last line

        value_of_l = 0
        do = pot_get(i, assembly_code_tokenized_by_word[i][1])
        if do == 1:  # value not found, go to mot table
            value_of_l = mot_get(assembly_code_tokenized_by_word[i][1], i)
# Working on element 2
            # symbol_present returns 0 if no symbol, 1 if symbol found, 2 if 'END' found
            symbol_present = literal_check(assembly_code_tokenized_by_word[i])

        location_counter = location_counter + value_of_l
        # print('val l:' + str(value_of_l))
        # print('val lc:' + str(location_counter))

# Replacing Literals and symbols in code.
for x in range(0,len(output_pass_1)-1):
    for y in range(0, len(symbol_table)-1):

        if ',' in str(output_pass_1[x]):
            commaval = str(output_pass_1[x]).split(',')
            if commaval[1] in symbol_table[y][1]:
                output_pass_1[x] = commaval[0] + ',' + symbol_table[y][0]

        if output_pass_1[x] in symbol_table[y][1]:
            output_pass_1[x] = symbol_table[y][0]
x = 0
while x < (len(output_pass_1)-1):
    for y in range(0, len(symbol_table)):
        if output_pass_1[x] == 'START':
            if [output_pass_1[x-1], output_pass_1[x], output_pass_1[x+1]] not in final_output_pass_1:
                final_output_pass_1.append([output_pass_1[x-1], output_pass_1[x], output_pass_1[x+1]])

    for y in range(0, len(machine_opcode_table_pass1)):
        if output_pass_1[x] in machine_opcode_table_pass1[y][0]:

            if [output_pass_1[x], output_pass_1[x+1]] not in final_output_pass_1:
                final_output_pass_1.append([output_pass_1[x], output_pass_1[x+1]])

    x = x+1


print('Input Code Tokenized')
print(assembly_code_tokenized_by_word)
print('Symbol Table')
print(symbol_table)
print('Literal Table')
print(literal_table)
print('Base Table')
print(base_table)
print('Output of pass 1')
print(output_pass_1)
