from fastapi.security import APIKeyHeader

auth_scheme = APIKeyHeader(name="Authorization")
