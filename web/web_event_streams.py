from flask import render_template, request, Response, stream_with_context
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
                    print("Sending marker data:", marker_data)  # Debug print
                    yield f"data: {json.dumps(marker_data)}\n\n"
                else:
                    # If no data, send a comment to keep the connection alive
                    yield ": keep-alive\n\n"
                time.sleep(1)

        return Response(stream_with_context(marker_stream()), mimetype='text/event-stream')
    """
    @app.route('/monuments')
    def get_monuments():
        def monument_stream():
            
            while True:
                # Check for new data in the queue
                if web_server.map_markers_queue:
                    marker_data = web_server.map_markers_queue.pop(0)
                    print("Sending monument data:", marker_data)  # Debug print
                    yield f"data: {json.dumps(marker_data)}\n\n"
                else:
                    # If no data, send a comment to keep the connection alive
                    yield ": keep-alive\n\n"
                time.sleep(1)

        return Response(stream_with_context(monument_stream()), mimetype='text/event-stream')
    """