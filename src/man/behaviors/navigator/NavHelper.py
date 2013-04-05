from math import fabs
from ..util import MyMath
import NavConstants as constants
from objects import RelLocation, RelRobotLocation, RobotLocation, Location
# TODO: Import CommandType properly.
#import PMotion_proto

def stand(nav):
    createAndSendWalkVector(nav, 0, 0, 0)

def getRelativeDestination(my, dest):

    field_dest = dest

    if isinstance(field_dest, RelRobotLocation):
        return field_dest

    elif isinstance(field_dest, RelLocation):
        return RelRobotLocation(field_dest.relX,
                                field_dest.relY,
                                field_dest.bearing)

    elif isinstance(field_dest, RobotLocation):
        return my.relativeRobotLocationOf(field_dest)

    elif isinstance(field_dest, Location):
        relLocation = my.relativeLocationOf(field_dest)
        return RelRobotLocation(relLocation.relX,
                                relLocation.relY,
                                relLocation.bearing)

    else:
        raise TypeError, "Navigator dest is not a Location type!" + str(dest)

def isDestinationRelative(dest):
    return isinstance(dest, RelLocation)

def adaptSpeed(distance, cutoffDistance, maxSpeed):
    return MyMath.mapRange(distance, 0, cutoffDistance, 0, maxSpeed)

def getStrafelessDest(dest):
    if ((dest.relX > 150 and dest.relY < 50) or
        (dest.relX <= 150 and dest.relX > 50 and dest.relY < 20) or
        (dest.relX <= 50 and dest.relX > 20 and dest.relY < 10)):
        #print "old dest: " + str(dest)
        return RelRobotLocation(dest.relX, 0, dest.relH)
    else:
        return dest

def setDestination(nav, dest, gain = 1.0):
    """
    Calls setDestination within the motion engine
    """
    # TODO: distinguish from setOdometryDestination method
    #       this method should overwrite motion commands.
    #       or, deprecate this method and use speed commands
    #       via the createAndSendWalkVector method.
    command = nav.brain.interface.bodyMotionCommand
    command.type = command.CommandType.DESTINATION_WALK #Destination Walk
    command.dest.rel_x = dest.relX
    command.dest.rel_y = dest.relY
    command.dest.rel_h = dest.relH
    # Mark this message for sending
    command.processed_by_motion = False

def setOdometryDestination(nav, dest, gain = 1.0):
    # TODO: distinguish from setDestination method
    #       this method should enqueue motion commands.
    command = nav.brain.interface.bodyMotionCommand
    command.type = command.CommandType.DESTINATION_WALK #Destination Walk
    command.dest.rel_x = dest.relX
    command.dest.rel_y = dest.relY
    command.dest.rel_h = dest.relH
    # Mark this message for sending
    command.processed_by_motion = False

#not used!
def getOrbitLocation(radius, angle):
    """
    Returns the RelRobotLocation destination of an orbit
    """
    if angle > 0:
        return RelRobotLocation(0.0, radius / 2, -angle)
    else:
        return RelRobotLocation(0.0, -radius / 2, -angle)

    dest = RelRobotLocation(radius, 0, 0)
    dest.rotate(-angle)
    return RelRobotLocation(0.0, -dest.relY, -angle)

def setSpeed(nav, speeds):
    """
    Wrapper method to easily change the walk vector of the robot
    """
    if speeds == constants.ZERO_SPEEDS:
        nav.printf("!!!!!! USE player.stopWalking() NOT walk(0,0,0)!!!!!")
        return

    createAndSendWalkVector(nav, *speeds)

def createAndSendWalkVector(nav, x, y, theta):
    command = nav.brain.interface.bodyMotionCommand
    command.type = command.CommandType.WALK_COMMAND #Walk Command
    command.speed.x = x
    command.speed.y = y
    command.speed.h = theta
    # Mark this message for sending
    command.processed_by_motion = False

def executeMove(nav, sweetMove):
    """
    Method to enqueue a SweetMove
    Can either take in a head move or a body command
    (see SweetMove files for descriptions of command tuples)
    """
    command = nav.brain.interface.bodyMotionCommand
    command.type = command.CommandType.SCRIPTED_MOVE #Scripted Move

    for position in sweetMove:
        if len(position) == 7:
            command.script.add_commands

            command.script.time = position[4]
            command.script.interpolation_type = position[5]
            command.script.chain_stiffnesses = position[6]

            move = command.script.commands(commands_size-1) #Current joint command
            move.l_shoulder_pitch = position[0][0]
            move.l_shoulder_roll = position[0][1]
            move.l_elbow_yaw = position[0][2]
            move.l_elbow_roll = position[0][3]
            move.l_hip_yaw_pitch = position[1][0]
            move.l_hip_roll = position[1][1]
            move.l_hip_pitch = position[1][2]
            move.l_knee_pitch = position[1][3]
            move.l_ankle_pitch = position[1][4]
            move.l_ankle_roll = poisition[1][5]
            move.r_hip_yaw_pitch = position[2][0]
            move.r_hip_roll = position[2][1]
            move.r_hip_pitch = position[2][2]
            move.r_knee_pitch = position[2][3]
            move.r_ankle_pitch = position[2][4]
            move.r_ankle_roll = poisition[2][5]
            move.r_shoulder_pitch = position[3][0]
            move.r_shoulder_roll = position[3][1]
            move.r_elbow_yaw = position[3][2]
            move.r_elbow_roll = position[3][3]

            # Mark this message for sending
            command.processed_by_motion = False

        else:
            print("What kind of sweet ass-Move is this?")