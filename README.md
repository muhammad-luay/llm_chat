# LLM Chat

A simple, self-hosted chat UI that allows you to talk to multiple LLM providers (OpenAI, Anthropic, and Google) through a unified interface.

## Features

*   **Switch between Providers**: Seamlessly switch between OpenAI, Anthropic, and Google (Gemini) models.
*   **Model Whitelisting**: Enable only the models you want your users to see.
*   **Secure Key Management**: API keys are stored in a `.env` file, not in the database.
*   **Automatic Key Rotation**: If an API key fails, the application automatically tries the next available key, ensuring no downtime.
*   **Extensible**: Easily add new providers by following a simple pattern.
*   **Chat History**: Persists chat history in a local SQLite database.

## Project Structure

```
llm_chat/
├── app/
│   ├── __init__.py
│   ├── cli.py
│   ├── forms.py
│   ├── models.py
│   ├── providers.py
│   ├── routes.py
│   └── templates/
│       ├── base.html
│       ├── chat.html
│       └── admin/
│           ├── provider_models.html
│           └── providers.html
├── config.py
├── llm_chat.db
├── README.md
├── requirements.txt
└── run.py
```

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/llm_chat.git
    cd llm_chat
    ```

2.  **Create a virtual environment and activate it:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Create a `.env` file** in the root directory and add your API keys. You can add multiple keys for each provider, separated by commas.

    ```
    SECRET_KEY=your_secret_key
    OPENAI_API_KEYS=key1,key2
    ANTHROPIC_API_KEYS=key1,key2
    GOOGLE_API_KEYS=key1,key2
    ```

5.  **Initialize the database and populate it with providers and models:**

    ```bash
    flask db-init
    flask providers-init
    flask models-init
    ```

6.  **Run the application:**

    ```bash
    flask run
    ```

The application will be available at `http://127.0.0.1:5000`.

## Usage

1.  **Admin Panel**: Navigate to `/admin/providers` to see the list of available providers. From there, you can click on a provider to manage the models that are enabled for the chat interface.

2.  **Chat Interface**: The main chat interface is at `/chat`. You can select any of the enabled models from the dropdown and start a conversation.

## Extending the Application

### Adding a New Provider

1.  **Create a chat function** in `app/providers.py`. This function should take a `model` and a `prompt` as input and return the AI's response. See the existing `openai_chat`, `anthropic_chat`, and `google_chat` functions for examples.

2.  **Add the new provider function** to the `PROVIDER_FUNCS` dictionary in `app/providers.py`.

3.  **Add the provider's API key(s)** to your `.env` file and update `config.py` to load them.

4.  **Run the `providers-init` and `models-init` commands again** to populate the database with the new provider and its models:

    ```bash
    flask providers-init
    flask models-init
    ```

### Persisting Chat History Per User

To persist chat history for each user, you can add a `user_id` or `session_id` column to the `ChatMessage` model in `app/models.py`. Then, you would filter the chat messages in the `chat` view function in `app/routes.py` based on the current user.
