local checks = require("checks")


-- _G.ERRORS:register("statistic", "")

function statistic(id, start_timestamp, end_timestamp)
    checks('string', 'number', 'number')
end

return statistic