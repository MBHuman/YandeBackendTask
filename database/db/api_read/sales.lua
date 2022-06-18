local checks = require("checks")
local util = require('util')


-- _G.ERRORS:register("sales", "")

function sales(date_timestamp)
    checks('number')
    local q = util.Queue:new()

    while not q:isEmpty() do

    end
end

return sales