# Macro Processor Implementation
# The input is being read from macro-input.txt file
# Please make sure that if there is a blank space, just a single space is used to signify it.
# Make sure that all the words are separated by single spaces
# *********************************************************************************************
# Functions Here


def macro_found(index_current):
    macro_name = macro_code_tokenized_by_word[index_current + 1][0]  # Getting Name of the Macro

    global mntc
    global mdt
    global mnt
    global mdtc
    global ala
    global alac

    mnt.append([mdtc, macro_name])
    mntc = mntc + 1

    try:
        to_append = []
        to_append.append(macro_name)
        if macro_code_tokenized_by_word[index_current + 1][1]:
            arguments_split = macro_code_tokenized_by_word[index_current + 1][1].split(',')

            for x in range(0, len(arguments_split)):
                ala.append([alac, arguments_split[x]])
                alac += 1
                # Add Comma to separate variables.
                if x == 0:
                    to_append.append('#' + str(alac))
                else:
                    to_append.append(',#' + str(alac))

        mdt.append([mdtc, ' '.join(to_append)])  # Use .join to convert list to string

        mdtc += 1
        flag = ' '
        indexval = index_current + 1
        while flag != 'MEND':
            if 'MEND' in macro_code_tokenized_by_word[indexval][0]:
                flag = 'MEND'
            else:
                mdt.insert(mdtc, [mdtc, macro_code_tokenized_by_word[indexval + 1]])
                mdtc = mdtc + 1
                indexval = indexval + 1

    except IndexError:
        pass


# *********************************************************************************************
# Macro Data Table
mdt = []
# Macro Data Table Counter
mdtc = 1
# Macro Name Table
mnt = []
# Macro Name Table Counter
mntc = 1
# Argument List Array
ala = []
# Argument List Array Counter
alac = 1
# Output of Pass 1
output_pass_1 = []
# *********************************************************************************************

# Reading Input
macro_input_code = open('macro-input.txt', 'r').read()
# print(macro_input_file)  # For user verification

# Tokenizing each line
macro_code_tokenized_by_line = macro_input_code.split('\n')
# Tokenizing each word
macro_code_tokenized_by_word = list(macro_code_tokenized_by_line)  # For matching size
for i in range(0, len(macro_code_tokenized_by_word) - 1):
    macro_code_tokenized_by_word[i] = macro_code_tokenized_by_word[i].split(' ')  # Splitting each line on a space
# print(macro_code_tokenized_by_word)  # For Debugging

# TODO Main Loop Starts Here

for i in range(0, len(macro_code_tokenized_by_line) - 1):
    if 'MACRO' in macro_code_tokenized_by_word[i][0]:
        macro_found(i)

        # TODO Macro Processing Function Call

    # TODO What when Macro is nor found.

# print(mdt)
# print(mdtc)
# print(mnt)
# print(mntc)
