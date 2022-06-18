local util = require('util')
local log = require('log')


_G.ERRORS:register("imports", 400)

local function imports(request)

    local _f = 'imports'
    local items = request.items
    local updateDate = request.updateDate
    log.info(items)
    log.info(updateDate)
    -- Валидация данных

    local is_validated = true
    box.begin()
    for _, item in pairs(items) do
        local id = item.id
        local name = item.name
        local parentId = item.parentId
        local type = item.type
        local price = item.price

        log.info(parentId)
        local parent = box.space.items.index.primary:get(parentId)
        local item_obj = box.space.items.index.primary:get(id)

        if item_obj ~= nil then
            if item_obj.item_type ~= ITEM_TYPE[type] then
                is_validated = false
            end
        end


        if parent ~= nil then
            if parent.item_type ~= ITEM_TYPE['CATEGORY'] then
                local line = debug.getinfo(2, 'l').currentline
                log.info({item, line})
                is_validated = false
            end
        else
            if parentId ~= 'None' then
                box.space.items:insert { parentId, '', ITEM_TYPE['CATEGORY'], box.NULL, updateDate, box.NULL, false }
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
        log.info(info)
        if info ~= nil then
            box.space.items.index.primary:update(id, {
                { '=', 2, name }, -- name
                { '=', 5, updateDate }, -- updateDate
                { '=', 7, true }
            })
            if parentId ~= 'None' then
                box.space.items.index.primary:update(id, {
                    { '=', 6, parentId } -- parentId
                })
            end
            if type == 'OFFER' then
                box.space.items.index.primary:update(id, {
                    { '=', 4, price } -- price
                })
            end
        else
            if parentId == 'None' then
                parentId = box.NULL
            end
            box.space.items:insert { id, name, ITEM_TYPE[type], price, updateDate, parentId, true }
        end
    end
    box.commit()
end

return imports
