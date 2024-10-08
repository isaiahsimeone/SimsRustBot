import * as util from "./util.js";

const MarkerNames = {
    "1": "PLAYER",
    "2": "EXPLOSION",
    "3": "SHOP",
    "4": "CHINOOK",
    "5": "CARGOSHIP",
    "6": "CRATE",
    "7": "RADIUS",
    "8": "ATTACKHELI" 
}

const ItemNames = {
    "2133269020": ["Red Berry Clone", "clone.red.berry"],
    "2126889441": ["Santa Beard", "santabeard"],
    "2120241887": ["Gold Mirror Standing", "goldmirror.standing"],
    "2114754781": ["Water Purifier", "water.purifier"],
    "2106561762": ["Decorative Tinsel", "xmas.decoration.tinsel"],
    "2104517339": ["Strobe Light", "strobelight"],
    "2100007442": ["Audio Alarm", "electric.audioalarm"],
    "2090395347": ["Large Solar Panel", "electric.solarpanel.large"],
    "2087678962": ["Search Light", "searchlight"],
    "2070189026": ["Large Banner on pole", "sign.pole.banner.large"],
    "2068884361": ["Small Backpack", "smallbackpack"],
    "2063916636": ["Advanced Ore Tea", "oretea.advanced"],
    "2055695285": ["Frontier Mirror Medium", "frontiermirror.medium"],
    "2054391128": ["Factory Door", "factorydoor"],
    "2052270186": ["Inner Tube", "innertube.unicorn"],
    "2048317869": ["Wolf Skull", "skull.wolf"],
    "2041899972": ["Triangle Ladder Hatch", "floor.triangle.ladder.hatch"],
    "2040726127": ["Combat Knife", "knife.combat"],
    "2024467711": ["Pure Scrap Tea", "scraptea.pure"],
    "2023888403": ["Medium Rechargeable Battery", "electric.battery.rechargable.medium"],
    "2021351233": ["Advanced Rad. Removal Tea", "radiationremovetea.advanced"],
    "2019042823": ["Tarp", "tarp"],
    "2009734114": ["Christmas Door Wreath", "xmasdoorwreath"],
    "2005491391": ["Extended Magazine", "weapon.mod.extendedmags"],
    "1992974553": ["Burlap Trousers", "burlap.trousers"],
    "1989785143": ["High Quality Horse Shoes", "horse.shoes.advanced"],
    "1983621560": ["Floor triangle grill", "floor.triangle.grill"],
    "1975934948": ["Survey Charge", "surveycharge"],
    "1973949960": ["Frontier Bolts Single Item Rack", "gunrack.single.1.horizontal"],
    "1973684065": ["Burnt Chicken", "chicken.burned"],
    "1973165031": ["Birthday Cake", "cakefiveyear"],
    "1965232394": ["Crossbow", "crossbow"],
    "1953903201": ["Nailgun", "pistol.nailgun"],
    "1951603367": ["Switch", "electric.switch"],
    "1950721418": ["Salvaged Shelves", "shelves"],
    "1950013766": ["Light-Up Frame Standing", "lightupframe.standing"],
    "1948067030": ["Ladder Hatch", "floor.ladder.hatch"],
    "1946219319": ["Camp Fire", "campfire"],
    "1931713481": ["Black Raspberries", "black.raspberries"],
    "1917703890": ["Burnt Horse Meat", "horsemeat.burned"],
    "1916016738": ["Light-Up Mirror Standing", "lightupmirror.standing"],
    "1914691295": ["Prototype 17", "pistol.prototype17"],
    "1911552868": ["Black Berry Seed", "seed.black.berry"],
    "1905387657": ["Pure Rad. Removal Tea", "radiationremovetea.pure"],
    "1903654061": ["Small Planter Box", "planter.small"],
    "1899610628": ["Medium Loot Bag", "halloween.lootbag.medium"],
    "1898094925": ["Pumpkin Plant Clone", "clone.pumpkin"],
    "1895235349": ["Disco Ball", "discoball"],
    "1885488976": ["Spooky Speaker", "spookyspeaker"],
    "1883981801": ["Medium Quality Pistons", "piston2"],
    "1883981800": ["High Quality Pistons", "piston3"],
    "1883981798": ["Low Quality Pistons", "piston1"],
    "1882709339": ["Metal Blade", "metalblade"],
    "1878053256": ["Rowboat", "rowboat"],
    "1877339384": ["Burlap Headwrap", "burlap.headwrap"],
    "1874610722": ["Armored Cockpit Vehicle Module", "vehicle.1mod.cockpit.armored"],
    "1873897110": ["Cooked Bear Meat", "bearmeat.cooked"],
    "1865253052": ["Dracula Mask", "draculamask"],
    "1856217390": ["Egg Basket", "easterbasket"],
    "1850456855": ["Road Sign Kilt", "roadsign.kilt"],
    "1849887541": ["Small Generator", "electric.fuelgenerator.small"],
    "1846605708": ["Abyss Torch", "divertorch"],
    "1840822026": ["Beancan Grenade", "grenade.beancan"],
    "1840570710": ["Above Ground Pool", "abovegroundpool"],
    "1835946060": ["Cable Tunnel", "electric.cabletunnel"],
    "1827479659": ["Burnt Wolf Meat", "wolfmeat.burned"],
    "1819863051": ["Sky Lantern", "skylantern"],
    "1814288539": ["Bone Knife", "knife.bone"],
    "1803831286": ["Garry's Mod Tool Gun", "toolgun"],
    "1796682209": ["Custom SMG", "smg.2"],
    "1789825282": ["Candy Cane Club", "candycaneclub"],
    "1787198294": ["Frontier Mirror Standing", "frontiermirror.standing"],
    "1784406797": ["Sousaphone", "fun.tuba"],
    "1784005657": ["Parachute Deployed", "parachute.deployed"],
    "1783512007": ["Cactus Flesh", "cactusflesh"],
    "1776460938": ["Blood", "blood"],
    "1771755747": ["Black Berry", "black.berry"],
    "1770744540": ["Generic vehicle chassis", "vehicle.chassis"],
    "1770475779": ["Worm", "worm"],
    "1769475390": ["Wood Frame Standing", "woodframe.standing"],
    "1768112091": ["Tomaha Snowmobile", "snowmobiletomaha"],
    "1762167092": ["Green ID Tag", "greenidtag"],
    "1758333838": ["Teal", "rockingchair.rockingchair2"],
    "1757265204": ["Silver Egg", "easter.silveregg"],
    "1751045826": ["Hoodie", "hoodie"],
    "1746956556": ["Bone Armor", "bone.armor.suit"],
    "1744298439": ["Blue Boomer", "firework.boomer.blue"],
    "1735402444": ["Disco Floor", "discofloor.largetiles"],
    "1729712564": ["Portrait Photo Frame", "photoframe.portrait"],
    "1729374708": ["Pure Ore Tea", "oretea.pure"],
    "1729120840": ["Wooden Door", "door.hinged.wood"],
    "1723747470": ["Tree Lights", "xmas.decoration.lights"],
    "1722154847": ["Hide Pants", "attire.hide.pants"],
    "1719978075": ["Bone Fragments", "bone.fragments"],
    "1714496074": ["Candle Hat", "hat.candle"],
    "1712261904": ["Pure Max Health Tea", "maxhealthtea.pure"],
    "1712070256": ["HV 5.56 Rifle Ammo", "ammo.rifle.hv"],
    "1711033574": ["Bone Club", "bone.club"],
    "1697996440": ["Landscape Photo Frame", "photoframe.landscape"],
    "1696050067": ["Modular Car Lift", "modularcarlift"],
    "1691223771": ["Light-Up Frame Small", "lightupframe.small"],
    "1686524871": ["Decorative Gingerbread Men", "xmas.decoration.gingerbreadmen"],
    "1675639563": ["Beenie Hat", "hat.beenie"],
    "1668858301": ["Small Stocking", "stocking.small"],
    "1668129151": ["Cooked Fish", "fish.cooked"],
    "1660145984": ["Yellow Berry", "yellow.berry"],
    "1659447559": ["Wooden Horse Armor", "horse.armor.wood"],
    "1659114910": ["Gas Mask", "hat.gas.mask"],
    "1658229558": ["Lantern", "lantern"],
    "1655979682": ["Empty Can Of Beans", "can.beans.empty"],
    "1655650836": ["Metal Barricade", "barricade.metal"],
    "1643667218": ["Large Animated Neon Sign", "sign.neon.xl.animated"],
    "1638322904": ["Incendiary Rocket", "ammo.rocket.fire"],
    "1629293099": ["Snowman", "snowman"],
    "1623701499": ["Industrial Wall Light", "industrial.wall.light"],
    "1614528785": ["Heavy Frankenstein Torso", "frankensteins.monster.03.torso"],
    "1608640313": ["Tank Top", "shirt.tanktop"],
    "1603174987": ["Confetti Cannon", "confetticannon"],
    "1602646136": ["Stone Spear", "spear.stone"],
    "1601468620": ["Blue Jumpsuit", "jumpsuit.suit.blue"],
    "1588492232": ["Drone", "drone"],
    "1588298435": ["Bolt Action Rifle", "rifle.bolt"],
    "1581210395": ["Large Planter Box", "planter.large"],
    "1575635062": ["Frankenstein Table", "frankensteintable"],
    "1572152877": ["Mint ID Tag", "mintidtag"],
    "1569882109": ["Handmade Fishing Rod", "fishingrod.handmade"],
    "1568388703": ["Diesel Fuel", "diesel_barrel"],
    "1561022037": ["Abyss Metal Pickaxe", "diverpickaxe"],
    "1559915778": ["Single Horse Saddle", "horse.saddle.single"],
    "1559779253": ["Engine Vehicle Module", "vehicle.1mod.engine"],
    "1557173737": ["Sunglasses", "sunglasses02red"],
    "1556365900": ["Molotov Cocktail", "grenade.molotov"],
    "1553078977": ["Bleach", "bleach"],
    "1548091822": ["Apple", "apple"],
    "1545779598": ["Assault Rifle", "rifle.ak"],
    "1542290441": ["Single Sign Post", "sign.post.single"],
    "1540934679": ["Wooden Spear", "spear.wooden"],
    "1538126328": ["Industrial Combiner", "industrial.combiner"],
    "1536610005": ["Cooked Human Meat", "humanmeat.cooked"],
    "1534542921": ["Chair", "chair"],
    "1533551194": ["White Berry Clone", "clone.white.berry"],
    "1525520776": ["Building Plan", "building.planner"],
    "1524980732": ["Carvable Pumpkin", "carvable.pumpkin"],
    "1524187186": ["Workbench Level 1", "workbench1"],
    "1523403414": ["Cassette - Short", "cassette.short"],
    "1523195708": ["Targeting Computer", "targeting.computer"],
    "1521286012": ["Double Sign Post", "sign.post.double"],
    "1516985844": ["Netting", "wall.frame.netting"],
    "1512054436": ["Potato Clone", "clone.potato"],
    "1491753484": ["Medium Frankenstein Torso", "frankensteins.monster.02.torso"],
    "1491189398": ["Paddle", "paddle"],
    "1488979457": ["Jackhammer", "jackhammer"],
    "1480022580": ["Basic Ore Tea", "oretea"],
    "1478091698": ["Muzzle Brake", "weapon.mod.muzzlebrake"],
    "1463862472": ["Wanted Poster 4", "wantedposter.wantedposter4"],
    "1451568081": ["Chainlink Fence Gate", "wall.frame.fence.gate"],
    "1443579727": ["Hunting Bow", "bow.hunting"],
    "1430085198": ["Industrial Crafter", "industrial.crafter"],
    "1426574435": ["MC repair", "minihelicopter.repair"],
    "1424075905": ["Water Bucket", "bucket.water"],
    "1422530437": ["Raw Deer Meat", "deermeat.raw"],
    "1414245522": ["Rope", "rope"],
    "1414245162": ["Note", "note"],
    "1413014235": ["Fridge", "fridge"],
    "1409529282": ["Door Closer", "door.closer"],
    "1401987718": ["Duct Tape", "ducttape"],
    "1400460850": ["Saddle bag", "horse.saddlebag"],
    "1397052267": ["Supply Signal", "supply.signal"],
    "1394042569": ["RHIB", "rhib"],
    "1391703481": ["Burnt Pork", "meat.pork.burned"],
    "1390353317": ["Sheet Metal Double Door", "door.double.hinged.metal"],
    "1382263453": ["Barbed Wooden Barricade", "barricade.woodwire"],
    "1381010055": ["Leather", "leather"],
    "1376065505": ["Rear Seats Vehicle Module", "vehicle.1mod.rear.seats"],
    "1373971859": ["Python Revolver", "pistol.python"],
    "1373240771": ["Wooden Barricade Cover", "barricade.wood.cover"],
    "1371909803": ["Tesla Coil", "electric.teslacoil"],
    "1367190888": ["Corn", "corn"],
    "1366282552": ["Leather Gloves", "burlap.gloves"],
    "1365234594": ["Gold Mirror large", "goldmirror.large"],
    "1364514421": ["Blue ID Tag", "blueidtag"],
    "1361520181": ["Minecart Planter", "minecart.planter"],
    "1358643074": ["Snow Machine", "snowmachine"],
    "1353298668": ["Armored Door", "door.hinged.toptier"],
    "1346158228": ["Pumpkin Bucket", "pumpkinbasket"],
    "1330084809": ["Low Quality Valves", "valve1"],
    "1327005675": ["Short Ice Wall", "wall.ice.wall"],
    "1326180354": ["Salvaged Sword", "salvaged.sword"],
    "1324203999": ["Champagne Boomer", "firework.boomer.champagne"],
    "1319617282": ["Small Loot Bag", "halloween.lootbag.small"],
    "1318558775": ["MP5A4", "smg.mp5"],
    "1315082560": ["Ox Mask", "hat.oxmask"],
    "1312843609": ["Skull", "skull"],
    "1312679249": ["Wood Mirror Large", "woodmirror.large"],
    "1307626005": ["Storage Barrel Vertical", "storage_barrel_b"],
    "1305578813": ["Small Neon Sign", "sign.neon.125x125"],
    "1296788329": ["Homing Missile", "ammo.rocket.seeker"],
    "1293102274": ["XOR Switch", "electric.xorswitch"],
    "1277159544": ["Weapon Rack Double Light", "weaponrack.doublelight"],
    "1272768630": ["Spoiled Human Meat", "humanmeat.spoiled"],
    "1272430949": ["Wheelbarrow Piano", "piano"],
    "1272194103": ["Red Berry", "red.berry"],
    "1268178466": ["Green Industrial Wall Light", "industrial.wall.light.green"],
    "1266491000": ["Hazmat Suit", "hazmatsuit"],
    "1263920163": ["Smoke Grenade", "grenade.smoke"],
    "1259919256": ["Mixing Table", "mixingtable"],
    "1258768145": ["Sunglasses", "sunglasses02black"],
    "1248356124": ["Timed Explosive Charge", "explosive.timed"],
    "1242522330": ["Cursed Cauldron", "cursedcauldron"],
    "1242482355": ["Jack O Lantern Angry", "jackolantern.angry"],
    "1234880403": ["Sewing Kit", "sewingkit"],
    "1234878710": ["Telephone", "telephone"],
    "1230691307": ["Captain's Log", "captainslog"],
    "1230323789": ["SMG Body", "smgbody"],
    "1223900335": ["Dog Tag", "dogtagneutral"],
    "1223729384": ["Lavender ID Tag", "lavenderidtag"],
    "1221063409": ["Armored Double Door", "door.double.hinged.toptier"],
    "1205607945": ["Two Sided Hanging Sign", "sign.hanging"],
    "1205084994": ["Large Photo Frame", "photoframe.large"],
    "1199391518": ["Road Signs", "roadsigns"],
    "1189981699": ["Crate Costume", "cratecostume"],
    "1186655046": ["Fuel Tank Vehicle Module", "vehicle.2mod.fuel.tank"],
    "1181207482": ["Heavy Plate Helmet", "heavy.plate.helmet"],
    "1177596584": ["Elevator", "elevator"],
    "1176355476": ["Concrete Hatchet", "concretehatchet"],
    "1171735914": ["AND Switch", "electric.andswitch"],
    "1168856825": ["Metal Detector", "metal.detector"],
    "1160881421": ["Hitch &amp; Trough", "hitchtroughcombo"],
    "1159991980": ["Code Lock", "lock.code"],
    "1158340334": ["Low Quality Crankshaft", "crankshaft1"],
    "1158340332": ["High Quality Crankshaft", "crankshaft3"],
    "1158340331": ["Medium Quality Crankshaft", "crankshaft2"],
    "1153652756": ["Large Wooden Sign", "sign.wooden.large"],
    "1149964039": ["Storage Monitor", "storage.monitor"],
    "1142993169": ["Ceiling Light", "ceilinglight"],
    "1132603396": ["Weapon Rack Stand", "gunrack_stand"],
    "1121925526": ["Candy Cane", "candycane"],
    "1113514903": ["Attack Helicopter", "attackhelicopter"],
    "1112162468": ["Blue Berry", "blue.berry"],
    "1110385766": ["Metal Chest Plate", "metal.plate.torso"],
    "1107575710": ["Arctic Scientist Suit", "hazmatsuit_scientist_arctic"],
    "1104520648": ["Chainsaw", "chainsaw"],
    "1103488722": ["Snowball Gun", "snowballgun"],
    "1099314009": ["Barbeque", "bbq"],
    "1094293920": ["Wrapping Paper", "wrappingpaper"],
    "1090916276": ["Pitchfork", "pitchfork"],
    "1081921512": ["Card Table", "cardtable"],
    "1081315464": ["Nest Hat", "attire.nesthat"],
    "1079279582": ["Medical Syringe", "syringe.medical"],
    "1072924620": ["High Quality Spark Plugs", "sparkplug3"],
    "1058261682": ["Christmas Lights", "xmas.lightstring"],
    "1055319033": ["40mm Shotgun Round", "ammo.grenadelauncher.buckshot"],
    "1052926200": ["Mining Quarry", "mining.quarry"],
    "1046904719": ["Abyss Metal Hatchet", "diverhatchet"],
    "1036321299": ["Blue Dog Tags", "bluedogtags"],
    "1028889957": ["Light-Up Mirror Medium", "lightupmirror.medium"],
    "1015352446": ["Duo Submarine", "submarineduo"],
    "999690781": ["Geiger Counter", "geiger.counter"],
    "998894949": ["Corn Seed", "seed.corn"],
    "996757362": ["Wagon", "wagon"],
    "996293980": ["Human Skull", "skull.human"],
    "989925924": ["Raw Fish", "fish.raw"],
    "988652725": ["Smart Switch", "smart.switch"],
    "980333378": ["Hide Poncho", "attire.hide.poncho"],
    "975983052": ["Twitch Rivals Trophy", "trophy"],
    "971362526": ["Skull Trophy", "skull.trophy.jar"],
    "968421290": ["Connected Speaker", "connected.speaker"],
    "968019378": ["Clatter Helmet", "clatter.helmet"],
    "963906841": ["Rock", "rock"],
    "960673498": ["Large Hunting Trophy", "huntingtrophylarge"],
    "952603248": ["Weapon flashlight", "weapon.mod.flashlight"],
    "946662961": ["Car Key", "car.key"],
    "936496778": ["Floor grill", "floor.grill"],
    "935692442": ["Longsleeve T-Shirt", "tshirt.long"],
    "935606207": ["Minigun", "minigun"],
    "926800282": ["Medium Quality Valves", "valve2"],
    "915408809": ["40mm Smoke Grenade", "ammo.grenadelauncher.smoke"],
    "895374329": ["Passenger Vehicle Module", "vehicle.2mod.passengers"],
    "888415708": ["RF Receiver", "electric.rf.receiver"],
    "884424049": ["Compound Bow", "bow.compound"],
    "882559853": ["Spider Webs", "spiderweb"],
    "878301596": ["Generic vehicle module", "vehicle.module"],
    "866889860": ["Wooden Barricade", "barricade.wood"],
    "866332017": ["Large Neon Sign", "sign.neon.xl"],
    "861513346": ["Lumberjack Suit", "hazmatsuit.lumberjack"],
    "858486327": ["Green Berry", "green.berry"],
    "854447607": ["White Berry", "white.berry"],
    "853471967": ["Laser Light", "laserlight"],
    "850280505": ["Bucket Helmet", "bucket.helmet"],
    "844440409": ["Bronze Egg", "easter.bronzeegg"],
    "839738457": ["Scrap Mirror Medium", "scrapmirror.medium"],
    "838831151": ["Blue Berry Clone", "clone.blue.berry"],
    "838308300": ["Burst Module", "weapon.mod.burstmodule"],
    "835042040": ["Medium Frankenstein Legs", "frankensteins.monster.02.legs"],
    "833533164": ["Large Wood Box", "box.wooden.large"],
    "832133926": ["Wood Armor Pants", "wood.armor.pants"],
    "831955134": ["Sky Lantern - Purple", "skylantern.skylantern.purple"],
    "830839496": ["Red Berry Seed", "seed.red.berry"],
    "826309791": ["Two Sided Town Sign Post", "sign.post.town.roof"],
    "818877484": ["Semi-Automatic Pistol", "pistol.semiauto"],
    "818733919": ["Industrial Door", "door.hinged.industrial.a"],
    "813023040": ["Cooked Wolf Meat", "wolfmeat.cooked"],
    "809942731": ["Scarecrow Wrap", "scarecrowhead"],
    "809199956": ["Gravestone", "gravestone"],
    "803954639": ["Blue Berry Seed", "seed.blue.berry"],
    "803222026": ["Repair Bench", "box.repair.bench"],
    "795371088": ["Pump Shotgun", "shotgun.pump"],
    "795236088": ["Torch", "torch"],
    "794443127": ["Christmas Tree", "xmas.tree"],
    "794356786": ["Hide Boots", "attire.hide.boots"],
    "785728077": ["Pistol Bullet", "ammo.pistol"],
    "782422285": ["Sofa - Pattern", "sofa.pattern"],
    "762289806": ["Siren Light", "electric.sirenlight"],
    "756517185": ["Medium Present", "xmas.present.medium"],
    "756125481": ["Wood Mirror Medium", "woodmirror.medium"],
    "755224797": ["Vodka Bottle", "bottle.vodka"],
    "742745918": ["Industrial Splitter", "industrial.splitter"],
    "723407026": ["Wood Mirror Standing", "woodmirror.standing"],
    "722955039": ["Water Gun", "gun.water"],
    "709206314": ["Tiger Mask", "hat.tigermask"],
    "703057617": ["Military Flame Thrower", ""],
    "699075597": ["Wooden Cross", "woodcross"],
    "696029452": ["Paper Map", "map"],
    "695450239": ["Chinese new year spear", "spear.cny"],
    "680234026": ["Yellow Perch", "fish.yellowperch"],
    "678698219": ["M4 Shotgun", "shotgun.m4"],
    "674734128": ["Festive Doorway Garland", "xmas.door.garland"],
    "671706427": ["Reinforced Glass Window", "wall.window.bars.toptier"],
    "671063303": ["Riot Helmet", "riot.helmet"],
    "665332906": ["Timer", "electric.timer"],
    "657352755": ["Beach Table", "beachtable"],
    "656371028": ["Low Quality Carburetor", "carburetor1"],
    "656371027": ["Medium Quality Carburetor", "carburetor2"],
    "656371026": ["High Quality Carburetor", "carburetor3"],
    "649912614": ["Revolver", "pistol.revolver"],
    "642482233": ["Sticks", "sticks"],
    "634478325": ["CCTV Camera", "cctv.camera"],
    "621915341": ["Raw Pork", "meat.boar"],
    "615112838": ["Rail Road Planter", "rail.road.planter"],
    "613961768": ["Bota Bag", "botabag"],
    "610102428": ["Industrial Conveyor", "industrial.conveyor"],
    "609049394": ["Battery - Small", "battery.small"],
    "607400343": ["Legacy Wood Shelter", "legacy.shelter.wood"],
    "605467368": ["Incendiary 5.56 Rifle Ammo", "ammo.rifle.incendiary"],
    "603811464": ["Advanced Max Health Tea", "maxhealthtea.advanced"],
    "602741290": ["Burlap Shirt", "burlap.shirt"],
    "602628465": ["Parachute", "parachute"],
    "596469572": ["RF Transmitter", "rf.detonator"],
    "593465182": ["Table", "table"],
    "588596902": ["Handmade Shell", "ammo.handmade.shell"],
    "576509618": ["Portable Boom Box", "fun.boomboxportable"],
    "573926264": ["Semi Automatic Body", "semibody"],
    "573676040": ["Coffin", "coffin.storage"],
    "567871954": ["Secret Lab Chair", "secretlabchair"],
    "567235583": ["8x Zoom Scope", "weapon.mod.small.scope"],
    "559147458": ["Survival Fish Trap", "fishtrap.small"],
    "553887414": ["Skull Fire Pit", "skull_fire_pit"],
    "553270375": ["Large Rechargeable Battery", "electric.battery.rechargable.large"],
    "550753330": ["Snowball", "ammo.snowballgun"],
    "528668503": ["Flame Turret", "flameturret"],
    "524678627": ["Advanced Scrap Tea", "scraptea.advanced"],
    "492357192": ["RAND Switch", "electric.random.switch"],
    "491263800": ["Nomad Suit", "hazmatsuit.nomadsuit"],
    "486661382": ["Clan Table", "clantable"],
    "479292118": ["Large Loot Bag", "halloween.lootbag.large"],
    "479143914": ["Gears", "gears"],
    "476066818": ["Cassette - Long", "cassette"],
    "468313189": ["Twitch Rivals Hazmat Suit", "hazmatsuittwitch"],
    "450531685": ["Light-Up Mirror Large", "lightupmirror.large"],
    "446206234": ["Torch Holder", "torchholder"],
    "443432036": ["Fluid Switch &amp; Pump", "fluid.switch"],
    "442886268": ["Rocket Launcher", "rocket.launcher"],
    "442289265": ["Holosight", "weapon.mod.holosight"],
    "418081930": ["Wood Chestplate", "wood.armor.jacket"],
    "390728933": ["Yellow Berry Clone", "clone.yellow.berry"],
    "363163265": ["Hose Tool", "hosetool"],
    "359723196": ["Chippy Arcade Game", "arcade.machine.chippy"],
    "355877490": ["Minigun Ammo Pack", "minigunammopack"],
    "352499047": ["Shotgun Trap", "guntrap"],
    "352321488": ["Sunglasses", "sunglasses"],
    "352130972": ["Rotten Apple", "apple.spoiled"],
    "349762871": ["40mm HE Grenade", "ammo.grenadelauncher.he"],
    "343045591": ["MLRS Aiming Module", "aiming.module.mlrs"],
    "342438846": ["Anchovy", "fish.anchovy"],
    "340210699": ["Frontier Mirror Small", "frontiermirror.small"],
    "317398316": ["High Quality Metal", "metal.refined"],
    "304481038": ["Flare", "flare"],
    "301063058": ["Wanted Poster 2", "wantedposter.wantedposter2"],
    "296519935": ["Diving Fins", "diving.fins"],
    "286648290": ["Disco Floor", "discofloor"],
    "286193827": ["Pickles", "jar.pickle"],
    "282103175": ["Giant Lollipop Decor", "giantlollipops"],
    "277730763": ["Mummy Suit", "halloween.mummysuit"],
    "273951840": ["Scarecrow Suit", "scarecrow.suit"],
    "273172220": ["Plumber's Trumpet", "fun.trumpet"],
    "271048478": ["Rat Mask", "hat.ratmask"],
    "268565518": ["Storage Vehicle Module", "vehicle.1mod.storage"],
    "263834859": ["Basic Scrap Tea", "scraptea"],
    "261913429": ["White Volcano Firework", "firework.volcano"],
    "254522515": ["Large Medkit", "largemedkit"],
    "242933621": ["Frontier Mirror Large", "frontiermirror.large"],
    "242421166": ["Light-Up Frame Large", "lightup.large"],
    "240752557": ["Tall Weapon Rack", "gunrack_tall.horizontal"],
    "237239288": ["Pants", "pants"],
    "236677901": ["Prototype Pickaxe", "lumberjack.pickaxe"],
    "223891266": ["T-Shirt", "tshirt"],
    "215754713": ["Bone Arrow", "arrow.bone"],
    "209218760": ["Head Bag", "head.bag"],
    "204970153": ["Wrapped Gift", "wrappedgift"],
    "204391461": ["Coal 🙁", "coal"],
    "200773292": ["Hammer", "hammer"],
    "198438816": ["Vending Machine", "vending.machine"],
    "196700171": ["Hide Vest", "attire.hide.vest"],
    "192249897": ["Green", "rockingchair.rockingchair3"],
    "190184021": ["Kayak", "kayak"],
    "185586769": ["Inner Tube", "innertube.horse"],
    "180752235": ["Pink ID Tag", "pinkidtag"],
    "177226991": ["Scarecrow", "scarecrow"],
    "176787552": ["Rifle Body", "riflebody"],
    "174866732": ["16x Zoom Scope", "weapon.mod.8x.scope"],
    "171931394": ["Stone Pickaxe", "stone.pickaxe"],
    "170758448": ["Cockpit With Engine Vehicle Module", "vehicle.1mod.cockpit.with.engine"],
    "143803535": ["F1 Grenade", "grenade.f1"],
    "140006625": ["PTZ CCTV Camera", "ptz.cctv.camera"],
    "122783240": ["Black Berry Clone", "clone.black.berry"],
    "121049755": ["Tall Picture Frame", "sign.pictureframe.tall"],
    "110116923": ["Ice Metal Facemask", "metal.facemask.icemask"],
    "106959911": ["Light Frankenstein Legs", "frankensteins.monster.01.legs"],
    "99588025": ["High External Wooden Wall", "wall.external.high"],
    "98508942": ["XXL Picture Frame", "sign.pictureframe.xxl"],
    "95950017": ["Metal Pipe", "metalpipe"],
    "86840834": ["NVGM Scientist Suit", "hazmatsuit_scientist_nvgm"],
    "81423963": ["Yellow ID Tag", "yellowidtag"],
    "73681876": ["Tech Trash", "techparts"],
    "70102328": ["Red ID Tag", "redidtag"],
    "69511070": ["Metal Fragments", "metal.fragments"],
    "62577426": ["Photograph", "photo"],
    "60528587": ["Roadsign Horse Armor", "horse.armor.roadsign"],
    "51984655": ["Incendiary Pistol Bullet", "ammo.pistol.fire"],
    "42535890": ["Medium Animated Neon Sign", "sign.neon.125x215.animated"],
    "39600618": ["Microphone Stand", "microphonestand"],
    "37122747": ["Green Keycard", "keycard_green"],
    "28201841": ["M39 Rifle", "rifle.m39"],
    "23391694": ["Bunny Hat", "hat.bunnyhat"],
    "23352662": ["Large Banner Hanging", "sign.hanging.banner.large"],
    "22947882": ["White ID Tag", "whiteidtag"],
    "21402876": ["Burlap Gloves", "burlap.gloves.new"],
    "20489901": ["Purple Sunglasses", "twitchsunglasses"],
    "15388698": ["Stone Barricade", "barricade.stone"],
    "14241751": ["Fire Arrow", "arrow.fire"],
    "3380160": ["Card Movember Moustache", "movembermoustachecard"],
    "3222790": ["Hide Halterneck", "attire.hide.helterneck"],
    "-4031221": ["Metal Ore", "metal.ore"],
    "-7270019": ["Orange Boomer", "firework.boomer.orange"],
    "-8312704": ["Beach Towel", "beachtowel"],
    "-17123659": ["Smoke Rocket WIP!!!!", "ammo.rocket.smoke"],
    "-20045316": ["Mobile Phone", "mobilephone"],
    "-22883916": ["Dragon Mask", "hat.dragonmask"],
    "-23994173": ["Boonie Hat", "hat.boonie"],
    "-25740268": ["Skull Spikes", "skullspikes.candles"],
    "-33009419": ["Pure Anti-Rad Tea", "radiationresisttea.pure"],
    "-41440462": ["Spas-12 Shotgun", "shotgun.spas12"],
    "-41896755": ["Workbench Level 2", "workbench2"],
    "-44066600": ["Small Chassis", "vehicle.chassis.2mod"],
    "-44066790": ["Large Chassis", "vehicle.chassis.4mod"],
    "-44066823": ["Medium Chassis", "vehicle.chassis.3mod"],
    "-44876289": ["Igniter", "electric.igniter"],
    "-48090175": ["Snow Jacket", "jacket.snow"],
    "-52398594": ["Frontier Horns Single Item Rack", "gunrack.single.3.horizontal"],
    "-73195037": ["Legacy bow", "legacy bow"],
    "-75944661": ["Eoka Pistol", "pistol.eoka"],
    "-78533081": ["Burnt Deer Meat", "deermeat.burned"],
    "-81700958": ["Brick Skin Window Bars", "wall.window.bars.brickskin"],
    "-82758111": ["Scrap Mirror Large", "scrapmirror.large"],
    "-89874794": ["Low Quality Spark Plugs", "sparkplug1"],
    "-92759291": ["Wooden Floor Spikes", "spikes.floor"],
    "-96256997": ["Wide Weapon Rack", "gunrack_wide.horizontal"],
    "-97459906": ["Jumpsuit", "jumpsuit.suit"],
    "-97956382": ["Tool Cupboard", "cupboard.tool"],
    "-99886070": ["Violet Roman Candle", "firework.romancandle.violet"],
    "-110921842": ["Locker", "locker"],
    "-113413047": ["Diving Mask", "diving.mask"],
    "-119235651": ["Water Jug", "waterjug"],
    "-126305173": ["Painted Egg", "easter.paintedeggs"],
    "-129230242": ["Decorative Pinecones", "xmas.decoration.pinecone"],
    "-132247350": ["Small Water Catcher", "water.catcher.small"],
    "-132516482": ["Weapon Lasersight", "weapon.mod.lasersight"],
    "-134959124": ["Light Frankenstein Head", "frankensteins.monster.01.head"],
    "-135252633": ["Sled", "sled.xmas"],
    "-139037392": ["Abyss Assault Rifle", "rifle.ak.diver"],
    "-143132326": ["Huge Wooden Sign", "sign.wooden.huge"],
    "-144417939": ["Wire Tool", "wiretool"],
    "-144513264": ["Pipe Tool", "pipetool"],
    "-148229307": ["Metal Shop Front", "wall.frame.shopfront.metal"],
    "-148794216": ["Garage Door", "wall.frame.garagedoor"],
    "-151387974": ["Deluxe Christmas Lights", "xmas.lightstring.advanced"],
    "-151838493": ["Wood", "wood"],
    "-156748077": ["Skull Trophy", "skull.trophy.table"],
    "-173268125": ["Rustigé Egg - Green", "rustige_egg_e"],
    "-173268126": ["Rustigé Egg - Ivory", "rustige_egg_d"],
    "-173268128": ["Rustigé Egg - White", "rustige_egg_f"],
    "-173268129": ["Rustigé Egg - Red", "rustige_egg_a"],
    "-173268131": ["Rustigé Egg - Purple", "rustige_egg_c"],
    "-173268132": ["Rustigé Egg - Blue", "rustige_egg_b"],
    "-176608084": ["Sunglasses", "sunglasses03black"],
    "-180129657": ["Wood Storage Box", "box.wooden"],
    "-187031121": ["Solo Submarine", "submarinesolo"],
    "-194509282": ["Butcher Knife", "knife.butcher"],
    "-194953424": ["Metal Facemask", "metal.facemask"],
    "-196667575": ["Flashlight", "flashlight.held"],
    "-209869746": ["Decorative Plastic Candy Canes", "xmas.decoration.candycanes"],
    "-211235948": ["Xylobone", "xylophone"],
    "-216116642": ["Skull Door Knocker", "skulldoorknocker"],
    "-216999575": ["Counter", "electric.counter"],
    "-218009552": ["Homing Missile Launcher", "homingmissile.launcher"],
    "-237809779": ["Hemp Seed", "seed.hemp"],
    "-239306133": ["Surface torpedo", "submarine.torpedo.rising"],
    "-242084766": ["Cooked Pork", "meat.pork.cooked"],
    "-243540612": ["Twitch Rivals Desk", "twitchrivals2023desk"],
    "-246672609": ["Horizontal Weapon Rack", "gunrack.horizontal"],
    "-253079493": ["Scientist Suit", "hazmatsuit_scientist"],
    "-258457936": ["Unused Storage Barrel Vertical", "storage_barrel_a"],
    "-258574361": ["Dracula Cape", "draculacape"],
    "-262590403": ["Salvaged Axe", "axe.salvaged"],
    "-265292885": ["Fluid Combiner", "fluid.combiner"],
    "-265876753": ["Gun Powder", "gunpowder"],
    "-277057363": ["Salt Water", "water.salt"],
    "-280223496": ["Violet Boomer", "firework.boomer.violet"],
    "-282113991": ["Simple Light", "electric.simplelight"],
    "-282193997": ["Orange ID Tag", "orangeidtag"],
    "-295829489": ["Test Generator", "electric.generator.small"],
    "-297099594": ["Heavy Frankenstein Head", "frankensteins.monster.03.head"],
    "-316250604": ["Wooden Ladder", "ladder.wooden.wall"],
    "-321431890": ["Beach Chair", "beachchair"],
    "-321733511": ["Crude Oil", "crude.oil"],
    "-324675402": ["Reindeer Antlers", "attire.reindeer.headband"],
    "-333406828": ["Sled", "sled"],
    "-335089230": ["High External Wooden Gate", "gates.external.high.wood"],
    "-343857907": ["Sound Light", "soundlight"],
    "-363689972": ["Snowball", "snowball"],
    "-365097295": ["Powered Water Purifier", "powered.water.purifier"],
    "-369760990": ["Small Stash", "stash.small"],
    "-379734527": ["Pattern Boomer", "firework.boomer.pattern"],
    "-384243979": ["SAM Ammo", "ammo.rocket.sam"],
    "-389796733": ["Light-Up Mirror Small", "lightupmirror.small"],
    "-394470247": ["Egg Suit Sign Test", "sign.egg.suit"],
    "-395377963": ["Raw Wolf Meat", "wolfmeat.raw"],
    "-399173933": ["Prototype Hatchet", "lumberjack.hatchet"],
    "-454370658": ["Red Volcano Firework", "firework.volcano.red"],
    "-455286320": ["Gray ID Tag", "grayidtag"],
    "-458565393": ["Root Combiner", "electrical.combiner"],
    "-463122489": ["Watch Tower", "watchtower.wood"],
    "-465682601": ["SUPER Stocking", "stocking.large"],
    "-470439097": ["Arctic Suit", "hazmatsuit.arcticsuit"],
    "-484206264": ["Blue Keycard", "keycard_blue"],
    "-487356515": ["Anti-Rad Tea", "radiationresisttea"],
    "-489848205": ["Large Candle Set", "largecandles"],
    "-493159321": ["Medium Quality Spark Plugs", "sparkplug2"],
    "-496584751": ["Rad. Removal Tea", "radiationremovetea"],
    "-498301781": ["Scrap Frame Small", "scrapframe.small"],
    "-502177121": ["Door Controller", "electric.doorcontroller"],
    "-515830359": ["Blue Roman Candle", "firework.romancandle.blue"],
    "-520133715": ["Yellow Berry Seed", "seed.yellow.berry"],
    "-541206665": ["Advanced Wood Tea", "woodtea.advanced"],
    "-542577259": ["Minnows", "fish.minnows"],
    "-544317637": ["Research Paper", "researchpaper"],
    "-555122905": ["Sofa", "sofa"],
    "-557539629": ["Pure Wood Tea", "woodtea.pure"],
    "-558880549": ["Gingerbread Suit", "gingerbreadsuit"],
    "-559599960": ["Sandbag Barricade", "barricade.sandbags"],
    "-560304835": ["Space Suit", "hazmatsuit.spacesuit"],
    "-561148628": ["Tugboat", "tugboat"],
    "-563624462": ["Splitter", "electric.splitter"],
    "-566907190": ["RF Pager", "rf_pager"],
    "-567909622": ["Pumpkin", "pumpkin"],
    "-568419968": ["Grub", "grub"],
    "-575483084": ["Santa Hat", "santahat"],
    "-575744869": ["Party Hat", "partyhat"],
    "-582782051": ["Snap Trap", "trap.bear"],
    "-583379016": ["Megaphone", "megaphone"],
    "-586342290": ["Blueberries", "blueberries"],
    "-586784898": ["Mail Box", "mailbox"],
    "-587989372": ["Catfish", "fish.catfish"],
    "-592016202": ["Explosives", "explosives"],
    "-596876839": ["Spray Can", "spraycan"],
    "-602717596": ["Red Dog Tags", "reddogtags"],
    "-626174997": ["Taxi Vehicle Module", "vehicle.1mod.taxi"],
    "-629028935": ["Electric Fuse", "fuse"],
    "-635951327": ["Wood Frame Large", "woodframe.large"],
    "-649128577": ["Basic Wood Tea", "woodtea"],
    "-656349006": ["Green Boomer", "firework.boomer.green"],
    "-682687162": ["Burnt Human Meat", "humanmeat.burned"],
    "-690276911": ["Glowing Eyes", "gloweyes"],
    "-690968985": ["Blocker", "electric.blocker"],
    "-691113464": ["High External Stone Gate", "gates.external.high.stone"],
    "-692338819": ["Small Rechargeable Battery", "electric.battery.rechargable.small"],
    "-695124222": ["Giant Candy Decor", "giantcandycanedecor"],
    "-695978112": ["Smart Alarm", "smart.alarm"],
    "-697981032": ["Inner Tube", "innertube"],
    "-699558439": ["Roadsign Gloves", "roadsign.gloves"],
    "-700591459": ["Can of Beans", "can.beans"],
    "-702051347": ["Bandana Mask", "mask.bandana"],
    "-722241321": ["Small Present", "xmas.present.small"],
    "-722629980": ["Heavy Scientist Youtooz", "heavyscientistyoutooz"],
    "-727717969": ["12 Gauge Slug", "ammo.shotgun.slug"],
    "-733625651": ["Paddling Pool", "paddlingpool"],
    "-742865266": ["Rocket", "ammo.rocket.basic"],
    "-746030907": ["Granola Bar", "granolabar"],
    "-746647361": ["Memory Cell", "electrical.memorycell"],
    "-747743875": ["Egg Suit", "attire.egg.suit"],
    "-751151717": ["Spoiled Chicken", "chicken.spoiled"],
    "-761829530": ["Burlap Shoes", "burlap.shoes"],
    "-763071910": ["Lumberjack Hoodie", "lumberjack hoodie"],
    "-765183617": ["Double Barrel Shotgun", "shotgun.double"],
    "-769647921": ["Skull Trophy", "skull.trophy"],
    "-770304148": ["Chinese Lantern White", "chineselanternwhite"],
    "-778367295": ["L96 Rifle", "rifle.l96"],
    "-778875547": ["Corn Clone", "clone.corn"],
    "-781014061": ["Sprinkler", "electric.sprinkler"],
    "-784870360": ["Electric Heater", "electric.heater"],
    "-796583652": ["Shop Front", "wall.frame.shopfront"],
    "-797592358": ["Abyss Divers Suit", "hazmatsuit.diver"],
    "-798293154": ["Laser Detector", "electric.laserdetector"],
    "-803263829": ["Coffee Can Helmet", "coffeecan.helmet"],
    "-804769727": ["Plant Fiber", "plantfiber"],
    "-810326667": ["Work Cart", "workcart"],
    "-819720157": ["Metal Window Bars", "wall.window.bars.metal"],
    "-842267147": ["Snowman Helmet", "attire.snowman.helmet"],
    "-845557339": ["Landscape Picture Frame", "sign.pictureframe.landscape"],
    "-849373693": ["Frontier Horseshoe Single Item Rack", "gunrack.single.2.horizontal"],
    "-850982208": ["Key Lock", "lock.key"],
    "-851988960": ["Salmon", "fish.salmon"],
    "-852563019": ["M92 Pistol", "pistol.m92"],
    "-854270928": ["Dragon Door Knocker", "dragondoorknocker"],
    "-855748505": ["Simple Handmade Sight", "weapon.mod.simplesight"],
    "-858312878": ["Cloth", "cloth"],
    "-869598982": ["Small Hunting Trophy", "huntingtrophysmall"],
    "-885833256": ["Vampire Stake", "vampire.stake"],
    "-886280491": ["Hemp Clone", "clone.hemp"],
    "-888153050": ["Halloween Candy", "halloween.candy"],
    "-901370585": ["Twitch Rivals Trophy 2023", "trophy2023"],
    "-904863145": ["Semi-Automatic Rifle", "rifle.semiauto"],
    "-907422733": ["Large Backpack", "largebackpack"],
    "-912398867": ["Cassette - Medium", "cassette.medium"],
    "-924959988": ["Skull Trophy", "skull.trophy.jar2"],
    "-929092070": ["Basic Healing Tea", "healingtea"],
    "-930193596": ["Fertilizer", "fertilizer"],
    "-932201673": ["Scrap", "scrap"],
    "-936921910": ["Flashbang", "grenade.flashbang"],
    "-939424778": ["Flasher Light", "electric.flasherlight"],
    "-946369541": ["Low Grade Fuel", "lowgradefuel"],
    "-956706906": ["Prison Cell Gate", "wall.frame.cell.gate"],
    "-961457160": ["New Year Gong", "newyeargong"],
    "-965336208": ["Chocolate Bar", "chocolate"],
    "-967648160": ["High External Stone Wall", "wall.external.high.stone"],
    "-979302481": ["Easter Door Wreath", "easterdoorwreath"],
    "-979951147": ["Jerry Can Guitar", "fun.jerrycanguitar"],
    "-985781766": ["High Ice Wall", "wall.external.high.ice"],
    "-986782031": ["Rabbit Mask", "hat.rabbitmask"],
    "-989755543": ["Burnt Bear Meat", "bearmeat.burned"],
    "-992286106": ["White Berry Seed", "seed.white.berry"],
    "-996185386": ["XL Picture Frame", "sign.pictureframe.xl"],
    "-996235148": ["Gold Frame large", "goldframe.large"],
    "-996920608": ["Blueprint", "blueprintbase"],
    "-1000573653": ["Frog Boots", "boots.frog"],
    "-1002156085": ["Gold Egg", "easter.goldegg"],
    "-1003665711": ["Super Serum", "supertea"],
    "-1004426654": ["Bunny Ears", "attire.bunnyears"],
    "-1009359066": ["SAM Site", "samsite"],
    "-1018587433": ["Animal Fat", "fat.animal"],
    "-1021495308": ["Metal Spring", "metalspring"],
    "-1022661119": ["Baseball Cap", "hat.cap"],
    "-1023065463": ["High Velocity Arrow", "arrow.hv"],
    "-1023374709": ["Wood Shutters", "shutter.wood.a"],
    "-1036635990": ["12 Gauge Incendiary Shell", "ammo.shotgun.fire"],
    "-1039528932": ["Small Water Bottle", "smallwaterbottle"],
    "-1040518150": ["Camper Vehicle Module", "vehicle.2mod.camper"],
    "-1043618880": ["Ghost Costume", "ghostsheet"],
    "-1044468317": ["RF Broadcaster", "electric.rf.broadcaster"],
    "-1049172752": ["Storage Adaptor", "storageadaptor"],
    "-1049881973": ["Cowbell", "fun.cowbell"],
    "-1050697733": ["Scrap Mirror Small", "scrapmirror.small"],
    "-1060567807": ["Scrap Frame Medium", "scrapframe.medium"],
    "-1073015016": ["Skull Spikes", "skullspikes"],
    "-1078639462": ["Skull Spikes", "skullspikes.pumpkin"],
    "-1094453063": ["Scrap Frame large", "scrapframe.large"],
    "-1100168350": ["Large Water Catcher", "water.catcher.large"],
    "-1100422738": ["Spinning wheel", "spinner.wheel"],
    "-1101924344": ["Wetsuit", "diving.wetsuit"],
    "-1102429027": ["Heavy Plate Jacket", "heavy.plate.jacket"],
    "-1104881824": ["Rug Bear Skin", "rug.bear"],
    "-1108136649": ["Tactical Gloves", "tactical.gloves"],
    "-1112793865": ["Door Key", "door.key"],
    "-1113501606": ["Boom Box", "boombox"],
    "-1117626326": ["Chainlink Fence", "wall.frame.fence"],
    "-1123473824": ["Multiple Grenade Launcher", "multiplegrenadelauncher"],
    "-1130350864": ["Raw Horse Meat", "horsemeat.raw"],
    "-1130709577": ["Pump Jack", "mining.pumpjack"],
    "-1137865085": ["Machete", "machete"],
    "-1138208076": ["Small Wooden Sign", "sign.wooden.small"],
    "-1151332840": ["Wooden Frontier Bar Doors", "door.double.hinged.bardoors"],
    "-1157596551": ["Sulfur Ore", "sulfur.ore"],
    "-1160621614": ["Red Industrial Wall Light", "industrial.wall.light.red"],
    "-1162759543": ["Cooked Horse Meat", "horsemeat.cooked"],
    "-1163532624": ["Jacket", "jacket"],
    "-1163943815": ["Weapon Rack Light", "weaponrack.light"],
    "-1166712463": ["Fluid Splitter", "fluid.splitter"],
    "-1167031859": ["Spoiled Wolf Meat", "wolfmeat.spoiled"],
    "-1175656359": ["Cultist Deer Torch", "torch.torch.skull"],
    "-1183726687": ["Wooden Window Bars", "wall.window.bars.wood"],
    "-1184406448": ["Basic Max Health Tea", "maxhealthtea"],
    "-1196547867": ["Electric Furnace", "electric.furnace"],
    "-1199897169": ["Metal horizontal embrasure", "shutter.metal.embrasure.a"],
    "-1199897172": ["Metal Vertical embrasure", "shutter.metal.embrasure.b"],
    "-1211166256": ["5.56 Rifle Ammo", "ammo.rifle"],
    "-1211268013": ["Basic Horse Shoes", "horse.shoes.basic"],
    "-1214542497": ["HMLMG", "hmlmg"],
    "-1215166612": ["A Barrel Costume", "barrelcostume"],
    "-1215753368": ["Flame Thrower", "flamethrower"],
    "-1230433643": ["Festive Double Doorway Garland", "xmas.double.door.garland"],
    "-1234735557": ["Wooden Arrow", "arrow.wooden"],
    "-1252059217": ["Hatchet", "hatchet"],
    "-1262185308": ["Binoculars", "tool.binoculars"],
    "-1265020883": ["Wanted Poster 3", "wantedposter.wantedposter3"],
    "-1266045928": ["Bunny Onesie", "attire.bunny.onesie"],
    "-1273339005": ["Bed", "bed"],
    "-1274093662": ["Bath Tub Planter", "bathtub.planter"],
    "-1284169891": ["Water Pump", "waterpump"],
    "-1286302544": ["OR Switch", "electric.orswitch"],
    "-1293296287": ["Small Oil Refinery", "small.oil.refinery"],
    "-1294739579": ["Light-Up Frame Medium", "lightupframe.medium"],
    "-1302129395": ["Pickaxe", "pickaxe"],
    "-1305326964": ["Green Berry Clone", "clone.green.berry"],
    "-1306288356": ["Green Roman Candle", "firework.romancandle.green"],
    "-1310391395": ["Legacy Furnace", "legacyfurnace"],
    "-1315992997": ["Dragon Rocket Launcher", "rocket.launcher.dragon"],
    "-1316706473": ["Camera", "tool.camera"],
    "-1321651331": ["Explosive 5.56 Rifle Ammo", "ammo.rifle.explosive"],
    "-1323101799": ["Double Horse Saddle", "horse.saddle.double"],
    "-1330640246": ["Junkyard Drum Kit", "drumkit"],
    "-1331212963": ["Star Tree Topper", "xmas.decoration.star"],
    "-1334569149": ["Hockey Mask", "metal.facemask.hockey"],
    "-1335497659": ["Assault Rifle - ICE", "rifle.ak.ice"],
    "-1336109173": ["Wood Double Door", "door.double.hinged.wood"],
    "-1344017968": ["Wanted Poster", "wantedposter"],
    "-1360171080": ["Concrete Pickaxe", "concretepickaxe"],
    "-1364246987": ["Snowmobile", "snowmobile"],
    "-1366326648": ["Spray Can Decal", "spraycandecal"],
    "-1367281941": ["Waterpipe Shotgun", "shotgun.waterpipe"],
    "-1368584029": ["Sickle", "sickle"],
    "-1370759135": ["Portrait Picture Frame", "sign.pictureframe.portrait"],
    "-1379036069": ["Canbourine", "fun.tambourine"],
    "-1379835144": ["Festive Window Garland", "xmas.window.garland"],
    "-1380144986": ["Scrap Mirror Standing", "scrapmirror.standing"],
    "-1386082991": ["Purple ID Tag", "purpleidtag"],
    "-1405508498": ["Muzzle Boost", "weapon.mod.muzzleboost"],
    "-1408336705": ["Sunglasses", "sunglasses03gold"],
    "-1421257350": ["Storage Barrel Horizontal", "storage_barrel_c"],
    "-1423304443": ["Medium Neon Sign", "sign.neon.125x215"],
    "-1429456799": ["Prison Cell Wall", "wall.frame.cell"],
    "-1432674913": ["Anti-Radiation Pills", "antiradpills"],
    "-1433390281": ["Sky Lantern - Red", "skylantern.skylantern.red"],
    "-1440987069": ["Raw Chicken Breast", "chicken.raw"],
    "-1442496789": ["Pinata", "pinata"],
    "-1442559428": ["Hobo Barrel", "hobobarrel"],
    "-1444650226": ["Gold Mirror Small", "goldmirror.small"],
    "-1448252298": ["Electrical Branch", "electrical.branch"],
    "-1449152644": ["MLRS", "mlrs"],
    "-1469578201": ["Longsword", "longsword"],
    "-1476278729": ["Wood Frame Small", "woodframe.small"],
    "-1478094705": ["Boogie Board", "boogieboard"],
    "-1478212975": ["Wolf Headdress", "hat.wolf"],
    "-1478445584": ["Tuna Can Lamp", "tunalight"],
    "-1478855279": ["Ice Metal Chest Plate", "metal.plate.torso.icevest"],
    "-1486461488": ["Red Roman Candle", "firework.romancandle.red"],
    "-1488398114": ["Composter", "composter"],
    "-1497205569": ["Wood Mirror Small", "woodmirror.small"],
    "-1501451746": ["Cockpit Vehicle Module", "vehicle.1mod.cockpit"],
    "-1506397857": ["Salvaged Hammer", "hammer.salvaged"],
    "-1506417026": ["Ninja Suit", "attire.ninja.suit"],
    "-1507239837": ["HBHF Sensor", "electric.hbhfsensor"],
    "-1509851560": ["Cooked Deer Meat", "deermeat.cooked"],
    "-1511285251": ["Pumpkin Seed", "seed.pumpkin"],
    "-1517740219": ["Speargun", "speargun"],
    "-1518883088": ["Night Vision Goggles", "nightvisiongoggles"],
    "-1519126340": ["Drop Box", "dropbox"],
    "-1520560807": ["Raw Bear Meat", "bearmeat"],
    "-1528767189": ["Gold Frame Standing", "goldframe.standing"],
    "-1530414568": ["Cassette Recorder", "fun.casetterecorder"],
    "-1535621066": ["Stone Fireplace", "fireplace.stone"],
    "-1536855921": ["Shovel", "shovel"],
    "-1538109120": ["Violet Volcano Firework", "firework.volcano.violet"],
    "-1539025626": ["Miners Hat", "hat.miner"],
    "-1541706279": ["Wood Frame Medium", "woodframe.medium"],
    "-1549739227": ["Boots", "shoes.boots"],
    "-1553999294": ["Red Boomer", "firework.boomer.red"],
    "-1557377697": ["Empty Tuna Can", "can.tuna.empty"],
    "-1569700847": ["Headset", "twitch.headset"],
    "-1579932985": ["Horse Dung", "horsedung"],
    "-1581843485": ["Sulfur", "sulfur"],
    "-1583967946": ["Stone Hatchet", "stonehatchet"],
    "-1588628467": ["Computer Station", "computerstation"],
    "-1607980696": ["Workbench Level 3", "workbench3"],
    "-1614955425": ["Strengthened Glass Window", "wall.window.glass.reinforced"],
    "-1615281216": ["Armored Passenger Vehicle Module", "vehicle.1mod.passengers.armored"],
    "-1621539785": ["Beach Parasol", "beachparasol"],
    "-1622110948": ["Bandit Guard Gear", "attire.banditguard"],
    "-1622660759": ["Large Present", "xmas.present.large"],
    "-1624770297": ["Light Frankenstein Torso", "frankensteins.monster.01.torso"],
    "-1647846966": ["Two Sided Ornate Hanging Sign", "sign.hanging.ornate"],
    "-1651220691": ["Pookie Bear", "pookie.bear"],
    "-1654233406": ["Sardine", "fish.sardine"],
    "-1663759755": ["Homemade Landmine", "trap.landmine"],
    "-1667224349": ["Decorative Baubels", "xmas.decoration.baubels"],
    "-1671551935": ["Torpedo", "submarine.torpedo.straight"],
    "-1673693549": ["Empty Propane Tank", "propanetank"],
    "-1677315902": ["Pure Healing Tea", "healingtea.pure"],
    "-1679267738": ["Graveyard Fence", "wall.graveyard.fence"],
    "-1683726934": ["Two-Way Mirror", "twowaymirror.window"],
    "-1685290200": ["12 Gauge Buckshot", "ammo.shotgun"],
    "-1691396643": ["HV Pistol Ammo", "ammo.pistol.hv"],
    "-1693832478": ["Large Flatbed Vehicle Module", "vehicle.2mod.flatbed"],
    "-1695367501": ["Shorts", "pants.shorts"],
    "-1696379844": ["Hazmat Youtooz", "hazmatyoutooz"],
    "-1698937385": ["Herring", "fish.herring"],
    "-1707425764": ["Fishing Tackle", "fishing.tackle"],
    "-1709878924": ["Raw Human Meat", "humanmeat.raw"],
    "-1729415579": ["Adv. Anti-Rad Tea", "radiationresisttea.advanced"],
    "-1732475823": ["Medium Frankenstein Head", "frankensteins.monster.02.head"],
    "-1736356576": ["Reactive Target", "target.reactive"],
    "-1754948969": ["Sleeping Bag", "sleepingbag"],
    "-1758372725": ["Thompson", "smg.thompson"],
    "-1759188988": ["Hab Repair", "habrepair"],
    "-1768880890": ["Small Shark", "fish.smallshark"],
    "-1770889433": ["Sky Lantern - Green", "skylantern.skylantern.green"],
    "-1772746857": ["Heavy Scientist Suit", "scientistsuit_heavy"],
    "-1773144852": ["Hide Skirt", "attire.hide.skirt"],
    "-1774190142": ["Scrap Frame Standing", "scrapframe.standing"],
    "-1776128552": ["Green Berry Seed", "seed.green.berry"],
    "-1778159885": ["Heavy Plate Pants", "heavy.plate.pants"],
    "-1778897469": ["Button", "electric.button"],
    "-1779180711": ["Water", "water"],
    "-1779183908": ["Paper", "paper"],
    "-1780802565": ["Salvaged Icepick", "icepick.salvaged"],
    "-1785231475": ["Surgeon Scrubs", "halloween.surgeonsuit"],
    "-1800345240": ["Speargun Spear", "speargun.spear"],
    "-1802083073": ["High Quality Valves", "valve3"],
    "-1804515496": ["Gold Mirror Medium", "goldmirror.medium"],
    "-1812555177": ["LR-300 Assault Rifle", "rifle.lr300"],
    "-1815301988": ["Water Pistol", "pistol.water"],
    "-1819233322": ["Medium Wooden Sign", "sign.wooden.medium"],
    "-1819763926": ["Wind Turbine", "generator.wind.scrap"],
    "-1824770114": ["Sky Lantern - Orange", "skylantern.skylantern.orange"],
    "-1824943010": ["Jack O Lantern Happy", "jackolantern.happy"],
    "-1832422579": ["One Sided Town Sign Post", "sign.post.town"],
    "-1836526520": ["Gold Frame Small", "goldframe.small"],
    "-1841918730": ["High Velocity Rocket", "ammo.rocket.hv"],
    "-1843426638": ["MLRS Rocket", "ammo.rocket.mlrs"],
    "-1848736516": ["Cooked Chicken", "chicken.cooked"],
    "-1850571427": ["Silencer", "weapon.mod.silencer"],
    "-1861522751": ["Research Table", "research.table"],
    "-1863063690": ["Rocking Chair", "rockingchair"],
    "-1863559151": ["Water Barrel", "water.barrel"],
    "-1878475007": ["Satchel Charge", "explosive.satchel"],
    "-1878764039": ["Small Trout", "fish.troutsmall"],
    "-1880231361": ["Flatbed Vehicle Module", "vehicle.1mod.flatbed"],
    "-1880870149": ["Red Keycard", "keycard_red"],
    "-1884328185": ["ScrapTransportHeliRepair", "scraptransportheli.repair"],
    "-1899491405": ["Glue", "glue"],
    "-1901993050": ["Gold Frame Medium", "goldframe.medium"],
    "-1903165497": ["Bone Helmet", "deer.skull.mask"],
    "-1904821376": ["Orange Roughy", "fish.orangeroughy"],
    "-1913996738": ["Fish Trophy", "fishtrophy"],
    "-1916473915": ["Chinese Lantern", "chineselantern"],
    "-1938052175": ["Charcoal", "charcoal"],
    "-1941646328": ["Can of Tuna", "can.tuna"],
    "-1944704288": ["Ice Throne", "chair.icethrone"],
    "-1950721390": ["Concrete Barricade", "barricade.concrete"],
    "-1958316066": ["Scientist Suit", "hazmatsuit_scientist_peacekeeper"],
    "-1961560162": ["Firecracker String", "lunar.firecrackers"],
    "-1962971928": ["Mushroom", "mushroom"],
    "-1966748496": ["Mace", "mace"],
    "-1973785141": ["Fogger-3000", "fogmachine"],
    "-1978999529": ["Salvaged Cleaver", "salvaged.cleaver"],
    "-1982036270": ["High Quality Metal Ore", "hq.metal.ore"],
    "-1985799200": ["Rug", "rug"],
    "-1989600732": ["Hot Air Balloon Armor", "hab.armor"],
    "-1992717673": ["Large Furnace", "furnace.large"],
    "-1994909036": ["Sheet Metal", "sheetmetal"],
    "-1997543660": ["Horse Saddle", "horse.saddle"],
    "-1997698639": ["Sunglasses", "sunglasses03chrome"],
    "-1999722522": ["Furnace", "furnace"],
    "-2001260025": ["Instant Camera", "tool.instant_camera"],
    "-2002277461": ["Road Sign Jacket", "roadsign.jacket"],
    "-2012470695": ["Improvised Balaclava", "mask.balaclava"],
    "-2022172587": ["Diving Tank", "diving.tank"],
    "-2024549027": ["Heavy Frankenstein Legs", "frankensteins.monster.03.legs"],
    "-2025184684": ["Shirt", "shirt.collared"],
    "-2026042603": ["Baseball Bat", "mace.baseballbat"],
    "-2027793839": ["Advent Calendar", "xmas.advent"],
    "-2027988285": ["Locomotive", "locomotive"],
    "-2040817543": ["Pan Flute", "fun.flute"],
    "-2047081330": ["Movember Moustache", "movembermoustache"],
    "-2049214035": ["Pressure Pad", "electric.pressurepad"],
    "-2058362263": ["Small Candle Set", "smallcandles"],
    "-2067472972": ["Sheet Metal Door", "door.hinged.metal"],
    "-2069578888": ["M249", "lmg.m249"],
    "-2072273936": ["Bandage", "bandage"],
    "-2073432256": ["Skinning Knife", "knife.skinning"],
    "-2084071424": ["Potato Seed", "seed.potato"],
    "-2086926071": ["Potato", "potato"],
    "-2094954543": ["Wood Armor Helmet", "wood.armor.helmet"],
    "-2097376851": ["Nailgun Nails", "ammo.nailgun.nails"],
    "-2099697608": ["Stones", "stones"],
    "-2103694546": ["Sunglasses", "sunglasses02camo"],
    "-2107018088": ["Shovel Bass", "fun.bass"],
    "-2123125470": ["Advanced Healing Tea", "healingtea.advanced"],
    "-2124352573": ["Acoustic Guitar", "fun.guitar"],
    "-2139580305": ["Auto Turret", "autoturret"]
}

