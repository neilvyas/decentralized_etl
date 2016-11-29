class StateSentinel:
    def __setattr__(self, attr, value):
        raise AssertionError("Attempted to modify state!")
