#!/usr/bin/python
import cgi
import cgitb

def convert_units(num_units,conv_constant, conv_factor, reverse=""):
	if conv_constant==0:
		print("conversion not found")
		return

	if reverse=="true":
		result=conv_factor*(num_units/conv_constant)
	else:
		result=conv_factor*(num_units*conv_constant)
	print "The result is: ", result
	return result

def main():
    print "Content-type:text/html\n\n"
    cgitb.enable()
    form = cgi.FieldStorage()

    original_units = form.getvalue("origunits").lower()
    conv_units = form.getvalue("convunits").lower()
    num_units = float(form.getvalue("numunits"))
    conv_factor = float(form.getvalue("convfactor"))


    reverse="false"
    if (original_units == conv_units):
	conv_const=1
    elif (original_units == "parsec" and conv_units== "lightyear")or(original_units == "lightyear" and conv_units== "parsec"):
    	conv_const=3.26
	if(original_units=="lightyear"):reverse="true"
    elif (original_units=="lightyear" and conv_units=="kilometer")or(original_units=="kilometer" and conv_units=="lightyear"):
    	conv_const=3.086*pow(10,13)
	if(original_units=="kilometer"):reverse="true"
    elif (original_units=="xlarn" and conv_units=="parsec")or(original_units=="parsec" and conv_units=="xlarn"):
    	conv_const=7.3672
	if(original_units=="parsec"):reverse="true"
    elif (original_units=="galacticyear" and conv_units=="terrestrialyear")or(original_units=="terrestrialyear" and conv_units=="galacticyear"):
    	conv_const=250000000
	if(original_units=="terrestrialyear"):reverse="true"
    elif (original_units=="xarnyear" and conv_units=="terrestrialyear")or(original_units=="terrestrialyear" and conv_units=="xarnyear"):
    	conv_const=1.2579
	if(original_units=="terrestrialyear"):reverse="true"
    elif (original_units=="terrestrialyear" and conv_units=="terrestrialminute")or(original_units=="terrestrialminute" and conv_units=="terrestrialyear"):
    	conv_const=525600
	if(original_units=="terrestrialminute"):reverse="true"
    else:
	conv_const=0

    convert_units(num_units,conv_const,conv_factor,reverse)

if __name__ == "__main__":
    main()
