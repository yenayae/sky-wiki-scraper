-- <nowiki>
-- Implements {{Template:Spirit Item}}, {{Template:Item Label}}, {{Template:Icon Name}}
local getArgs = require('Dev:Arguments').getArgs
local stdData = require('Module:StdData')
local stdText = require('Module:stdText')
local icon = require('Module:Icon')
local spirits = require('Module:Spirits')

local itemData = mw.loadData("Module:Spirit_Item/data")

local p = {}

-- Invoked by Template:Spirit_Item
function p.icon(frame)
    local args = getArgs(frame, {removeBlanks=false} )
    return p.doIcon(args)
end

-- Invoked by Template:Item_Label
function p.name(frame)
    local args = getArgs(frame, {removeBlanks=false} )
    return p.doName(args[1])
end

-- Invoked by Template:Icon_Name
-- This function is named 'file' instead of 'name' to make it clear that this
-- is used to get a filename (whereas 'name' in the context of itemData
-- is a translatable string providing the label for this item type)
function p.file(frame)
    local args = getArgs(frame, {removeBlanks=false})
    return p.doFile(args)
end


-- Does actual work of implementing Template:Spirit_Item
function p.doIcon(args)
    -- Transfer all numeric arguments into named arguments
    args.spirit = spirits.getKey(args)
    args.icon_type = args.icon_type or args[2] or ''
    -- Because position of format in args is different, make sure format is set even if args[3] is nil
    args.format    = args.format or args[3] or ''

    -- If icon_type is music#, send request to Music_Sheet to generate
    -- full icon + overlay.
    -- (Whereas if icon_type is just 'music', handle it here with the
    -- generic music sheet icon)
    if (string.sub(args.icon_type,1,5)=='music' and string.len(args.icon_type)>5) then
        local music = require('Module:Music Sheet')
        args.music_id = args.music_id or string.sub(args.icon_type,6)
        return music.doIcon(args)
    end
	
    p.prepIcon(args)
    return icon.doIcon(args)
end

-- Configures all information in args so that icon.doIcon will generate
-- the spirit item icon.
-- Expects all input to be in named (not numeric) args
function p.prepIcon(args)
    args.spirit = args.spirit or args.season
    if not args.season then
        -- Add season into args for sake of ultimate item labels
        local seasonData = mw.loadData("Module:Seasons/data")
        local season = stdData.getKey(args.spirit.key or args.spirit, seasonData)
        if season.table then
    	    args.season = season.key
        end
    end
    
    args.icon  = args.icon or p.doFile(args)

    -- For label, args is passed into doName so that emote_name/inst_name
    -- are used as appropriate
    stdData.setLabelByType(args)
    args.label = args.label or p.doName(args.icon_type, args)

    p.setLink(args)
    return args
end

-- Link for spirit_items is handled differently than nearly all other
-- links.  Because default is spirit_page#section instead of item_page
function p.setLink(args)
    if (mw.title.getCurrentTitle().text ~= stdText.doText('closet_spaces_name')
    		and (args.link_type == 'in_page' or args.in_page)) then
        -- As always, in_page overrides any automatic link
        -- Closet Spaces page ignores in_page
        args.link_base = args.link_base or mw.title.getCurrentTitle().text
    else
        local seasonData = mw.loadData("Module:Seasons/data")
        local spiritData = mw.loadData("Module:Spirits/data")
        local itemType, baseType, suffix = p.getItemType(args.icon_type)

        -- For emote/inst, use a spirit-specific link if available
        -- (This is not expected to be the typical case .... it's really
        -- just here for overall logic consistency.  And so that if there
        -- were some reason why the default failed, it's possible to
        -- override it).
        -- Note that these do *not* fallback to emote_name/inst_name --
        -- because spirit_page#Expression / spirit_page#Instrument
        -- are considered to be safer/more reliable (they don't require
        -- redirects to be setup; they work as in-page links within the
        -- spirit_page instead of forcing an unneded redirect page load)
        if baseType=='emote' then
            args.link = args.link or stdData.getValue({ key=args.spirit, value='emote_link' }, spiritData, seasonData)
        elseif baseType=='instrument' then
            args.link = args.link or stdData.getValue({ key=args.spirit, value='inst_link' }, spiritData, seasonData)
        end

        if not args.link then
            -- Default treatment here is to fill link_base NOT link
            -- so that final output is spirit_page#section
            args.link_base = args.link_base or spirits.getLink(args)

            -- args.section and args.label invoke p.doName slightly differently --
            -- args is NOT passed in here; want to get generic 'Expression'/'Instrument'.
            -- But for args.label, want to do emote_name/inst_name lookup.
            -- Also for now at least section for any ultimate gift should be 'Ultimate Gifts'
            if suffix and suffix=='u' then
            	local stdText = require('Module:StdText')
            	args.section = args.section or stdText.doText('ult_section')
            else
            	args.section = args.section or p.doName(args.icon_type)
            end
        end
    end
    return args
