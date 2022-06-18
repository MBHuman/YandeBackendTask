local util = require('util')
local log = require('log')


_G.ERRORS:register("imports", 400)

local function imports(request)

    local _f = 'imports'
    local items = request.items
    local updateDate = request.updateDate
    -- Валидация данных

    local is_validated = true
    box.begin()
    for _, item in pairs(items) do
        local id = item.id
        local name = item.name
        local parentId = item.parentId
        local type = item.type
        local price = item.price


        local elem = box.space.items.index.primary:get(id)
        if elem ~= nil then
            if elem.item_type ~= ITEM_TYPE[type] then
                is_validated = false
            end
        else
            if ITEM_TYPE[type] == ITEM_TYPE.CATEGORY then
                box.space.items:insert { id, name, ITEM_TYPE.CATEGORY, box.NULL, updateDate, parentId, false, 0 }
            else
                box.space.items:insert { id, name, ITEM_TYPE.OFFER, price, updateDate, parentId, false, 1 }
            end
        end

        if parentId ~= 'None' then
            local parent = box.space.items.index.primary:get(parentId)
            if parent ~= nil then
                if parent.item_type ~= ITEM_TYPE.CATEGORY then
                    is_validated = false
                end
            else
                box.space.items:insert { parentId, '', ITEM_TYPE.CATEGORY, box.NULL, updateDate, box.NULL, false, 0 }
            end
        end

        if not is_validated then
            goto p_end
        end
    end
    ::p_end::
    if not is_validated then
        util.res_except(_f, 400, "ValidationFailed")
    end

    for _, item in pairs(items) do
        local id = item.id
        local name = item.name
        local parentId = item.parentId
        local type = item.type
        local price = item.price

        local info = box.space.items:get(id)

        -- Заносим данные в историю

        ---
        if type == 'OFFER' then
            box.space.items.index.primary:update(id, {
                { '=', 4, price } -- price
            })
        end

        box.space.items.index.primary:update(id, {
            { '=', 2, name }, -- name
            { '=', 5, updateDate }, -- updateDate
            { '=', 7, true }
        })

        

        if parentId ~= 'None' then
            
        else
            box.space.items.index.primary:update(id, {
                { '=', 6, box.NULL }
            })
        end
    end
    box.commit()
end

return imports