//Reverse map item shortname to item id
export const shortname_to_id = new Map(Object.entries(ItemNames).map(([id, [_, shortName]]) => {
    return [shortName, id];
}));



const MonumentNames = {
    /* Omitted DungeonBase & train_tunnel_display_name */
	"airfield_display_name": "AIRFIELD",
	"bandit_camp": "BANDIT CAMP",
	"dome_monument_name": "THE DOME",
	"excavator": "GIANT EXCAVATOR PIT",
	"fishing_village_display_name": "FISHING VILLAGE",
	"gas_station": "OXUM'S GAS STATION",
	"harbor_2_display_name": "HARBOR",
	"harbor_display_name": "HARBOR",
	"junkyard_display_name": "JUNKYARD",
	"large_fishing_village_display_name": "LARGE FISHING VILLAGE",
	"large_oil_rig": "LARGE OIL RIG",
	"launchsite": "LAUNCH SITE",
	"lighthouse_display_name": "LIGHTHOUSE",
	"military_tunnels_display_name": "MILITARY TUNNEL",
	"mining_outpost_display_name": "MINING OUTPOST",
	"mining_quarry_hqm_display_name": "HQM QUARRY",
	"mining_quarry_stone_display_name": "STONE QUARRY",
	"mining_quarry_sulfur_display_name": "SULFUR QUARRY",
	"oil_rig_small": "OIL RIG",
	"outpost": "OUTPOST",
	"power_plant_display_name": "POWER PLANT",
	"satellite_dish_display_name": "SATELLITE DISH",
	"sewer_display_name": "SEWER BRANCH",
	"stables_a": "RANCH",
	"stables_b": "LARGE BARN",
	"supermarket": "ABANDONED SUPERMARKET",
	"swamp_c": "ABANDONED CABINS",
	"train_tunnel_display_name": "",
	"train_yard_display_name": "TRAIN YARD",
	"underwater_lab": "UNDERWATER LAB",
	"water_treatment_plant_display_name": "WATER TREATMENT PLANT",
	"ferryterminal": "FERRY TERMINAL",
	"arctic_base_a": "ARCTIC RESEARCH BASE",
	"missile_silo_monument": "MISSILE SILO",
	"AbandonedMilitaryBase": "ABANDONED MILITARY BASE"
}


