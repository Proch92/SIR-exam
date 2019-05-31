local vector = require('utils.vector');
local func = require('utils.functional');
local matrix = require('utils.matrix');

-- Put your global variables here
n_steps = 0
MAX_POWER = 10

-- Aggregation #########################
-- State 0 : wander
-- State 1 : stop
state = 0

SENSE_RANGE = 30
W = 0.1
S = 0.15
Pmaxs = 0.99
Pminw = 0.01
alpha = 0.1
beta = 0.05

function init()
	n_steps = 0
	robot.leds.set_all_colors("black")
	robot.leds.set_single_color(1, "blue")
	robot.leds.set_single_color(12, "blue")
	robot.leds.set_single_color(6, "red")
	robot.leds.set_single_color(7, "red")
end

function step()
	stopped_robots = countRAB()
	probabilistic_state_change(stopped_robots)
	act()

	n_steps = n_steps + 1
end


function countRAB()
	number_robot_sensed = 0

	max_chain = 0

	for i = 1, #robot.range_and_bearing do
		if robot.range_and_bearing[i].range < SENSE_RANGE and robot.range_and_bearing[i].data[1] == 1 then
			number_robot_sensed = number_robot_sensed + 1
			max_chain = math.max(number_robot_sensed, robot.range_and_bearing[i].data[2])
		end
	end

	robot.range_and_bearing.set_data(2, max_chain)

	return max_chain
end


function probabilistic_state_change(stopped_robots)
	rand = robot.random.uniform(0, 1)

	ps = math.min(Pmaxs, S + (alpha * stopped_robots))
	pw = math.max(Pminw, W - (beta * stopped_robots))

	if state == 0 then
		if rand < ps then
			state = 1
		end
	else
		if rand < pw then
			state = 0
		end
	end

	robot.range_and_bearing.set_data(1, state)
end


function act()
	if state == 0 then
		random_direction = randomdir()

		out = dir2powers(random_direction)
		robot.wheels.set_velocity(out.left, out.right)
	else
		robot.wheels.set_velocity(0, 0)
	end
end


STEER_MAX_STEPS = 100
rand_angle = math.pi / 2
function randomdir()
	if n_steps % STEER_MAX_STEPS == 0 then
		rand_angle = robot.random.uniform(-math.pi/3, math.pi/3)
	end

	resultant = vector.newPolar(rand_angle, MAX_POWER)
	
	return resultant
end


function dir2powers(vec)
	angle = vector.getAngle(vec)
	magnitude = vector.getMag(vec)

	L = robot.wheels.axis_length

	conversion = matrix{{1, -L/2}, {1, L/2}}
	polar = matrix{{magnitude}, {angle}}

	linear = conversion * polar

	return {left = linear[1][1], right = linear[2][1]}
end

function reset()
	n_steps = 0
	robot.leds.set_all_colors("black")
	robot.leds.set_single_color(1, "blue")
	robot.leds.set_single_color(12, "blue")
	robot.leds.set_single_color(6, "red")
	robot.leds.set_single_color(7, "red")
end

function destroy()
   -- put your code here
end
