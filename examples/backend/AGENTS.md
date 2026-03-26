# Backend Directory Configuration

This file provides backend-specific context and conventions for Windsurf Cascade.

---

## Backend Technology Stack

**[PROJECT-SPECIFIC]** Define backend-specific technologies:

* **Framework**: [e.g., FastAPI, Flask, Django, Express, Spring Boot, Axum]
* **API style**: [e.g., REST, GraphQL, gRPC]
* **Database**: [e.g., PostgreSQL, MySQL, MongoDB, Redis]
* **ORM/Query builder**: [e.g., SQLAlchemy, Prisma, Hibernate, Diesel]
* **Authentication**: [e.g., JWT, OAuth2, Session-based]

---

## API Design Conventions

**[PROJECT-SPECIFIC]** Define API design patterns:

### Endpoint Structure

* **Base path**: [e.g., /api/v1/]
* **Naming convention**: [e.g., plural nouns, kebab-case, snake_case]
* **Versioning strategy**: [e.g., URL versioning, header versioning]

### Request/Response Format

* **Request body format**: [e.g., JSON, Protocol Buffers]
* **Response envelope**: [e.g., `{"data": ..., "error": null}`, direct response]
* **Error format**: [e.g., RFC 7807 Problem Details, custom error schema]
* **Pagination**: [e.g., offset/limit, cursor-based]

### HTTP Status Codes

* **Success**: 200 OK, 201 Created, 204 No Content
* **Client errors**: 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 422 Unprocessable Entity
* **Server errors**: 500 Internal Server Error, 503 Service Unavailable

---

## Database Interaction Rules

**[PROJECT-SPECIFIC]** Define database conventions:

### Schema Management

* **Migration tool**: [e.g., Alembic, Flyway, Liquibase, sqlx migrate]
* **Migration location**: [e.g., migrations/, db/migrations/]
* **Create migration**: [e.g., `alembic revision --autogenerate -m "description"`, `sqlx migrate add description`]
* **Apply migrations**: [e.g., `alembic upgrade head`, `sqlx migrate run`]

### Query Patterns

* **Prefer**: [e.g., "Use ORM for simple queries", "Use raw SQL for complex queries"]
* **Avoid**: [e.g., "N+1 queries", "SELECT * without filtering"]
* **Transaction handling**: [e.g., "Use context managers", "Explicit transaction boundaries"]

### Connection Management

* **Connection pooling**: [e.g., "Use connection pool with max 20 connections"]
* **Connection lifecycle**: [e.g., "Request-scoped connections", "Long-lived pool"]

---

## Service Layer Patterns

**[PROJECT-SPECIFIC]** Define service organization:

### Service Structure

* **Service location**: [e.g., src/services/, backend/services/]
* **Service naming**: [e.g., UserService, user_service.py]
* **Service responsibility**: [e.g., "Business logic only", "Orchestration layer"]

### Dependency Injection

* **DI pattern**: [e.g., "Constructor injection", "FastAPI Depends", "Spring @Autowired"]
* **Service lifecycle**: [e.g., "Singleton", "Request-scoped", "Transient"]

---

## Authentication and Authorization

**[PROJECT-SPECIFIC]** Define auth patterns:

### Authentication

* **Auth mechanism**: [e.g., JWT tokens, API keys, OAuth2]
* **Token storage**: [e.g., HTTP-only cookies, Authorization header]
* **Token expiration**: [e.g., 1 hour access token, 7 day refresh token]

### Authorization

* **Permission model**: [e.g., RBAC, ABAC, simple role checks]
* **Permission checking**: [e.g., Decorator-based, middleware-based]
* **Admin endpoints**: [e.g., "Require admin role", "Require specific permissions"]

---

## Error Handling

**[PROJECT-SPECIFIC]** Define error handling patterns:

### Exception Hierarchy

* **Base exception**: [e.g., ApplicationError, DomainException]
* **Specific exceptions**: [e.g., NotFoundError, ValidationError, UnauthorizedError]

### Error Logging

* **Logger**: [e.g., Python logging, Winston, Log4j]
* **Log levels**: [e.g., DEBUG for development, INFO for production, ERROR for failures]
* **Sensitive data**: [e.g., "Never log passwords or tokens", "Redact PII"]

---

## Testing Conventions

**[PROJECT-SPECIFIC]** Define backend testing patterns:

### Unit Tests

* **Location**: [e.g., tests/unit/backend/, backend/tests/unit/]
* **Mocking strategy**: [e.g., "Mock external dependencies", "Use test doubles for database"]
* **Test naming**: [e.g., test_service_method_scenario, testServiceMethodScenario]

### Integration Tests

* **Location**: [e.g., tests/integration/backend/, backend/tests/integration/]
* **Database**: [e.g., "Use test database", "Use in-memory database", "Use Docker container"]
* **External services**: [e.g., "Mock external APIs", "Use test instances"]

### API Tests

* **Location**: [e.g., tests/api/, backend/tests/api/]
* **Test client**: [e.g., TestClient, supertest, RestAssured]
* **Authentication**: [e.g., "Use test tokens", "Create test users"]

---

## Performance Considerations

**[PROJECT-SPECIFIC]** Define performance guidelines:

### Response Time Targets

* **Simple queries**: [e.g., < 100ms]
* **Complex queries**: [e.g., < 500ms]
* **Batch operations**: [e.g., < 2s]

### Optimization Strategies

* **Caching**: [e.g., Redis for frequently accessed data]
* **Indexing**: [e.g., "Index foreign keys", "Index frequently queried columns"]
* **Query optimization**: [e.g., "Use EXPLAIN to analyze queries", "Avoid N+1 problems"]

---

## Security Guidelines

**[PROJECT-SPECIFIC]** Define security practices:

### Input Validation

* **Validation library**: [e.g., Pydantic, Joi, Hibernate Validator]
* **Validation location**: [e.g., "At API boundary", "In request models"]
* **Sanitization**: [e.g., "Sanitize user input", "Escape SQL", "Validate file uploads"]

### SQL Injection Prevention

* **Use**: [e.g., "Parameterized queries", "ORM query builders"]
* **Avoid**: [e.g., "String concatenation for SQL", "Raw user input in queries"]

### Secrets Management

* **Storage**: [e.g., "Environment variables", "AWS Secrets Manager", "HashiCorp Vault"]
* **Never**: [e.g., "Commit secrets to git", "Log secrets"]

---

## Deployment and Configuration

**[PROJECT-SPECIFIC]** Define deployment specifics:

### Environment Configuration

* **Config source**: [e.g., Environment variables, .env files, config service]
* **Required vars**: [e.g., DATABASE_URL, SECRET_KEY, API_KEY]
* **Optional vars**: [e.g., LOG_LEVEL, CACHE_TTL]

### Health Checks

* **Health endpoint**: [e.g., /health, /api/health]
* **Readiness endpoint**: [e.g., /ready, /api/ready]
* **Checks included**: [e.g., Database connectivity, external service availability]

---

## Additional Backend Resources

**[PROJECT-SPECIFIC]** Link to backend-specific documentation:

* **API documentation**: [e.g., /docs (Swagger), /graphql (GraphQL Playground)]
* **Database schema**: [e.g., docs/database-schema.md]
* **Service architecture**: [e.g., docs/backend-architecture.md]
