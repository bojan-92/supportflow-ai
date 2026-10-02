class AIServiceError(Exception):
    code = "AI_SERVICE_ERROR"
    message = "AI service is temporarily unavailable."


class AIAuthenticationError(AIServiceError):
    code = "AI_AUTHENTICATION_ERROR"
    message = "AI service configuration is invalid."


class AIRateLimitError(AIServiceError):
    code = "AI_RATE_LIMITED"
    message = "AI service is temporarily busy. Please try again."


class AITimeoutError(AIServiceError):
    code = "AI_TIMEOUT"
    message = "AI processing timed out. Please try again."


class AIConnectionError(AIServiceError):
    code = "AI_CONNECTION_ERROR"
    message = "Could not connect to the AI service."


class AIInvalidResponseError(AIServiceError):
    code = "AI_INVALID_RESPONSE"
    message = "AI service returned an invalid response."


class AIUpstreamError(AIServiceError):
    code = "AI_UPSTREAM_ERROR"
    message = "AI service is temporarily unavailable."