export class ServerInfo {
    /**
     * @param {any} serverData
     */
    constructor(serverData) {
        this._data = serverData;
    }

    get header_image() { return this._data.header_image; }

    get logo_image() { return this._data.logo_image; }

    get map() { return this._data.map; }

    get max_players() { return this._data.max_players; }
    
    get name() { return this._data.name; }

    get player_count() { return this._data.players; }

    get queued_players() { return this._data.queued_players; }

    get map_seed() { return this._data.seed; }

    get map_size() { return this._data.size; }

    get url() { return this._data.url; }

    get wipe_time() { return this._data.wipe_time; }
}

export class TeamInfo {
    /**
     * @param {any} teamData
     */
    constructor(teamData) {
        this._data = teamData;
        this._member_map = new Map();

        this._data.members.forEach((memberData) => {
            const member = new Member(memberData);
            this._member_map.set(member.steam_id, member);
        });
    }

    get leader_map_notes() { return this._data.map_notes.map((/** @type {any} */ note) => new MapNote(note)); }

    get leader_steam_id() { return this._data.leader_steam_id; }

    get map_notes() { return this._data.map_notes.map((/** @type {any} */ note) => new MapNote(note)); }
    
    /** @returns {Member[]} */
    get members() { return Array.from(this._member_map.values()); }

