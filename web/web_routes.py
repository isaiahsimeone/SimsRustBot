from flask import render_template, request, Response, stream_with_context
from ipc.messenger import Service
import json
import time

def setup_routes(app, web_server):
    @app.route('/')
    def index():
        return render_template("index.html")

    @app.route('/submit_command')
    def submit_command():
        command = request.args.get('command')
        web_server.log(f"Got cmd '{command}'")
        web_server.send_message(command)
        return f"Command '{command}' received"

    @app.route('/stream')
    def stream():
        def event_stream():
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

        return Response(stream_with_context(event_stream()), mimetype='text/event-stream')