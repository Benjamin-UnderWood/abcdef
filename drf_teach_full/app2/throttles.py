from rest_framework import throttling


class BurstRateThrottle(throttling.UserRateThrottle):
    scope = 'burst'


class DurationRateThrottle(throttling.UserRateThrottle):
    scope = 'duration'



import random

class RandomRateThrottle(throttling.BaseThrottle):

    def allow_request(self, request, view):
        return random.randint(1, 5) != 1


