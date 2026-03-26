# Frontend Directory Configuration

This file provides frontend-specific context and conventions for Windsurf Cascade.

---

## Frontend Technology Stack

**[PROJECT-SPECIFIC]** Define frontend-specific technologies:

* **Framework**: [e.g., React 18, Vue 3, Angular 16, Svelte, Solid]
* **Language**: [e.g., TypeScript 5.x, JavaScript ES2022]
* **Build tool**: [e.g., Vite, Webpack, Turbopack, esbuild]
* **Package manager**: [e.g., pnpm, npm, yarn]
* **UI library**: [e.g., shadcn/ui, Material-UI, Ant Design, Chakra UI]

---

## Component Structure and Conventions

**[PROJECT-SPECIFIC]** Define component organization:

### Component Organization

* **Component location**: [e.g., src/components/, frontend/src/components/]
* **Component naming**: [e.g., PascalCase for files, kebab-case for directories]
* **Component types**: [e.g., "Presentational vs Container", "Smart vs Dumb", "Page vs Component"]

### File Structure

```
[EXAMPLE - REPLACE WITH YOUR PATTERN]
components/
├── Button/
│   ├── Button.tsx
│   ├── Button.test.tsx
│   ├── Button.stories.tsx
│   └── index.ts
└── UserProfile/
    ├── UserProfile.tsx
    ├── UserProfile.test.tsx
    ├── UserProfile.module.css
    └── index.ts
```

### Component Patterns

* **Prefer**: [e.g., "Functional components", "Composition over inheritance"]
* **Avoid**: [e.g., "Class components unless necessary", "Deeply nested components"]
* **Props**: [e.g., "Use TypeScript interfaces", "Destructure props", "Provide default values"]

---

## State Management

**[PROJECT-SPECIFIC]** Define state management patterns:

### State Management Tool

* **Tool**: [e.g., Redux Toolkit, Zustand, Jotai, Pinia, NgRx]
* **Store location**: [e.g., src/store/, src/state/]
* **Store structure**: [e.g., "Feature-based slices", "Domain-based modules"]

### State Organization

* **Local state**: [e.g., "Use useState for component-local state"]
* **Shared state**: [e.g., "Use context for theme/auth", "Use store for app-wide state"]
* **Server state**: [e.g., "Use React Query/TanStack Query", "Use SWR", "Use Apollo Client"]

### State Updates

* **Immutability**: [e.g., "Use Immer", "Spread operators", "Immutable patterns"]
* **Async actions**: [e.g., "Use thunks", "Use async actions", "Use mutations"]

---

## Routing

**[PROJECT-SPECIFIC]** Define routing conventions:

### Router

* **Router library**: [e.g., React Router v6, Vue Router, Angular Router]
* **Route definition location**: [e.g., src/routes/, src/router/]
* **Route structure**: [e.g., "Nested routes", "Flat routes", "File-based routing"]

### Route Protection

* **Auth guards**: [e.g., "ProtectedRoute component", "Route guards", "Navigation guards"]
* **Redirect logic**: [e.g., "Redirect to /login if unauthenticated"]

---

## Styling Conventions

**[PROJECT-SPECIFIC]** Define styling approach:

### Styling Method

* **Approach**: [e.g., Tailwind CSS, CSS Modules, Styled Components, Emotion, SCSS]
* **Config file**: [e.g., tailwind.config.js, postcss.config.js]
* **Global styles**: [e.g., src/styles/globals.css, src/index.css]

### Styling Guidelines

* **Class naming**: [e.g., "BEM methodology", "Utility-first", "Component-scoped"]
* **Responsive design**: [e.g., "Mobile-first", "Desktop-first", "Breakpoints: sm, md, lg, xl"]
* **Theme**: [e.g., "Use CSS variables", "Use theme provider", "Support dark mode"]

---

## API Integration

**[PROJECT-SPECIFIC]** Define API interaction patterns:

### API Client

* **HTTP client**: [e.g., fetch, axios, ky]
* **API client location**: [e.g., src/api/, src/services/]
* **Base URL**: [e.g., "Use environment variable", "VITE_API_BASE_URL"]

### Data Fetching

* **Library**: [e.g., React Query, SWR, RTK Query, Apollo Client]
* **Caching strategy**: [e.g., "Cache for 5 minutes", "Stale-while-revalidate"]
* **Error handling**: [e.g., "Show error toast", "Error boundary", "Retry logic"]

### Authentication

* **Token storage**: [e.g., "localStorage", "sessionStorage", "HTTP-only cookies"]
* **Token refresh**: [e.g., "Automatic refresh", "Refresh on 401"]
* **Interceptors**: [e.g., "Add auth header", "Handle token expiration"]

---

## Form Handling

**[PROJECT-SPECIFIC]** Define form patterns:

### Form Library

* **Library**: [e.g., React Hook Form, Formik, VeeValidate, Angular Forms]
* **Validation**: [e.g., Zod, Yup, Joi, class-validator]

