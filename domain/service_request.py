from .exceptions import InvalidPriorityError, RequestAlreadyResolvedError


class ServiceRequest:
    """A service request aggregate with its own priority and resolution rules."""

    VALID_PRIORITIES = ("LOW", "MEDIUM", "HIGH")
    VALID_STATUSES = ("OPEN", "RESOLVED")

    def __init__(self, request_id, employee_name, issue, priority, status="OPEN"):
        try:
            normalized_request_id = int(request_id)
        except (TypeError, ValueError) as error:
            raise ValueError("Request ID must be a positive number") from error
        if normalized_request_id < 1:
            raise ValueError("Request ID must be a positive number")
        self.request_id = normalized_request_id

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
