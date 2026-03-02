class UserDomainError(Exception):
    """
    Base exception for users domain.
    """


class UserAlreadyExistsError(UserDomainError):
    """
    Raised when user with given credentials already exists.
    """


class InvalidCredentialsError(UserDomainError):
    """
    Raised when authentication fails.
    """


class UserInactiveError(UserDomainError):
    """
    Raised when inactive user tries to authenticate.
    """