### Form Patterns

* **Controlled vs uncontrolled**: [e.g., "Prefer controlled components", "Use uncontrolled for performance"]
* **Validation timing**: [e.g., "On blur", "On submit", "Real-time"]
* **Error display**: [e.g., "Inline errors", "Toast notifications", "Error summary"]

---

## Testing Conventions

**[PROJECT-SPECIFIC]** Define frontend testing patterns:

### Unit Tests

* **Location**: [e.g., tests/unit/frontend/, frontend/src/components/**/*.test.tsx]
* **Testing library**: [e.g., React Testing Library, Vue Test Utils, Jest, Vitest]
* **What to test**: [e.g., "Component rendering", "User interactions", "State changes"]

### Integration Tests

* **Location**: [e.g., tests/integration/frontend/]
* **Scope**: [e.g., "Multi-component interactions", "API integration", "Routing"]

### E2E Tests

* **Location**: [e.g., tests/e2e/, e2e/]
* **Framework**: [e.g., Playwright, Cypress, Puppeteer]
* **Test scenarios**: [e.g., "Critical user flows", "Authentication", "Checkout process"]

---

## Performance Optimization

**[PROJECT-SPECIFIC]** Define performance guidelines:

### Bundle Size

* **Target**: [e.g., "< 200KB initial bundle", "< 500KB total"]
* **Code splitting**: [e.g., "Route-based splitting", "Component lazy loading"]
* **Tree shaking**: [e.g., "Import only what you need", "Use named imports"]

### Runtime Performance

* **Rendering**: [e.g., "Use React.memo", "Use useMemo/useCallback", "Avoid unnecessary re-renders"]
* **Images**: [e.g., "Use next/image", "Lazy load images", "Use WebP format"]
* **Fonts**: [e.g., "Preload critical fonts", "Use font-display: swap"]

### Performance Monitoring

* **Tools**: [e.g., "Lighthouse", "Web Vitals", "Bundle analyzer"]
* **Metrics**: [e.g., "LCP < 2.5s", "FID < 100ms", "CLS < 0.1"]

---

## Accessibility (a11y)

**[PROJECT-SPECIFIC]** Define accessibility standards:

### Accessibility Requirements

* **Standard**: [e.g., WCAG 2.1 Level AA]
* **Testing**: [e.g., "axe DevTools", "WAVE", "Lighthouse accessibility audit"]

### Accessibility Practices

* **Semantic HTML**: [e.g., "Use proper heading hierarchy", "Use semantic elements"]
* **ARIA**: [e.g., "Use ARIA labels", "Use ARIA roles when necessary", "Avoid ARIA when native HTML works"]
* **Keyboard navigation**: [e.g., "All interactive elements keyboard accessible", "Visible focus indicators"]
* **Screen readers**: [e.g., "Test with NVDA/JAWS", "Provide alt text for images"]

---

## Internationalization (i18n)

**[PROJECT-SPECIFIC]** Define i18n approach if applicable:

### i18n Library

* **Library**: [e.g., react-i18next, vue-i18n, @angular/localize]
* **Translation files**: [e.g., src/locales/, public/locales/]
* **Supported languages**: [e.g., en, es, fr, de, ja, zh]

### i18n Practices

* **Text extraction**: [e.g., "Use translation keys", "Never hardcode user-facing text"]
* **Pluralization**: [e.g., "Use library plural rules"]
* **Date/number formatting**: [e.g., "Use Intl API", "Use library formatters"]

---

## Build and Deployment

**[PROJECT-SPECIFIC]** Define build configuration:

### Build Configuration

* **Build command**: [e.g., `npm run build`, `pnpm build`]
* **Output directory**: [e.g., dist/, build/]
* **Environment variables**: [e.g., VITE_API_URL, NEXT_PUBLIC_API_URL]

### Development Server

* **Dev command**: [e.g., `npm run dev`, `pnpm dev`]
* **Dev port**: [e.g., 3000, 5173]
* **Hot reload**: [e.g., "Enabled by default", "Fast Refresh"]

---

## Code Quality

**[PROJECT-SPECIFIC]** Define frontend code quality tools:

### Linting

* **ESLint config**: [e.g., .eslintrc.js, eslint.config.js]
* **Rules**: [e.g., "Airbnb style guide", "Standard", "Custom rules"]
* **Lint command**: [e.g., `npm run lint`, `pnpm lint`]

### Type Checking

* **TypeScript config**: [e.g., tsconfig.json]
* **Strict mode**: [e.g., "Enabled", "Disabled"]
* **Type check command**: [e.g., `npm run typecheck`, `tsc --noEmit`]

---

## Additional Frontend Resources

**[PROJECT-SPECIFIC]** Link to frontend-specific documentation:

* **Component library**: [e.g., Storybook at /storybook]
* **Design system**: [e.g., docs/design-system.md]
* **Frontend architecture**: [e.g., docs/frontend-architecture.md]
