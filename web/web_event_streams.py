from flask import render_template, Response, stream_with_context
import json
import time

def setup_event_streams(app, web_server):
    
    @app.route('/markers')
    def get_markers():
        def marker_stream():
            while True:
                # Check to see if map marker data has been updated
                if web_server.map_marker_data:
                    #print("Sending marker data:", marker_data)  # Debug print
                    yield f"data: {json.dumps(web_server.map_marker_data)}\n\n"
                else:
                    # If no data, send a comment to keep the connection alive
                    yield ": keep-alive\n\n"
                time.sleep(abs(web_server.map_poll_frequency - 1))

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
                else:
                    # If no data, send a comment to keep the connection alive
                    yield ": keep-alive\n\n"
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
                else:
                    # If no data, send a comment to keep the connection alive
                    yield ": keep-alive\n\n"
                time.sleep(1)

        return Response(stream_with_context(team_chat_stream()), mimetype='text/event-stream') 
    