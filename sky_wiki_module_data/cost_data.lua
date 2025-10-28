-- <nowiki>
-- Primary data for cost-related templates
local data = {
    unknown = {
        name = "Cost Unknown",
        link = "",
        alt_name = { "?", "??" },
        icon = 'Question-mark-Ray.png',
        sort = -1,
        no_num = true,
    },
    na = {
        name = "--",
        popup_name = "Cannot be purchased",
        sort = 99999,
        no_num = true,
    },
    free = {
        name = "free",
        sort = 0,
        no_num = true,
    },
    sp = {
        name = "[[Season Pass|SP]]",
        short_name = "SP",
        alt_name = { "Season Pass", "AP" },
        sort = 0.5,
        no_num = true,
    },
    ['$'] = {
        -- This name is not actually used
        name = "US Dollars",
        short_name = "USD",
        sort = false,
    },
    ['jpy'] = {
        -- This name is not actually used
        name = "Japanese Yen",
        short_name = "JPY",
        sort = false,
    },
    c = {
        name = "Candle",
        short_name = "C",
        link = "Candle (Currency)",
        icon = "Regular-candle-icon-Morybel-0146.png",
        sort = false,
    },
    h = {
        name = "Heart",
        short_name = "H",
        icon = "Heart.png",
        sort = false,
    },
    ac = {
        name = "Ascended Candle",
        short_name = "AC",
        icon = "Ascended-candle-icon-Morybel-0146.png",
        sort = false,
    },
    sc = {
        name = "Season Candle",
        short_name = "SC",
        alt_name = { "Seasonal Candle" },
        use_season = "sc_icon",
        sort = false,
    },
    sh = {
        name = "Season Heart",
        short_name = "SH",
        alt_name = { "Seasonal Heart" },
        use_season = "sh_icon",
        sort = false,
    },
    t = {
    	name = "Ticket",
    	short_name = "T",
    	alt_name = { "Event Currency", "Event Ticket" },
    	use_day = "t_icon",
    	sort = false,
    },
    wax = {
    	name = "Pieces of Light",
    	short_name = "L",
    	alt_name = { "Wax", "Piece of Light" },
    	icon = "Piece-of-light.png",
    	sort = false,
    },
    d = {
    	name = "Dye",
    	short_name = "D",
    	alt_name = { "Dyes "},
    	use_dye = "d_icon",
    	sort = false,
	}
}
local stdData = require('Module:stdData')
-- Process data, including merging in language-specific overrides
return stdData.processData(data, 'Cost')