from .exceptions import InvalidPriorityError, RequestAlreadyResolvedError


class ServiceRequest:
    VALID_PRIORITIES = ("LOW", "MEDIUM", "HIGH")
    VALID_STATUSES = ("OPEN", "RESOLVED")

    def __init__(self, request_id, employee_name, issue, priority, status="OPEN"):
        self.request_id = self._normalize_request_id(request_id)
        self.employee_name = self._required_text(employee_name, "Employee Name")
        self.issue = self._required_text(issue, "Issue")
        normalized_priority = priority.strip().upper()
        if normalized_priority not in self.VALID_PRIORITIES:
            raise InvalidPriorityError("Priority must be LOW, MEDIUM or HIGH")
        self.priority = normalized_priority
        normalized_status = status.strip().upper()
        if normalized_status not in self.VALID_STATUSES:
            raise ValueError("Status must be OPEN or RESOLVED")
        self.status = normalized_status

    @staticmethod
    def _required_text(value, field_name):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} cannot be empty")
        return value.strip()

    @staticmethod
    def _normalize_request_id(value):
        text = str(value).strip().upper()
        if not text:
            raise ValueError("Request ID must be in format SR<number>")

        if text.startswith("SR"):
            number_text = text[2:]
        elif text.isdigit():
            number_text = text
        else:
            raise ValueError("Request ID must be in format SR<number>")

        if not number_text.isdigit() or int(number_text) < 1:
            raise ValueError("Request ID must be in format SR<number>")

        return f"SR{int(number_text)}"

    @classmethod
    def normalize_request_id(cls, value):
        return cls._normalize_request_id(value)

    def resolve(self):
        #domain business thing to resolve
        if self.status == "RESOLVED":
            raise RequestAlreadyResolvedError(
                f"Request {self.request_id} is already RESOLVED"
            )
        self.status = "RESOLVED"

    def to_dict(self):
        return {
            "request_id": self.request_id,
            "employee_name": self.employee_name,
            "issue": self.issue,
            "priority": self.priority,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            request_id=data["request_id"],
            employee_name=data["employee_name"],
            issue=data["issue"],
            priority=data["priority"],
            status=data.get("status", "OPEN"),
        )
