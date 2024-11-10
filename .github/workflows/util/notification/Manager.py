from Observer import Observer


class Manager:
    def __init__(self):
        self._observers = []
    
    def attach(self, observer: Observer):
        """Attach an observer."""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: Observer):
        """Detach an observer."""
        self._observers.remove(observer)
    
    def notify(self, message: str):
        """Notify all observers of the state change."""
        for observer in self._observers:
            observer.update(message)