import time
from watchdog.events import FileSystemEventHandler

from typing import Callable

class FileWatchdog(FileSystemEventHandler):
    def __init__(self, filepath: str, callback: Callable, debounce_time: float = 1.0, *args, **kwargs):
        """Watches for when a file 'filepath' changes, then gets a callback at on_modified,
        which then calls the specified callback function. Modifications to a file can call on_modified
        multiple times (e.g. writing the first chunk, writing the second, updating mtime, etc). To
        work around this, debounce_time specifies the window of time where all calls to on_modified,
        after an initial call, will be suppressed (i.e. callback won't be called)

        :param filepath: The path to the file to be watched
        :type filepath: str
        :param callback: The function to callback when the file is modified
        :type callback: Callable
        :param debounce_time: The window of time (after a callback) that callbacks are suppressed for, defaults to 1.0
        :type debounce_time: float, optional
        """
        super().__init__(*args, **kwargs)
        self._filepath = filepath
        self._callback = callback
        self._debounce_time = debounce_time
        self._last_called = 0

    def on_modified(self, event):
        """Called by the watchdog library when a file is modified. Which then calls
        the callback specified on construction of this class. Debounce time becomes relevant here.

        :param event: The file modification event
        :type event: :class:`FileSystemEvent`
        """
        # Check if the modified file is the one we're interested in
        if event.src_path == self._filepath:
            current_time = time.time()
            # Check if the current call is within the debounce time
            if current_time - self._last_called >= self._debounce_time:
                self._last_called = current_time
                self._callback()

