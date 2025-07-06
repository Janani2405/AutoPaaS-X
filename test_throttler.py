from sdn.throttler import enforce_bandwidth_policy

enforce_bandwidth_policy({
    "tenant1": 3.5,
    "tenant2": 2.1,
    "tenant3": 8.9,
    "tenant4": 1.0
})

