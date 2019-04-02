local vector = require('utils.vector');
local func = require('utils.functional');

-- Put your global variables here
n_steps = 0
MAX_POWER = 10


--[[ This function is executed every time you press the 'execute'
     button ]]
function init()
	n_steps = 0
	robot.leds.set_all_colors("black")
	robot.leds.set_single_color(1, "blue")
	robot.leds.set_single_color(12, "blue")
	robot.leds.set_single_color(6, "red")
	robot.leds.set_single_color(7, "red")
end

--[[ This function is executed at each time step
     It must contain the logic of your controller ]]
function step()
	out = dir2powers(
			hinib(
				randomdir(input()),
				hinib(
					light2force(input()),
					proximity2force(input()),
					0.1
				),
				0.005
			)
		)

	robot.wheels.set_velocity(out.left, out.right)

	n_steps = n_steps + 1
end

function light2force(inputs)
	non_zero = func.filter(function (vec) return vector.getMag(vec) > 0 end, inputs.light)
	resultant = func.foldr(function (v1, v2) return vector.add(v1, v2) end, vector.new(0,0), non_zero)
	
	log('light force: ', resultant.x, resultant.y)

	return resultant
end

function proximity2force(inputs)
	non_zero = func.filter(function (vec) return (vector.getMag(vec) > 0) end, inputs.proximity)
	resultant = func.foldr(function (v1, v2) return vector.add(v1, v2) end, vector.new(0,0), non_zero)
	resultant = vector.neg(resultant)
	
	log('proximity force: ', resultant.x, resultant.y)

	return resultant;
end

function hinib(vec1, vec2, cutoff)
	if vector.getMag(vec2) > cutoff then
		return vec2
	end

	return vec1
end

function dir2powers(dir)
	angle = vector.getAngle(dir)
	
	left = 1
	if (math.sin(angle) > 0) then
		left = math.cos(angle) 
	end
	
	right = 1
	if (math.sin(angle) < 0) then
		right = math.cos(angle)
	end

	left = left * MAX_POWER
	right = right * MAX_POWER

	return {left = left, right = right}
end

STEER_MAX_STEPS = 15
LAST_RAND = 0
function randomdir(table)
	if n_steps % STEER_MAX_STEPS == 0 then
		angle = robot.random.uniform(-math.pi, math.pi)
		LAST_RAND = vector.fromAngle(angle)
	end

	return LAST_RAND
end

function input()
	light_vectors = {}
	for i=1,24 do
		light_vectors[i] = vector.fromAngle(robot.light[i].angle)
		light_vectors[i] = vector.setMag(light_vectors[i], robot.light[i].value)
	end

	max_light = 0
	max_idx = 1
	for i=1,24 do
		if robot.light[i].value >= max_light then
			max_light = robot.light[i].value
			max_idx = i
		end
	end
	max_light_vec = vector.fromAngle(robot.light[max_idx].angle)
	max_light_vec = vector.setMag(max_light_vec, robot.light[max_idx].value)

	proximity_vectors = {}
	for i=1,24 do
		proximity_vectors[i] = vector.fromAngle(robot.proximity[i].angle)
		proximity_vectors[i] = vector.setMag(proximity_vectors[i], robot.proximity[i].value)
	end

	return {
		light = light_vectors,
		proximity = proximity_vectors,
		max_light = max_light_vec
	}
end

--[[ This function is executed every time you press the 'reset'
     button in the GUI. It is supposed to restore the state
     of the controller to whatever it was right after init() was
     called. The state of sensors and actuators is reset
     automatically by ARGoS. ]]
function reset()
	n_steps = 0
	robot.leds.set_all_colors("black")
	robot.leds.set_single_color(1, "blue")
	robot.leds.set_single_color(12, "blue")
	robot.leds.set_single_color(6, "red")
	robot.leds.set_single_color(7, "red")
end



--[[ This function is executed only once, when the robot is removed
     from the simulation ]]
function destroy()
   -- put your code here
end
