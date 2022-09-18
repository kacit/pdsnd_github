"""This application will display and analyse Bikeshare data for the US
cities of Chicago, New York City and Washington.

The data was supplied in comma separated value files (.csv)
format, with the first row containing column names.

There are two parts to the app:

1. this part allows the user to print to console a full 'pandas'
dataframe dataset, or just a part of the data, according to the user's
choice of city, columns & rows.

2. this part allows the user to run various statistical analysis on
their chosen city dataset.

'Pandas' needs to be installed for the application to run.

Optionally,'Colorama' and 'Rich' should also be installed to enhance the
visual experience. The application will check for and install these
modules if any are found missing.
"""

# IMPORTS :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
import textwrap
import os
# from os import system
import time as t
import importlib as il
import subprocess as sp
import sys as s
import pandas as pd

# GLOBAL VARIABLES ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
text_border = ":"
console_columns = int
parent_process_state = bool

required_modules_list = ["colorama", "rich"]
installed_modules_list = []
missing_modules_list = []
missing_modules_names = ""
q_install_missing_modules = ""
current_module = ""
progress_bar_bool_state = False

is_colorama_installed = False
is_rich_installed = False

choose_continue_or_exit = ""

allowed_city_choices = ("c","n","w")
allowed_data_display_choices = ("d","a")
allowed_data_analysis_choices = range(1, 12)  

letters_of_the_alphabet_list = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

city_choice_lower = ""
city_name = ""

city_or_data_analysis_choice = str

data_anlysis_type_lower_case = ""
data_anlysis_type_name = ""

csv_filename = ""

raw_data_rows_int = 0
raw_data_display_rows = 0
raw_data_display_cols = []

full_df = pd.DataFrame
city_data_loaded = pd.DataFrame
working_df = pd.DataFrame
constructed_df = pd.DataFrame

number_of_df_rows = int

city_csv_file_name = ""

display_all_rows = False
no_of_rows = 0

working_df_columns_list = []
working_df_columns_str = ""

filtered_cols_list = []
filtered_cols_str = ""

filtered_cols_index_positions_list = []

raw_data_cols_list = []
raw_data_cols_str = ""
raw_data_rows_str_lower = ""

q_confirm_cols_choice = ""

chosen_data_analysis_option_int = int

data_analysis_type_choice = int

data_analysis_one_name = ""
data_analysis_two_name = ""
data_analysis_three_name = ""
data_analysis_four_name = ""
data_analysis_five_name = ""
data_analysis_six_name = ""
data_analysis_seven_name = ""
data_analysis_eight_name = ""
data_analysis_nine_name = ""
data_analysis_ten_name = ""
data_analysis_eleven_name = ""
data_analysis_twelve_name = ""

rerun_text_based_app = False

# COMMON FUNCTIONS :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

def join_str_to_fixed_no_of_characters(text_str=str, number_of_joins=int):
	"""builds a string the length of the console width as called by
	set_text_border_to_console_width(text_border_str=str)

	Parameters
	----------
	parameter 1 : text_str=str
		description: the text string used in the built string

	parameter 2: number_of_joins=int
	description: the number of console columns (console width) = joins
	for repeating the text string

	Returns
	-------
	return: str: new_length_str
		description: new_length_str: returns a string of length console
		width
	"""
	
	new_length_str = ""
	
	for i in range(number_of_joins):
	
		joined_text = (text_str.join(text_str))
  
		new_length_str += joined_text
  
		i = i + 1

	return new_length_str

def set_text_border_to_console_width(text_border_str=str):
	"""manages the build of a string the length of the console width
	using function join_str_to_fixed_no_of_characters(text_str=str,
	number_of_joins=int)

	Parameters
	----------
	parameter : str: text_border_str=str
		description: the base string used to build the console width
		string

	Returns
	-------
	return: str: console_width_text_border_str
		description: manages the build of a string the length of the
		console width
	"""
	
	global console_columns
 
	console_columns, lines = os.get_terminal_size()
 
	console_width_text_border_str = join_str_to_fixed_no_of_characters(text_border_str, console_columns)

	return console_width_text_border_str

console_width_text_border = set_text_border_to_console_width(text_border)

def wrap_console_text_display(unshaped_text):
	"""uses the 'textwrap' module to wrap the console text display to
	fit the console width at code execution time

	Parameters
	----------
	parameter : str: unshaped_text
		description: the input block of unwrapped text

	Returns
	-------
	return: str: shaped_text
		description: returns the text block with lines set to wrap to
		the console width at code execution time
	"""

	wrapper = textwrap.TextWrapper(width=(console_columns), replace_whitespace=False, drop_whitespace=False, expand_tabs=True, tabsize=1)

	shaped_text = wrapper.fill(text=unshaped_text)

	return shaped_text

def app_exit_simple():
	"""displays a simple exit message and then actions a graceful
			termination of the app

	Parameters
	----------
	parameter : nil
		description: nil

	Returns
	-------
	return: 1. print: simple_app_exit_message 2. s.exit()
		description: returns a message "Thanks for using the
		app...goodbye" then terminates the app
	"""

	print(simple_app_exit_message)

	pause(2)

	s.exit()

def clear_console():
	"""clears the console when called

	Parameters
	----------
	parameter : nil
		description: nil

	Returns
	-------
	return: os.system('cls||clear')
		description: returns an instruction to clear the console
	"""

	print(simple_app_exit_message)

	os.system('cls||clear')

# def all_terms_clear():
# 	"""clears the console when called

# 	Parameters
# 	----------
# 	parameter : nil
# 		description: nil

# 	Returns
# 	-------
# 	return: clears the console when called
# 		description: clears the console when called
# 	"""

# 	cls = lambda: system("cls")
# 	cls()

# 	print("\033[H\033[J")

def pause(secs):
	"""a convenience function to pause the code execution for a input
	length of time

	Parameters
	----------
	parameter : int: secs
		description: the input integer value used to set pause length

	Returns
	-------
	return: t.sleep(secs)
		description: returns a code sleep action of duration 'secs'
	"""
	
	t.sleep(secs)

def convert_list_to_string(input_list):
	"""converts a list to a string

	Parameters
	----------
	parameter_one : str: input_list
		description: the input list for conversion to a string

	Returns
	-------
	return: str: (seperation_str.join(input_list))
		description: returns a string composed of list items joined by
		seperation_str value 
	"""

	seperation_str = ", "

	return (seperation_str.join(input_list))

def invalid_choice_plain():
	"""returns a plain text message (no 'Colorama' syntax) stating that
	the input value wasn't valid

	Parameters
	----------
	parameter_one : str: input_list
		description: the input list for conversion to a string

	Returns
	-------
	return: str: invalid_choice_message
		description: returns an invalid choice message
	"""

	invalid_choice_message = (f"\n\n\n{console_width_text_border}\n\nYour choice wasn't valid, please choose again...\n\n{console_width_text_border}\n\n\n")

	return invalid_choice_message

def print_q_install_missing_modules_message():
	"""prints a message asking the user to install missing modules
	before continuing

	Parameters
	----------
	parameter_one : nil
		description: nil

	Returns
	-------
	return: print: print_q_install_missing_modules
		description: returns a message asking the user to install
		modules which have been detected as not installed
	"""
	
	global missing_modules_names
	
	print_q_install_missing_modules = print(q_install_missing_modules)
	
	return print_q_install_missing_modules


# SIMPLE TEXT ELEMENTS :::::::::::::::::::::::::::::::::::::::::::::::::
simple_welcome_message = (f"\n\n\n{console_width_text_border}\n\nWelcome to the Bikeshare Data Display & Analysis App\n\n{console_width_text_border}\n\n")

simple_app_exit_message = (f"\n\n{console_width_text_border}\n\nThanks for using the app...goodbye\n\n{console_width_text_border}\n\n")

# CHECK FOR & INSTALL MISSING REQUIRED MODULES :::::::::::::::::::::::::
def check_for_missing_required_modules():
	"""checks installed modules against the required_modules_list,
	creates lists of the missing modules if any are found and also
	generates a message asking whether to install the missing modules or
	not

	Parameters
	----------
	parameter_one : nil
		description: nil

	Returns
	-------
	return 1: list: missing_modules_list
		description: list of missing modules that need to be installed
		before continuing
	return 2: str: missing_modules_names
		description: a string of the list of missing modules that need
		to be installed before continuing
	return 3: q_install_missing_modules
		description: a message describing the missing modules, which
		also asks wether to install these or not
	"""

	global missing_modules_list
	global missing_modules_names
	global q_install_missing_modules

	for m in required_modules_list:

		try:

			globals()[m] = il.import_module(m)

		except ImportError:

			missing_modules_list.append(m)

	missing_modules_names = convert_list_to_string(missing_modules_list)

	q_install_missing_modules_text_block_one = "Additional modules need to be installed to get the best from this app:"

	q_install_missing_modules_text_block_one_shaped = wrap_console_text_display(q_install_missing_modules_text_block_one)

	q_install_missing_modules = (f"\n\n{console_width_text_border}\n\n{q_install_missing_modules_text_block_one_shaped}\n\n>>> {missing_modules_names}\n\n\n* Hit ENTER to install these\n\n* Or choose 'x' to exit\n\n{console_width_text_border}\n\n")
 
	return missing_modules_list, missing_modules_names, q_install_missing_modules

def install_missing_module(current_install_module):
	"""installs a single missing module when called by function
	install_missing_required_modules(missing_modules_list) and generates
	a variable containing the current module just installed and a list
	of the modules just installed

	Parameters
	----------
	parameter_one : str: current_install_module
		description: the name of the module to be installed

	Returns
	-------
	return 1: str: current_module
		description: returns a str variable containing the current
		module just installed
	return 2: list: installed_modules_list
		description: returns a list of the modules just installed
	return 3: action: named module install
		description: installs the current named module
	"""

	global current_module
	
	try:

		sp.check_call([s.executable, "-m", "pip", "install",
					  "-q", "-q", "-q", current_install_module])
		globals()[current_install_module] = il.import_module(current_install_module)
		installed_modules_list.append(current_install_module)

		current_module = current_install_module

	except ImportError:

		print("\n")

		print("The install of module {} failed. Please hit ENTER to exit & install the missing modules manually before continuing".format(
			str(current_install_module)))

	return current_module, installed_modules_list

# def set_process_state(bool_state):
# 	"""sets the variable start_process_state to bool_state value

# 	Parameters
# 	----------
# 	parameter_one : str: bool_state
# 		description: a variable holding the sting value 'True' or
#       'False'

# 	Returns
# 	-------
# 	return: bool: start_process_state
# 		description: returns the variable start_process_state set to a
#       boolian value of either 'True' or 'False'
# 	"""

# 	start_process_state = bool_state

# 	return start_process_state

def run_progress_bar():
	"""displays a progress bar during module installation when called by
	install_missing_required_modules(missing_modules_list)

	Parameters
	----------
	parameter : nil
		description: nil

	Returns
	-------
	return: plain text progress bar
		description: returns a plain text progress bar for display
		during module installation
	"""
	
	global console_columns

	try:

		dot = ["."]

		print(f"Installing {current_module}", end="", flush=True)

		for i in range(5):
			
			print(*dot, end="", flush=True)

			pause(1)

		print("\n")

	except Exception as e:

		print(e)

def install_missing_required_modules(missing_modules_list):
	"""manages the install of missing modules. If a module fails to
	install then a message is displayed prompting the user to install
	the problem module manually

	Parameters
	----------
	parameter : missing_modules_list
		description: the list of moduless needing to be installed

	Returns
	-------
	return: manages the install of missing modules
		description: calls install_missing_module(m)
	"""
	
	for m in missing_modules_list:

		try:

			install_missing_module(m)

			run_progress_bar()
			
		except ImportError:
			
			print("\n")

			print("The install of module {} failed. Please hit ENTER to exit & install the missing modules manually before continuing".format(str(current_module)))
			
			break
			
	return

def check_essential_modules_are_installed():
	"""checks that the essential modules are installed.
 
	NOTE: THIS NEEDS WORK: THE MODULES LISTED HERE NEED TO CORRELATE
	WITH THE MODULES IN required_modules_list AND THE FUNCTION'S GLOBAL
	VARIABLES. CAN BE REFACTORED TO REMOVE MODULE NAME DEPENDENCY

	Parameters
	----------
	parameter : nil
		description: nil

	Returns
	-------
	return: is_colorama_installed
		description: returns 'True' if module 'Colorama' is installed
	return: is_rich_installed
		description: returns 'True' if module 'Rich' is installed
	"""
	
	global is_colorama_installed
	global is_rich_installed

	for m in s.modules:
			
		if m == "colorama":

			is_colorama_installed = True
			
		elif m == "rich":

			is_rich_installed = True

