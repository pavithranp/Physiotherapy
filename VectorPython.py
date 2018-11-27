
from pylab import *
from visual import *
import math
import serial
theta1 = math.radians(-60)		# pitch angle of 1st pendulum to vertical (initial value)
phi1 = math.radians(10)		# roll angle of 1st pendulum to vertical (initial value)


theta2 =math.radians(-45)		# pitch angle of 2nd pendulum to vertical (initial value)
phi2 = math.radians(60)			# roll angle of 2nd pendulum to vertical (initial value)


theta_dot = 0.0	# rate of change of theta - initial value
phi_dot = 0.1

g = 9.8	# acceleration of gravity
l = 1.0	# pendulum arm length 
m = 0.3	# mass of pendulum ball

time = 0.0 	# initial value of time
dt = 0.0001		# time step
ser=serial.Serial('/dev/ttyACM0',38400)
# Create balls
ball1 = sphere(pos=vector(l*sin(theta1)*cos(theta2),-l*cos(theta1)*cos(theta2),l*sin(theta2)), radius=0.12, color=color.blue)
ball2 = sphere(pos=vector(l*sin(theta1)*cos(theta2) + l*sin(phi1)*cos(phi2),-l*cos(theta1)*cos(theta2) - l*cos(phi2),l*sin(theta2) + l*sin(phi2)), radius=0.12, color=color.blue)

arm1 = cylinder(pos=(0,0,0), axis=(l*sin(theta1)*cos(theta2),-l*cos(theta1)*cos(theta2),l*sin(theta2)), radius=.03, color=color.cyan)
arm2 = cylinder(pos=(0,0,0), axis=(l*sin(theta1)*cos(theta2) + l*cos(phi2), -l*cos(theta1)*cos(theta2) - l*cos(phi2), l*sin(theta2) + l*sin(phi2)), radius=.03, color=color.cyan)
in_x_plane=arrow(pos=(0,0,0), axis=(2,0,0), shaftwidth=0.1, headwidth=0.1, color=color.orange, opacity=0.3)
in_y_plane=arrow(pos=(0,0,0), axis=(0,-2,0), shaftwidth=0.1, headwidth=0.1, color=color.orange, opacity=0.3)
in_z_plane=arrow(pos=(0,0,0), axis=(0,0,2), shaftwidth=0.1, headwidth=0.1, color=color.orange, opacity=0.3)
nub = sphere(pos=vector(0,0,0), radius=0.05, color=color.white)		# little white nub
scene.userspin = 1
#scene.fullscreen=1
scene.autoscale = 0		# stop it from zooming in and out
#scene.title = 'Double pendulum'
scene.range = (2.05,2.05,2.05)

# Time loop for moving Ball(s)
timestep=0.01

while 1:	
	#rate(5000)		# Set number of times loop is repeated per second
	try:	
		s=ser.readline().split()
		k=map(float,s)
		print k
		theta1=math.radians(k[4])
		theta2=math.radians(k[5])
		#phi1 = math.radians(k[1])
		phi2 = math.radians(k[1])
		ball1.pos.x = l*sin(theta1)*cos(theta2)
		ball1.pos.y = -l*cos(theta1)*cos(theta2)
		ball1.pos.z = l*sin(theta2)
		arm1.axis = (ball1.pos.x, ball1.pos.y, ball1.pos.z)

		ball2.pos.x = l*sin(theta1)*cos(theta2) + l*cos(phi2)
		ball2.pos.y = -l*cos(theta1)*cos(theta2) - l*cos(phi2)
		ball2.pos.z = l*sin(theta2) + l*sin(phi2)

		arm2.pos = (l*sin(theta1)*cos(theta2), -l*cos(theta1)*cos(theta2), l*sin(theta2))
		arm2.axis = (ball2.pos.x - ball1.pos.x, ball2.pos.y - ball1.pos.y, ball2.pos.z-ball1.pos.z)
	except:
		pass
	#time += dt
