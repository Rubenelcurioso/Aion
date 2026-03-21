# Frontend Web Application Documentation

The Aion frontend is built using **Vue.js 3** and the **Quasar Framework**. It acts as the primary user interface for users to manage tasks, collaborate with teams, and view progress on projects.

## Architecture & Tooling
- **Framework:** Vue 3 (Composition API) with Quasar Framework.
- **State Management:** Pinia (assumed, typical with Quasar) or Vue's reactive composables.
- **Routing:** Vue Router.
- **Styling:** Tailwind CSS (assumed based on `postcss.config.js`) + Quasar utility classes.
- **Package Manager:** npm or yarn.
- **Linting:** ESLint (`.eslintrc.cjs`).

---

## Directory Structure Overview (`aionapp/`)
- `public/`: Static files that don't need Webpack processing.
- `src/`: The main application source code.
  - `components/`: Reusable Vue components for various UI elements.
  - `pages/`: View components mapped to application routes.
  - `router/`: Vue Router configuration.
  - `stores/`: State management.
  - `css/` & `assets/`: Styling and images/fonts.

---

## Key Components (`src/components/`)
Components are primarily designed to be modular and reusable blocks of UI.

### General & Layout Elements
- `MainDrawer.vue` / `MainFooter.vue`: Layout components for side navigation and footer.
- `LandHeader.vue` / `DrawerButton.vue`: Header and navigation buttons.
- `AvatarMenu.vue` / `NotificationBell.vue`: User-related interactive UI elements in the app bar.
- `BadgeTypes.vue`: Displays badges, often for statuses or roles.

### Project & Business Management
- `ProjectEditCard.vue` / `ProjectInfo.vue` / `ProjectList.vue` / `ProjectsItem.vue`: Managing project details and listings.
- `BusinessItem.vue`: Component for displaying individual businesses.
- `UserProjectManagement.vue` / `NewUserProject.vue`: Managing users within projects.

### Task Management
- `TaskCreationCard.vue` / `TaskEditCard.vue`: Forms for adding or editing tasks.
- `TaskList.vue` / `TaskTable.vue`: Display modes for task lists.

### Teams & Employees
- `TeamList.vue` / `TeamEditCard.vue` / `NewTeam.vue`: Viewing, editing, and creating teams.
- `NewEmployee.vue`: Component for adding employees to businesses/teams.

### Visualizations & UI Sections
- `ApexCharts.vue`: Wrapper/integration for rendering dashboard charts.
- `AuthForm.vue`: Generic form wrapper for authentication views.
- `HeroSection.vue` / `ImageSection.vue` / `HelpUsSection.vue`: Promotional and visual segments typically seen on landing pages.

---

## Key Pages (`src/pages/`)
Pages map directly to application routes and act as the main views.

### Public & Informational
- `LandscapePage.vue` (Landing Page).
- `AboutUsPage.vue` / `ContactPage.vue` / `OurMissionPage.vue` / `PrivacyPoliticsPage.vue` / `SecurityBestPracticesPage.vue`.
- `ErrorNotFound.vue`: Custom 404 page.

### Authentication
- `LoginPage.vue`: User sign in.
- `RegisterPage.vue`: User sign up.

### App Core Views
- `HomeUser.vue`: The main authenticated dashboard showing an overview for the user.
- `ProjectPage.vue` / `NewProject.vue`: Full page views for specific project details and project creation.
- `BusinessPage.vue` / `NewBusiness.vue`: Full page views for business details and business creation.

---

## Development Guidelines
1. **Naming:** Stick to PascalCase for component file names (e.g., `TaskList.vue`).
2. **Setup:** Use `<script setup>` in Vue Single-File Components (SFCs) as the standard approach.
3. **Styles:** Leverage Quasar's pre-built classes and components before writing custom CSS, to ensure consistency.
4. **Hungarian Notation:** Apply the same data typing conventions defined in `COLLABORATION.md` for variables (`b_auth_status`, `arr_tasks`, etc.).
5. **Running Locally:** Navigate to `aionapp/`, `npm install` and then `npm run dev` or `quasar dev`.