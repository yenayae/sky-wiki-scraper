-- <nowiki>
-- Names and icons for all Dye colors
local data = {
    red = {
        name       = "Red Dye",
        short_name = "Red",
        d_icon     = "Red-dye-container-icon.png",
        sort       = 1
    },
    yellow = {
        name       = "Yellow Dye",
        short_name = "Yellow",
        d_icon     = "Yellow-dye-container-icon.png",
        sort       = 2
    },
    green = {
        name       = "Green Dye",
        short_name = "Green",
        d_icon     = "Green-dye-container-icon.png",
        sort       = 3
    },
    cyan = {
        name       = "Cyan Dye",
        short_name = "Cyan",
        d_icon     = "Cyan-dye-container-icon.png",
        sort       = 4
    },
    blue = {
        name       = "Blue Dye",
        short_name = "Blue",
        d_icon     = "Blue-dye-container-icon.png",
        sort       = 5
    },
    purple = {
        name       = "Purple Dye",
        short_name = "Purple",
        d_icon	   = "Purple-dye-container-icon.png",
        sort       = 6
    },
    black = {
        name       = "Black Dye",
        short_name = "Black",
        d_icon     = "Black-dye-container-icon.png",
        sort       = 7
    },
    white = {
        name       = "White Dye",
        short_name = "White",
        d_icon     = "White-dye-container-icon.png",
        sort       = 8
    },
    
}
local stdData = require('Module:stdData')
-- Process data, including merging in language-specific overrides
return stdData.processData(data, 'Dyes')