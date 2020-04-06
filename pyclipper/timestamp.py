class VideoTimestamp:
    def __init__(self, stamp):
        self._raw = stamp.split(":")
        vals = list(map(int, self._raw))
        h, m, s = 0, 0, 0
        if len(vals) > 2:
            h, m, s = vals[0:3]
        elif len(vals) == 2:
            m, s = vals[0:2]
        else:
            s = vals[0]
        self._time_components = h, m, s

    @property
    def seconds(self):
        return (
            self._time_components[0] * 3600
            + self._time_components[1] * 60
            + self._time_components[2]
        )
