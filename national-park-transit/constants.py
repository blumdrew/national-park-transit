"""constants for transit etc."""

import os

BASE_PATH = os.path.dirname(__file__)
QUERY_PATH = os.path.join(BASE_PATH, "queries")
DATA_PATH = os.path.join(BASE_PATH, "data")

OSM_NAME_ID_MAP = {
    'Olympic National Park': 163769, 
    'Death Valley National Park': 174732, 
    'Kings Canyon National Park': 175059, 
    'Sequoia National Park': 175060, 
    'Grand Canyon National Park': 183377, 
    'Redwood National Park': 215231, 
    'Rocky Mountain National Park': 390960, 
    'Black Canyon of the Gunnison National Park': 395552, 
    'Glacier National Park': 1242641, 
    'Crater Lake National Park': 1274747, 
    'Cuyahoga Valley National Park': 1286297, 
    'Mount Rainier National Park': 1399219, 
    'Yellowstone National Park': 1453306, 
    'Grand Teton National Park': 1492555, 
    'White Sands National Park': 1504622, 
    'Yosemite National Park': 1643367, 
    'Isle Royale National Park': 1870066, 
    'Great Smoky Mountains National Park': 2131838, 
    'Acadia National Park': 2176999, 
    'North Cascades National Park': 2421537, 
    'Big Bend National Park': 2625382, 
    'Virgin Islands National Park': 2910708, 
    'Wind Cave National Park': 2998186, 
    'Hot Springs National Park': 3136144, 
    'New River Gorge National Park and Preserve': 3178915, 
    'Channel Islands National Park': 3636334, 
    'Dry Tortugas National Park': 4437721, 
    'Petrified Forest National Park': 4640162, 
    'Bryce Canyon National Park': 4716641, 
    'Capitol Reef National Park': 4716642, 
    'Shenandoah National Park': 5548542, 
    'Great Sand Dunes National Park': 5725308, 
    'Badlands National Park': 5731065, 
    'Mesa Verde National Park': 5749837, 
    'Zion National Park': 5758583, 
    'Arches National Park': 5868384, 
    'Carlsbad Caverns National Park': 5953459, 
    'Guadalupe Mountains National Park': 5953502, 
    'Great Basin National Park': 5974781, 
    'Glacier Bay National Park': 6077677, 
    'Joshua Tree National Park': 6145614, 
    'Pinnacles National Park': 6183160, 
    'Lassen Volcanic National Park': 6207158, 
    'Indiana Dunes National Park': 6414018, 
    'Wrangell-Saint Elias National Park': 6561033, 
    'Gates of the Arctic National Park': 7025660, 
    'Kobuk Valley National Park': 7058636, 
    'Haleakalā National Park': 8174174, 
    'Katmai National Park and Preserve': 9090352, 
    'Biscayne National Park': 9107419, 
    'Saguaro National Park': 9529323, 
    'Kenai Fjords National Park': 9563873, 
    'Mammoth Cave National Park': 9615817, 
    'Voyageurs National Park': 11116441, 
    'The Gateway Arch National Park': 12627717, 
    'Congaree National Park': 12627729, 
    'Theodore Roosevelt National Park': 13235948, 
    'Canyonlands National Park': 13624591
}
# taken from https://irma.nps.gov/STATS/Reports/National, 2021 data
OSM_ID_VISITOR_MAP = {
    2176999:4069098,
    5868384:1806865,
    5731065:1224226,
    2625382:581220,
    9107419:705655 ,
    395552:308910 ,
    4716641:2104600, 
    13624591:911594 ,
    4716642:1405353 ,
    5953459:349244 ,
    3636334:319252 ,
    12627729:215181 ,
    1274747:647751 ,
    1286297:2575275 ,
    174732:1146551 ,
    4437721:83817, 
    2163707:942130 ,
    1242641:3081656 ,
    183377:4532677 ,
    1492555:3885230 ,
    5974781:144875 ,
    2131838:14161548, 
    5953502:243291 ,
    3136144:2162884 ,
    6414018:3177210 ,
    1870066:25844 ,
    6145614:3064400, 
    9563873:411782 ,
    175059:562918 ,
    7058636:11540 ,
    6207158:359635 ,
    9615817:515774 ,
    5749837:548477 ,
    1399219:1670063 ,
    2421537:17855 ,
    163769:2718925 ,
    4640162:590334 ,
    6183160:348857 ,
    215231:435879 ,
    390960:4434848 ,
    9529323:1079786 ,
    175060:1059548 ,
    5548542:1592312 ,
    13235948:796085 ,
    2910708:323999 ,
    11116441:243042 ,
    1504622:782469 ,
    2998186:709001 ,
    1999909:247862 ,
    1453306:4860242 ,
    1643367:3287595 ,
    5758583:5039835 ,
    12627717:1145081,
}