import random
import time

class DisasterEnvironment:
    def __init__(self):
        self.severity_levels = ["LOW", "MODERATE", "HIGH", "CRITICAL"]

    def sense(self):
        """Simulate sensing disaster conditions"""
        event = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "severity": random.choice(self.severity_levels)
        }
        return event
