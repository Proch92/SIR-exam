local module = {}

--- input smoothing ----------------------------------------------

window_size = 3
mod_idx = 0
window = {}
index = {}

local function next(key, tbl)
    -- add table to window
    if index[key] == nil then
        index[key] = 0
    end
    log(index[key])
    index[key] = (index[key] + 1) % window_size
    window[key][index[key]] = copy_table(tbl)

    -- sum
    smoothed = {}
    non_nil = 0
    for w=0,(window_size-1) do
        if window[w] ~= nil then
            for i=1,24 do
                if smoothed[i] == nil then
                    smoothed[i] = 0
                end
                smoothed[i] = smoothed[i] + window[key][w][i]
            end
            non_nil = non_nil + 1
        end
    end

    -- average
    for i=1,24 do
        smoothed[i] = smoothed[i] / non_nil
    end

    return smoothed
end

local function init(ws)
    window_size = ws
end

local function copy_table(tbl)
    local newtable = {}

    for k,v in pairs(tbl) do
        newtable[k] = v
    end

    return newtable
end

-------------------------------------------------------------

module.init = init
module.next = next
return setmetatable(module, {__call = function(_,...) return new(...) end})