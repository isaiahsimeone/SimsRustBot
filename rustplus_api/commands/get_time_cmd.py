from .command import Command
from .command_registry import command

@command
class GetTimeCommand(Command):
    def get_aliases(self):
        return ["time", "gettime", "whatisthetime", "timecheck", "checktime", "timenow", "now"]

    async def execute(self, rust_api, sender_steam_id, args=[]):
        try:
            # Get the time from the Rust API
            response = await rust_api.get_socket().get_time()
            now = response.time
            sunset = response.sunset
            sunrise = response.sunrise
            timescale = response.time_scale
            
            msg = f"It's {now}."
            
            # If it's night, state when sunrise is, if it's day, state when night is
            if to_time(now) > to_time(sunrise) and to_time(now) < to_time(sunset):
                msg += f" Night falls at {response.sunset}"
            else:
                msg += f" Day comes at {response.sunrise}"
            
            await rust_api.send_game_message(msg)

        except Exception as e:
            rust_api.log(f"Failed to execute GetTimeCommand: {e}", type="error")
    
    def help(self):
        pass

@staticmethod
def to_time(time_str):
    hours, minutes = map(int, time_str.split(":"))
    total_minutes = hours * 60 + minutes
    return total_minutes

@staticmethod
def to_real_minutes(start_str, end_str, timescale):
    print(f"timescale = {timescale}")
    start_min = to_time(start_str)
    end_min = to_time(end_str)
    
    if end_min < start_min:
        end_min += 1440 # 24 hours in minutes
    """
    TimerSeconds = 8.96 * 10^-7 * Rustminutes^3 

		- 0.00398 * RustMinutes^2

		+ 6.37000 * RustMinutes
    """
    real_seconds_per_rust_minute = 4.75 / timescale
    one_real_minute = (60 / real_seconds_per_rust_minute)
    
    return abs(end_min - start_min) / one_real_minute