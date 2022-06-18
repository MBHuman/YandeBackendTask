

local api_write = {}

local name_mod = "api_write"

local submodules = {
    'imports',
    'delete'
}

api_write.reload = function()
    for _, name_submod in pairs(submodules) do
        package.loaded[name_mod .. "." .. name_submod] = nil
    end
    for _, name_submod in pairs(submodules) do
        api_write[name_submod] = require(name_mod .. "." .. name_submod)
    end
end

api_write.reload()


return api_write