# print("this is main.py")
from pathlib import Path
from application.request_service import RequestService
from domain.exceptions import InvalidMenuChoiceError, InvalidPriorityError, RequestAlreadyResolvedError, RequestNotFoundError
from infrastructure.file_repository import FileRepository



PROJECT_ROOT = Path(__file__).resolve().parent


def print_request(request):
    print(
        f"{request.request_id} | {request.employee_name} | "
        f"{request.issue} | {request.priority} | {request.status}"
    )


def get_menu_choice():
    choice_text = input("Enter your choice: ").strip()
    try:
        choice = int(choice_text)
    except ValueError as error:
        raise InvalidMenuChoiceError("Invalid menu input. Enter a number from 1 to 5.") from error

    if choice not in range(1, 6):
        raise InvalidMenuChoiceError("Invalid menu input. Enter a number from 1 to 5.")
    return choice


def create_request(service):
    employee_name = input("Enter Employee Name: ").strip()
    issue = input("Enter Issue: ").strip()
    priority = input("Enter Priority: ").strip()
    created = service.create_request(employee_name, issue, priority)
    print(f"Service Request {created.request_id} created successfully.")


def view_requests(service):
    requests = service.view_requests()
    if not requests:
        print("No service requests found.")
        return
    for request in requests:
        print_request(request)


def search_request(service):
    request_id = input("Enter Request ID: ").strip()
    try:
        print_request(service.search_request(request_id))
    except RequestNotFoundError:
        print("Request not found")
    except ValueError as error:
        print(f"Error: {error}")


def resolve_request(service):
    request_id = input("Enter Request ID: ").strip()
    try:
        resolved = service.resolve_request(request_id)
        print(f"Request {resolved.request_id} resolved successfully.")
    except RequestNotFoundError:
        print("Request not found")
    except RequestAlreadyResolvedError as error:
        print(f"Error: {error}")
    except ValueError as error:
        print(f"Error: {error}")

def main():
    try:
        repository = FileRepository(PROJECT_ROOT / "data" / "requests.json")
        service = RequestService(repository)
    except (ValueError, OSError) as error:
        print(f"Could not load service requests: {error}")
        return

    while True:
        print("\nSMART SERVICE DESK SYSTEM")
        print("1. Create Service Request")
        print("2. View All Requests")
        print("3. Search Request")
        print("4. Resolve Request")
        print("5. Exit")

        try:
            choice = get_menu_choice()
        except InvalidMenuChoiceError as error:
            print(f"Error: {error}")
            continue

        if choice == 1:
            try:
                create_request(service)
            except InvalidPriorityError as error:
                print(f"Error: {error}")
            except ValueError as error:
                print(f"Error: {error}")
        elif choice == 2:
            view_requests(service)
        elif choice == 3:
            search_request(service)
        elif choice == 4:
            resolve_request(service)
        elif choice == 5:
            print("Goodbye.")
            break

if __name__ == "__main__":
    main()
