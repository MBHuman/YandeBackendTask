local checks = require("checks")
local util = require('util')


-- _G.ERRORS:register("sales", "")

function sales(from_timestamp, to_timestamp)
    checks('number', 'number')
    local result = {}

    for _, e in box.space.items.index.date_timestamp:pairs({to_timestamp, ITEM_TYPE['OFFER']}, {iterator='LE'}) do
        if e.item_type == ITEM_TYPE.OFFER then
            table.insert(result, e)
        end
        if e.date_timestamp <= from_timestamp then
            goto continue 
        end
    end
    ::continue::
    return result
end

return sales