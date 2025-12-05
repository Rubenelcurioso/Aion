## Development Conventions

### Code Style

#### Variable Naming (Hungarian Notation)
- Use Hungarian notation with data type prefix followed by variable name in snake_case
- Format: `{type_prefix}_{variable_name}`
- Examples:
  - `b_auth_status` (boolean)
  - `str_username` (string)
  - `int_user_id` (number/integer)
  - `flt_progress` (float)
  - `arr_tasks` (array)
  - `obj_user_data` (object)

#### Function Naming
- Use infinitive and imperative verbs like `get`, `set`, `update`, `create`, `delete`, `validate`, etc.
- Follow camelCase for function names
- Examples:
  - `get_user_info()`
  - `set_auth_token()`
  - `validate_input()`
  - `create_project()`

#### Bracket Placement
- Opening bracket (`{`) should be on the same line as the function declaration
- Closing bracket (`}`) should be on a new line by itself
- Example:
```javascript
function get_user_info(str_user_id) {
  // function body
  return obj_user_data;
}
```

### Git Workflow

#### Branch Naming Convention
- Use the format: `{type}/{short-description}`
- Types: `feature`, `bugfix`, `hotfix`, `chore`, `docs`, `test`, `refactor`
- Examples:
  - `feature/user-authentication`
  - `bugfix/login-validation`
  - `docs/update-readme`
  - `chore/update-dependencies`

#### Commit Messages
- Use conventional commits format: `type(scope): description`
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
- Examples:
  - `feat(auth): add user registration`
  - `fix(api): resolve null pointer exception`
  - `docs(readme): update installation instructions`
  - `refactor(utils): optimize helper functions`

#### Pull Requests
- Create PRs from feature branches to the `main` branch
- Include a clear description of changes and related issue numbers
- Request reviews from at least one team member
- Ensure all tests pass before merging

### Project Structure
- `/aionapi` - Backend API application
- `/aionapp` - Frontend application
- `/diagrams` - Architecture and design diagrams
- `/docs` - Documentation files

### Issue Tracking
- Use GitHub Issues for task management
- Follow the template when creating new issues
- Assign appropriate labels: `bug`, `feature`, `enhancement`, `documentation`
- Set priority levels: `low`, `medium`, `high`, `critical`

### Code Review Process
- All code changes require peer review
- Reviewers should check for:
  - Code quality and adherence to conventions
  - Proper testing coverage
  - Security considerations
  - Performance implications
- Use constructive feedback and provide suggestions for improvement

### Testing Guidelines
- Write unit tests for all new functionality
- Follow the AAA pattern: Arrange, Act, Assert
- Maintain high test coverage (>80% recommended)
- Run tests before pushing code to ensure nothing is broken

### Communication
- Use GitHub Discussions for general project discussions
- Use GitHub Issues for bug reports and feature requests
- Use pull request comments for code-specific discussions
- Maintain a professional and respectful tone in all communications
