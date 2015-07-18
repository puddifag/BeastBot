#!/usr/bin/python2
#Creator: khofo with the help of thewormkill, chris1, Phage and Evilzone's IRC
#for: Evilzone's EZBot
#github: github.com/khofosec/snippets
#IRC Module to convert units
#Usage: !convert <number> unit1 t unit2
    #Example: !convert 10 ft to m (convert 10 ft to meters)

#Imports
from inc import *                                     

#IRC Parsing function:
modFunc.addCommand('convert', 'convert', 'convert')   
# Adds the command to the ezbot db
 
#STARTConversions: 
def kg_to_lb(number):
    result = number * float(2.2046)
    ircFunc.ircSay(msgto,str(number) + "kilograms = " + str(result) + "pounds", irc)

def lb_to_kg(number):
    result = number * float(0.453592)
    ircFunc.ircSay(msgto,str(number) + "pounds = " + str(result) + "kilograms", irc)

def f_to_c(number):
    result = (number-32)*float(0.555)
    ircFunc.ircSay(msgto,str(number)+ " degrees Fahreinheit = " + str(result) + " degrees Celsius", irc)

def c_to_f(number):
    result = (number*float(1.8))+32
    ircFunc.ircSay(msgto,str(number)+ " degrees Celsius = " + str(result) + " degrees Fahreinheit", irc)
def m_to_ft(number):
    result = number*float(3.28084)
    ircFunc.ircSay(msgto, str(number) + "meters = " + str(result)+"feet" ,irc)

def ft_to_m(number):
    result = number*float(0.3048)
    ircFunc.ircSay(msgto, str(number) + "feet = " + str(result)+"meters" ,irc)

def m_to_yds(number):
    result = number*float(1.09361)
    ircFunc.ircSay(msgto, str(number) + "meters = " + str(result)+"yards" ,irc)

def ft_to_yds(number):
    result = float(number)*float(0.3333)
    ircFunc.ircSay(msgto, str(number) + "feet = " + str(result)+"yards" ,irc)

def yrds_to_m(number):
    result = number*float(0.9144)
    ircFunc.ircSay(msgto, str(number) + "yards = " + str(result)+"meters" ,irc)    

def yrds_to_ft(number):
    result = float(number)*float(3)
    ircFunc.ircSay(msgto, str(number) + "yards = " + str(result)+"feet" ,irc)  
#END of conversions
    

def convert(line, irc):
    message, username, msgto = ircFunc.ircMessage(line) # Parse the line
    numArgs = len(message) - 1 # Subtract 1 to get rid of !convert
    if numArgs >= 4: #Num of arguments required 
            number = message[1] #the number to be converted or "help" message
            unit_from = message[2].lower() # unit to convert from 
            unit_to = message[4].lower() # unit to convert to
            conversion(unit_from, unit_to, number)
    else:
        return help()
 
def conversion(unit_from, unit_to, number):
    try:
        number = float(number.strip())
    except:
        return help()
    
    linear = { ('m', 'ft')  : "m_to_ft",  
               ('m', 'yds') : "m_to_yds",   
               ("ft", "m")  : "ft_to_m",
               ("ft", "yds"): "ft_to_yds",
               ("yds", "m") : "yds_to_m",
               ("yds", "ft"): "yds_to_ft",
               ("kg", "lb") : "kg_to_lb",
               ("lb", "kg") : "lb_to_kg",
               ("F", "C")   : "f_to_c",
               ("C", "F")   : "c_to_f",
               }
    if (unit_from, unit_to) in linear:
        if linear[(unit_from, unit_to)] == "m_to_ft":
            return m_to_ft(number)
        
        elif linear[(unit_from, unit_to)] == "m_to_yds":
            return m_to_yds(number)
        
        elif linear[(unit_from, unit_to)] == "ft_to_m":
            return ft_to_m(number)
        
        elif linear[(unit_from, unit_to)] == "ft_to_yds":
            return ft_to_yds(number)
        
        elif linear[(unit_from, unit_to)] == "yds_to_m":
            return yds_to_m(number)
        
        elif linear[(unit_from, unit_to)] == "yds_to_ft":
            return yds_to_ft(number)
        
        elif linear[(unit_from, unit_to)] == "kg_to_lb":
            return kg_to_lb(number)
        
        elif linear[(unit_from, unit_to)] == "lb_to_kg":
            return lb_to_kg(number)
        
        elif linear[(unit_from, unit_to)] == "f_to_c":
            return f_to_c(number)
        
        elif linear[(unit_from, unit_to)] == "c_to_f":
            return c_to_f(number)
        else:
            pass
    else:
        return "ERROR: For usage please refer to !convert help"

def help():
    ircFunc.ircSay(msgto, "Usage: !convert <float(aka number)> kg to lb" ,irc)
