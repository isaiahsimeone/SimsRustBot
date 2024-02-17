from flask import render_template, Response, stream_with_context
from flask_socketio import emit
import json
import time

def setup_event_streams(socketio, web_server):
  
    @socketio.on('connect')
    def socketio_connect():
        print("Client connected")
        
    @socketio.on('disconnect')
    def socketio_disconnect():
        print("Client disconnected")
        
    @socketio.on('request')
    def request_data(message):
        request_what = message.get("type")
        data = None
        
        match request_what:
            case "teamchat":
                data = web_server.team_chat_log
            case "monuments":
                data = web_server.map_monuments
            case "mapmarkers":
                data = web_server.map_marker_data
            case "serverinfo":
                data = web_server.server_info
            case "teaminfo":
                data = web_server.team_info
            case _:
                print("Unknown request type")
                
        emit("data_response", {"type": request_what, "data": data})
        
        print("Client requesting:", str(request_what))
  

  
    """
    @app.route('/markers')
    def get_markers():
        def marker_stream():
            while True:
                # Check to see if map marker data has been updated
                if web_server.map_marker_data:
                    #print("Sending marker data:", marker_data)  # Debug print
                    yield f"data: {json.dumps(web_server.map_marker_data)}\n\n"
                time.sleep(1)

        return Response(stream_with_context(marker_stream()), mimetype='text/event-stream')
    
    @app.route('/teammemberupdates')
    def get_team_member_update():
        def team_info_stream():
            while True:
                # Check for new data in the queue
                if web_server.team_update_queue:
                    team_update = web_server.team_update_queue.pop(0)
                    print("Sending TEAM data:", team_update)  # Debug print
                    yield f"data: {json.dumps(team_update)}\n\n"
                time.sleep(1)

        return Response(stream_with_context(team_info_stream()), mimetype='text/event-stream') 
    
    @app.route('/teamchat')   
    def get_team_chat():
        def team_chat_stream():
            last_len = 0
            while True:
                # Check for new data in the queue
                if web_server.team_chat_log and len(web_server.team_chat_log) > last_len:
                    print("SEND")
                    chats = []
                    for i in range(last_len, len(web_server.team_chat_log)):
                        chats.append(web_server.team_chat_log[i])
                    #print("Sending team chat:", chats)  # Debug print
                    last_len = len(web_server.team_chat_log)
                    yield f"data: {json.dumps(chats)}\n\n"
                time.sleep(1)

        return Response(stream_with_context(team_chat_stream()), mimetype='text/event-stream') 
    """