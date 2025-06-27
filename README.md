### What it does
* Switch between OpenAI / Anthropic / Gemini.
* Enable only the models you want your users to see.
* Store nothing sensitive in the database; API keys live in `.env`.
* If a key dies, the next one is tried automatically—refresh without downtime.

### Extending
* Add another provider: create a `foo_chat()` in `app/providers.py`,
  add it to `PROVIDER_FUNCS`, add your env variable in `config.py`,
  and run `flask providers-init` again.
* Persist chat history per user: add a `session_id` or `user_id` column
  to `ChatMessage` and filter in `/chat`.
