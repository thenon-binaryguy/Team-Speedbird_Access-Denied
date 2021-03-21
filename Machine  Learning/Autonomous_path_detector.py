from dronekit import connect, Vehicle, VehicleMode, LocationGlobalRelative, LocationGlobal
import numpy as np
from pymavlink import mavutil
import time

import argparse
parser = argparse.ArgumentParser(description='Commands vehicle')
parser.add_argument('--connect',help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
sitl = None

#Turning on the SITL simulator as pixhawk isnt available
if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()
#Connecting to the vechicle using UDP port in mission planner
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)

#vechicle takeoff function
def arm_and_takeoff(aTargetAltitude):
    
    print "Basic pre-arm checks"
    while not vehicle.is_armable:
        print " Waiting for vehicle to initialise..."
        time.sleep(1)
        
    print "Arming motors"
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True
    
    while not vehicle.armed:      
        print " Waiting for arming..."
        time.sleep(1)

    print "Taking off!"
    vehicle.simple_takeoff(aTargetAltitude)

    while True:
        print " Altitude: ", vehicle.location.global_relative_frame.alt      
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95: 
            print "Reached target altitude"
            break
        time.sleep(1)

#Considering that vechicle follows an initial trajectory of square on a fixed path
def mission(aLocation, aSize):
    cmds = vehicle.commands
    cmds.clear() 
    #Define the four MAV_CMD_NAV_WAYPOINT locations and add the commands
    point1 = get_location_metres(aLocation, aSize, -aSize)
    point2 = get_location_metres(aLocation, aSize, aSize)
    point3 = get_location_metres(aLocation, -aSize, aSize)
    point4 = get_location_metres(aLocation, -aSize, -aSize)
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, point1.lat, point1.lon, 11))
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, point2.lat, point2.lon, 12))
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, point3.lat, point3.lon, 13))
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, point4.lat, point4.lon, 14))
    #add dummy waypoint "5" at point 4 (lets us know when have reached destination)
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, point4.lat, point4.lon, 14))    
    cmds.upload()


#Function to get the current location of the aircraft from the base station

def get_location_metres(original_location, dNorth, dEast):
    earth_radius=6378137
    dLat = dNorth/earth_radius
    dLon = dEast/(earth_radius*math.cos(math.pi*original_location.lat/180))
    newlat = original_location.lat + (dLat * 180/math.pi)
    newlon = original_location.lon + (dLon * 180/math.pi)
    return LocationGlobal(newlat, newlon,original_location.alt)


# Function to add a new waypoint where the crowd of people is detected

def gotowaypoint(dNorth, dEast, gotoFunction=vehicle.simple_goto):
    currentLocation=vehicle.location.global_relative_frame
    targetLocation=get_location_metres(currentLocation, dNorth, dEast)
    targetDistance=get_distance_metres(currentLocation, targetLocation)
    gotoFunction(targetLocation)

    while vehicle.mode.name=="GUIDED": #Stop action if we are no longer in guided mode.
        remainingDistance=get_distance_metres(vehicle.location.global_frame, targetLocation)
        print "Distance to target: ", remainingDistance
        if remainingDistance<=targetDistance*0.01: #Just below target, in case of undershoot.
            print "Reached target"
            break;

#start the initial mission
arm_and_takeoff(15)
vehicle.airspeed(8)
vehicle.mode = VehicleMode("AUTO")

#if a crowd of 3 or people are detected in the trajectory with the range of 50 or less from the current location

while True:

    if no>=3:
    #Decrease the airplane speed and start dropping the altitude to 10m
        vehicle.mode = VehicleMode("GUIDED")
        vehicle.simple_takeoff(10)
        dn,de=vehicle.location.global_relative_frame
        vehicle.airspeed(5)
        getlocation
        gotowaypoint(dn,de)
    #The servo motors are given commanded to drop of relief kit
        servo.operate(no)  
    # The aircraft continues is previous trajectory of
        vehicle.mode = VehicleMode("AUTO")
        adds_square_mission(vehicle.location.global_frame,50)
    # The speed  and the altitude
        vehicle.simple_takeoff(15)
        vehicle.airspeed(8)


print('Return to launch')
vehicle.mode = VehicleMode("RTL")
vehicle.close()
if sitl is not None:
    sitl.stop()
