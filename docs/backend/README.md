# Backend API Documentation

The Aion backend is built using Django and Django Rest Framework (DRF). It provides RESTful APIs for managing users, businesses, teams, projects, roles, and tasks. Authentication is handled using Simple JWT tokens.

## Architecture & Conventions

- **Framework**: Django REST Framework.
- **Authentication**: JSON Web Tokens (JWT) using `rest_framework_simplejwt`.
- **Database**: PostgreSQL (defined in Docker setup).
- **Responses**: standard JSON formatting, often paired with standard HTTP status codes (`200 OK`, `201 CREATED`, `400 BAD REQUEST`, `403 FORBIDDEN`, `404 NOT FOUND`).

---

## Models Overview (`aionapi/api/models.py`)

### User
Custom User model extending `AbstractBaseUser`.
- `username`: Unique username, alphanumeric.
- `email`: Unique email.
- `fullname`: User's full name, letters only.
- `birthday`: Minimum age validation (14+).
- `picture`: Binary data for user avatar.

### Business
Represents an organization or company.
- `name`: Unique business name.
- `owner`: Foreign key to `User`.

### Team
Represents a group of employees within a business.
- `business`: Foreign key to `Business`.
- `name`: Team name.

### Employee
Represents a user's association with a business, optionally within a specific team.
- `user`: Foreign key to `User`.
- `business`: Foreign key to `Business`.
- `team`: Optional foreign key to `Team`.

### Project
Projects that belong to a business or user.
- `name`: Project name.
- `owner`: Foreign key to `User`.
- `business`: Foreign key to `Business`.
- `progress`: Auto-calculated completion percentage.
- Dates: `start_date`, `end_date`.

### Task
Work items within a project.
- `project`: Foreign key to `Project`.
- `status`: `TODO`, `IN_PROGRESS`, `DONE`.
- `priority`: `L` (Low), `M` (Medium), `H` (High).
- Assignments: `user_assigned` or `team_assigned`.

### Role
Defines permission levels.
- `name`: E.g., Guest, Admin.
- `perm`: Integer representing permission level.

### UserProjectRole
Many-to-Many mapping for users to projects with a specific role.

---

## API Endpoints Overview (`aionapi/api/views.py`)

Most endpoints require the user to be authenticated via JWT (Bearer Token).

### Authentication & Users
- `POST /register`: Register a new user (`UserRegistration`).
- `POST /login`: Log in to receive JWT tokens (`UserLogin`).
- `POST /logout`: Blacklist refresh token (`UserLogout`).
- `GET /user/<id>`: Get user details (`UserDetail`).
- `GET /search/username/<username>` or `/employees/username/<username>`: Search users (`UsernameSearch`).

### Businesses (`BusinessList`)
- `GET /businesses` or `/businesses/<id>`: List businesses where user is an employee, or specific business details.
- `POST /businesses`: Create a new business (requester becomes owner).
- `PUT /businesses`: Update business details (owner only).
- `DELETE /businesses/<id>`: Delete business (owner only).

### Teams (`TeamList`)
- `GET /businesses/<id>/teams` or `/businesses/<id>/teams/<team_id>`: List teams or get specific team.
- `POST /teams`: Create a team (owner only).
- `PUT /teams`: Update team (owner only).
- `DELETE /businesses/<id>/teams/<team_id>`: Delete team (owner only).

### Employees (`EmployeeList`)
- `GET /businesses/<id>/employees` or `/businesses/<id>/teams/<team_id>/employees`: List employees.
- `POST /employees`: Add employee to business (owner only).
- `PUT /employees`: Update employee team assignment.
- `DELETE /businesses/<id>/employees/<username>`: Remove employee (owner only).

### Projects (`ProjectList`)
- `GET /projects` or `/projects/<id>`: List user's projects or get details including progress.
- `POST /projects`: Create project (requester becomes owner).
- `PUT /projects`: Update project (owner only).
- `DELETE /projects/<id>`: Delete project (owner only).

### Project Roles & Users (`UserProjectRoleList`, `UserProjects`, `ProjectUsers`)
- `GET /projects/<id>/roles`: List user roles in a project.
- `POST /projects/roles`: Add user to project (requires permission `> 31`).
- `PUT /projects/roles`: Modify user role (requires higher perm than target).
- `DELETE /projects/<id>/users/<username>`: Remove user from project (requires higher perm).
- `GET /users/<id>/projects`: Get all projects for a specific user.
- `GET /projects/<id>/users`: Get all users and their roles for a project.

### Tasks (`TaskList`)
- `GET /projects/<id>/tasks`: List project tasks.
- `GET /tasks/<id>`: Get specific task details.
- `GET /users/<id>/tasks`: List user's active tasks.
- `GET /users/<id>/team/tasks`: List user's team active tasks.
- `POST /tasks`: Create a task (requires permission `> 7`).
- `PUT /tasks/<id>`: Update a task (requires permission `> 7`).
- `DELETE /tasks/<id>`: Delete a task (requires permission `> 7`).

### Analytics & Stats (`Stats`)
- `GET /projects/<id>/stats`: General stats (total, done, pending).
- `GET /projects/<id>/stats/priority/`: Task count by priority (H, M, L).
- `GET /projects/<id>/stats/status/`: Task count by status (DONE, IN_PROGRESS, TODO).
- `GET /projects/<id>/stats/workload/`: Task count grouped by assigned user.

---

## Guidelines for Developers
1. Follow Hungarian notation as detailed in `COLLABORATION.md`.
2. Ensure new endpoints check for `JWTAuthentication` and `IsAuthenticated` unless specifically meant to be public.
3. Validate permissions carefully inside the views. Typically, roles are checked against the `UserProjectRole.perm` field or business `owner`.
4. Run tests with `python manage.py test` locally or `docker-compose exec api python manage.py test`.