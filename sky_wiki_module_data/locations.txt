-- <nowiki>
-- Primary data for all seasons
-- Translations should **NOT** be added to this file -- this file should always
-- be identical across all wikis.
-- Instead, a language-specific subfile provides all translated text.
-- Only variables ending in 'name' will ever need to be translated.
local data = {

    isle = {
        name         = "Isle of Dawn",
        short_name   = "Isle",
        sort         = 100,
    },
    cave_of_prophecies = {
        name         = "Cave of Prophecies",
        sort         = 101,
        realm        = "isle",
    },
    passage_stone = {
    	name         = "Passage Stone",
        sort         = 102,
        realm        = "isle",
    },
    isle_temple = {
        name         = "Isle Temple",
        sort         = 103,
        realm        = "isle",
    },
    prairie = {
        name         = "Daylight Prairie",
        short_name   = "Prairie",
        sort         = 200,
    },
    butterfly_fields = {
        name         = "Butterfly Fields",
        sort         = 201,
        realm        = "prairie",
    },
    prairie_villages = {
        name         = "Prairie Villages",
        short_name   = "Villages",
        sort         = 202,
        realm        = "prairie",
    },
    prairie_caves = {
        name         = "Prairie Caves",
        short_name   = "Caves",
        sort         = 203,
        realm        = "prairie",
    },
    prairie_temple = {
        name         = "Prairie Temple",
        sort         = 204,
        realm        = "prairie",
    },
    bird_nest = {
        name         = "Bird Nest",
        sort         = 205,
        realm        = "prairie",
    },
    sanctuary_islands = {
        name         = "Sanctuary Islands",
        sort         = 206,
        realm        = "prairie",
    },
    eight_player_puzzle = {
        name         = "Eight Player Puzzle",
        sort         = 207,
        realm        = "prairie",
    },
    prairie_peaks = {
        name         = "Prairie Peaks",
        sort         = 208,
        realm        = "prairie",
    },
    forest = {
        name         = "Hidden Forest",
        short_name   = "Forest",
        sort         = 300,
    },
    forest_clearing = {
        name         = "Forest Clearing",
        sort         = 301,
        realm        = "forest",
    },
    forests_brook = {
        name         = "Forest's Brook",
        sort         = 302,
        realm        = "forest",
    },
    forest_boneyard = {
        name         = "Forest Boneyard",
	    short_name   = "Boneyard",
        alt_name     = { "Tree Tunnels", "Broken Bridge" },
        sort         = 303,
        realm        = "forest",
    },
    forest_temple = {
        name         = "Forest Temple",
        sort         = 304,
        realm        = "forest",
    },
    elevated_clearing = {
        name         = "Elevated Clearing",
        sort         = 305,
        realm        = "forest",
    },
    underground_cavern = {
        name         = "Underground Cavern",
        sort         = 306,
        realm        = "forest",
    },
    the_wind_paths = {
        name         = "The Wind Paths",
        sort         = 307,
        realm        = "forest",
    },
    the_treehouse = {
        name         = "The Treehouse",
        alt_name     = { "Treehouse" },
        sort         = 308,
        realm        = "forest",
    },
    blue_bird_theater = {
        name         = "Blue Bird Theater",
        sort         = 309,
        realm        = "forest",
    },
    valley = {
        name         = "Valley of Triumph",
        short_name   = "Valley",
        sort         = 400,
    },
    ice_rink = {
        name         = "Ice Rink",
        sort         = 401,
        realm        = "valley",
    },
    sliding_race = {
        name         = "Sliding Race",
        sort         = 402,
        realm        = "valley",
    },
    coliseum = {
        name         = "Coliseum",
        sort         = 403,
        realm        = "valley",
    },
    citadel = {
        name         = "Citadel",
        sort         = 404,
        realm        = "valley",
    },
    flying_race = {
        name         = "Flying Race",
        sort         = 405,
        realm        = "valley",
    },
    valley_temple = {
        name         = "Valley Temple",
        sort         = 406,
        realm        = "valley",
    },
    village_of_dreams = {
        name         = "Village of Dreams",
        sort         = 407,
        realm        = "valley",
    },
    hermit_valley = {
        name         = "Hermit Valley",
        sort         = 408,
        realm        = "valley",
    },
    village_theater = {
        name         = "Village Theater",
        sort         = 409,
        realm        = "valley",
    },
    harmony_hall = {
        name         = "Harmony Hall",
        alt_name     = { "Music Shop" },
        sort         = 410,
        realm        = "valley",
    },
    wasteland = {
        name         = "Golden Wasteland",
        short_name   = "Wasteland",
        sort         = 500,
    },
    broken_temple = {
        name         = "Broken Temple",
        sort         = 501,
        realm        = "wasteland",
    },
    first_krill_area = {
        name         = "Graveyard Entrance",
        alt_name     = { "First Krill Area" },
        sort         = 502,
        realm        = "wasteland",
    },
    graveyard = {
        name         = "Graveyard",
        sort         = 503,
        realm        = "wasteland",
    },
    battlefield = {
        name         = "Battlefield",
        sort         = 504,
        realm        = "wasteland",
    },
    wasteland_temple = {
        name         = "Wasteland Temple",
        sort         = 505,
        realm        = "wasteland",
    },
    crab_fields = {
        name         = "Crab Fields",
        alt_name     = { "Shipwreck" },
        sort         = 506,
        realm        = "wasteland",
    },
    forgotten_ark = {
        name         = "Forgotten Ark",
        sort         = 507,
        realm        = "wasteland",
    },
    treasure_reef = {
        name         = "Treasure Reef",
        sort         = 508,
        realm        = "wasteland",
    },
    last_city = {
        name         = "The Last City",
        sort         = 509,
        realm        = "wasteland",
    },
    vault = {
        name         = "Vault of Knowledge",
        short_name   = "Vault",
        sort         = 600,
    },
    first_floor_vault = {
        name         = "First Floor Vault",
        alt_name     = { "First Floor" },
        sort         = 601,
        realm        = "vault",
    },
    second_floor_vault = {
        name         = "Second Floor Vault",
        alt_name     = { "Second Floor" },
        sort         = 602,
        realm        = "vault",
    },
    third_floor_vault = {
        name         = "Third Floor Vault",
        alt_name     = { "Third Floor" },
        sort         = 603,
        realm        = "vault",
    },
    fourth_floor_vault = {
        name         = "Fourth Floor Vault",
        alt_name     = { "Fourth Floor" },
        sort         = 604,
        realm        = "vault",
    },
    fifth_floor_vault = {
        name         = "Fifth Floor Vault",
        alt_name     = { "Fifth Floor" },
        sort         = 605,
        realm        = "vault",
    },
    vault_summit = {
        name         = "Vault Summit",
        alt_name     = { "Sixth Floor", "The Summit" },
        sort         = 606,
        realm        = "vault",
    },
    archives = {
        name         = "Archives",
        sort         = 607,
        realm        = "vault",
    },
    starlight_desert = {
        name         = "Starlight Desert",
        sort         = 608,
        realm        = "vault",
    },
    repository_of_refuge = {
    	name         = "Repository of Refuge",
    	sort         = 609,
    	realm        = "vault",
    },
    crescent_oasis = {
    	name         = "Crescent Oasis",
    	sort         = 610,
    	realm        = "vault",
    },
    moominvalley = {
    	name         = "Moominvalley",
    	sort         = 611,
    	realm        = "vault",
    },
    collab_room = {
    	name         = "Collaboration Room",
    	sort         = 612,
    	realm        = "vault",
    },
    secret_area = {
        name         = "Secret Area",
        alt_name     = { "Office", "The Office" },
        sort         = 650,
        realm        = "vault",
    },
    eden = {
        name         = "Eye of Eden",
        short_name   = "Eden",
        sort         = 700,
    },
    -- After finishing a Red Shard Eruption, the teleported location
    -- is refered to as an "Ancient Memory". But I'm also keeping the short
    -- name as "void" as we refer to the memories as voids as well.
    void = {
        name         = "Ancient Memory",
        short_name   = "Void",
        sort         = 800,
    },
    home = {
		name		= "Home",
		short_name	= "Home",
		sort		= 801,
	},
	aviary = {
        name         = "Aviary Village",
        short_name   = "Aviary",
        sort         = 802,    
	},
	nests = {
		name		= "Nests",
		short_name	= "Nest",
		sort		= 803,
	},
	nesting_workshop = {
		name		= "Nesting Workshop",
		sort		= 804,
	},
	concert_hall = {
		name		= "Concert Hall",
		short_name	= "Concert Hall",
		sort		= 805,
	},
 }
local stdData = require('Module:stdData')
-- Process data, including merging in language-specific overrides
return stdData.processData(data, 'Locations')