#import required modules

class Signal():
    def __init__(self, signal_type):
        self._active = None
        self._callback = None
        self._signal_type = signal_type
    
    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, n_active):
        if self._active is None or n_active != self._active:
            self._active = n_active
            if self._callback:
                self._callback(self._signal_type, n_active)

    def set_callback(self, callback):
        self._callback = callback