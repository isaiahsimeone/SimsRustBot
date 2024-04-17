# Sim's Rust Bot

With web map notes, how about we just translate the coordinates to JSON coordinates like those that we would get from the companion API, then just inject them into the map_notes list and let the rest of the current flow handle the positioning

- rust_plus_api.py should be able to translate names to steam IDs


drone that can spot nodes? image processor, could send a 
custom map marker indicating a node 

## Need to:
- Modify BUS to allow a caller to await a response
- Put config and database on the BUS
- Make the bigger classes in rustplus their own service in a thread like MapPoller and TeamPoller. We can still use the rustplus bus probably

Next:
- put ConfigManager and Database on the bus
- Capture player x,y when they pair a device - Then, we know where their base probably is
- Map note labels
- make heli & chinook gifs
- Heli exploded at (grid cell) - We need to check when the marker for it disappears during polling
- Include a verbosity setting so the bot doesn't yap too much on the chat
- Death markers
- set min marker size for zoom in - they get too small
- Player list in web interface
- Shop UI browser in web interface
- grouping vending machines on map
- browser shop search - snap to shop
- browser map control - snap to player
- we can tell when heli goes down if it vanishes within the map
- we can get oil crate by chinook?
- make map bigger to fit oil - we can add img of rig to map before saivg as map.jpg
- map grid toggleable
- track player logins/logouts/positions/deaths in DB -> EOW summary -> heatmap
- END OF WIPE SUMMARY
- When heli/cargo comes in, give player compass bearing to its entry point

Maybe
- Marker extrapolation (player, chinook, cargo, heli)
- Consider takig the map image, and expanding thhe sides to make it the same as game map, math is already workig, but we i don't thhhik we can curretly plot oil etc
- alert new shops? option

Done:
- [x] Receive team chats on web
- [x] Send rust server team messages from web
- [x] GetSteamPic() function. Call from JS
- [x] Chinook/heli blades animation on map
