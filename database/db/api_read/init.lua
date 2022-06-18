local api_read = {}

local name_mod = 'api_read'

local submodules = {
    'nodes',
    'sales',
    'statistic'
}

api_read.reload = function()
    for _, name_submod in pairs(submodules) do
        package.loaded[name_mod .. "." .. name_submod] = nil
    end
    for _, name_submod in pairs(submodules) do
        api_read[name_submod] = require(name_mod .. "." .. name_submod)
    end
end

api_read.reload()


return api_read