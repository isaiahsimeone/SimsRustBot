from flask import render_template, Response, stream_with_context
import json
import time

def setup_event_streams(app, web_server):
    
    @app.route('/markers')
    def get_markers():
        def marker_stream():
            while True:
                # Check for new data in the queue
                if web_server.map_markers_queue:
                    marker_data = web_server.map_markers_queue.pop(0)
                    #print("Sending marker data:", marker_data)  # Debug print
                    yield f"data: {json.dumps(marker_data)}\n\n"
                else:
                    # If no data, send a comment to keep the connection alive
                    yield ": keep-alive\n\n"
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
                else:
                    # If no data, send a comment to keep the connection alive
                    yield ": keep-alive\n\n"
                time.sleep(1)

        return Response(stream_with_context(team_info_stream()), mimetype='text/event-stream') 
    
    @app.route('/teamchat')   
    def get_team_chat():
        def team_chat_stream():
            while True:
                # Check for new data in the queue
                if web_server.team_chat_log:
                    chats = []
                    for message in web_server.team_chat_log:
                        chats.append(web_server.team_chat_log.pop(0))
                    #print("Sending team chat:", chats)  # Debug print
                    yield f"data: {json.dumps(chats)}\n\n"
                else:
                    # If no data, send a comment to keep the connection alive
                    yield ": keep-alive\n\n"
                time.sleep(1)

        return Response(stream_with_context(team_chat_stream()), mimetype='text/event-stream') 
    