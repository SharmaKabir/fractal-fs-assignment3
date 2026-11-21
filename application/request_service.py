# print("this is service reuqest feature file")
from domain.exceptions import DuplicateRequestIdError, RequestNotFoundError
from domain.service_request import ServiceRequest
class RequestService:
    #create view search functionilty

    def __init__(self, repository):
        self.repository = repository
        self.requests = {}
        self._load_requests()

    def _load_requests(self):
        for data in self.repository.load():
            request = ServiceRequest.from_dict(data)
            self.requests[request.request_id] = request

    def _save_requests(self):
        self.repository.save([request.to_dict() for request in self.requests.values()])

    def create_request(self, employee_name, issue, priority):
        request_id = max(self.requests, default=0) + 1
        if request_id in self.requests:
            raise DuplicateRequestIdError(
                f"Request ID {request_id} already exists"
            )

        request = ServiceRequest(request_id, employee_name, issue, priority)
        self.requests[request.request_id] = request
        self._save_requests()
        return request

    def view_requests(self):
        return list(self.requests.values())

    def search_request(self, request_id):
        try:
            key = int(str(request_id).strip())
        except (TypeError, ValueError) as error:
            raise ValueError("Request ID must be a positive number") from error

        if key < 1:
            raise ValueError("Request ID must be a positive number")

        request = self.requests.get(key)
        if request is None:
            raise RequestNotFoundError(f"Request {key} not found")
        return request

    def resolve_request(self, request_id):
        request = self.search_request(request_id)
        request.resolve()
        self._save_requests()
        return request
