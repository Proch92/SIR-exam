local module = {}

--- input smoothing ----------------------------------------------

window_size = 3
mod_idx = 0
window = {}

local function next()
    window[mod_idx] = table.copy(robot)
    log('svdfvfv')
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

local function init(ws)
    window_size = ws
end

-------------------------------------------------------------

module.init = init
module.next = next
return setmetatable(module, {__call = function(_,...) return new(...) end})