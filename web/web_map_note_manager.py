import asyncio

class WebMapNoteManager():
    def __init__(self, socketio, web_server):
        self.map_notes = [] # Map notes made through web interface (not proper rust ones)
        self.socketio = socketio
        self.web_server = web_server
        self.map_notes = []
        pass
    
    def add_note(self, note, sender):
        """"""
        print(str(note) + " from " + str(sender))
        self.map_notes.append((note, sender))
        self.notify_change("add", note, sender)
    
    def remove_note(self, message, sender):
        pass
    
    def get_notes(self):
        map_notes_data = []
        for note, sender in self.map_notes:
            map_notes_data.append(note)
        
        return {"type": "mapnotesweb", "data": map_notes_data}
        
    def format_message(self, type, changeType, note, sender):
        return {"type": type, "data": {"change": changeType, "author": sender, "note": note}}
    
    def notify_change(self, changeType, note, sender):
        self.socketio.emit("broadcast", {"type": "mapnotechange", "data": {"change": changeType, "author": sender, "note": note}})