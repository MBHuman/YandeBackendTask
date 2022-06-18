local checks = require("checks")
local util = require('util')

local _M = {}

_G.ERRORS:register("nodes", 404)

local function nodes(id)
    checks('string')
    _f = 'nodes'

    local elem = box.space.items.index.primary:get(id)
    if elem == nil then
        util.res_except(_f, 404, "Item not found")
    end

    local result = {}
    local parent_id = -1


    local q = util.Queue:new()
    q:enqueue({id, parent_id})

    while not q:isEmpty() do
        local cur = q:dequeue()
        -- Логика c добавлением в результат
        local data = box.space.items.index.primary:get(cur[1])
        if data == nil then
            goto continue
        end
        if data.is_created then
            table.insert(result, {data, cur[2]})
            parent_id = parent_id + 1
            for _, child in box.space.items.index.parent_id:pairs({cur[1], true}) do
                q:enqueue({child.id, parent_id})
            end
        end
        ::continue::
    end
    return result
end

return nodes