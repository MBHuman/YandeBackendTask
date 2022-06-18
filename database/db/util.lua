local checks = require('checks')
local json = require('json')
local log = require('log')

local _M = {}

local Queue = {}

function Queue:new()
    local object = {}

    object.list = {}
    object.offset = 1

    self.__index = self
    return setmetatable(object, self)
end

function Queue:length()
    return #self.list - self.offset
end

function Queue:isEmpty()
    return #self.list == 0
end

function Queue:enqueue(item)
    table.insert(self.list, item)

    return self
end

function Queue:peek()
    if not self:isEmpty() then
        return self.list[self.offset]
    end

    return nil
end

function Queue:dequeue()
    if self:isEmpty() then return nil end

    local item = self.list[self.offset]
    self.offset = self.offset + 1

    if (self.offset * 2) >= #self.list then
        self:optimize()
    end

    return item
end

function Queue:optimize()
    local pos, new = 1, {}

    for i = self.offset, #self.list do
        new[pos] = self.list[i]
        pos = pos + 1
    end

    self.offset = 1
    self.list = new
end

_M.Queue = Queue

function _M.res_except(func, code, msg)
    checks('string', 'number', 'string')
    local mod = debug.getinfo(2, "S").source
    local line = debug.getinfo(2, 'l').currentline
    log.error("EXCEPTION (module=\"%s\", func=\"%s\", line=%s, code_err=\"%s\", msg=\"%s\")", mod, func, line, code, msg)
    if _G.ERRORS:get(mod, func, code) == nil then
        log.error("UNREGISTER ERROR (module=\"%s\", func=\"%s\", line=%s, code_err=\"%s\", msg=\"%s\")", mod, func, line, code, msg)
    end
    local reason = json.encode({
        status = "exception",
        code = code,
        description = msg,
        ver = "v1"
    })
    local reason = reason:gsub('\"', '\\"') -- экранирование ковычек для nginx
    box.error({ code = code, reason = reason })
end

return _M
