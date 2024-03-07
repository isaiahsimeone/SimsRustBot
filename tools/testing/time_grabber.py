import asyncio
from rustplus import RustSocket
import time
POLL_TIME = 1

async def main():
    socket = RustSocket("49.2.177.161", "28083", 76561198032291162, -1746662161)
    await socket.connect()
    print(f"Connected. Waiting for midnight, then, we will poll every {POLL_TIME} seconds")
    
    out_f = open("upsurgequick.txt", "w")
    
    
    out_f.write("Time_now, raw_time, sunrise, sunset, timescale, real_time_since_last_sample, rust_time_advancement_since_last_sample, rust_min/real_sec")
    
    loop_end = 0
    last_raw = 0
    
    # wait for midnight
    while True:
        resp = await socket.get_time()
        if resp.raw_time >= 0 and resp.raw_time <= 1:
            break
        time.sleep(1)
    
    print("It's midnight. Starting...")
    
    while True:
        resp = await socket.get_time()
        
        now = resp.time
        raw = resp.raw_time
        
        rust_time_advancement = raw - last_raw
        
        print(f"Rust time is {now}, a difference of {rust_time_advancement}. Took {POLL_TIME}")
        
        out_f.write(f"{now}, {raw}, {resp.sunrise}, {resp.sunset}, {resp.time_scale}, {POLL_TIME}, {rust_time_advancement}, {rust_time_advancement/POLL_TIME}\n")     
        out_f.flush()   
        
        time.sleep(POLL_TIME)
        last_raw = raw

    await socket.disconnect()

@staticmethod
def to_time(time_str):
    hours, minutes = map(int, time_str.split(":"))
    total_minutes = hours * 60 + minutes
    return total_minutes

asyncio.run(main())