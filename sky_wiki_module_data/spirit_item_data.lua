-- <nowiki>
-- Data for spirit items and also for other links found
-- on friendship tree
-- For types recognized by spirit items (i.e., tags that are used to
-- identify icons in Spirits/data), use icon_type='Spirit Item',

-- Note that many of the tags/IDs used in this file are also used
-- in other data sets (e.g., heart and season_heart also appear in
-- Costs/data).  This is expected to not cause any conflict, because
-- this dataset is only going to be used for specific lookups, not
-- for general match-an-ID-to-any-data lookups.
local data = {
    cape = {
        name = "Cape",
        ult_name = "Ultimate Cape",
        icon_type = 'Spirit Item'
    },
    hair = {
        name = "Hair",
        ult_name = "Ultimate Hair",
        icon_type = 'Spirit Item'
    },
    headpiece = {
        name = "Head Accessory",
        ult_name = "Ultimate Head Accessory",
        icon_type = 'Spirit Item'
    },
    hairpiece = {
        name = "Hair Accessory",
        ult_name = "Ultimate Hair Accessory",
        icon_type = 'Spirit Item'
    },  
    facepiece = {
        name = "Face Accessory",
        ult_name = "Ultimate Face Accessory",
        icon_type = 'Spirit Item'
    },      
    instrument = {
        name = "Instrument",
        ult_name = "Ultimate Instrument",
        alt_name = { "prop" },
        icon_type = 'Spirit Item'
    },
    mask = {
        name = "Mask",
        ult_name = "Ultimate Mask",
        icon_type = 'Spirit Item'
    },
    necklace = {
        name = "Necklace",
        ult_name = "Ultimate Pendant",
        alt_name = { "pendant" },
        icon_type = 'Spirit Item'
    },
    neckpiece= {
        name = "Neck Accessory",
        ult_name = "Ultimate Neck Accessory",
        icon_type = 'Spirit Item'
    },
    outfit = {
        name = "Outfit",
        ult_name = "Ultimate Outfit",
        icon_type = 'Spirit Item'
    },
    footwear = {
        name = "Shoes",
        ult_name = "Ultimate Shoes",
        icon_type = 'Spirit Item'
    }, 
    shoes = {
        name = "Shoes",
        ult_name = "Ultimate Shoes",
        icon_type = 'Spirit Item'
    },  
    prop = {
        name = "Prop",
        ult_name = "Ultimate Prop",
        alt_name = { "instrument" },
        icon_type = 'Spirit Item',
    },
    emote = {
        -- This is being handled like the other item types, even though 'emote' is no longer being
        -- used as an icon ID in the spirit data.  It effectively still works because the emote
        -- is now provided under 'icon' which is the default icon for the spirit.
        -- As far as Spirit_Item template, emote might not need to be recognized long term.
        -- BUT this id does have to remain present permanently for the sake of
        -- Friendship Node
        name = "Expression",
        alt_name = { "call", "stance", "expression", "action", "friend action" },
        icon_type = 'Spirit Item',
    },
    stance = {
    	name = "Stance"	
    },
    call = {
    	name = "Call"	
    },
    action = {
    	name = "Friend Action"	
    },

    -- Friendship Node icons generated using Cost.doIcon
    heart = {
        icon_type = 'Cost',
        cost = '3 C',
    },
    season_heart = {
        icon_type = 'Cost',
        cost = '3 SC SP',
    },
    
    -- Generate music using Music_Sheet.doIcon
    -- Special processing is also done in code to extract ID
    music = {
         icon_type = 'Music_Sheet',
         cost = '15 C',
    },

    -- Items generated using specified icons.
    -- On English wiki, redirects have been setup for each of the following
    -- names, so 'name' works as both label and link.
    -- Other languagues could opt to specify 'name' for the label, and
    -- then separately specify 'link' instead of setting up a redirect.
    wing = {
        name = 'Wing Buff',
        icon = 'Winglight.png',
        cost = '2 AC',
    },
    spell1 = {
        name = '1 Candle Blessing',
        icon = '1CandleSpell.png',
        cost = '1 C',
    },
    spell5 = {
        name = '5 Candle Blessing',
        icon = '5CandlesSpell.png',
        cost = '5 C',
    },
    spellx = {
        name = 'Special Blessings',
        icon = 'Special-event-spell-icon.png',
    },
    trail_spell = {
        name = 'Color Trail Spell',
        icon = 'Color-trail.png',
    },
    
    dye = {
    	name = 'Dye',
    	icon = 'Test-dye-container-icon.png',
    },
    random_dye = {
    	name = 'Random Dye',
		icon = 'Random-dye-icon.png',
    },
    red_dye = {
    	name = 'Red Dye',
    	icon = 'Red-dye-container-icon.png',
    },
    yellow_dye = {
    	name = 'Yellow Dye',
    	icon = 'Yellow-dye-container-icon.png',
    },
    green_dye = {
    	name = 'Green Dye',
    	icon = 'Green-dye-container-icon.png',
    },
    cyan_dye = {
    	name = 'Cyan Dye',
    	icon = 'Cyan-dye-container-icon.png',
    },
    blue_dye = {
    	name = 'Blue Dye',
    	icon = 'Blue-dye-container-icon.png',
    },
    purple_dye = {
    	name = 'Purple Dye',
    	icon = 'Purple-dye-container-icon.png',
    },
    black_dye = {
    	name = 'Black Dye',
    	icon = 'Black-dye-container-icon.png',
    },
    white_dye = {
    	name = 'White Dye',
    	icon = 'White-dye-container-icon.png',
    },
    
    quest = {
        icon = 'Exclamation-mark-Ray.png',
    },
    warp = {
    	name = 'Warp',
    	icon = 'Icon_warp.png'
    },
    follow = {
    	icon = 'Spirit-relationship-follow-icon.png',
    },
    relationship = {
    	icon = 'Spirit-relationship-icon.png',	
    },
    new = {
        icon = 'Four-point-star-Ray.png',
    },
    

}
local stdData = require('Module:stdData')
-- Process data, including merging in language-specific overrides
return stdData.processData(data, 'Spirit Item')