# print("this is main.py")
from pathlib import Path
from application.request_service import RequestService
from domain.exceptions import InvalidMenuChoiceError, InvalidPriorityError, RequestAlreadyResolvedError, RequestNotFoundError
from infrastructure.file_repository import FileRepository




if __name__ == "__main__":
    main()
