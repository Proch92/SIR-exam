local vector = require('utils.vector');
local func = require('utils.functional');
local matrix = require('utils.matrix');

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
	inputs = input(robot)
	light_component = light2force(inputs)
	proximity_component = proximity2force(inputs)
	random_component = randomdir(light_component, proximity_component)
	forward_component = forward(light_component, proximity_component)

	components = {light_component, proximity_component, forward_component}
	sum = func.foldr(function(v1, v2) return vector.add(v1, v2) end, vector.new(0,0), components)

	if vector.getMag(sum) < MAX_POWER then
		sum = vector.setMag(sum, MAX_POWER)
	end

	log('total: ', vector.getMag(sum))

	out = dir2powers(sum)
	robot.wheels.set_velocity(out.left, out.right)

	n_steps = n_steps + 1
end

function light2force(inputs)
	non_zero = func.filter(function (vec) return vector.getMag(vec) > 0 end, inputs.light)
	resultant = func.foldr(function (v1, v2) return vector.add(v1, v2) end, vector.new(0,0), non_zero)
	resultant = vector.setMag(resultant, vector.getMag(resultant) ^ 0.1)

	log('light: ', vector.getMag(resultant))

	return resultant
end

function proximity2force(inputs)
	non_zero = func.filter(function (vec) return (vector.getMag(vec) > 0) end, inputs.proximity)
	resultant = func.foldr(function (v1, v2) return vector.add(v1, v2) end, vector.new(0,0), non_zero)
	resultant = vector.neg(resultant)

	angle = vector.getAngle(resultant)
	mag = vector.getMag(resultant)

	if math.sin(angle) > 0 then
		angle = angle - (math.pi / 2.2)
	else
		angle = angle + (math.pi / 2.2)
	end

	tangent = vector.fromAngle(angle)
	tangent = vector.setMag(tangent, tanh(mag) * 2)
	
	log('proximity: ', vector.getMag(tangent))

	return tangent;
end

STEER_MAX_STEPS = 100
rand_angle = math.pi / 2
function randomdir(light, proximity)
	if n_steps % STEER_MAX_STEPS == 0 then
		rand_angle = robot.random.uniform(-math.pi, math.pi)
	end

	light_mag = vector.getMag(light)
	proximity_mag = vector.getMag(proximity)
	resultant = vector.fromAngle(rand_angle)
	resultant = vector.setMag(resultant, relu(1 - math.max(light_mag, proximity_mag)))

	log('random: ', vector.getMag(resultant))

	return resultant
end

function forward(light, proximity)
	light_mag = vector.getMag(light)
	proximity_mag = vector.getMag(proximity)
	resultant = vector.fromAngle(0)
	resultant = vector.setMag(resultant, relu(1 - math.max(light_mag, proximity_mag)))

	log('forward: ', vector.getMag(resultant))

	return resultant
end

function relu(x)
	y = 0
	if x > 0 then
		y = x
	end
	return y
end

function tanh(x)
	return (math.exp(2*x) - 1) / (math.exp(2*x) + 1)
end

function dir2powers(vec)
	angle = vector.getAngle(vec)
	magnitude = vector.getMag(vec)

	L = robot.wheels.axis_length

	conversion = matrix{{1, -L/2}, {1, L/2}}
	polar = matrix{{magnitude}, {angle}}

	linear = conversion * polar

	log('linear: ', linear[1][1], ' ', linear[2][1])

	return {left = linear[1][1], right = linear[2][1]}
	--return {left = left, right = right}
end

window_size = 3
mod_idx = 0
window = {}

function smooth()
	log('gf')
    window[mod_idx] = table.copy(robot)
    log('asd')
    mod_idx = (mod_idx + 1) % window_size
    smoothed = {}
    non_nil = 0
    for w=0,(window_size-1) do
        if window[w] ~= nil then
            for i=1,24 do
                smoothed.light[i] = smoothed.light[i] + window[w].light[i]
            end
            for i=1,24 do
                smoothed.proximity[i] = smoothed.proximity[i] + window[w].proximity[i]
            end
            non_nil = non_nil + 1
        end
    end

    for i=1,24 do
        smoothed.light[i] = smoothed.light[i] / non_nil
        smoothed.proximity[i] = smoothed.proximity[i] / non_nil
    end

    return smoothed
end

function input(tbl)
	light_vectors = {}
	for i=1,24 do
		light_vectors[i] = vector.fromAngle(tbl.light[i].angle)
		light_vectors[i] = vector.setMag(light_vectors[i], tbl.light[i].value)
	end

	proximity_vectors = {}
	for i=1,24 do
		proximity_vectors[i] = vector.fromAngle(tbl.proximity[i].angle)
		proximity_vectors[i] = vector.setMag(proximity_vectors[i], tbl.proximity[i].value)
	end

	return {
		light = light_vectors,
		proximity = proximity_vectors
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
