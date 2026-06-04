class ApplicationError(Exception):
    pass


class GroqConnectionError(ApplicationError):
    pass


class InvalidLLMResponseError(ApplicationError):
    pass


class InputValidationError(ApplicationError):
    pass