# ENABLE COLORAMA FUNCTIONALITY ::::::::::::::::::::::::::::::::::::::::
def enable_colorama_functionality():
	"""this function enables the app to run using 'Colorama' to enhance
	the visual data display in the console. It allows the dynamic import
	of module 'Colorama' depending upon whether or not 'Colorama' has been
	installed. The main body of the code exists within this function

	Parameters
	----------
	parameter : nil
		description: nil

	Returns
	-------
	return: nil
		description: 'Colorama' rendered output for display on the
		console
	"""
	
	global is_colorama_installed
	
	# checks if Colorama IS NOT installed; if not installed then exit
	if is_colorama_installed == False:
	 
		colorama_install_message_text_block_one = "To get the best experience from this app, 'Colorama' should first be installed. We were unable to install this automatically, so the app will now close to allow you to complete this yourself"

		colorama_install_message_text_block_one_shaped = wrap_console_text_display(colorama_install_message_text_block_one)
	 
		print(f"\n\n{console_width_text_border}\n\n{colorama_install_message_text_block_one_shaped}\n\n{console_width_text_border}\n\n")

		app_exit_simple()

	# if Colorama IS installed, then proceed
	else:
	
		import colorama
		from colorama import Fore, Back, Style
		colorama.init(autoreset=True)

		app_exit_message_text_block_one = (f"{Fore.CYAN}\n\n\n{console_width_text_border}\n\nThanks for using the app...goodbye\n\n{console_width_text_border}\n\n{Style.RESET_ALL}")

		app_exit_message_text_block_one_shaped = wrap_console_text_display(app_exit_message_text_block_one)

		app_exit_message = (f"{app_exit_message_text_block_one_shaped}")
  
		q_welcome_and_choose_city_text_block_one = (f"{Fore.CYAN}\n\n\n{console_width_text_border}\n\nThis application will display and analyse US Bikeshare data, please choose a city dataset to work with:\n\n{console_width_text_border}\n\n{Style.RESET_ALL}")

		q_welcome_and_choose_city_text_block_two = (f"{Fore.CYAN} * {Fore.GREEN}Chicago{Fore.CYAN} - select {Fore.MAGENTA}c\n\n{Style.RESET_ALL}")

		q_welcome_and_choose_city_text_block_three = (f"{Fore.CYAN} * {Fore.GREEN}New York City{Fore.CYAN} - select {Fore.MAGENTA}n\n\n{Style.RESET_ALL}")

		q_welcome_and_choose_city_text_block_four = (f"{Fore.CYAN} * {Fore.GREEN}Washington{Fore.CYAN} - select {Fore.MAGENTA}w\n\n{Style.RESET_ALL}")

		q_welcome_and_choose_city_text_block_five = (f"{Fore.CYAN}\n\n >>> {Style.RESET_ALL}")

		q_welcome_and_choose_city_text_block_one_shaped = wrap_console_text_display(q_welcome_and_choose_city_text_block_one)

		q_welcome_and_choose_city_text_block_two_shaped = wrap_console_text_display(q_welcome_and_choose_city_text_block_two)

		q_welcome_and_choose_city_text_block_three_shaped = wrap_console_text_display(q_welcome_and_choose_city_text_block_three)

		q_welcome_and_choose_city_text_block_four_shaped = wrap_console_text_display(q_welcome_and_choose_city_text_block_four)

		q_welcome_and_choose_city_text_block_five_shaped = wrap_console_text_display(q_welcome_and_choose_city_text_block_five)

		q_welcome_and_choose_city = (f"{q_welcome_and_choose_city_text_block_one_shaped}{q_welcome_and_choose_city_text_block_two_shaped}{q_welcome_and_choose_city_text_block_three_shaped}{q_welcome_and_choose_city_text_block_four_shaped}{q_welcome_and_choose_city_text_block_five_shaped}")

		def print_invalid_choice():
			"""composes a general purpose 'invalid choice' message

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: str: invalid_choice
				description: returns a varaible containing a general
				purpose 'invalid choice' message string
			"""

			invalid_choice_text_block_one = (f"{Fore.CYAN}\n\n\n{console_width_text_border}\n\n{Fore.RED}Your choice wasn't valid, please choose again...{Fore.CYAN}\n\n{console_width_text_border}\n\n{Style.RESET_ALL}")

			invalid_choice_text_block_one_shaped = wrap_console_text_display(invalid_choice_text_block_one)

			invalid_choice = (f"{invalid_choice_text_block_one_shaped}")

			clear_console()
   
			print(invalid_choice)
   
			pause(2)

			clear_console()
   
			return invalid_choice

		def q_choose_all_or_some_rows():
			"""composes a message asking the user to choose to display
			the full dataset or just the top portion of the dataset

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: str: q_choose_all_or_some_rows
				description: returns a variable containing a message
				string asking the user to choose to display the full
				dataset or just the top portion of the dataset
			"""

			q_choose_all_or_some_rows_text_block_one = (f"{Fore.CYAN}\n\n\n{console_width_text_border}\n\nPlease choose the number of rows to display:\n\n{console_width_text_border}\n\n{Style.RESET_ALL}")

			q_choose_all_or_some_rows_text_block_two = (f"{Fore.CYAN} * to view the {Fore.GREEN}FULL DATASET{Fore.CYAN} select {Fore.MAGENTA}f{Style.RESET_ALL}")
   
			q_choose_all_or_some_rows_text_block_three = (f"{Fore.CYAN}\n\n * alternatively, to display just the {Fore.GREEN}TOP PORTION{Fore.CYAN} of the dataset enter the {Fore.MAGENTA}number of rows{Fore.CYAN} you wish to see{Style.RESET_ALL}")
   
			q_choose_all_or_some_rows_text_block_four = (f"{Fore.CYAN}\n\n\n >>> {Style.RESET_ALL}")

			q_choose_all_or_some_rows_text_block_one_shaped = wrap_console_text_display(q_choose_all_or_some_rows_text_block_one)

			q_choose_all_or_some_rows_text_block_two_shaped = wrap_console_text_display(q_choose_all_or_some_rows_text_block_two)
   
			q_choose_all_or_some_rows_text_block_three_shaped = wrap_console_text_display(q_choose_all_or_some_rows_text_block_three)
   
			q_choose_all_or_some_rows_text_block_four_shaped = wrap_console_text_display(q_choose_all_or_some_rows_text_block_four)
	  
			q_choose_all_or_some_rows = (f"{q_choose_all_or_some_rows_text_block_one_shaped}{q_choose_all_or_some_rows_text_block_two_shaped}{q_choose_all_or_some_rows_text_block_three_shaped}{q_choose_all_or_some_rows_text_block_four_shaped}")
	
			return q_choose_all_or_some_rows

		def q_choose_data_display_or_analysis():
			"""composes a message asking the user to choose to run the
			data display or data analysis portions of the app

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: str: q_choose_data_display_or_analysis
				description: returns a variable containing a message
				string asking the user to choose to run the data display
				or data analysis portions of the app
			"""

			q_choose_data_display_or_analysis_text_block_one = (f"{Fore.CYAN}\n\n\n{console_width_text_border}\n\nPlease choose a data analysis option:\n\n{console_width_text_border}\n\n{Style.RESET_ALL}")

			q_choose_data_display_or_analysis_text_block_two = (f"{Fore.CYAN} * To {Fore.GREEN}display {Fore.CYAN}Bikeshare data for {Fore.GREEN}{city_name}{Fore.CYAN} - choose {Fore.MAGENTA}d\n\n{Style.RESET_ALL}")

			q_choose_data_display_or_analysis_text_block_three = (f"{Fore.CYAN} Or\n\n{Style.RESET_ALL}")

			q_choose_data_display_or_analysis_text_block_four = (f"{Fore.CYAN} * To {Fore.GREEN}analyse {Fore.CYAN}Bikeshare data for {Fore.GREEN}{city_name}{Fore.CYAN} - choose {Fore.MAGENTA}a\n\n{Style.RESET_ALL}")

			q_choose_data_display_or_analysis_text_block_five = (f"{Fore.CYAN}\n\n >>> {Style.RESET_ALL}")

			q_choose_data_display_or_analysis_text_block_one_shaped = wrap_console_text_display(q_choose_data_display_or_analysis_text_block_one)

			q_choose_data_display_or_analysis_text_block_two_shaped = wrap_console_text_display(q_choose_data_display_or_analysis_text_block_two)

			q_choose_data_display_or_analysis_text_block_three_shaped = wrap_console_text_display(q_choose_data_display_or_analysis_text_block_three)

			q_choose_data_display_or_analysis_text_block_four_shaped = wrap_console_text_display(q_choose_data_display_or_analysis_text_block_four)

			q_choose_data_display_or_analysis_text_block_five_shaped = wrap_console_text_display(q_choose_data_display_or_analysis_text_block_five)

			q_choose_data_display_or_analysis = (f"{q_choose_data_display_or_analysis_text_block_one_shaped}{q_choose_data_display_or_analysis_text_block_two_shaped}{q_choose_data_display_or_analysis_text_block_three_shaped}{q_choose_data_display_or_analysis_text_block_four_shaped}{q_choose_data_display_or_analysis_text_block_five_shaped}")

			return q_choose_data_display_or_analysis
   
		def choose_all_or_some_cols_str():
			"""composes a message asking the user to choose to display
			all columns, or to select columns for display manually

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: str: choose_all_or_some_cols_str
				description: returns a variable containing a message
				string asking the user to choose to display all columns,
				or to select columns for display manually
			"""

			choose_all_or_some_cols_str_text_block_one = (f"{Fore.CYAN}\n\n\n{console_width_text_border}\n\nPlease choose the columns you wish displayed:\n\n{console_width_text_border}\n\n{Style.RESET_ALL}")

			choose_all_or_some_cols_str_text_block_two = (f"{Fore.CYAN} * to display {Fore.MAGENTA}ALL{Fore.CYAN} columns hit {Fore.MAGENTA}ENTER\n\n{Style.RESET_ALL}")

			choose_all_or_some_cols_str_text_block_three = (f"{Fore.CYAN} * Otherwise select columns from:\n\n{Style.RESET_ALL}")

			choose_all_or_some_cols_str_text_block_four = (f"{Fore.GREEN}{working_df_columns_str}\n\n{Style.RESET_ALL}")

			choose_all_or_some_cols_str_text_block_five = (f"{Fore.CYAN} ...by selecting {Fore.MAGENTA}s{Style.RESET_ALL}")

			choose_all_or_some_cols_str_text_block_six = (f"{Fore.CYAN}\n\n\n >>> {Style.RESET_ALL}")

			choose_all_or_some_cols_str_text_block_one_shaped = wrap_console_text_display(choose_all_or_some_cols_str_text_block_one)

			choose_all_or_some_cols_str_text_block_two_shaped = wrap_console_text_display(choose_all_or_some_cols_str_text_block_two)

			choose_all_or_some_cols_str_text_block_three_shaped = wrap_console_text_display(choose_all_or_some_cols_str_text_block_three)

			choose_all_or_some_cols_str_text_block_four_shaped = wrap_console_text_display(choose_all_or_some_cols_str_text_block_four)

			choose_all_or_some_cols_str_text_block_five_shaped = wrap_console_text_display(choose_all_or_some_cols_str_text_block_five)

			choose_all_or_some_cols_str_text_block_six_shaped = wrap_console_text_display(choose_all_or_some_cols_str_text_block_six)

			choose_all_or_some_cols_str = input(f"{choose_all_or_some_cols_str_text_block_one_shaped}{choose_all_or_some_cols_str_text_block_two_shaped}{choose_all_or_some_cols_str_text_block_three_shaped}{choose_all_or_some_cols_str_text_block_four_shaped}{choose_all_or_some_cols_str_text_block_five_shaped}{choose_all_or_some_cols_str_text_block_six_shaped}")

			return choose_all_or_some_cols_str

		def q_data_analysis_options():
			"""composes a message asking the user to choose a data
			analysis option to run

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: str: q_data_analysis_options
				description: returns a variable containing a message
				asking the user to choose a data analysis option to run
			"""

			q_data_analysis_options_text_block_one = (f"{Fore.CYAN}\n\n\n{console_width_text_border}\n\nPlease select an analysis to run on your chosen city dataset:\n\n{console_width_text_border}\n\n{Style.RESET_ALL}")

			q_data_analysis_options_text_block_two = (f"{Fore.CYAN} * {Fore.GREEN}The most common month of the year Bikeshare was used{Fore.CYAN} - select {Fore.MAGENTA}1\n\n{Style.RESET_ALL}")

			q_data_analysis_options_text_block_three = (f"{Fore.CYAN} * {Fore.GREEN}The most common week of the month Bikeshare was used{Fore.CYAN} - select {Fore.MAGENTA}2\n\n{Style.RESET_ALL}")

			q_data_analysis_options_text_block_four = (f"{Fore.CYAN} * {Fore.GREEN}The most common hour of the day Bikeshare was used{Fore.CYAN} - select {Fore.MAGENTA}3\n\n{Style.RESET_ALL}")

			q_data_analysis_options_text_block_five = (f"{Fore.CYAN} * {Fore.GREEN}The most common start station at which Bikeshare was used{Fore.CYAN} - select {Fore.MAGENTA}4\n\n{Style.RESET_ALL}")

			q_data_analysis_options_text_block_six = (f"{Fore.CYAN} * {Fore.GREEN}The most common end station at which Bikeshare was used{Fore.CYAN} - select {Fore.MAGENTA}5\n\n{Style.RESET_ALL}")

			q_data_analysis_options_text_block_seven = (f"{Fore.CYAN} * {Fore.GREEN}The most common Bikeshare trip from start to end stations{Fore.CYAN} - select {Fore.MAGENTA}6\n\n{Style.RESET_ALL}")

			q_data_analysis_options_text_block_eight = (f"{Fore.CYAN} * {Fore.GREEN}Total travel time{Fore.CYAN} - select {Fore.MAGENTA}7\n\n{Style.RESET_ALL}")

			q_data_analysis_options_text_block_nine = (f"{Fore.CYAN} * {Fore.GREEN}Average travel time{Fore.CYAN} - select {Fore.MAGENTA}8\n\n{Style.RESET_ALL}")

			q_data_analysis_options_text_block_ten = (f"{Fore.CYAN} * {Fore.GREEN}Counts of each user type{Fore.CYAN} - select {Fore.MAGENTA}9\n\n{Style.RESET_ALL}")

			q_data_analysis_options_text_block_eleven = (f"{Fore.CYAN} * {Fore.GREEN}Counts of each gender (only available for NYC and Chicago){Fore.CYAN} - select {Fore.MAGENTA}10\n\n{Style.RESET_ALL}")

			q_data_analysis_options_text_block_twelve = (f"{Fore.CYAN} * {Fore.GREEN}Earliest, most recent, most common year of birth (only available for NYC and Chicago){Fore.CYAN} - select {Fore.MAGENTA}11\n\n{Style.RESET_ALL}")

			q_data_analysis_options_text_block_thirteen = (f"{Fore.CYAN}\n\n >>> {Style.RESET_ALL}")

			q_data_analysis_options_text_block_one_shaped = wrap_console_text_display(q_data_analysis_options_text_block_one)

			q_data_analysis_options_text_block_two_shaped = wrap_console_text_display(q_data_analysis_options_text_block_two)

			q_data_analysis_options_text_block_three_shaped = wrap_console_text_display(q_data_analysis_options_text_block_three)

			q_data_analysis_options_text_block_four_shaped = wrap_console_text_display(q_data_analysis_options_text_block_four)

			q_data_analysis_options_text_block_five_shaped = wrap_console_text_display(q_data_analysis_options_text_block_five)

			q_data_analysis_options_text_block_six_shaped = wrap_console_text_display(q_data_analysis_options_text_block_six)

			q_data_analysis_options_text_block_seven_shaped = wrap_console_text_display(q_data_analysis_options_text_block_seven)

			q_data_analysis_options_text_block_eight_shaped = wrap_console_text_display(q_data_analysis_options_text_block_eight)

			q_data_analysis_options_text_block_nine_shaped = wrap_console_text_display(q_data_analysis_options_text_block_nine)

			q_data_analysis_options_text_block_ten_shaped = wrap_console_text_display(q_data_analysis_options_text_block_ten)

			q_data_analysis_options_text_block_eleven_shaped = wrap_console_text_display(q_data_analysis_options_text_block_eleven)

			q_data_analysis_options_text_block_twelve_shaped = wrap_console_text_display(q_data_analysis_options_text_block_twelve)

			q_data_analysis_options_text_block_thirteen_shaped = wrap_console_text_display(q_data_analysis_options_text_block_thirteen)

			q_data_analysis_options = (f"{q_data_analysis_options_text_block_one_shaped}{q_data_analysis_options_text_block_two_shaped}{q_data_analysis_options_text_block_three_shaped}{q_data_analysis_options_text_block_four_shaped}{q_data_analysis_options_text_block_five_shaped}{q_data_analysis_options_text_block_six_shaped}{q_data_analysis_options_text_block_seven_shaped}{q_data_analysis_options_text_block_eight_shaped}{q_data_analysis_options_text_block_nine_shaped}{q_data_analysis_options_text_block_ten_shaped}{q_data_analysis_options_text_block_eleven_shaped}{q_data_analysis_options_text_block_twelve_shaped}{q_data_analysis_options_text_block_thirteen_shaped}")
			
			return q_data_analysis_options

		def q_rerun_or_exit():
			"""composes a message asking the user to choose to run
			another Bikeshare data display or analysis, or exit the app

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: str: q_rerun_or_exit
				description: returns a variable containing a message
				asking the user to choose to run another Bikeshare data
				display or analysis, or exit the app
			"""

			q_rerun_or_exit_text_block_one = (f"{Fore.CYAN}\n\n\n{console_width_text_border}\n\nIf you'd like to run another Bikeshare data display or analysis then please choose to:\n\n{console_width_text_border}\n\n{Style.RESET_ALL}")

			q_rerun_or_exit_text_block_two = (f"{Fore.CYAN} * {Fore.GREEN}view Bikeshare data{Fore.CYAN} - select {Fore.MAGENTA}d\n\n{Style.RESET_ALL}")

			q_rerun_or_exit_text_block_three = (f"{Fore.CYAN} * {Fore.GREEN}analyse Bikeshare data{Fore.CYAN} - select {Fore.MAGENTA}a\n\n{Style.RESET_ALL}")

			q_rerun_or_exit_text_block_four = (f"{Fore.CYAN} * Or just hit {Fore.MAGENTA}ENTER{Fore.CYAN} to exit the app\n\n{Style.RESET_ALL}")

			q_rerun_or_exit_text_block_five = (f"{Fore.CYAN}\n\n >>> {Style.RESET_ALL}")

			q_rerun_or_exit_text_block_one_shaped = wrap_console_text_display(q_rerun_or_exit_text_block_one)

			q_rerun_or_exit_text_block_two_shaped = wrap_console_text_display(q_rerun_or_exit_text_block_two)

			q_rerun_or_exit_text_block_three_shaped = wrap_console_text_display(q_rerun_or_exit_text_block_three)

			q_rerun_or_exit_text_block_four_shaped = wrap_console_text_display(q_rerun_or_exit_text_block_four)

			q_rerun_or_exit_text_block_five_shaped = wrap_console_text_display(q_rerun_or_exit_text_block_five)

			q_rerun_or_exit = (f"{q_rerun_or_exit_text_block_one_shaped}{q_rerun_or_exit_text_block_two_shaped}{q_rerun_or_exit_text_block_three_shaped}{q_rerun_or_exit_text_block_four_shaped}{q_rerun_or_exit_text_block_five_shaped}")
   
			return q_rerun_or_exit

		def q_choose_another_city_str():
			"""composes a message asking the user to choose another
			Bikeshare city, continue the the current one

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: str: q_choose_another_city_str
				description: returns a variable containing a message
				asking the user to choose another Bikeshare city,
				continue the the current one
			"""

			q_choose_another_city_str_text_block_one = (f"{Fore.CYAN}\n\n\n{console_width_text_border}\n\nWould you like to choose another Bikeshare city to work with?\n\n{console_width_text_border}\n\n{Style.RESET_ALL}")

			q_choose_another_city_str_text_block_two = (f"{Fore.CYAN} * select {Fore.MAGENTA}y{Fore.CYAN} to choose another city dataset{Fore.CYAN}\n\n{Style.RESET_ALL}")

			q_choose_another_city_str_text_block_three = (f"{Fore.CYAN} * or hit {Fore.MAGENTA}ENTER{Fore.CYAN} to continue with {Fore.GREEN}{city_name}{Fore.CYAN}\n\n{Style.RESET_ALL}")

			q_choose_another_city_str_text_block_four = (f"{Fore.CYAN}\n\n >>> {Style.RESET_ALL}")

			q_choose_another_city_str_text_block_one_shaped = wrap_console_text_display(q_choose_another_city_str_text_block_one)

			q_choose_another_city_str_text_block_two_shaped = wrap_console_text_display(q_choose_another_city_str_text_block_two)

			q_choose_another_city_str_text_block_three_shaped = wrap_console_text_display(q_choose_another_city_str_text_block_three)

			q_choose_another_city_str_text_block_four_shaped = wrap_console_text_display(q_choose_another_city_str_text_block_four)

			q_choose_another_city_str = input(f"{q_choose_another_city_str_text_block_one_shaped}{q_choose_another_city_str_text_block_two_shaped}{q_choose_another_city_str_text_block_three_shaped}{q_choose_another_city_str_text_block_four_shaped}")
   
			return q_choose_another_city_str
	
		def rich_not_installed_message():
			"""composes a message advising the user that 'Rich' was not
			found to be installed, and to install it before	rerunning
			the function to display the dataset in a 'Rich' format

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: str: rich_not_installed
				description: returns a variable containing a message
				advising the user that 'Rich' was not found to be
				installed, and to install it before trying to run the
				function to display the dataset in a 'Rich' format
			"""

			rich_not_installed = input(f"{Fore.YELLOW}\n\n\n{console_width_text_border}\n\nUnfortunately '{Fore.GREEN}Rich{Fore.YELLOW}' was found not to be installed. Please install '{Fore.GREEN}Rich{Fore.YELLOW}' before retrying this function\n\nHit {Fore.MAGENTA}ENTER{Fore.YELLOW} to cancel and return\n\n{console_width_text_border}\n\n\n>>> {Style.RESET_ALL}")
	 
			return rich_not_installed

		# COLORAMA DEPENDANT FUNCTIONS ::::::::::::::::::::::::::::::::::::::::
		def app_exit():
			"""displays an exit message and then actions a graceful
			termination of the app

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: 1. print: simple_app_exit_message 2. s.exit()
				description: returns a message "Thanks for using the
				app...goodbye" then terminates the app
			"""

			print(app_exit_message)

			pause(1)

			s.exit()

		def clear_app_exit():
			"""combines to first clear the console, then display an exit
			message on the console, then terminates the app

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: 1. print: simple_app_exit_message 2. s.exit()
				description: clears the console, displays a message "Thanks for using the
				app...goodbye" on the console, then terminates the app
			"""
	  
			pause(1)
	  
			clear_console()
	  
			app_exit()
	  
		def generate_csv_filename(city_name):
			"""creates a full csv file filename based upon the user's
			chosen city

			Parameters
			----------
			parameter : city_name
				description: the name of the user's chosen city

			Returns
			-------
			return: LiteralString: csv_filename
				description: returns the full csv file filename based upon the user's
			chosen city
			"""
	  
			global csv_filename
   
			s = ""
	  
			filename = (city_name.lower().replace(" ", "_"), ".csv")
   
			csv_filename = s.join(filename)
   
			return csv_filename

		def run_loading_progress_indicator():
			"""builds a loading progress indicator, generally
			run before a dataset is being composed for console display.
			It's actually a false indicator to indicate that something
			is happening behind the scenes, and it doesn't relate to the
			time taken to compose the dataset for display

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: str: 
				description: builds a loading progress indicator, 
				generally run before a dataset is being composed for
				console display
			"""
	  
			clear_console()
	  
			global console_columns

			try:

				dot = [(f"{Fore.CYAN}.{Style.RESET_ALL}")]

				print(f"{Fore.CYAN}\n\n{console_width_text_border}\n\n{Style.RESET_ALL}")
				print(f"{Fore.CYAN}Data now loading", end="", flush=True)

				for i in range(5):
					
					print(*dot, end="", flush=True)

					pause(1)
	 
			except Exception as e:

				print(e)
	
			clear_console()

		def choose_df_columns():
			"""composes a message asking the user to choose which
			dataframe columns to display

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: str: filtered_cols_str
				description: returns a variable containing a message
				asking the user to choose which dataframe columns
				to display
			"""

			global working_df_columns_list
			global working_df_columns_str
			global filtered_cols_str
			global filtered_cols_list
			global raw_data_cols_list
			global raw_data_cols_str

			global full_df
			global working_df
   
			global filtered_cols_index_positions_list   

			filtered_cols_list = []
			filtered_cols_str = ""

			good_cols_choice_char = bool

			clear_console()

			working_df_columns_text_block_one = (f"{Fore.CYAN}\n\n\n{console_width_text_border}\n\nYou can now choose which columns to display\n\n{console_width_text_border}\n\n{Style.RESET_ALL}")

			working_df_columns_text_block_two = (f"{Fore.CYAN} * for each column, hit {Fore.MAGENTA}x{Fore.CYAN} to select that column for display\n\n >>> {Style.RESET_ALL}")

			working_df_columns_text_block_one_shaped = wrap_console_text_display(working_df_columns_text_block_one)

			working_df_columns_text_block_two_shaped = wrap_console_text_display(working_df_columns_text_block_two)
	
			print(f"{working_df_columns_text_block_one_shaped}{working_df_columns_text_block_two_shaped}")

			# step through a series of messages asking user to select columns to display
			for col in working_df_columns_list:

				col_choice_str = input(f"{Fore.CYAN}\n\n\nColumn: {Fore.GREEN}{col}{Fore.CYAN}?\n\n\n >>> {Style.RESET_ALL}")
	
				col_choice = col_choice_str.lower()

				if col_choice == "x":

					filtered_cols_list.append(col)
	 
					col_index = full_df.columns.get_loc(col)
					
					filtered_cols_index_positions_list.append(col_index)

					filtered_cols_index_positions_list = filtered_cols_index_positions_list
	 
					good_cols_choice_char = True

				elif col_choice == "":

					continue

				else:
	 
					if col_choice != "x":

						if col_choice == "":

							pass

						clear_console()

						restart_cols_selection_message_str_text_block_one = (f"{Fore.CYAN}\n\n\n{console_width_text_border}\n\n{Fore.RED}Your column choice wasn't valid{Fore.CYAN}\n\n * Please restart your columns selection using {Fore.MAGENTA}x{Fore.CYAN} to make a column choice, or {Fore.MAGENTA}ENTER{Fore.CYAN} to bypass a column\n\n{console_width_text_border}\n\n\n{Style.RESET_ALL}")

						restart_cols_selection_message_str_text_block_one_shaped = wrap_console_text_display(restart_cols_selection_message_str_text_block_one)

						restart_cols_selection_message = (f"{restart_cols_selection_message_str_text_block_one_shaped}")

						print(restart_cols_selection_message)

						pause(3)

						good_cols_choice_char = False

						pass
  
					break

			if good_cols_choice_char == False:

				choose_df_columns()	

			# convert the df columns list to a string
			filtered_cols_str = convert_list_to_string(filtered_cols_list)

			raw_data_cols_list = []
			raw_data_cols_str = ""
			raw_data_cols_list = filtered_cols_list
			raw_data_cols_str = filtered_cols_str
			
			return filtered_cols_str

		def get_raw_data_display_cols():
			"""formats a list of the chosen dataframe columns, then
			presents a message asking the user to choose to display all
			or some of the columns. If some columns, then calls
			choose_df_columns() to allow the user to make their columns
			choice

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: str:
				description: creates a formatted list of dataframe
			columns, then presents a message asking the user to choose
			to display all or some columns
			"""

			global working_df
			global working_df_columns_list
			global working_df_columns_str
			global filtered_cols_str
			global q_confirm_cols_choice
			global raw_data_cols_list
			global raw_data_cols_str

			# drop the first column from the list of df columns
			working_df.drop(columns = working_df.columns[0], axis = 1, inplace= True)

			# get a list of df columns
			working_df_columns_list = working_df.columns.values.tolist()
   
			# convert the df columns list to a string
			working_df_columns_str = convert_list_to_string(working_df_columns_list)

			clear_console()

			choose_all_or_some_cols_lower = choose_all_or_some_cols_str().lower()

			raw_data_cols_list = []
			raw_data_cols_str = ""

			raw_data_cols_list = working_df_columns_list
			raw_data_cols_str = working_df_columns_str

			if choose_all_or_some_cols_lower == "s":
   
				choose_df_columns() # filtered_cols_str is returned

				q_confirm_cols_choice = ""
			
				def ask_to_confirm_cols_choice():
					"""displays a list of the chosen dataframe columns,
					then presents a message asking the user to confirm
					the selections made, or to re-run column selection
					again
	 
					Parameters
					----------
					parameter : nil
						description: nil

					Returns
					-------
					return:
						description: displays a list of the chosen
						dataframe columns, then presents a message
						asking the user to confirm the selections made,
						or to re-run column selection again
					"""
		
					global q_confirm_cols_choice

					clear_console()

					q_confirm_cols_choice_text_block_one = (f"{Fore.CYAN}\n\n\n{console_width_text_border}\n\nYou chose these columns:\n\n{Style.RESET_ALL}")

					q_confirm_cols_choice_text_block_two = (f"{Fore.CYAN}* {Fore.GREEN}{filtered_cols_str}{Fore.CYAN}\n\n{console_width_text_border}\n\n{Style.RESET_ALL}")

					q_confirm_cols_choice_text_block_three = (f"{Fore.CYAN} * ...hit {Fore.MAGENTA}ENTER{Fore.CYAN} to proceed with this choice\n\n{Style.RESET_ALL}")

					q_confirm_cols_choice_text_block_four = (f"{Fore.CYAN} * Or select {Fore.MAGENTA}a{Fore.CYAN} to choose again\n\n{Style.RESET_ALL}")

					q_confirm_cols_choice_text_block_five = (f"{Fore.CYAN}\n\n >>> {Style.RESET_ALL}")

					q_confirm_cols_choice_text_block_one_shaped = wrap_console_text_display(q_confirm_cols_choice_text_block_one)

					q_confirm_cols_choice_text_block_two_shaped = wrap_console_text_display(q_confirm_cols_choice_text_block_two)

					q_confirm_cols_choice_text_block_three_shaped = wrap_console_text_display(q_confirm_cols_choice_text_block_three)

					q_confirm_cols_choice_text_block_four_shaped = wrap_console_text_display(q_confirm_cols_choice_text_block_four)

					q_confirm_cols_choice_text_block_five_shaped = wrap_console_text_display(q_confirm_cols_choice_text_block_five)

					q_confirm_cols_choice = input(f"{q_confirm_cols_choice_text_block_one_shaped}{q_confirm_cols_choice_text_block_two_shaped}{q_confirm_cols_choice_text_block_three_shaped}{q_confirm_cols_choice_text_block_four_shaped}{q_confirm_cols_choice_text_block_five_shaped}")

				ask_to_confirm_cols_choice()
	
				while q_confirm_cols_choice == "a":
		 
					choose_df_columns()
	 
					q_confirm_cols_choice = ""
	 
					ask_to_confirm_cols_choice()

			elif choose_all_or_some_cols_lower == "":
	   
				return

			else:

				count = 4
		
				while (choose_all_or_some_cols_lower != "" and (count > 0)) or (choose_all_or_some_cols_lower != "s" and (count > 0)):

					count -= 1
	 
					print_invalid_choice()
	 
					choose_all_or_some_cols_lower = choose_all_or_some_cols_str().lower()
	 
					if (choose_all_or_some_cols_lower == "") or (choose_all_or_some_cols_lower == "s"):

						break

		def calculate_df_total_rows():
			"""calculates the total number of the base dataframe rows

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: int: full_df_rows_count
				description: returns the total number of the base
				dataframe rows
			"""

			# generate raw df
			full_df = pd.read_csv(csv_filename)

			full_df_rows_count = full_df.shape[0]

			return full_df_rows_count
  
		def get_raw_data_display_rows():
			"""manages the process of asking the user whether to display
			all or some dataset rows

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: Literal:True: display_all_rows
				description: returns confirmation that the user has
				chosen to display all rows
			return: int: raw_data_rows_int
				description: returns the number of rows that the user
				has chosen to display
			"""
	  
			global display_all_rows
			global raw_data_rows_int
			global raw_data_rows_str_lower
			global number_of_df_rows
			global working_df
   
			clear_console()

			# display a message asking for ALL rows or a NUMBER of rows to be chosen
			raw_data_rows_str = input(q_choose_all_or_some_rows())

			raw_data_rows_str_lower = raw_data_rows_str.lower()
   
			try:
				
				raw_data_rows_int = int(raw_data_rows_str_lower)

			except:
		
				count = 4
	
				while ((raw_data_rows_int == 0) or (raw_data_rows_str_lower != "f")) and (count > 0):
		 
					full_df_total_rows_count = calculate_df_total_rows()

					if 1 <= raw_data_rows_int <= full_df_total_rows_count or (raw_data_rows_str_lower == "f"):
	
						break
	 
					print_invalid_choice()
	
					count -= 1
	 
					raw_data_rows_str = input(q_choose_all_or_some_rows())

					raw_data_rows_str_lower = raw_data_rows_str.lower()

					try:
	  
						raw_data_rows_int = int(raw_data_rows_str_lower)
	  
					except:
	  
						pass

				if (raw_data_rows_int == 0) and (raw_data_rows_str_lower != "f"):

					clear_app_exit()
   
			if raw_data_rows_str_lower == "f":
   
				raw_data_rows_int = 0
   
			if raw_data_rows_int == 0:
	
				# choose to display all rows
				display_all_rows = True

				return display_all_rows

			elif raw_data_rows_int > 0:
	
				# choose to display a block of rows at a time
				return raw_data_rows_int

			else:
	
				pause(1)
	   
				clear_app_exit()

		def get_rows_and_cols_dimensions():
			"""brings together the dataframe rows and columns dimensions
			and generates a dataframe based upon all rows, a 'head' of
			rows or the user's chosen rows.
   
			Parent of nested function:
   				construct_df_with_specified_rows_and_cols()

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: dataframe: working_df
				description: returns a dataframe sized according to the
				users chosen rows and columns, prior to generating a
				dataframe for display
			"""
			
			global display_all_rows
			global raw_data_rows_int

			global full_df
			global working_df
			global constructed_df
	  
			generate_csv_filename(city_name)

			# get the rows to display
			get_raw_data_display_rows()
   
			# generate raw df
			full_df = pd.read_csv(csv_filename)

			if display_all_rows:
	
				working_df = full_df
				
			else:
	   
				# generate df for top no of rows
				top_rows_df = full_df.head(raw_data_rows_int)

				working_df = top_rows_df

			# get the columns to display
			get_raw_data_display_cols()

			def construct_df_with_specified_rows_and_cols():
				"""creates a dataframe based upon the user's chosen rows
				and columns dimensions

				Parameters
				----------
				parameter : nil
					description: nil

				Returns
				-------
				return: dataframe: constructed_df
					description: returns a dataframe based upon the
					user's chosen rows and columns dimensions
				"""

				global working_df
				global constructed_df
				global city_data_loaded
				global number_of_df_rows

				global filtered_cols_index_positions_list

				city_data_loaded = pd.read_csv(csv_filename)
	
				if raw_data_rows_int == 0:
		
					number_of_df_rows = len(city_data_loaded)
	 
				else:
		
					number_of_df_rows = raw_data_rows_int

				rows_and_cols_configured_df = city_data_loaded.loc[range(0,number_of_df_rows), raw_data_cols_list]
	
				constructed_df = rows_and_cols_configured_df

			construct_df_with_specified_rows_and_cols()

			working_df = constructed_df

		def format_and_display_raw_data_df(raw_df=pd.DataFrame):
			"""formats & displays a dataframe of the chosen number of
			rows and columns in then offers the user a choice to display
			a 'Rich' formatted version of the dataframe and displays
			this if selected
   
			Parent of nested functions:
   				q_full_data_display_warning()
				q_enter_number_of_rows_per_block_or_choose_full_data_
					display()
				run_showing_bikeshare_data_message()
				run_showing_bikeshare_data_preload()
				run_showing_bikeshare_data()
				run_rich_table_display()
				choose_y_n_rich_run_rich_table_display()
	
			Parameters
			----------
			parameter : working_df
				description: the correctly user-dimensioned dataframe

			Returns
			-------
			return 1: dataFrame
				description: returns a dataframe of the chosen number of
			rows and columns formatted by 'Colorama' for console display
			return 2: dataFrame
				description: returns a dataframe of the chosen number of
			rows and columns formatted by 'Rich' for console display
			"""
	  
			global working_df
			global city_data_loaded
   
			global display_all_rows

			pd.options.display.width = 0
			pd.set_option('display.max_rows', None)
			pd.set_option('display.max_columns', 0)
			pd.set_option('display.width', None)
			pd.set_option('display.max_colwidth', 50)
			pd.set_option('display.colheader_justify', 'center')

			def q_enter_number_of_rows_per_block_or_choose_full_data_display():
				"""generates a question asking the user to choose a
				block size in rows to step through the dataset display,
				or to choose to display the full dataset in one
				operation 

				Parameters
				----------
				parameter : nil
					description: nil

				Returns
				-------
				return: str: q_enter_number_of_rows_per_block_or_choose_
								full_data_display
					description: returns the number of rows in a block
				"""

				q_enter_number_of_rows_per_block_or_choose_full_data_display_text_block_one = (f"{Fore.CYAN}\n\n\n{console_width_text_border}\n\nPlease choose to display a block of rows, or the full dataset in one:\n\n{console_width_text_border}\n\n{Style.RESET_ALL}")

				q_enter_number_of_rows_per_block_or_choose_full_data_display_text_block_two = (f"{Fore.CYAN} *  to step through the data in blocks enter the {Fore.MAGENTA}NUMBER OF ROWS{Fore.CYAN} per block\n\n{Style.RESET_ALL}")

				q_enter_number_of_rows_per_block_or_choose_full_data_display_text_block_three = (f"{Fore.CYAN} * ...or hit {Fore.MAGENTA}ENTER{Fore.CYAN} to display {Fore.MAGENTA}ALL{Fore.CYAN} rows\n\n{Style.RESET_ALL}")

				q_enter_number_of_rows_per_block_or_choose_full_data_display_text_block_four = (f"{Fore.YELLOW} WARNING! DON'T CHOOSE TO DISPLAY ALL ROWS IN A SINGLE OPERATION UNLESS YOUR COMPUTER HAS THE RESOURCES TO COPE!\n\n{Style.RESET_ALL}")

				q_enter_number_of_rows_per_block_or_choose_full_data_display_text_block_five = (f"{Fore.YELLOW} WARNING! DEPENDING UPON YOUR COMPUTER RESOURCES, DISPLAYING ALL ROWS IN A SINGLE OPERATION MAY TAKE A WHILE TO COMPLETE!\n\n{Style.RESET_ALL}")
	
				q_enter_number_of_rows_per_block_or_choose_full_data_display_text_block_six = (f"{Fore.CYAN}\n\n >>> {Style.RESET_ALL}")

				q_enter_number_of_rows_per_block_or_choose_full_data_display_text_block_one_shaped = wrap_console_text_display(q_enter_number_of_rows_per_block_or_choose_full_data_display_text_block_one)

				q_enter_number_of_rows_per_block_or_choose_full_data_display_text_block_two_shaped = wrap_console_text_display(q_enter_number_of_rows_per_block_or_choose_full_data_display_text_block_two)

				q_enter_number_of_rows_per_block_or_choose_full_data_display_text_block_three_shaped = wrap_console_text_display(q_enter_number_of_rows_per_block_or_choose_full_data_display_text_block_three)

				q_enter_number_of_rows_per_block_or_choose_full_data_display_text_block_four_shaped = wrap_console_text_display(q_enter_number_of_rows_per_block_or_choose_full_data_display_text_block_four)

				q_enter_number_of_rows_per_block_or_choose_full_data_display_text_block_five_shaped = wrap_console_text_display(q_enter_number_of_rows_per_block_or_choose_full_data_display_text_block_five)

				q_enter_number_of_rows_per_block_or_choose_full_data_display_text_block_six_shaped = wrap_console_text_display(q_enter_number_of_rows_per_block_or_choose_full_data_display_text_block_six)

				q_enter_number_of_rows_per_block_or_choose_full_data_display = input(f"{q_enter_number_of_rows_per_block_or_choose_full_data_display_text_block_one_shaped}{q_enter_number_of_rows_per_block_or_choose_full_data_display_text_block_two_shaped}{q_enter_number_of_rows_per_block_or_choose_full_data_display_text_block_three_shaped}{q_enter_number_of_rows_per_block_or_choose_full_data_display_text_block_four_shaped}{q_enter_number_of_rows_per_block_or_choose_full_data_display_text_block_five_shaped}{q_enter_number_of_rows_per_block_or_choose_full_data_display_text_block_six_shaped}")
	
				return q_enter_number_of_rows_per_block_or_choose_full_data_display

			def run_showing_bikeshare_data_message():
				"""generates a message informing the user that Bikeshare
				data for their chosen city is being displayed

				Parameters
				----------
				parameter : nil
					description: nil

				Returns
				-------
				return: print: 
					description: returns a message informing the user that Bikeshare
					data for their chosen city is being displayed
				"""

				print(f"{Fore.CYAN}{console_width_text_border}{Style.RESET_ALL}")
				print(f"{Fore.CYAN}\n\nNow showing Bikeshare data for {Fore.GREEN}{city_name}{Fore.CYAN}...\n\n{Style.RESET_ALL}")

			def run_showing_bikeshare_data_preload():
				"""runs a series of actions that clear the console, run
				the loading progress indicator and shows a message
				informing the user that Bikeshare data for their chosen
				city is being displayed

				Parameters
				----------
				parameter : nil
					description: nil

				Returns
				-------
				return: console display actions
					description: clears the console, runs the loading
				progress indicator and shows a message informing the
				user that Bikeshare data for their chosen city is being
				displayed
				"""
	
				clear_console()

				run_loading_progress_indicator()

				clear_console()

				run_showing_bikeshare_data_message()
	
				pause(3)

			def run_showing_bikeshare_data():
				"""prints a 'Colorama' formatted dataframe, of the
				correct number of rows and columns, either a full
				dataset, or a rows/columns limited dataset, as decided
				by the user
	
				Parent of nested functions:
					print_formatted_dataset_table()
					end_of_data_check()

				Parameters
				----------
				parameter : nil
					description: nil

				Returns
				-------
				return: print
					description: prints a 'Colorama' formatted
					dataframe, of the correct number of rows and columns
				"""
	   
				global parent_process_state
	   
				if display_all_rows:
		
					no_of_block_rows = None
		
					no_of_block_rows_int = None

					clear_console()

					no_of_block_rows = q_enter_number_of_rows_per_block_or_choose_full_data_display()

					try:

						no_of_block_rows_int = int(no_of_block_rows)

					except:

						no_of_block_rows_int = 0

					count = 4

					while (no_of_block_rows_int == 0 and (count > 0)):

						try:

							no_of_block_rows_int = int(no_of_block_rows)

							if no_of_block_rows == "" or no_of_block_rows_int > 0:
		
								break

						except:
							
							pass

						if no_of_block_rows == "" or no_of_block_rows_int > 0:

							break
   
						print_invalid_choice()
	  
						count -= 1

						no_of_block_rows = q_enter_number_of_rows_per_block_or_choose_full_data_display()

					if (no_of_block_rows == "") or (no_of_block_rows_int > 0):
		 
						pass

					else:

						app_exit()

					# if ALL, then display the full df
					if no_of_block_rows == "":

						parent_process_state = True
	  
						run_showing_bikeshare_data_preload()

						def print_formatted_dataset_table():
							"""prints a 'Colorama' formatted FULL
							dataframe, of the correct number of rows
							and columns

							Parameters
							----------
							parameter : nil
								description: nil

							Returns
							-------
							return: print
								description: prints a 'Colorama'
								formatted FULL dataframe, of the correct
								number of rows and columns
							"""
		  
							global parent_process_state
	   
							print(f"{Fore.CYAN}{console_width_text_border}{Style.RESET_ALL}")
							print(f"{Fore.GREEN}{working_df}{Style.RESET_ALL}")
							print(f"{Fore.CYAN}{console_width_text_border}{Style.RESET_ALL}")
	  
							parent_process_state = False
	   
						print_formatted_dataset_table()

					# if by block size, then display block & step thru mechanism
					elif no_of_block_rows_int > 0:

						run_showing_bikeshare_data_preload()

						rows_block_start = 0
						rows_block_end = no_of_block_rows_int

						def end_of_data_check():
							"""calculates if the end of the dataset
							being displayed has been reached or not

							Parameters
							----------
							parameter : nil
								description: nil

							Returns
							-------
							return: boolean 'True' or 'False'
								description: returns boolean 'True' or
								'False', depending on whether or not the
								end of the
								dataframe rows display has been reached
								or not
							"""
			
							if rows_block_end >= city_data_loaded.shape[0]:
								
								return True
								
							return False    
						
						eod = end_of_data_check()

						# loop through displayed dataset a block of n rows at a time
						while eod == False: 
	   
							eod = bool(end_of_data_check())
					
							cols_configured_df = city_data_loaded.loc[:, raw_data_cols_list]

							block_of_rows_df = cols_configured_df.iloc[rows_block_start:rows_block_end]

							print(f"{Fore.CYAN}\n\n{console_width_text_border}\n\n{Fore.GREEN}{block_of_rows_df}{Fore.CYAN}\n\n{console_width_text_border}\n\n{Style.RESET_ALL}")


							def continue_with_block_display_or_exit():

								continue_or_exit_text_block_one = (f"{Fore.CYAN}\n{console_width_text_border}\nHit {Fore.MAGENTA}ENTER{Fore.CYAN} to continue, or {Fore.MAGENTA}x{Fore.CYAN} to exit the dataset display{Style.RESET_ALL}")
		
								continue_or_exit_text_block_two = (f"{Fore.CYAN}\n{console_width_text_border}\n\n{Style.RESET_ALL}")

								continue_or_exit_text_block_three = (f"{Fore.CYAN}\n\n >>> {Style.RESET_ALL}")

								continue_or_exit_text_block_one_shaped = wrap_console_text_display(continue_or_exit_text_block_one)

								continue_or_exit_text_block_two_shaped = wrap_console_text_display(continue_or_exit_text_block_two)

								continue_or_exit_text_block_three_shaped = wrap_console_text_display(continue_or_exit_text_block_three)

								continue_or_exit = input(f"{continue_or_exit_text_block_one_shaped}{continue_or_exit_text_block_two_shaped}{continue_or_exit_text_block_three_shaped}")
		
								return continue_or_exit
							
							continue_or_exit_lower = continue_with_block_display_or_exit().lower()

							count = 4
		
							while (continue_or_exit_lower != "x" and (count > 0)) or (continue_or_exit_lower != "" and (count > 0)):
		   
								if (continue_or_exit_lower == "x") or (continue_or_exit_lower == ""):

									break
		   
								print_invalid_choice()

								count -= 1
		
								continue_or_exit_lower = ""		
  
								continue_or_exit_lower = continue_with_block_display_or_exit().lower()
		
		   
							if continue_or_exit_lower == "x":
								
								break
							
							rows_block_start = rows_block_end
							rows_block_end = rows_block_start + no_of_block_rows_int
							
							eod = end_of_data_check()
							
							if eod == True:
								
								block_of_rows_df = cols_configured_df.iloc[rows_block_start:rows_block_end]
								
								print(f"{Fore.CYAN}\n\n{console_width_text_border}\n\n{Fore.GREEN}{block_of_rows_df}{Fore.CYAN}\n\n{console_width_text_border}\n\n{Style.RESET_ALL}")
								
								break
							
							elif (bool(continue_or_exit_lower) == False):
								
								continue
							
							else:
								
								break
	
				else:

					run_showing_bikeshare_data_preload()

					print(f"{Fore.CYAN}{console_width_text_border}{Style.RESET_ALL}")
					print(f"{Fore.CYAN}\n\n{console_width_text_border}\n\n{Fore.GREEN}{working_df}{Fore.CYAN}\n\n{console_width_text_border}\n\n{Style.RESET_ALL}")
					print(f"{Fore.CYAN}{console_width_text_border}{Style.RESET_ALL}")

				pause(2)

			def run_rich_table_display():
				"""checks to see if the 'Rich' module is installed, 
				imports 'print from 'Rich', then prints the head
				(currently set to 50 rows) of the 'Rich' formatted
				dataframe

				Parameters
				----------
				parameter : nil
					description: nil

				Returns
				-------
				return: print
					description: prints the head
					(currently set to 50 rows) of the 'Rich' formatted
					dataframe
				"""

				global is_rich_installed
				
				# if Rich IS NOT installed then exit
				if is_rich_installed == False:
		
					rich_not_installed_message()
	 
					pause(3)

					pass

				# proceed if Rich IS installed then proceed
				else:
		
					# import rich
					from rich import print
 
					print(f"{Fore.GREEN}{working_df.head(50)}{Style.RESET_ALL}")
	 
			run_showing_bikeshare_data()
   
			def choose_y_n_rich_run_rich_table_display():
				"""generates a message asking the user if they wish to
				display the currently displayed dataset with 'Rich'
				formatting

				Parameters
				----------
				parameter : nil
					description: nil

				Returns
				-------
				return: str: y_n_rich_run_rich_table_display
					description: returns a variable containing a text
					string message asking the user if they wish to
					display the currently displayed dataset with 'Rich'
					formatting
				"""
	
				y_n_rich_run_rich_table_display_text_block_one = (f"{Fore.CYAN}\n\n\n{console_width_text_border}\n\n{Fore.YELLOW}WARNING: EXPERIMENTAL!\n\n{Style.RESET_ALL}")

				y_n_rich_run_rich_table_display_text_block_two = (f"{Fore.CYAN}Would you like to see a possibly improved table display using the {Fore.GREEN}'Rich'{Fore.CYAN} Python Library?\n\n{Style.RESET_ALL}")

				y_n_rich_run_rich_table_display_text_block_three = (f"{Fore.CYAN}The following table will show {Fore.MAGENTA}up to the top 50 lines{Fore.CYAN} of the data in a '{Fore.GREEN}Rich{Fore.CYAN}' format\n\n{Style.RESET_ALL}")

				y_n_rich_run_rich_table_display_text_block_four = (f"{Fore.YELLOW}TIP: THE WIDER YOUR CONSOLE THE BETTER THE DISPLAY!{Fore.CYAN}\n\n{console_width_text_border}\n\n{Style.RESET_ALL}")

				y_n_rich_run_rich_table_display_text_block_five = (f"{Fore.CYAN} ...to proceed, hit {Fore.MAGENTA}ENTER{Fore.CYAN}\n\n{Style.RESET_ALL}")

				y_n_rich_run_rich_table_display_text_block_six = (f"{Fore.CYAN} ...or choose {Fore.MAGENTA}x{Fore.CYAN} to bypass this option\n\n{Style.RESET_ALL}")

				y_n_rich_run_rich_table_display_text_block_seven = (f"{Fore.CYAN}\n\n >>> {Style.RESET_ALL}")

				y_n_rich_run_rich_table_display_text_block_one_shaped = wrap_console_text_display(y_n_rich_run_rich_table_display_text_block_one)

				y_n_rich_run_rich_table_display_text_block_two_shaped = wrap_console_text_display(y_n_rich_run_rich_table_display_text_block_two)

				y_n_rich_run_rich_table_display_text_block_three_shaped = wrap_console_text_display(y_n_rich_run_rich_table_display_text_block_three)

				y_n_rich_run_rich_table_display_text_block_four_shaped = wrap_console_text_display(y_n_rich_run_rich_table_display_text_block_four)

				y_n_rich_run_rich_table_display_text_block_five_shaped = wrap_console_text_display(y_n_rich_run_rich_table_display_text_block_five)

				y_n_rich_run_rich_table_display_text_block_six_shaped = wrap_console_text_display(y_n_rich_run_rich_table_display_text_block_six)

				y_n_rich_run_rich_table_display_text_block_seven_shaped = wrap_console_text_display(y_n_rich_run_rich_table_display_text_block_seven)

				y_n_rich_run_rich_table_display = input(f"{y_n_rich_run_rich_table_display_text_block_one_shaped}{y_n_rich_run_rich_table_display_text_block_two_shaped}{y_n_rich_run_rich_table_display_text_block_three_shaped}{y_n_rich_run_rich_table_display_text_block_four_shaped}{y_n_rich_run_rich_table_display_text_block_five_shaped}{y_n_rich_run_rich_table_display_text_block_six_shaped}{y_n_rich_run_rich_table_display_text_block_seven_shaped}")
	
				return y_n_rich_run_rich_table_display
   
			y_n_rich_run_rich_table_display = choose_y_n_rich_run_rich_table_display()
   
			y_n_rich_run_rich_table_display_lower = y_n_rich_run_rich_table_display.lower()

			if y_n_rich_run_rich_table_display_lower == "x":
	 
				clear_console()

				choose_rerun_or_exit()
	   
			elif y_n_rich_run_rich_table_display_lower == "":
	   
				run_showing_bikeshare_data_preload()

				run_rich_table_display()

				pause(2)

				choose_rerun_or_exit()

			else:

				count = 4

				while (y_n_rich_run_rich_table_display_lower != "" and count > 0) or (y_n_rich_run_rich_table_display_lower != "x" and count > 0):
		
					print_invalid_choice()

					count -= 1

					y_n_rich_run_rich_table_display = choose_y_n_rich_run_rich_table_display()
		
					y_n_rich_run_rich_table_display_lower = y_n_rich_run_rich_table_display.lower()

					if y_n_rich_run_rich_table_display_lower == "":

						run_showing_bikeshare_data_preload()

						run_rich_table_display()

						pause(2)

						choose_rerun_or_exit()

					elif y_n_rich_run_rich_table_display_lower == "x":
			
						clear_console()

						choose_rerun_or_exit()
	  
				if (y_n_rich_run_rich_table_display_lower != "") or (y_n_rich_run_rich_table_display_lower != "x"):

					app_exit()

		def city_options():
			"""displays a message asking the user to choose a city, for
			other functions to work with that city's dataset

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return 1: str: city_choice_lower
				description: returns a varable containing the user's
			lower-case city choice letter
			return 2: str: city_name
				description: returns a varable containing the user's
				city choice name
			"""
			
			global city_choice_lower
			global city_name

			clear_console()
			
			city_choice = input(q_welcome_and_choose_city)
			
			city_choice_lower = city_choice.lower()
   
			if city_choice_lower == "c":
				
				city_name = "Chicago"
				
			elif city_choice_lower == "n":
				
				city_name = "New York City"
				
			elif city_choice_lower == "w":
				
				city_name = "Washington"
   
			return city_choice_lower, city_name
	
		def choose_city():
			"""checks the user's city choice from city_options() is valid

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: nil
				description: exits the app if the user's city choice is
				invalid after 5 trys
			"""

			global city_choice_lower

			city_options()

			count = 4
		
			while city_choice_lower not in allowed_city_choices and count > 0:
	
				print_invalid_choice()

				city_options()

				count -= 1
	
			if city_choice_lower:
				
				pass

			else:
	   
				clear_app_exit()
		
		def data_display_options():
			"""asks the user to choose between dataset display or
			dataset analysis

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: data_anlysis_type_lower_case
				description: returns a variable containing the user's
				lowercase letter choice between 'd' and 'a'
			return: data_anlysis_type_name
				description: returns a variable containing the user's
				lowercase letter choice between 'Display' and 'Analyse'
			"""

			global data_anlysis_type_lower_case
			global data_anlysis_type_name
			global city_name

			clear_console()
   
			data_display_choice = input(q_choose_data_display_or_analysis())
			
			data_anlysis_type_lower_case = data_display_choice.lower()
   
			if data_anlysis_type_lower_case == "d":
				
				data_anlysis_type_name = "Display"
				
			elif data_anlysis_type_lower_case == "a":
				
				data_anlysis_type_name = "Analyse"
   
			return data_anlysis_type_lower_case, data_anlysis_type_name

		def choose_data_analysis_type():
			"""

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: nil
				description: returns ...
			"""
			
			global data_anlysis_type_lower_case

			data_display_options()

			count = 4

			while data_anlysis_type_lower_case not in allowed_data_display_choices and count > 0:
				
				print_invalid_choice()
				
				data_display_options()
	
				count -= 1
	
			# if 'd' then display raw data
			if data_anlysis_type_lower_case == "d": 

				manage_raw_data_display()
	
			# if 'a' then display statistical information about the data
			elif data_anlysis_type_lower_case == "a":
		
				manage_data_analysis_display()
	
			else:
	   
				clear_app_exit()

		def manage_raw_data_display():
			"""

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: nil
				description: returns ...
			"""

			# generated an unformatted df, correct for rows & cols
			get_rows_and_cols_dimensions()
   
			# format & display formatted df, filtered for rows & cols
			format_and_display_raw_data_df(working_df)

		def q_run_this_analysis(data_analysis_name):
			"""

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: nil
				description: returns ...
			"""
	  
			clear_console()
			
			q_run_this_analysis_text_block_one = (f"{Fore.CYAN}\n\n\n{console_width_text_border}\n\nYou've chosen to find:\n\n{Style.RESET_ALL}")

			q_run_this_analysis_text_block_two = (f"{Fore.CYAN}{data_analysis_name}\n\n{console_width_text_border}\n\n{Style.RESET_ALL}")

			q_run_this_analysis_text_block_three = (f"{Fore.CYAN} * Hit {Fore.MAGENTA}ENTER{Fore.CYAN} to continue\n\n{Style.RESET_ALL}")

			q_run_this_analysis_text_block_four = (f"{Fore.CYAN} * or {Fore.MAGENTA}x{Fore.CYAN} to return to the data analysis menu\n\n{Style.RESET_ALL}")

			q_run_this_analysis_text_block_five = (f"{Fore.CYAN}\n\n >>> {Style.RESET_ALL}")

			q_run_this_analysis_text_block_one_shaped = wrap_console_text_display(q_run_this_analysis_text_block_one)

			q_run_this_analysis_text_block_two_shaped = wrap_console_text_display(q_run_this_analysis_text_block_two)

			q_run_this_analysis_text_block_three_shaped = wrap_console_text_display(q_run_this_analysis_text_block_three)

			q_run_this_analysis_text_block_four_shaped = wrap_console_text_display(q_run_this_analysis_text_block_four)

			q_run_this_analysis_text_block_five_shaped = wrap_console_text_display(q_run_this_analysis_text_block_five)

			q_run_this_analysis = input(f"{q_run_this_analysis_text_block_one_shaped}{q_run_this_analysis_text_block_two_shaped}{q_run_this_analysis_text_block_three_shaped}{q_run_this_analysis_text_block_four_shaped}{q_run_this_analysis_text_block_five_shaped}")

			q_run_this_analysis_lower = q_run_this_analysis.lower()

			if q_run_this_analysis_lower == "x":
				
				run_this_data_analysis_y_n = False
				
			else:
				
				run_this_data_analysis_y_n = True
			
			return run_this_data_analysis_y_n

		def generate_raw_df():
			"""

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: nil
				description: returns ...
			"""
	  
			generate_csv_filename(city_name)
   
			# 1. generate raw df
			raw_df = pd.read_csv(csv_filename)

			# set pandas basic display options
			pd.options.display.width = 0
			pd.set_option('display.max_rows', None)
			pd.set_option('display.max_columns', 0)
			pd.set_option('display.width', None)
			pd.set_option('display.colheader_justify', 'center')

			optimised_raw_df = raw_df.copy(deep = True)
			
			# convert 'Start Time' column data type to datetime data type, overwriting values with timestamps
			optimised_raw_df["Start Time"] = pd.to_datetime(optimised_raw_df["Start Time"])
   
			# tidy trip duration column by converting it from float to int
			optimised_raw_df["Trip Duration"] = optimised_raw_df["Trip Duration"].astype(int)

			return optimised_raw_df

		def data_analysis_one_calculation(optimised_raw_df):
			"""returns the result of the calculation of the most common
			month(s) of the year Bikeshare was used

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: unbound / any: print_most_common_moty_conv
				description: returns ...
			"""

			# STEP 1: convert 'Start Time' column data type to datetime data type, overwriting values with timestamps
			optimised_raw_df["Start Time"] = pd.to_datetime(optimised_raw_df["Start Time"])

			# STEP 2: make a dataframe copy of the new dataset
			df_datetime = optimised_raw_df.copy(deep = True)

			# STEP 3: extract month of the year from timestamps
			start_month_of_the_year = df_datetime['Start Time'].dt.month

			# STEP 4: insert a new  month of the year column into the df
			df_datetime.insert(loc=2, column='Month Of The Year', value=start_month_of_the_year)

			# STEP 5: make a dataframe copy of the new dataset
			extended_df = df_datetime.copy(deep = True)
   
			# STEP 6: find the most common month of the year 
			most_common_moty = extended_df['Month Of The Year'].mode()

			# STEP 7: in case of more than one mode value, place the mode valu(s) in a list
			most_common_moty_list = most_common_moty.tolist()
   
			# STEP 8: create a month labels dictionary
			month_labels = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
	
			# STEP 8: puts all values of the most common month of the year into a list and converts integer value(s) to a string for display
			print_most_common_moty_conv_str = ""

			for i in most_common_moty:
	   
				print_most_common_moty_conv = most_common_moty.apply(lambda x: month_labels[x]).to_string(index=False)
	
				print_most_common_moty_conv_str += print_most_common_moty_conv

			return print_most_common_moty_conv

		def data_analysis_two_calculation(optimised_raw_df):
			"""returns the result of the calculation of the most common
			day(s) of the week Bikeshare was used

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: unbound / any: print_most_common_dotw_conv
				description: returns ...
			"""
	  
			# STEP 1: convert 'Start Time' column data type to datetime data type, overwriting values with timestamps
			optimised_raw_df["Start Time"] = pd.to_datetime(optimised_raw_df["Start Time"])

			# STEP 2: make a dataframe copy of the new dataset
			df_datetime = optimised_raw_df.copy(deep = True)

			# STEP 3: extract day of the week from timestamps
			start_day = df_datetime['Start Time'].dt.weekday
   
			# STEP 4: insert a new day of the week column into the df
			df_datetime.insert(loc=2, column='Day Of The Week', value=start_day)

			# STEP 5: make a dataframe copy of the new dataset
			extended_df = df_datetime.copy(deep = True)
   
			# STEP 6: find the most common day of the week
			most_common_dotw = extended_df['Day Of The Week'].mode()

			# STEP 7: create a weekdays labels dictionary
			day_labels = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6:"Saturday", 7:"Sunday"}

			# STEP 8: puts all values of the most common day of the week into a list and converts integer value(s) to a string for display
			print_most_common_dotw_conv_str = ""

			for i in most_common_dotw:
	   
				print_most_common_dotw_conv = most_common_dotw.apply(lambda x: day_labels[x]).to_string(index=False)
	
				print_most_common_dotw_conv_str += print_most_common_dotw_conv

			return print_most_common_dotw_conv

		def data_analysis_three_calculation(optimised_raw_df):
			"""returns the result of the calculation of the most common
			hour(s) of the day Bikeshare was used

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: str: most_common_hotd_str
				description: returns ...
			"""
	  
			# STEP 1: convert 'Start Time' column data type to datetime data type, overwriting values with timestamps
			optimised_raw_df["Start Time"] = pd.to_datetime(optimised_raw_df["Start Time"])

			# STEP 2: make a dataframe copy of the new dataset
			df_datetime = optimised_raw_df.copy(deep = True)

			# STEP 3: extract hour of the day from timestamps
			start_day = df_datetime['Start Time'].dt.hour
   
			# STEP 4: insert a new hour of the day column into the df
			df_datetime.insert(loc=2, column='Hour of the day', value=start_day)

			# STEP 5: make a dataframe copy of the new dataset
			extended_df = df_datetime.copy(deep = True)
   
			# STEP 6: find the most common hour(s) of the day
			most_common_hotd = extended_df['Hour of the day'].mode()

			# STEP 7: format most common hour of the day series as a list
			most_common_hotd_list = most_common_hotd.tolist()

			# STEP 8: create new list, formatting each list element as **:00
			most_common_hotd_list_ext = [f"{elem}:00" for elem in most_common_hotd_list]

			# STEP 9: merge the most common hour of the day list items to display as a string
			most_common_hotd_str = ", ".join([str(elem) for elem in most_common_hotd_list_ext])
   
			return most_common_hotd_str
		
		def data_analysis_four_calculation(optimised_raw_df):
			"""returns the result of the calculation of the most common
			start station at which Bikeshare was used

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: str: most_common_start_station_list_str
				description: returns ...
			"""

			# STEP 1: find the most common start station
			most_common_start_station = optimised_raw_df['Start Station'].mode()

			# STEP 2: in case of more than one mode value, place the mode value(s) in a list
			most_common_start_station_list = most_common_start_station.tolist()
   
			# STEP 3: join the list mode value(s) into a string for printing
			most_common_start_station_list_str = ", ".join(str(x) for x in most_common_start_station_list)

			return most_common_start_station_list_str

		def data_analysis_five_calculation(optimised_raw_df):
			"""returns the result of the calculation of the most common
			end station at which Bikeshare was used

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: str: most_common_end_station_list_str
				description: returns ...
			"""

			# STEP 1: find the most common end station
			most_common_end_station = optimised_raw_df['End Station'].mode()

			# STEP 2: in case of more than one mode value, place the mode value(s) in a list
			most_common_end_station_list = most_common_end_station.tolist()
   
			# STEP 3: join the list mode value(s) into a string for printing
			most_common_end_station_list_str = ", ".join(str(x) for x in most_common_end_station_list)

			return most_common_end_station_list_str

		def data_analysis_six_calculation(optimised_raw_df):
			"""returns the result of the calculation of the most common
			trip from start to end stations on which Bikeshare was used

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: str: start_end_col_mode_str
				description: returns ...
			"""

			# STEP 1: create new combined start / end stations column
			optimised_raw_df["Start - End Stations"] = optimised_raw_df["Start Station"] + [" - "] + optimised_raw_df["End Station"]

			# STEP 2: make a copy of the df with the new column added
			df_str_ext = optimised_raw_df.copy(deep=True)

			# STEP 3: apply mode() algorythm to new column to find most common start / end stations combination(s)
			start_end_col_mode = df_str_ext["Start - End Stations"].mode()

			# STEP 4: order by (for easier viewing of mode values)
			df_ordered = df_str_ext.sort_values(by=["Start - End Stations"], ascending=True, inplace=False)

			# STEP 6: convert most common start / end stations combination(s) to a list 
			start_end_col_mode_list = start_end_col_mode.tolist()

			# STEP 7: format most common start / end stations combination(s) list as a string for display
			start_end_col_mode_str = ", ".join(str(x) for x in start_end_col_mode_list)
   
			return start_end_col_mode_str

		def data_analysis_seven_calculation(optimised_raw_df):
			"""returns the result of the calculation of the total travel
			time of Bikeshare trips

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: str: sum_of_trip_times_time_qty
				description: returns ...
			"""

			# STEP 1: apply sum calculation to new trip duration column to total all trip durations in seconds
			sum_of_trip_times = optimised_raw_df["Trip Duration"].sum()

			# STEP 2: format new trip duration sum calculation as a string for display
			sum_of_trip_times_time_qty = t.strftime("%H:%M:%S", t.gmtime(sum_of_trip_times))
			
			return sum_of_trip_times_time_qty
	  
		def data_analysis_eight_calculation(optimised_raw_df):
			"""returns the result of the calculation of the average
			travel time of all Bikeshare trips

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: str: avg_of_trip_times_time_qty
				description: returns ...
			"""

			# STEP 1: apply mean calculation to trip duration column to find the average of all trip durations in seconds
			avg_of_trip_times = optimised_raw_df["Trip Duration"].mean()

			# STEP 2: format new trip duration average calculation as a string for display
			avg_of_trip_times_time_qty = t.strftime("%H:%M:%S", t.gmtime(avg_of_trip_times))

			return avg_of_trip_times_time_qty

		def data_analysis_nine_calculation(optimised_raw_df):
			"""returns a calculation of the count of each Bikeshare user
			type

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: any: df_groupby_count
				description: returns ...
			"""

			# # use groupby() and count() to group and count each Bikeshare user type
			df_groupby_count = optimised_raw_df.groupby(['User Type'])['User Type'].count().to_string(header=False)

			return df_groupby_count

		def data_analysis_ten_calculation(optimised_raw_df):
			"""returns the count of each Bikeshare gender type

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: any: df_groupby_count
				description: returns ...
			"""

			# # use groupby() and count() to group and count each Bikeshare gender type
			df_groupby_count = optimised_raw_df.groupby(['Gender'])['Gender'].count().to_string(header=False)

			return df_groupby_count

		def data_analysis_eleven_calculation(optimised_raw_df):
			"""returns the oldest customer's year of birth, the youngest
			customer's year of birth and the most common year of birth
			for all customers

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return 1: int: oldest_customers_yob_int
				description: returns ...
			return 2: int: youngest_customers_yob_int
				description: returns ...
			return 3: str: most_common_customers_yob_mode_str
				description: returns ...
			"""

			# STEP 1: calculate earliest year in the 'Birth Year' column
			oldest_customers_yob = optimised_raw_df['Birth Year'].min()

			# Convert single column to int dtype.
			oldest_customers_yob_int = int(oldest_customers_yob)

			# STEP 2: calculate the most recent year in the 'Birth Year' column
			youngest_customers_yob = optimised_raw_df['Birth Year'].max()
			
			# Convert single column to int dtype.
			youngest_customers_yob_int = int(youngest_customers_yob)

			# STEP 3: get most common year in the 'Birth Year' column
			most_common_customers_yob_df_float = optimised_raw_df['Birth Year'].mode()

			# STEP 4: convert df_float to df_int type
			most_common_customers_yob_df_int = most_common_customers_yob_df_float.astype(int)
			
			# STEP 5: convert df_int type to list
			most_common_customers_yob_df_int_list = most_common_customers_yob_df_int.tolist()
			
			# STEP 6: format list as a string for display
			most_common_customers_yob_mode_str = ", ".join(str(x) for x in most_common_customers_yob_df_int_list)
					
			return oldest_customers_yob_int, youngest_customers_yob_int, most_common_customers_yob_mode_str

		def data_analysis_one():
			"""displays the result of the calculation of the most common
			month of the year in which Bikeshare was used

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: 
				description: returns ...
			"""
	  
			global data_analysis_one_name
	  
			data_analysis_one_name = f"...{Fore.GREEN}the most common month of the year in which Bikeshare was used{Style.RESET_ALL}"
			
			if q_run_this_analysis(data_analysis_one_name) == True:
	   
				clear_console()
   
				most_common_month_of_the_year = data_analysis_one_calculation(generate_raw_df())

				most_common_month_of_the_year_text_block_one = (f"{Fore.CYAN}\n\n\n{console_width_text_border}\n\nThe most common month of the year Bikeshare was used in {Fore.GREEN}{city_name}{Fore.CYAN} was:\n\n{Style.RESET_ALL}")

				most_common_month_of_the_year_text_block_two = (f"{Fore.CYAN} * {Fore.GREEN}{most_common_month_of_the_year}{Fore.CYAN}\n\n{console_width_text_border}\n\n\n{Style.RESET_ALL}")

				most_common_month_of_the_year_text_block_one_shaped = wrap_console_text_display(most_common_month_of_the_year_text_block_one)

				most_common_month_of_the_year_text_block_two_shaped = wrap_console_text_display(most_common_month_of_the_year_text_block_two)

				print(f"{most_common_month_of_the_year_text_block_one_shaped}{most_common_month_of_the_year_text_block_two_shaped}")
	
				choose_rerun_or_exit()

			else:
	   
				manage_data_analysis_display()

		def data_analysis_two():
			"""displays the result of the calculation of the most common
			day of the week in which Bikeshare was used

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: 
				description: returns ...
			"""
			
			global data_analysis_two_name
	  
			data_analysis_two_name = f"...{Fore.GREEN}the most common day of the week in which Bikeshare was used{Style.RESET_ALL}"
			
			if q_run_this_analysis(data_analysis_two_name) == True:
	   
				clear_console()
   
				most_common_day_of_the_week = data_analysis_two_calculation(generate_raw_df())

				most_common_day_of_the_week_text_block_one = (f"{Fore.CYAN}\n\n\n{console_width_text_border}\n\nThe most common day of the week Bikeshare was used in {Fore.GREEN}{city_name}{Fore.CYAN} was:\n\n{Style.RESET_ALL}")

				most_common_day_of_the_week_text_block_two = (f"{Fore.CYAN} * {Fore.GREEN}{most_common_day_of_the_week}{Fore.CYAN}\n\n{console_width_text_border}\n\n\n{Style.RESET_ALL}")

				most_common_day_of_the_week_text_block_one_shaped = wrap_console_text_display(most_common_day_of_the_week_text_block_one)

				most_common_day_of_the_week_text_block_two_shaped = wrap_console_text_display(most_common_day_of_the_week_text_block_two)

				print(f"{most_common_day_of_the_week_text_block_one_shaped}{most_common_day_of_the_week_text_block_two_shaped}")
	
				choose_rerun_or_exit()

			else:
	   
				manage_data_analysis_display()
		
		def data_analysis_three():
			"""displays the result of the calculation of the most common
			hour of the day in which Bikeshare was used

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: 
				description: returns ...
			"""
	  
			global data_analysis_three_name
	  
			data_analysis_three_name = f"...{Fore.GREEN}the most common hour(s) of the day Bikeshare was used{Style.RESET_ALL}"
			
			if q_run_this_analysis(data_analysis_three_name) == True:
	   
				clear_console()
   
				most_common_hour_of_the_day = data_analysis_three_calculation(generate_raw_df())

				most_common_hour_of_the_day_text_block_one = (f"{Fore.CYAN}\n\n\n{console_width_text_border}\n\nThe most common hour of the day Bikeshare was used in {Fore.GREEN}{city_name}{Fore.CYAN} was:\n\n{Style.RESET_ALL}")

				most_common_hour_of_the_day_text_block_two = (f"{Fore.CYAN} * {Fore.GREEN}{most_common_hour_of_the_day}{Fore.CYAN}\n\n{console_width_text_border}\n\n\n{Style.RESET_ALL}")

				most_common_hour_of_the_day_text_block_one_shaped = wrap_console_text_display(most_common_hour_of_the_day_text_block_one)

				most_common_hour_of_the_day_text_block_two_shaped = wrap_console_text_display(most_common_hour_of_the_day_text_block_two)

				print(f"{most_common_hour_of_the_day_text_block_one_shaped}{most_common_hour_of_the_day_text_block_two_shaped}")
	
				choose_rerun_or_exit()

			else:
	   
				manage_data_analysis_display()

		def data_analysis_four():
			"""displays the result of the calculation of the most common
			start station at which Bikeshare was used

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: 
				description: returns ...
			"""			
	  
			global data_analysis_four_name

			data_analysis_four_name = f"...{Fore.GREEN}the most common start station(s) at which Bikeshare was used{Style.RESET_ALL}"
			
			if q_run_this_analysis(data_analysis_four_name) == True:
	   
				clear_console()
   
				most_common_start_station = data_analysis_four_calculation(generate_raw_df())

				most_common_start_station_text_block_one = (f"{Fore.CYAN}\n\n\n{console_width_text_border}\n\nThe most common start station(s) at which Bikeshare was used in {Fore.GREEN}{city_name}{Fore.CYAN} was:\n\n{Style.RESET_ALL}")

				most_common_start_station_text_block_two = (f"{Fore.CYAN} * {Fore.GREEN}{most_common_start_station}{Fore.CYAN}\n\n{console_width_text_border}\n\n\n{Style.RESET_ALL}")

				most_common_start_station_text_block_one_shaped = wrap_console_text_display(most_common_start_station_text_block_one)

				most_common_start_station_text_block_two_shaped = wrap_console_text_display(most_common_start_station_text_block_two)

				print(f"{most_common_start_station_text_block_one_shaped}{most_common_start_station_text_block_two_shaped}")
	
				choose_rerun_or_exit()
				
			else:
			
				manage_data_analysis_display()

		def data_analysis_five():
			"""displays the result of the calculation of the most common
			end station at which Bikeshare was used	

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: 
				description: returns ...
			"""		
	  
			global data_analysis_five_name

			data_analysis_five_name = f"...{Fore.GREEN}the most common end station(s) at which Bikeshare was used{Style.RESET_ALL}"
			
			if q_run_this_analysis(data_analysis_five_name) == True:
	   
				clear_console()
   
				most_common_end_station = data_analysis_five_calculation(generate_raw_df())

				most_common_end_station_text_block_one = (f"{Fore.CYAN}\n\n\n{console_width_text_border}\n\nThe most common end station(s) at which Bikeshare was used in {Fore.GREEN}{city_name}{Fore.CYAN} was:\n\n{Style.RESET_ALL}")

				most_common_end_station_text_block_two = (f"{Fore.CYAN} * {Fore.GREEN}{most_common_end_station}{Fore.CYAN}\n\n{console_width_text_border}\n\n\n{Style.RESET_ALL}")

				most_common_end_station_text_block_one_shaped = wrap_console_text_display(most_common_end_station_text_block_one)

				most_common_end_station_text_block_two_shaped = wrap_console_text_display(most_common_end_station_text_block_two)

				print(f"{most_common_end_station_text_block_one_shaped}{most_common_end_station_text_block_two_shaped}")
	
				choose_rerun_or_exit()
				
			else:
			
				manage_data_analysis_display()

		def data_analysis_six():
			"""displays the result of the calculation of the most common
			trip from start to end on which Bikeshare was used

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: 
				description: returns ...
			"""	
			
			data_analysis_six_name = f"...{Fore.GREEN}the most common trip from start to end stations on which Bikeshare was used{Style.RESET_ALL}"
			
			if q_run_this_analysis(data_analysis_six_name) == True:
	   
				clear_console()
   
				most_common_start_to_end_station_combination = data_analysis_six_calculation(generate_raw_df())

				most_common_start_to_end_station_combination_text_block_one = (f"{Fore.CYAN}\n\n\n{console_width_text_border}\n\nThe most common trip from start to end on which Bikeshare was used in {Fore.GREEN}{city_name}{Fore.CYAN} was:\n\n{Style.RESET_ALL}")

				most_common_start_to_end_station_combination_text_block_two = (f"{Fore.CYAN} * {Fore.GREEN}{most_common_start_to_end_station_combination}{Fore.CYAN}\n\n{console_width_text_border}\n\n\n{Style.RESET_ALL}")

				most_common_start_to_end_station_combination_text_block_one_shaped = wrap_console_text_display(most_common_start_to_end_station_combination_text_block_one)

				most_common_start_to_end_station_combination_text_block_two_shaped = wrap_console_text_display(most_common_start_to_end_station_combination_text_block_two)

				print(f"{most_common_start_to_end_station_combination_text_block_one_shaped}{most_common_start_to_end_station_combination_text_block_two_shaped}")

				choose_rerun_or_exit()
				
			else:
			
				manage_data_analysis_display()

		def data_analysis_seven():
			"""displays the result of calculating the sum of Bikeshare
			trip durations

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: 
				description: returns ...
			"""	
			
			data_analysis_seven_name = f"...{Fore.GREEN}the sum of Bikeshare trip durations{Style.RESET_ALL}"
			
			if q_run_this_analysis(data_analysis_seven_name) == True:
	   
				clear_console()
   
				sum_of_trip_durations = data_analysis_seven_calculation(generate_raw_df())

				sum_of_trip_durations_text_block_one = (f"{Fore.CYAN}\n\n\n{console_width_text_border}\n\nThe sum of Bikeshare trip durations in {Fore.GREEN}{city_name}{Fore.CYAN} in hrs:mins:secs was:\n\n{Style.RESET_ALL}")

				sum_of_trip_durations_text_block_two = (f"{Fore.CYAN} * {Fore.GREEN}{sum_of_trip_durations}{Fore.CYAN}\n\n{console_width_text_border}\n\n\n{Style.RESET_ALL}")

				sum_of_trip_durations_text_block_one_shaped = wrap_console_text_display(sum_of_trip_durations_text_block_one)

				sum_of_trip_durations_text_block_two_shaped = wrap_console_text_display(sum_of_trip_durations_text_block_two)

				print(f"{sum_of_trip_durations_text_block_one_shaped}{sum_of_trip_durations_text_block_two_shaped}")
	
				choose_rerun_or_exit()
				
			else:
			
				manage_data_analysis_display()

		def data_analysis_eight():
			"""displays the result of calculating the average of
			Bikeshare trip durations

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: 
				description: returns ...
			"""	
			
			data_analysis_eight_name = f"...{Fore.GREEN}the average of Bikeshare trip durations{Style.RESET_ALL}"
			
			if q_run_this_analysis(data_analysis_eight_name) == True:
	   
				clear_console()
   
				mean_of_trip_durations = data_analysis_eight_calculation(generate_raw_df())

				mean_of_trip_durations_text_block_one = (f"{Fore.CYAN}\n\n\n{console_width_text_border}\n\nThe average of Bikeshare trip durations in {Fore.GREEN}{city_name}{Fore.CYAN} in hrs:mins:secs was:\n\n{Style.RESET_ALL}")

				mean_of_trip_durations_text_block_two = (f"{Fore.CYAN} * {Fore.GREEN}{mean_of_trip_durations}{Fore.CYAN}\n\n{console_width_text_border}\n\n\n{Style.RESET_ALL}")

				mean_of_trip_durations_text_block_one_shaped = wrap_console_text_display(mean_of_trip_durations_text_block_one)

				mean_of_trip_durations_text_block_two_shaped = wrap_console_text_display(mean_of_trip_durations_text_block_two)

				print(f"{mean_of_trip_durations_text_block_one_shaped}{mean_of_trip_durations_text_block_two_shaped}")
	
				choose_rerun_or_exit()
				
			else:
			
				manage_data_analysis_display()

		def data_analysis_nine():
			"""displays the count of each Bikeshare user type

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: 
				description: returns ...
			"""
			
			data_analysis_nine_name = f"...{Fore.GREEN}the count of each Bikeshare user type{Style.RESET_ALL}"
			
			if q_run_this_analysis(data_analysis_nine_name) == True:
	   
				clear_console()
   
				user_type_count = data_analysis_nine_calculation(generate_raw_df())

				user_type_count_text_block_one = (f"{Fore.CYAN}\n\n\n{console_width_text_border}\n\nThe count of each Bikeshare user type in {Fore.GREEN}{city_name}{Fore.CYAN} was:\n\n{Style.RESET_ALL}")

				user_type_count_text_block_two = (f"{Fore.CYAN}{Fore.GREEN}{user_type_count}{Fore.CYAN}\n\n{console_width_text_border}\n\n\n{Style.RESET_ALL}")

				user_type_count_text_block_one_shaped = wrap_console_text_display(user_type_count_text_block_one)

				user_type_count_text_block_two_shaped = wrap_console_text_display(user_type_count_text_block_two)

				print(f"{user_type_count_text_block_one_shaped}{user_type_count_text_block_two_shaped}")

				choose_rerun_or_exit()
				
			else:
			
				manage_data_analysis_display()

		def data_analysis_ten():
			"""displays the count of each Bikeshare gender type

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: 
				description: returns ...
			"""
			
			data_analysis_ten_name = f"...{Fore.GREEN}the count of each Bikeshare gender type{Style.RESET_ALL}"
			
			if q_run_this_analysis(data_analysis_ten_name) == True:
	   
				clear_console()
   
				gender_type_count = data_analysis_ten_calculation(generate_raw_df())

				gender_type_count_text_block_one = (f"{Fore.CYAN}\n\n\n{console_width_text_border}\n\nThe count of each Bikeshare gender type in {Fore.GREEN}{city_name}{Fore.CYAN} was:\n\n{Style.RESET_ALL}")

				gender_type_count_text_block_two = (f"{Fore.CYAN}{Fore.GREEN}{gender_type_count}{Fore.CYAN}\n\n{console_width_text_border}\n\n\n{Style.RESET_ALL}")

				gender_type_count_text_block_one_shaped = wrap_console_text_display(gender_type_count_text_block_one)

				gender_type_count_text_block_two_shaped = wrap_console_text_display(gender_type_count_text_block_two)

				print(f"{gender_type_count_text_block_one_shaped}{gender_type_count_text_block_two_shaped}")
	
				choose_rerun_or_exit()
				
			else:
			
				manage_data_analysis_display()

		def data_analysis_eleven():
			"""displays the result of the calculation of the most common
			trip from start to end on which Bikeshare was used

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: 
				description: returns ...
			"""	
			
			data_analysis_eleven_name = f"* {Fore.GREEN}the earliest year of birth (oldest Bikeshare customers){Fore.CYAN}\n\n* {Fore.GREEN}the most recent year of birth (youngest Bikeshare customers){Fore.CYAN}\n\n* {Fore.GREEN}the most common year of birth of Bikeshare customers{Style.RESET_ALL}"
			
			if q_run_this_analysis(data_analysis_eleven_name) == True:
	   
				clear_console()
   
				oldest_customers_yob_int, youngest_customers_yob_int, most_common_customers_yob_mode_str = data_analysis_eleven_calculation(generate_raw_df())

				oldest_customers_yob_int_text_block_one = (f"{Fore.CYAN}\n\n\n{console_width_text_border}\n\n * {Fore.CYAN}The earliest year of birth (oldest) for Bikeshare customers in {Fore.GREEN}{city_name}{Fore.CYAN} was: {Fore.GREEN}{oldest_customers_yob_int}{Style.RESET_ALL}")

				youngest_customers_yob_int_text_block_one = (f"{Fore.CYAN}\n\n * {Fore.CYAN}The most recent year of birth (youngest) for Bikeshare customers in {Fore.GREEN}{city_name}{Fore.CYAN} was: {Fore.GREEN}{youngest_customers_yob_int}{Style.RESET_ALL}")

				most_common_customers_yob_mode_str_text_block_one = (f"{Fore.CYAN}\n\n * {Fore.CYAN}The most common year of birth of Bikeshare customers in {Fore.GREEN}{city_name}{Fore.CYAN} was: {Fore.GREEN}{most_common_customers_yob_mode_str}{Fore.CYAN}\n\n{console_width_text_border}\n\n\n{Style.RESET_ALL}")

				oldest_customers_yob_int_text_block_one_shaped = wrap_console_text_display(oldest_customers_yob_int_text_block_one)

				youngest_customers_yob_int_text_block_one_shaped = wrap_console_text_display(youngest_customers_yob_int_text_block_one)

				most_common_customers_yob_mode_str_text_block_one_shaped = wrap_console_text_display(most_common_customers_yob_mode_str_text_block_one)

				print(f"{oldest_customers_yob_int_text_block_one_shaped}{youngest_customers_yob_int_text_block_one_shaped}{most_common_customers_yob_mode_str_text_block_one_shaped}")
	
				choose_rerun_or_exit()
				
			else:
			
				manage_data_analysis_display()

		def display_data_analysis_options():
			"""manages the display of the eleven data analysis options

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: int: chosen_data_analysis_option_int
				description: returns an integer equating to the user's
			chosen data analysis option
			"""
	  
			global chosen_data_analysis_option_int
   
			clear_console()
   
			chosen_data_analysis_option = input(q_data_analysis_options())

			chosen_data_analysis_option_lower = chosen_data_analysis_option.lower()

			count = 4

			while chosen_data_analysis_option_lower in letters_of_the_alphabet_list and count > 0:
	
				print_invalid_choice()

				count -= 1

				chosen_data_analysis_option = input(q_data_analysis_options())

				chosen_data_analysis_option_lower = chosen_data_analysis_option.lower()
	
			if chosen_data_analysis_option_lower in letters_of_the_alphabet_list:

				app_exit()

			if chosen_data_analysis_option_lower == "":
	   
				chosen_data_analysis_option_lower = "0"
   
			chosen_data_analysis_option_int = int(chosen_data_analysis_option_lower)
   
			return chosen_data_analysis_option_int

		def make_city_or_data_analysis_choices_change():
			"""a message telling the user that if their chosen city is
			Washington, and their data analysis option is either int
			'10' or '11', then their data analysis option isn't
			aviailable. They are also asked to change either thier city
			or data analysis option

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: str: q_invalid_city_or_data_analysis_choice_str
				description: returns a variable containing a message
			telling the user that if their chosen city is Washington,
			and their data analysis option is either int '10' or '11',
			then their data analysis option isn't	aviailable. They are
			also asked to change either thier city or data analysis
			option
			"""

			q_invalid_city_or_data_analysis_choice_str = ""

			global invalid_city_or_data_analysis_choice

			q_invalid_city_or_data_analysis_choice_str_text_block_one = (f"{Fore.CYAN}\n\n\n{console_width_text_border}\n\n{Fore.YELLOW}This data analysis isn't available for Washington\n\n{Style.RESET_ALL}")

			q_invalid_city_or_data_analysis_choice_str_text_block_two = (f"{Fore.CYAN}Please change either your {Fore.MAGENTA}city{Fore.CYAN} or {Fore.MAGENTA}data analysis{Fore.CYAN} choice:\n\n{console_width_text_border}\n\n{Style.RESET_ALL}")

			q_invalid_city_or_data_analysis_choice_str_text_block_three = (f"{Fore.CYAN} * to select another city - choose {Fore.MAGENTA}c\n\n{Style.RESET_ALL}")

			q_invalid_city_or_data_analysis_choice_str_text_block_four = (f"{Fore.CYAN} * to choose another data analysis - select {Fore.MAGENTA}d\n\n{Style.RESET_ALL}")

			q_invalid_city_or_data_analysis_choice_str_text_block_five = (f"{Fore.CYAN}\n\n >>> {Style.RESET_ALL}")

			q_invalid_city_or_data_analysis_choice_str_text_block_one_shaped = wrap_console_text_display(q_invalid_city_or_data_analysis_choice_str_text_block_one)

			q_invalid_city_or_data_analysis_choice_str_text_block_two_shaped = wrap_console_text_display(q_invalid_city_or_data_analysis_choice_str_text_block_two)

			q_invalid_city_or_data_analysis_choice_str_text_block_three_shaped = wrap_console_text_display(q_invalid_city_or_data_analysis_choice_str_text_block_three)

			q_invalid_city_or_data_analysis_choice_str_text_block_four_shaped = wrap_console_text_display(q_invalid_city_or_data_analysis_choice_str_text_block_four)

			q_invalid_city_or_data_analysis_choice_str_text_block_five_shaped = wrap_console_text_display(q_invalid_city_or_data_analysis_choice_str_text_block_five)

			q_invalid_city_or_data_analysis_choice_str = input(f"{q_invalid_city_or_data_analysis_choice_str_text_block_one_shaped}{q_invalid_city_or_data_analysis_choice_str_text_block_two_shaped}{q_invalid_city_or_data_analysis_choice_str_text_block_three_shaped}{q_invalid_city_or_data_analysis_choice_str_text_block_four_shaped}{q_invalid_city_or_data_analysis_choice_str_text_block_five_shaped}")

			invalid_city_or_data_analysis_choice = q_invalid_city_or_data_analysis_choice_str.lower()

			return invalid_city_or_data_analysis_choice

		def disallow_washington_city_choice():
			"""if the user's chosen city is Washington, and their data
			analysis option is either int '10' or '11', then a message
			telling them that their data analysis option isn't
			aviailable, and asking them to change either thier city or
			data analysis option, is displayed

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: function call: choose_city()
				description: reruns the process of choosing a city to
				work with
			return: function call: manage_data_analysis_display()
				description: reruns the process of choosing a data
				analysis to work with
			"""

			global city_or_data_analysis_choice

			clear_console()

			city_or_data_analysis_choice = make_city_or_data_analysis_choices_change()

			if city_or_data_analysis_choice == "c":

				choose_city()

			elif city_or_data_analysis_choice == "d":

				manage_data_analysis_display()

			count = 4
   
			while (city_or_data_analysis_choice != "c"  and count > 0) or (city_or_data_analysis_choice != "d" and count > 0):
	
				print_invalid_choice()

				count -= 1

				city_or_data_analysis_choice = ""

				city_or_data_analysis_choice = make_city_or_data_analysis_choices_change()
	
				if city_or_data_analysis_choice == "c" or city_or_data_analysis_choice == "d":
		
					break

			if city_or_data_analysis_choice == "c":

				choose_city()

				count = 4

				while city_choice_lower == "w":
		
					print_invalid_choice()

					count -= 1

					choose_city()

				if city_choice_lower == "w":

					app_exit()

			elif city_or_data_analysis_choice == "d":

				manage_data_analysis_display()

			else:
	
				app_exit()

		def manage_data_analysis_display():
			"""runs the user's chosen data analysis calculation
			according to their data analysis choice

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			returns 1 - 11: data_analysis_one() to data_analysis_
					eleven()
				description: each returns the result of a data analysis
				calculation
			"""
	
			global city_choice_lower
			global data_analysis_type_choice
			global allowed_data_analysis_choices

			# check allowed_data_analysis_choices = range(1, 12)   
			allowed_data_analysis_choices_list = list(allowed_data_analysis_choices)
   
			# display data analysis choices
			data_analysis_type_choice = display_data_analysis_options()
   
			count = 4

			while (data_analysis_type_choice not in allowed_data_analysis_choices_list) and (count > 0):
   
				if data_analysis_type_choice not in allowed_data_analysis_choices_list:
		
					print_invalid_choice()
		
					count -= 1
	 
					data_analysis_type_choice = display_data_analysis_options()

				else:
		
					break

			if data_analysis_type_choice == 1:
	
				data_analysis_one()

			elif data_analysis_type_choice == 2:
	
				data_analysis_two()
	
			elif data_analysis_type_choice == 3:
	   
				data_analysis_three()
	
			elif data_analysis_type_choice == 4:
	
				data_analysis_four()
	
			elif data_analysis_type_choice == 5:
	
				data_analysis_five()
	
			elif data_analysis_type_choice == 6:
	
				data_analysis_six()
	
			elif data_analysis_type_choice == 7:
	
				data_analysis_seven()
	
			elif data_analysis_type_choice == 8:
	
				data_analysis_eight()
	
			elif data_analysis_type_choice == 9:
	   
				data_analysis_nine()
	
			elif data_analysis_type_choice == 10:

				if city_choice_lower == "w":
		
					disallow_washington_city_choice()

				data_analysis_ten()
	
			elif data_analysis_type_choice == 11:

				if city_choice_lower == "w":
		
					disallow_washington_city_choice()
 
				data_analysis_eleven()

			clear_app_exit()

		def choose_rerun_or_exit():
			"""offers the user options to either run another dataset
			display, to run another data analysis, or to exit the app.
			Called at the end of each dataset display or data analysis

			Parameters
			----------
			parameter : nil
				description: nil

			Returns
			-------
			return: manage_raw_data_display()
				description: restarts the dataset display process
			return: manage_data_analysis_display()
				description: restarts the data analysis process
			return: app_exit()
				description: exits the app
			"""

			pause(3)
	  
			global city_name
			global rerun_text_based_app
   
			choose_rerun_or_exit = input(q_rerun_or_exit())
		
			choose_rerun_or_exit_lower = choose_rerun_or_exit.lower()
	 
			if choose_rerun_or_exit_lower == "d" or choose_rerun_or_exit_lower == "a":
						
				rerun_text_based_app = True
	
				clear_console()
	
				q_choose_another_city = q_choose_another_city_str().lower()

				if q_choose_another_city == "y":
					
					choose_city()

					generate_csv_filename(city_name)
 
				else:
		
					pass

			elif choose_rerun_or_exit_lower == "":
	   
				app_exit()

			while rerun_text_based_app == True:
	
				if choose_rerun_or_exit_lower == "d":

					manage_raw_data_display()

				elif choose_rerun_or_exit_lower == "a":
						
					manage_data_analysis_display()

			count = 4

			while ((choose_rerun_or_exit_lower != "d") and (count > 0)) or ((choose_rerun_or_exit_lower != "a") and (count > 0)):
	
				print_invalid_choice()

				count -= 1

				choose_rerun_or_exit = input(q_rerun_or_exit())
			
				choose_rerun_or_exit_lower = choose_rerun_or_exit.lower()
	
				if choose_rerun_or_exit_lower == "d":

					manage_raw_data_display()

				elif choose_rerun_or_exit_lower == "a":
						
					manage_data_analysis_display()
	  
			clear_app_exit()
   

