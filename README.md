# News Parser

This is a Django-based web application that allows users to parse and search for news articles based on specific keywords. The application also includes filtering and sorting options, user authentication, and the ability to save articles.

## Features

- **News Parsing**: Fetch news articles from various sources using a keyword search.
- **Filtering & Sorting**: Users can filter news based on keywords and sort by publication date.
- **Article Saving**: Logged-in users can save and unsave articles to their personal list.
- **Pagination**: Efficiently displays articles with pagination support.
- **AJAX for Saving Articles**: Articles can be saved or unsaved without reloading the page.

## Project Structure

- **`parser_app/`**: The main application that contains models, views, and templates.
  - **`models.py`**: Defines the `Articles` model, representing news articles.
  - **`views.py`**: Handles requests for news parsing, filtering, and article management.
  - **`templates/`**: Contains HTML templates for rendering the web pages.
- **`modules/get_info.py`**: Custom module that includes the logic for scraping news articles from the web.
- **`static/`**: Contains static files like CSS, JavaScript, and images.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/news-parser.git
    ```
2. Navigate to the project directory:
    ```bash
    cd news-parser
    ```
3. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
4. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5. Set up the database:
    ```bash
    python manage.py migrate
    ```
6. Create a superuser account:
    ```bash
    python manage.py createsuperuser
    ```
7. Run the development server:
    ```bash
    python manage.py runserver
    ```

## Usage

- Visit the homepage and enter a keyword to search for news articles.
- Filter and sort the search results as needed.
- Logged-in users can save or unsave articles, which are stored in their personal list.
- To view detailed information about an article, click on its title.


## Technologies

- **Django**: Web framework for building the back-end.
- **Bootstrap**: Used for front-end styling and layout.
- **AJAX**: Used for asynchronous requests to save articles.
- **SQLite**: Default database for development purposes.
- **BeautifulSoup**: Used for web scraping to fetch news articles.

## Future Improvements

- Add more news sources.
- Improve the scraping logic to handle a wider variety of websites.
- Implement advanced filtering options such as categories and tags.
- Add tests for improved reliability and maintainability.
