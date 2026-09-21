from typing import Dict, List
NETWORK_DEVICES = [
    {
        "hostname": "Main_router1",
        "device_type": "Router",
        "management_ip": "10.10.1.1",
        "location": "CPP_DC",
        "status": "online",
        "cpu_percent": 85,
        "memory_percent": 74,
        "uptime_days": 420,
        "backup_status": "success",
    },
    {
        "hostname": "Main_router2",
        "device_type": "Router",
        "management_ip": "10.10.1.2",
        "location": "CPP_DC",
        "status": "online",
        "cpu_percent": 42,
        "memory_percent": 55,
        "uptime_days": 180,
        "backup_status": "success",
    },
    {
        "hostname": "Main_switch1",
        "device_type": "Switch",
        "management_ip": "10.10.1.3",
        "location": "CPP_DC",
        "status": "online",
        "cpu_percent": 24,
        "memory_percent": 86,
        "uptime_days": 95,
        "backup_status": "failed",
    },
    {
        "hostname": "Main_switch2",
        "device_type": "Switch",
        "management_ip": "10.10.1.4",
        "location": "CPP_DC",
        "status": "online",
        "cpu_percent": 19,
        "memory_percent": 48,
        "uptime_days": 210,
        "backup_status": "success",
    },
    {
        "hostname": "Main_firewall",
        "device_type": "Firewall",
        "management_ip": "10.1.1.1",
        "location": "CPP_DC",
        "status": "online",
        "cpu_percent": 91,
        "memory_percent": 89,
        "uptime_days": 3,
        "backup_status": "success",
    },
    {
        "hostname": "Dorm_Router",
        "device_type": "Router",
        "management_ip": "192.168.10.1",
        "location": "Dorms",
        "status": "offline",
        "cpu_percent": 0,
        "memory_percent": 0,
        "uptime_days": 0,
        "backup_status": "failed",
    },
    {
        "hostname": "Dorm_switch1",
        "device_type": "Switch",
        "management_ip": "192.168.10.2",
        "location": "Dorms",
        "status": "online",
        "cpu_percent": 31,
        "memory_percent": 52,
        "uptime_days": 4,
        "backup_status": "success",
    },
    {
        "hostname": "Dorm_firewall",
        "device_type": "Firewall",
        "management_ip": "10.1.2.1",
        "location": "Dorms",
        "status": "online",
        "cpu_percent": 58,
        "memory_percent": 63,
        "uptime_days": 145,
        "backup_status": "success",
    },
]


def evaluate_device_health(device: dict) -> List[str]:
    """Evaluates operational metrics and returns health warning flags."""
    issues = []
    if device["status"].lower() != "online":
        issues.append(f"CRITICAL: Device is {device['status'].upper()}")
    if device["cpu_percent"] >= 80.0:
        issues.append(f"High CPU utilization: {device['cpu_percent']}%")
    if device["memory_percent"] >= 80.0:
        issues.append(f"High Memory utilization: {device['memory_percent']}%")
    if device["backup_status"].lower() != "success":
        issues.append(f"Backup alert: {device['backup_status'].upper()}")
    if device["status"].lower() == "online" and device["uptime_days"] < 7:
        issues.append(f"Recent reboot warning: Uptime is {device['uptime_days']}d")
    return issues


def generate_report(devices: List[dict]) -> None:
    """Calculates fleet summaries and prints operational report."""
    type_counts = {}
    location_counts = {}
    flagged_devices = []

    for dev in devices:
        dtype = dev["device_type"]
        loc = dev["location"]
        type_counts[dtype] = type_counts.get(dtype, 0) + 1
        location_counts[loc] = location_counts.get(loc, 0) + 1

        issues = evaluate_device_health(dev)
        if issues:
            flagged_devices.append((dev, issues))

    print("=" * 80)
    print(f"{'NETWORK OPERATIONS HEALTH REPORT':^80}")
    print("=" * 80)

    print("\n[+] INVENTORY TOTALS BY DEVICE TYPE")
    for dtype, count in sorted(type_counts.items()):
        print(f"    - {dtype:<15}: {count} device(s)")

    print("\n[+] INVENTORY TOTALS BY LOCATION")
    for loc, count in sorted(location_counts.items()):
        print(f"    - {loc:<15}: {count} device(s)")

    print("\n" + "-" * 80)
    print(f"FLAGGED DEVICES REQUIRING ATTENTION ({len(flagged_devices)} DETECTED)")
    print("-" * 80)

    for dev, problems in flagged_devices:
        print(f"\nDevice: {dev['hostname']} ({dev['management_ip']})")
        print(f"  Type: {dev['device_type']} | Location: {dev['location']}")
        print("  Findings:")
        for prob in problems:
            print(f"    * {prob}")

    print("\n" + "=" * 80)
    print(f"{'END OF REPORT':^80}")
    print("=" * 80)


if __name__ == "__main__":
    generate_report(NETWORK_DEVICES)
