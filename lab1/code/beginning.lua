-- Put your global variables here

MOVE_STEPS = 15
n_steps = 0

states = {FOTOTASSI=0, FOLLOWBORDER=1};

state = states.FOTOTASSI;

--[[ This function is executed every time you press the 'execute'
     button ]]
function init()
	left_v = robot.random.uniform(0,15)
	right_v = robot.random.uniform(0,15)
	robot.wheels.set_velocity(left_v,right_v)
	n_steps = 0
	robot.leds.set_all_colors("black")
end

function fototassi()
	---
end

function followborder()
	---
end



--[[ This function is executed at each time step
     It must contain the logic of your controller ]]
function step()
	n_steps = n_steps + 1
	
	MAX_VELOCITY = 10
	dir = light_dir_rad()
	log("dir: " .. dir)

	velocityL = MAX_VELOCITY * math.cos(dir) * math.sin(dir)
	velocityR = MAX_VELOCITY * math.cos(dir) * math.sin(dir) * -1

	robot.wheels.set_velocity(velocityL, velocityR)

	log("robot.position.x = " .. robot.positioning.position.x)
	log("robot.position.y = " .. robot.positioning.position.y)
	log("robot.position.z = " .. robot.positioning.position.z)
	light_front = robot.light[1].value + robot.light[24].value
	log("robot.light_front = " .. light_front)
	ground = robot.motor_ground
	log("ground NE: " .. ground[1].value)
	log("ground NW: " .. ground[2].value)
	log("ground SW: " .. ground[3].value)
	log("ground SE: " .. ground[4].value)

	-- Search for the reading with the highest value
	value = -1 -- highest value found so far
	idx = -1   -- index of the highest value
	for i=1,24 do
		if value < robot.proximity[i].value then
			idx = i
			value = robot.proximity[i].value
		end
	end
	log("robot max proximity sensor: " .. idx .. "," .. value)

	-- Check if on spot
	spot = false
	for i=1,4 do
		if ground[i].value == 0 then
			spot = true
			break
		end
	end


	--[[ Check if close to light 
	(note that the light threshold depends on both sensor and actuator characteristics) ]]
	light = false
	sum = 0
	for i=1,24 do
		sum = sum + robot.light[i].value
	end
	if sum > 1.5 then
		light = true
	end


	if spot == true then
		robot.leds.set_all_colors("red")
	elseif light == true then
		robot.leds.set_all_colors("yellow")
	else
		robot.leds.set_all_colors("black")
	end


end

function light_dir_rad()
	max_i = 1
	for i=1,24 do
		if robot.light[i].value >= robot.light[max_i].value then
			max_i = i
		end
	end

	return math.rad(max_i * (360 / 24))
end



--[[ This function is executed every time you press the 'reset'
     button in the GUI. It is supposed to restore the state
     of the controller to whatever it was right after init() was
     called. The state of sensors and actuators is reset
     automatically by ARGoS. ]]
function reset()
	left_v = robot.random.uniform(0,15)
	right_v = robot.random.uniform(0,15)
	robot.wheels.set_velocity(left_v,right_v)
	n_steps = 0
	robot.leds.set_all_colors("black")
end



--[[ This function is executed only once, when the robot is removed
     from the simulation ]]
function destroy()
   -- put your code here
end
