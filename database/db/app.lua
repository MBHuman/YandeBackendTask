#!/usr/bin/env tarantool

local _M = {}


local log = require('log')
local console = require('console')

box.cfg {
    listen = 3301
}

local ITEMS_SPACE = "items"

local ITEM_TYPE = {
    OFFER = 1,
    CATEGORY = 2,
    [1] = "OFFER",
    [2] = "CATEGORY"
}

local format_items_storage = {}
format_items_storage[1] = { name = 'id', type = 'string', is_nullable = false }
format_items_storage[2] = { name = 'name', type = 'string', is_nullable = false }
format_items_storage[3] = { name = 'item_type', type = 'unsigned', is_nullable = false }
format_items_storage[4] = { name = 'price', type = 'integer', is_nullable = true }
format_items_storage[5] = { name = 'date_timestamp', type = 'number', is_nullable = false }
format_items_storage[6] = { name = 'parent_id', type = 'string', is_nullable = true }
format_items_storage[7] = { name = 'is_created', type = 'boolean', is_nullable = false }
format_items_storage[8] = { name = 'child_nums', type = 'number', is_nullable = false }

-- local format_changed_items = {}
-- format_changed_items[1] = { name ='id', type = 'string', is_nullable = false}
-- format_changed_items[2] = { name = ''}

if not box.space[ITEMS_SPACE] then
    local s = box.schema.space.create(ITEMS_SPACE, { format = format_items_storage })
    s:create_index('primary', { type = 'tree', parts = { 'id' }, unique = true })
    s:create_index('date_timestamp', { type = 'tree', parts = { 'date_timestamp', 'item_type' }, unique = false })
    s:create_index('parent_id', { type = 'tree', parts = { 'parent_id', 'is_created' }, unique = false })
    s:create_index('created', { type = 'tree', parts = { 'is_created' }, unique = false })
end

_G.ITEM_TYPE = ITEM_TYPE
_G.ERRORS = require('errors').new()
_G.api_read = require("api_read.init")
_G.api_write = require("api_write.init")