# APPLICATION FLOW CONTROL ::::::::::::::::::::::::::::::::::::::::::::::::::::

		choose_city()
		
		choose_data_analysis_type()

def main():
	"""starts the application and executes the global control logic

	Parameters
	----------
	parameter : nil
		description: nil

	Returns
	-------
	return: nil
		description: global application execution and control logic
	"""
	
	global text_border 
	global missing_modules_list
	global missing_modules_names

	clear_console()

	# initial lo-fi welcome message
	print(simple_welcome_message)

	pause(3)
 
	# check for essential missing modules, and initialize q_install_missing_modules
	check_for_missing_required_modules()
	
	# if there ARE missing modules, missing_modules_list evaluates to 'True'
	if missing_modules_list:

		# ask to install essential missing modules. Exit if not
		choose_continue_or_exit = input(q_install_missing_modules)

		# convert the person's response to lower case
		choose_continue_or_exit_lower = choose_continue_or_exit.lower()

		count = 4

		while (choose_continue_or_exit_lower != "") and (count > 0):
	  
			if  choose_continue_or_exit_lower == "x":
	   
				app_exit_simple()

			clear_console()

			print(invalid_choice_plain())

			pause(2)
   
			# ask to install essential missing modules. Exit if not
			choose_continue_or_exit = input(q_install_missing_modules)

			# convert the person's response to lower case
			choose_continue_or_exit_lower = choose_continue_or_exit.lower()
   
			count -= 1

			if choose_continue_or_exit_lower == "":
	   
				break
   
		# if 'ENTER', then continue with missing modules install
		if choose_continue_or_exit_lower == "":

			pass
		
		# if not "", then exit
		elif choose_continue_or_exit_lower != "":

			app_exit_simple()

		# install missing modules
		install_missing_required_modules(missing_modules_list)
	
	# if there ARE NOT missing modules, missing_modules_list evaluates to 'False'
	else:
	
		pass
 
	# check essential modules are installed
	check_essential_modules_are_installed()
   
	# move to Colorama-enabled display syntax
	enable_colorama_functionality()
 
if __name__ == "__main__":
	main()