end

-- Get the standard name (label) for a given type of item
-- Takes two arguments
-- * icon_type/item (string), for consistency with Template:Icon_Label usage)
-- * args (the full args array) is an OPTIONAL second argument. It should only be
--   provided when requesting the spirit-specific emote_name/inst_name
function p.doName(value, args)
    local seasonData = mw.loadData("Module:Seasons/data")
    local itemType, baseType, suffix = p.getItemType(value)
    local id, name

    if not baseType then
        if itemType=='music' then
            local music = require('Module:Music Sheet')
            return music.getStdName()
        else
            return itemType
        end
    elseif args and args.spirit and (baseType=='emote' or baseType=='prop' or baseType=='mask' or baseType=='instrument') then
        local spiritData = mw.loadData("Module:Spirits/data")
        -- Custom names for multiple emotes, props, and masks
        if (baseType~='instrument') then
            id = baseType .. '_name'
            if suffix ~= nil and suffix ~= '' then
            	id = baseType .. '_' .. suffix .. '_name'
            end
        else
        	-- When there is no suffix and is not an ult instrument
        	if suffix ~= nil and suffix ~= '' and suffix ~= 'u' then
        		id = 'inst_' .. suffix .. '_name'
        	else
            	id = 'inst_name'
            end
        end
        name = stdData.getValue( { key=args.spirit, value=id }, spiritData, seasonData)
        if name then
            return name
        end
    end

    if suffix=='u' then
        name = stdData.getValue( { key=baseType , value='ult_name' } , itemData)
        if name and name~='' then
        	if args and args.season then
        		-- Add season short name to the item label
        		local prep = stdData.getValue({ key=args.season, value={'preposition'}}, seasonData)
        		-- For languages with gendered words
        		if prep and prep~='' and prep~=nil then
        			name = name .. ' ' .. prep .. ' ' .. stdData.getValue({ key=args.season, value={'short_name','name'}}, seasonData)
        		-- For languages with neutral words
        		else
        			name = stdData.getValue({ key=args.season, value={'short_name','name'}}, seasonData)
        		    	   .. ' ' .. name
        		end
            end
        	return name
        end
    end
    
    -- Providing labels for spirit items as <Spirit Name> <Cosmetic>
    -- Or <Season Short Name> <Cosmetic>, but not for the inline_text format
    -- because it becomes redundant
    if args and args.spirit and args.format~='inline_text' then
    	local spiritData = mw.loadData("Module:Spirits/data")
    	local spirit_name = stdData.getValue({ key=args.spirit, value='name' }, spiritData) or stdData.getValue({ key=args.spirit, value='short_name' }, seasonData)
    	local cosmetic = stdData.getValue({ key=baseType, value='name' }, itemData)

    	local prep = stdData.getValue({ key=args.spirit, value='preposition'}, spiritData) or stdData.getValue({ key=args.spirit, value='preposition' }, seasonData)
        if spirit_name~=nil and cosmetic~=nil then
        	-- For languages with gendered words
        	if prep and prep~='' and prep~=nil then
        		return cosmetic .. ' ' .. prep .. ' ' ..  spirit_name
        	-- For languages with neutral words
        	else
        		return spirit_name .. ' ' .. cosmetic
        	end
        end
    end
    return stdData.getValue({ key=baseType , value='name' } , itemData)
end

