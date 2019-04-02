local module = {}

--- functional -------------------------------------------

local function map(func, tbl)
    local newtbl = {}
    for i,v in pairs(tbl) do
        newtbl[i] = func(v)
    end
    return newtbl
end

local function filter(func, tbl)
    local newtbl= {}
    for i,v in pairs(tbl) do
        if func(v) then
		    newtbl[i]=v
        end
    end
    return newtbl
end

local function foldr(func, val, tbl)
    for i,v in pairs(tbl) do
        val = func(val, v)
    end
    return val
end

-------------------------------------------------------------

module.map = map
module.filter = filter
module.foldr = foldr
return setmetatable(module, {__call = function(_,...) return new(...) end})