    /** @returns {Member} */
    getMemberBySteamId(steam_id) { return this._member_map.get(steam_id); }
}

export class MapNote {
    /**
     * @param {any} mapNoteData
     */
    constructor(mapNoteData) {
        this._data = mapNoteData;
    }

    get colour_index() { return this._data.colour_index; }

    get label() { return this._data.label; }

    get icon() { return this._data.icon; }

    get x() { return this._data.x; }

    get y() { return this._data.y; }
}

export class Member {
    /**
     * @param {any} memberData
     */
    constructor(memberData) {
        this._data = memberData;
    }

    get death_time() { return this._data.death_time; }

    get is_alive() { return this._data.is_alive.toLowerCase() === "true"; }

    get is_online() { return this._data.is_online.toLowerCase() === "true"; }

    get name() { return this._data.name; }

    get spawn_time() { return this._data.spawn_time; }

    get steam_id() { return this._data.steam_id; }

    get x() { return this._data.x; }

    get y() { return this._data.y; }
}

export class Monument {
    constructor(monumentData) {
        this._data = monumentData;
    }

    get name() { return MonumentNames[this.token]; }

    get token() { return this._data.token; }

    get x() { return this._data.x; }

    get y() { return this._data.y; }
}

export class Marker {
    constructor(markerData) { 
        this._data = markerData;
        this._spawn_time = util.timeNow();
    }