-- Returns the itemType, baseType, and suffix
-- * itemType is the ID used for this icon in spiritData/seasonData.
-- * baseType is the ID used to get secondary data (name) from itemData
--   baseType is nil if there is no itemData entry
-- * suffix is any extra text that converts baseType into itemType
--   if suffix is nil, itemType==baseType
--   otherwise, itemType == baseType .. '_' .. suffix
function p.getItemType(value)
    local itemType = stdData.getKeyString(value)
    local baseType, suffix

    -- Backwards compatibility
    -- tier_2_cape has also been added as an alt_name for cape in Spirit_Item/data
    -- But then I remembered why I put in this hard-coded exception: need to have
    -- tier_2_cape map to 'cape_2' not just 'cape'.  In other words, handling via
    -- alt_name would convert tier_2_cape into just 'cape' and therefore would
    -- return the tier 1 cape.
    if itemType == 'tier_2_cape' then
        return 'cape_2', 'cape', '2'
    end
    
    -- Adding additional hard-coded exceptions for "real" versions of the cosmetics
    -- Similarly to the tier 2 cape, this allows the label and link to not include
    -- the '_real', '_front', or '_interior' part of the itemType
    if string.sub(itemType,1,5)== 'cape_' then
    	if string.sub(itemType,-6,-1)== '_front' or string.sub(itemType,-9,-1)== '_interior' then
    		if string.sub(itemType,7,7)=='_' then
    			-- Has a suffix
    			return itemType, 'cape', string.sub(itemType,6,6)
    		else
        		return itemType, 'cape'
        	end
    	elseif string.sub(itemType,-5,-1)== '_real' or string.sub(itemType,-5,-1)== '_back' then
    		if string.sub(itemType,7,7)=='_' then
    			-- Has a suffix
    			return string.sub(itemType,1,-5) .. 'real', 'cape', string.sub(itemType,6,6)
    		else
        		return string.sub(itemType,1,-5) .. 'real', 'cape'
        	end
    	end
    elseif string.sub(itemType,-5,-1)== '_real' then
       	if string.sub(itemType,-7,-7)=='_' then
       		-- Has a suffix
    		return itemType, string.sub(itemType,1,-8), string.sub(itemType,-6,-6)
    	else
    		return itemType, string.sub(itemType,1,-6)
    	end
    end
    
    -- Extract any suffix
    if string.sub(itemType,-2,-2)=='_' then
        suffix = string.sub(itemType,-1)
        baseType = string.sub(itemType,1,-3)
    else
        baseType = itemType
    end

    -- Check whether baseType exists in itemData table AND has icon_type=='Spirit Item'
    -- (other entries in itemData table are friendship-node-specific and should not
    -- exist as spirit item icons)
    if not itemData[baseType] then
            return itemType
    -- Look for base type (non-suffixed) in itemData table, see whether it is an alias
    elseif type(itemData[baseType])=='string' then
        baseType = itemData[baseType]
    end
    if itemData[baseType].icon_type~='Spirit Item' then
        return itemType
    end

    -- Construct final value of itemType, in case alias conversion was done
    local itemType = baseType
    if suffix then
        itemType = itemType .. '_' .. suffix
    end

    return itemType, baseType, suffix
end

-- Find name of the icon based on the requested purpose
function p.doFile(args)
    local spiritData = mw.loadData("Module:Spirits/data")
    local seasonData = mw.loadData("Module:Seasons/data")
    
    local instData = mw.loadData("Module:Instruments/data")
    local daysItemData = mw.loadData("Module:Days Item/data")

    -- Requested spirit (or season)
    local spiritKey = spirits.getKey(args)
    -- Requested item type
    -- itemType is the key used for this icon in the spirits data table
    -- baseType is itemType without any suffix OR nil if type is not recognized
    -- suffix is any extra character that appears at end of type after an underscore
    local itemType, baseType, suffix = p.getItemType(args.item or args.icon_type or args[2])
    
    -- Requested modification to the item type
    -- Provides the variations of the cosmetics by adding _variation to the itemType
    local variations = {
    	['real'] = true,
    	['back'] = true,
    	['front'] = true,
    	['interior'] = true,
    	['exterior'] = true,
    	['side'] = true,
    	['held'] = true,
    }
    if (args[3] and not variations[string.lower(args[2])] ) then
    	local realKeyword = string.lower(args[3])
    	if variations[realKeyword] then
    		-- Catch if you accidentally request for 'back' for capes
    		if realKeyword=='back'and string.lower(args[2]).sub(itemType,1,4)=='cape' then
    			itemType = itemType .. '_real'
    			suffix   = 'real'
    		else
    			itemType = itemType .. '_' .. realKeyword
    			suffix   = realKeyword
    		end
    	end
    end
    -- Work out whether other alternative values should be recognized for itemType,
    -- based on info specified in data file.
    -- In particular, allows instrument/prop to be synonyms.
    -- Also could allow other languages to set up keys that work better in those languages
    local lookupType = { itemType }
    if baseType then
        local alt_names = itemData[baseType]['alt_name']
        if type(alt_names)=='string' and alt_names~='' then
            alt_names = { alt_names }
        end
        if type(alt_names)=='table' then
            for _,name in pairs(alt_names) do
                if suffix then
                	name = name .. '_'.. suffix
                end
                table.insert( lookupType, name )
            end
        end
    elseif itemType=='music' then
        -- Generic music sheet icon
        -- (Don't even try to handle full spirit-specific music icon here,
        --  because it requires overlaying two separate files)
        local music = require('Module:Music Sheet')
        return music.getStdIcon()
    end
    
    -- Catch if you accidentally request for 'back' for capes for Days Items
    if itemType=='back' and baseType==nil and suffix==nil then
    	table.insert( lookupType, 'real' )
    end
    -- Final fallback is 'icon'
    table.insert( lookupType, 'icon' )

    -- Lookup file name checking each value name in lookupType
    local file = stdData.getValue( { key = spiritKey, value = lookupType }, spiritData, seasonData, daysItemData, instData )

    if not file or file=='' then
        -- On any type of failure, return defaultIcon
        return icon.defaultIcon
    else
        return file
    end
end

return p