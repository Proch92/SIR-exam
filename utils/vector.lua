local module = {}

--- 2D vectors ----------------------------------------------

local function new(x, y)
    return {x = x, y = y}
end

local function fromAngle(angle)
    return {x = math.cos(angle), y = -math.sin(angle)}
end

local function getAngle(vec)
    return -math.atan2(vec.y, vec.x)
end

local function add(v1, v2)
    return new(v1.x + v2.x, v1.y + v2.y)
end

local function setMag(vec, magnitude)
    local newvec = module.norm(vec)
    return {x = newvec.x * magnitude, y = newvec.y * magnitude}
end

local function getMag(vec)
    return math.sqrt(vec.x^2 + vec.y^2)
end

local function neg(vec)
    return {x = -vec.x, y = -vec.y}
end

local function mul_scalar(vec, scalar)
    return {x = vec.x * scalar, y = vec.y * scalar}
end

local function norm(vec)
    magnitude = module.getMag(vec)
    if magnitude == 0 then
        return vec
    end

    return {x = vec.x / magnitude, y = vec.y / magnitude}
end

-------------------------------------------------------------

module.fromAngle = fromAngle
module.getAngle = getAngle
module.new = new
module.add = add
module.setMag = setMag
module.getMag = getMag
module.neg = neg
module.mul_scalar = mul_scalar
module.norm = norm
return setmetatable(module, {__call = function(_,...) return new(...) end})