    get alpha() { return this._data.alpha; }

    get colour1() { return new Colour(this._data.colour1); }
    
    get colour2() { return new Colour(this._data.colour2); }

    get id() { return this._data.id; }

    get name() { return this._data.name; }

    get out_of_stock() { return this._data.out_of_stock.toLowerCase() !== "false"; }

    get radius() { return this._data.radius; }

    get rotation() { return this._data.rotation; }

    get sell_orders() { 
        let _sell_orders = [];
        for (let i = 0; i < this._data.sell_orders.length; i++)
            _sell_orders[i] = new SellOrder(this._data.sell_orders[i]);
        return _sell_orders;
    }

    get steam_id() { return this._data.steam_id; }

    get type() { return this._data.type; }

    get typeName() { return MarkerNames[this.type]; }

    get x() { return this._data.x; }
    
    get y() { return this._data.y; }

    get spawn_time() { return this._spawn_time; }

}

export class Colour {
    constructor(colourData) {
        this._data = colourData;
    }

    get w() { return this._data.w; }

    get x() { return this._data.x; }

    get y() { return this._data.y; }
    
    get z() { return this._data.z; }
}

export class SellOrder {
    constructor(sellOrderData) {
        this._data = sellOrderData;
    }

    get amount_in_stock() { return this._data.amount_in_stock; }

    get cost_per_item() { return this._data.cost_per_item; }

    get currency_id() { return this._data.currency_id; }

    get currency_name() { return ItemNames[this._data.currency_id][0]; }

    get currency_shortname() { return ItemNames[this._data.currency_id][1]; }

    get currency_is_blueprint() { return this._data.currency_is_blueprint; }

    get item_id() { return this._data.item_id; }

    get item_name() { return ItemNames[this._data.item_id][0]; }

    get item_shortname() { return ItemNames[this._data.item_id][1]; }

    get item_is_blueprint() { return this._data.item_is_blueprint; }

    get quantity() { return this._data.quantity; }
}

export class Chat {
    constructor(chat) {
        this._data = chat;
    }

    get steam_id() { return this._data.steam_id; }

    get name() { return this._data.name; }

    get message() { return this._data.message; }
    
    get colour() { return this._data.colour; }

    get time() { return this._data.time }
}