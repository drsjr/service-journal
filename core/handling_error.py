from model.error_model import ApiError
from fastapi import HTTPException, status


def http_422_incorrect_email_or_password() -> HTTPException:
    return HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=ApiError(
                    code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                    message="Your email or password is invalid", 
                    short="incorrect_credential").dict(),
                headers={"WWW-Authenticate": "Bearer"}
            )

def http_401_expired_token_access() -> HTTPException:
    return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ApiError(
                    code=status.HTTP_401_UNAUTHORIZED, 
                    message="expired token access", 
                    short="credential_expired").dict(),
            headers={"WWW-Authenticate": "Bearer"})

def http_404_object_not_found(message: str, short: str) -> HTTPException:
    return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ApiError(
                    code=status.HTTP_404_NOT_FOUND, 
                    message=message, 
                    short=short).dict(),
            headers={"WWW-Authenticate": "Bearer"})
