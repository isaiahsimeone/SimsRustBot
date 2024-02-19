# Sim's Rust Bot

Next:
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
