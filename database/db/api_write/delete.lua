local checks = require("checks")
local util = require("util")

_G.ERRORS:register("delete", 404)
_G.ERRORS:register("delete", 400)

local function delete(id)
    checks('string')
    local _f = 'delete'

    local elem = box.space.items.index.primary:get(id)
    if elem == nil or not elem.is_created then
        util.res_except(_f, 404, "Item not found")
    end

    local q = util.Queue:new()
    q:enqueue(id)

    box.begin()
    while not q:isEmpty() do
        local cur = q:dequeue()
        box.space.items.index.primary:delete(cur)
        for _, child in box.space.items.index.parent_id:pairs({cur, true}) do
            q:enqueue(child.id)
        end
    end
    box.commit()
end

return delete
