#!/usr/bin/env python3

# x10-pyro - A web (flask) interface to the x10 Firecracker serial module
# By Sam Foster

# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask
from flask import render_template
from firecracker import send_command as x10_send
 
app = Flask(__name__)
  
@app.route('/')
def show_main_menu():
    """ Show the remote conrol user interface """
    #return 'X10 Pyro'
    dev_numbers = [*range(1,17)]
    return render_template("index.html", device_number_list=dev_numbers)

@app.route('/beta')
def show_beta_menu():
    """ Show the UI in development """
    dev_numbers = [*range(1,17)]
    return render_template("beta.html", device_number_list=dev_numbers)

@app.route('/old')
def show_old_screen():
    """ Show the UI in development """
    return render_template("remote-old.html")

@app.route('/<house>/<unit>/<command>')
def run_x10_command(house, unit, command):
    """ Take x10 remote command via URL, run it """
    # basic sanitation checks    
    if not verify_house(house):
        return f"House error, value: {house}"
    if not verify_unit(unit):
        return f"Unit error, value: {unit}"
    if not verify_command(command):
        return f"Command error, value: {command}"

    x10_send('/dev/ttyUSB0', house, int(unit), command)
    return_string = f'{house} {unit}: {command}'
    print(return_string)
    return return_string

def verify_house(house: str):
    """ Verify that house is a, b, c .. p """
    valid_houses = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p']
    if house in valid_houses:
        return True
    else:
        return False

def verify_unit(unit: str):
    """ Verify that unit is a number 1-16 """
    try:    # verify it's an int
        i_unit = int(unit)
    except ValueError:
        return False
    if i_unit in range(1,17):   
        return True
    else:
        return False

def verify_command(command: str):
    """ Verify that command is x10 valid: BRT, DIM, OFF or ON """
    valid_cmds = ['BRT', 'DIM', 'OFF', 'ON']
    if command in valid_cmds:
        return True
    else:
        return False
  
if __name__ == '__main__':
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(host="0.0.0.0", debug = True)

