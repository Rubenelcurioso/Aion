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

2. **Install JavaScript dependencies**
   ```bash
   npm install
   ```

3. **Start backend containers**
   ```bash
   docker-compose up -d
   ```

4. **Launch the Django API**
   ```bash
   source venv/bin/activate
   cd aionapi
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

5. **Build or run the UI**
   ```bash
   cd ../aionapp
   quasar build     # For production
   quasar dev       # For development
   ```

> _This setup will be further streamlined in upcoming releases._

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
- [LinkedIn](https://www.linkedin.com/in/rubenelcurioso)
- [Blog](https://rubenelcurioso.github.io)
