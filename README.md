# Aion

A web application designed for individuals and teams to organize tasks, collaborate, and monitor progress with a secure, free, and friendly interface.

## Table of Contents
- [Highlights](#highlights)
- [Installation](#installation)
- [Development Workflow](#development-workflow)
- [Roadmap](#roadmap)
- [License](#license)
- [Contact](#contact)

## Highlights
- ✅ **User-friendly interface** that keeps task creation, scheduling, and tracking intuitive.
- 🛡️ **Augmented security measures** to ensure data protection across teams.
- 🧭 **Task prioritization and categorization**.
- 📊 **Progress tracking and reporting** with clear visuals and status indicators.
- 🆓 **Free and open-source**.

## Installation

### Requirements
- Docker & Docker Compose
- Python 3.9+
- Node.js
- Git

### Steps
1. **Clone the repository**
   ```bash
   git clone https://github.com/Rubenelcurioso/Aion.git
   cd Aion
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your desired configuration
   ```

3. **Start the application with Docker Compose**
   ```bash
   docker-compose up --build -d
   ```

4. **Initialize the Database**
   ```bash
   docker-compose exec api python manage.py migrate
   docker-compose exec api python manage.py createsuperuser
   ```

5. **Access the Application**
   - **Frontend UI:** [http://localhost:9000](http://localhost:9000) (or the `NODE_PORT` specified in `.env`)
   - **Backend API:** [http://localhost:8000](http://localhost:8000) (or the `API_PORT` specified in `.env`)
   - **pgAdmin:** [http://localhost:5050](http://localhost:5050) (or the `PGADMIN_PORT` specified in `.env`)

> _For local development without Docker, refer to the `aionapi/` and `aionapp/` directories directly._

## Development Workflow
- **Feature branches**: Use descriptive names like `feat/notifications` or `fix/auth`.
- **Linters & tests**: Run `npm run lint`, `npm test`, or any project-specific checks before committing.
- **Commits**: Keep them focused and follow Conventional Commits (e.g., `feat: add task batching`).
- **Pull requests**: Provide testing steps, affected areas, and screenshots if UI changes.

## Roadmap
- [x] Refactor structure to improve collaboration and workflow efficiency.
- [ ] Add comprehensive documentation.
- [ ] Establish automated testing pipelines.
- [ ] Redesign the UI with a more engaging experience.
- [ ] Build better collaboration capabilities for enterprise teams.

## License
GNU GENERAL PUBLIC LICENSE Version 3

## Contact
- [GitHub](https://github.com/rubenelcurioso)
- [LinkedIn](https://www.linkedin.com/in/rub%C3%A9n-rosales-01b114356/)
- [Blog](https://rubenelcurioso.github.io)
