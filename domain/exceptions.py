class DuplicateRequestIdError(Exception):
    pass
    #Custom exception for when a request ID has already been  in use


class RequestNotFoundError(Exception):
    pass
    #Custom exception when a request ID cannot be found 


class InvalidPriorityError(Exception):
    pass
    #Raised when a priority is not low/med/high


class RequestAlreadyResolvedError(Exception):
    pass
    #Raised when an already resolved request is resolved again


class InvalidMenuChoiceError(Exception):
    pass
    #when  menu choice is not between 1 to 5
