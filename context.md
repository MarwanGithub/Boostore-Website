### Project Context: "Isma3il Book Website"

**Project:** A Django-based e-commerce website for a small, used-book bookstore. The project is hosted on Render's free tier.

**Core Technologies:**
*   **Backend:** Django
*   **Frontend:** HTML, Bootstrap, and vanilla JavaScript (for AJAX interactions).
*   **Database:** PostgreSQL on Supabase free use, SQLite for local development.
*   **Static & Media Files:** `django-cloudinary-storage` is used to handle all static and media files in the production environment on Render.
*   **Admin Theme:** `django-jazzmin` is used for an enhanced admin interface.

**Key Architectural Patterns & Features:**
*   **Session-Based Cart:** The shopping cart is implemented entirely in the user's session (`bookstore/cart.py`) to be lightweight and avoid database writes for anonymous users. It's made globally available in all templates via a context processor.
*   **Asynchronous UI:** The cart functionality ("Add to Cart", quantity updates) is built with the JavaScript `fetch` API for AJAX calls. This prevents full page reloads. The quantity controls provide instant user feedback by disabling buttons and showing a spinner until the server confirms the update.
*   **"Contact to Order" Checkout:** Instead of a complex checkout and payment system, the site uses a simplified process where the user is directed to a page that generates pre-filled WhatsApp and Messenger links containing their cart's contents.
*   **Unique Item Logic:** On the home and book list pages, the "Add to Cart" button is conditionally hidden for books that are already in the user's cart, preventing attempts to purchase a unique used book more than once.

**Deployment & Configuration:**
*   **Hosting:** The site is deployed on Render. The configuration in `settings.py` uses the `RENDER` environment variable to differentiate between production and local environments.
*   **Environment Variables:** A custom `Germaneya.env` file stores secrets and configuration, which is loaded via `python-dotenv` and is included in `.gitignore`.
*   **Critical `settings.py` Logic:** The settings file dynamically configures `DEBUG`, `ALLOWED_HOSTS`, and storage backends based on the `IS_RENDER` flag, which is crucial for both local development and production deployment to work correctly.
*   **Local Media Files:** For local development, the project's root `urls.py` is configured to serve user-uploaded media files when `DEBUG=True`.

This project is about a small bookstore that presents books to the users. The books should be added by an admin from an admin panel. Books have categories and will belong to a category. For now only the admin panel will require a log in and we will use the django admin for this.

note we are using render as a free hosting platform. we want to keep things free for this project. also importantly note that this project is going to handle maybe max 5 users per day and usually 3 only so not much traffic