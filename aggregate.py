from collections import defaultdict, Counter
import re

LOG_PATTERN = re.compile(r"\[(.*?)\]\s+(ERROR|WARN|INFO)\s+(.*)")

def aggregate_logs(logs: list[str]) -> dict:
    """
    Aggregates raw logs into structured summaries.
    """

    service_data = defaultdict(lambda: {
        "error_count": 0,
        "messages": []
    })

    for log in logs:
        match = LOG_PATTERN.match(log)
        if not match:
            continue

        service, level, message = match.groups()

        if level == "ERROR":
            service_data[service]["error_count"] += 1
            service_data[service]["messages"].append(message)

    aggregated_result = {}

    for service, data in service_data.items():
        message_counter = Counter(data["messages"])
        top_messages = [msg for msg, _ in message_counter.most_common(3)]

        aggregated_result[service] = {
            "error_count": data["error_count"],
            "top_messages": top_messages
        }

    return aggregated_result
