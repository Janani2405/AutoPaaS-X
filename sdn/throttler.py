import requests
import statistics

# Mock credentials for OpenDaylight SDN controller
ODL_URL = "http://localhost:8181/restconf/config/opendaylight-inventory:nodes"
ODL_USER = "admin"
ODL_PASS = "admin"

# Simulated bandwidth logs (in Mbps)
MOCK_BANDWIDTH_LOGS = {
    "tenant1": 3.5,
    "tenant2": 2.1,
    "tenant3": 8.9,
    "tenant4": 1.0
}

def enforce_bandwidth_policy(tenant_usage: dict):
    usage_values = list(tenant_usage.values())
    median_usage = statistics.median(usage_values)

    print(f"📊 Median bandwidth: {median_usage} Mbps")

    for tenant, usage in tenant_usage.items():
        if usage > 2 * median_usage:
            print(f"🚨 Tenant {tenant} is using {usage} Mbps (over limit)")
            apply_throttle_rule(tenant)
        else:
            print(f"✅ Tenant {tenant} is within limits.")

def apply_throttle_rule(tenant_id):
    """
    Placeholder for OpenDaylight API call.
    Normally, you'd create an OpenFlow rule to limit bandwidth.
    """
    print(f"⚙️ Throttle rule triggered for {tenant_id}. [Simulated]")
    # Example (not functional):
    # response = requests.put(
    #     f"{ODL_URL}/node/flow/{tenant_id}",
    #     auth=(ODL_USER, ODL_PASS),
    #     json=openflow_rule_data
    # )
