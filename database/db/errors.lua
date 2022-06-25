--- Модуль для динамической регистрации ошибок

-- import
local checks = require('checks')
local log = require('log')


local _M = {}

-- Класс объекта ErrorsClass
local ErrorsClass = {}

--- Регистрация ошибка
function ErrorsClass:register(func, code)
    checks('table', 'string', 'number')
    local mod = debug.getinfo(2, "S").source
    -- log.verbose("register: module=%s, func=%s, code=%s", mod, func, code)
    if self[mod] == nil then
        self[mod] = {}
    end
    if self[mod][func] == nil then
        self[mod][func] = {}
    end
    if self[mod][func][code] ~= nil then
        log.error("ErrorClass:register already code=%s exists for func=%s", code, func)
    end
    self[mod][func][code] = 1
end

--- Получение ошибки по коду, нужно вызывать в том же методе
function ErrorsClass:get(file, func, code)
    checks('table', 'string', 'string', 'number')
    
    if self[file] == nil then
        return nil
    end
    if self[file][func] == nil then
        return nil
    end
    if self[file][func][code] == nil then
        return nil
    end
    return self[file][func][code]
end


--- Функция возвращает объект Errors для регистрации и обработки ошибок
function _M.new(data)
    local self = {}
    setmetatable(self, { __index = ErrorsClass })
    return self
end


return _M