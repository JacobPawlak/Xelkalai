#!/usr/bin/python

#grab the right libraries to do the python cgi stuff
import cgi
import cgitb

#
def convert_units(orig_units, conv_units ,num_units,conv_constant, conv_factor, reverse=""):

	if reverse=="true":
		result=conv_factor*(num_units/conv_constant)
	else:
		result=conv_factor*(num_units*conv_constant)
	print "<p class='answer-header'>The result is: </p><br>"
	print "<p>", num_units, "</p>", "<p class='blue'>", orig_units, "</p>", "<p>converts to </p> <p class='green'>", result, "</p>", "<p class='blue'>", conv_units, "</p>"

	return result

def is_valid_get(form_data):

	possible_units = ["parsec", "lightyear", "kilometer", "xlarn", "galacticyear", "terrestrialyear", "xarnyear", "terrestrialminute"]
	keys = form_data.keys()

	#If the user provides the wrong number of params, error
	if (len(keys) != 4):
		print "<p class='error_msg> You did not supply the correct ammount of parameters... please try again </p>"
		return

	#if the params passed in aren't correct, error
	if ( (keys[0] != "origunits") or (keys[1] != "convunits") or (keys[2] != "numunits") or (keys[3] != "convfactor") ):
		if(keys[0] != "origunits"):
			print "<p class='error_msg> You gave: ", keys[0], "you should have supplied: origunits </p>"
		if(keys[1] != "convunits"):
			print "<p class='error_msg> You gave: ", keys[1], "you should have supplied: convunits </p>"
		if(keys[2] != "numunits"):
			print "<p class='error_msg> You gave: ", keys[2], "you should have supplied: numunits </p>"
		if(keys[3] != "convfactor"):
			print "<p class='error_msg> You gave: ", keys[3], "you should have supplied: convfactor </p>"
		return

	#a rough way to check for float values on input
	# split along a period (decimal) and then check for digits on
	# both sides 
	num_units_split = form_data[keys[2]].split('.')
	conv_factor_split = form_data[keys[3]].split('.')

	#set up some flags to report the validity of the two decimals
	num_units_all_digits = True
	conv_factor_all_digits = True

	#If there are multiple decimals in the split, throw the flag
	if(len(num_units_split) > 2):
		num_units_all_digits = False
	if(len(conv_factor_split) > 2):
		conv_factor_all_digits = False
	
	#Now check each side of the decimal for non digits
	for part in num_units_split:
		if(not(part.isdigit())):
			num_units_all_digits = False
	for part in conv_factor_split:
		if(not(part.isdigit())):
			conv_factor_all_digits = False

	#if the param's values are not in the right scope, error
	if( (form_data[keys[0]] not in possible_units) or (form_data[keys[1]] not in possible_units) or (not num_units_all_digits) or (not conv_factor_all_digits) ):
		if(form_data[keys[0]] not in possible_units):
			print "<p class='error_msg>Please supply origunits with an option from the dropdown menu</p>"
		if(form_data[keys[1]] not in possible_units):
			print "<p class='error_msg>Please supply convunits with an option from the dropdown menu</p>"
		if(not num_units_all_digits):
			print "<p class='error_msg>numunits needs to be a float or an integer value</p>"
		if(not conv_factor_all_digits):
			print "<p class='error_msg>convfactor needs to be a float or an integer value</p>"
		return

	#if the GET input gets to here it should be valid
	return True

def main():
	#CGI header stuff
	print "Content-type:text/html\n\n"
	cgitb.enable()

	print "<html>"
	print '<head> <title>Project Xelkalai | CS316</title><meta charset="utf-8">	<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">	<meta name="viewport" content="width=device-width, initial-scale=1">'
	print '.blue {color: #0b60e8;} .red {color: #e80b0b;font-style: italic;} .green {color: #00e00e;} .error_msg {color: #e80b0b;font-weight: bold;} .answer-header { color: #9b0081;}'
	print "<body>"
	
	#grab all of the GET tokens and values
	form = cgi.FieldStorage()

	#validate all of the tokens and values really quickly
	good_url = is_valid_get(form)

	#capture all of the tokens's value
	original_units = form.getvalue("origunits").lower()
	conv_units = form.getvalue("convunits").lower()
	num_units = float(form.getvalue("numunits"))
	conv_factor = float(form.getvalue("convfactor"))

	#set the reverse flag to false and the conversion constant to 1 (it will be changed)
	reverse="false"
	conv_const = 1

	#if the units happen to be the same, we know the conversion constant will be 
	if (original_units == conv_units):
		conv_const=1

	#now check for the correct unit pairs for conversion
	elif(original_units == "parsec" and conv_units== "lightyear")or(original_units == "lightyear" and conv_units== "parsec"):
		conv_const=3.26
		if(original_units=="lightyear"):
			reverse="true"
	elif (original_units=="lightyear" and conv_units=="kilometer")or(original_units=="kilometer" and conv_units=="lightyear"):
		conv_const=3.086*pow(10,13)
		if(original_units=="kilometer"):
			reverse="true"
	elif (original_units=="xlarn" and conv_units=="parsec")or(original_units=="parsec" and conv_units=="xlarn"):
		conv_const=7.3672
		if(original_units=="parsec"):
			reverse="true"
	elif (original_units=="galacticyear" and conv_units=="terrestrialyear")or(original_units=="terrestrialyear" and conv_units=="galacticyear"):
		conv_const=250000000
		if(original_units=="terrestrialyear"):
			reverse="true"
	elif (original_units=="xarnyear" and conv_units=="terrestrialyear")or(original_units=="terrestrialyear" and conv_units=="xarnyear"):
		conv_const=1.2579
		if(original_units=="terrestrialyear"):
			reverse="true"
	elif (original_units=="terrestrialyear" and conv_units=="terrestrialminute")or(original_units=="terrestrialminute" and conv_units=="terrestrialyear"):
		conv_const=525600
		if(original_units=="terrestrialminute"):
			reverse="true"

	#if we get to here and the units have not matched up, the user gave the incorrect original units or converted units
	else:
		#we set the conversion const to zero as a psuedo flag, and throw an error
		conv_const=0
		print "<p class='error_msg'>You did not supply the program with a correct pair for conversion</p>"
		return

	convert_units(num_units,conv_const,conv_factor,reverse)

	print "</body>"
	print "</html>"

if __name__ == "__main__":
	main()
