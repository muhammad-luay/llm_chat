from flask.cli import with_appcontext
import click
from . import db
from .models import Provider, LLMModel
from .providers import _iter_keys

# helper to fetch each provider's model list
def fetch_openai_models():
    import openai
    # pick the first working key
    for key in _iter_keys("openai"):
        try:
            client = openai.OpenAI(api_key=key)
            resp = client.models.list().data  # list of ModelInfo
            return [m.id for m in resp]
        except:
            continue
    return []

def fetch_anthropic_models():
    import anthropic
    for key in _iter_keys("anthropic"):
        try:
            cli = anthropic.Anthropic(api_key=key)
            resp = cli.models.list().data  # list of ModelInfo
            return [m.id for m in resp if m.id.startswith("claude-")]
        except:
            continue
    return []

def fetch_google_models():
    import google.generativeai as genai
    for key in _iter_keys("google"):
        try:
            genai.configure(api_key=key)
            all_models = genai.list_models()
            return [m.name for m in all_models if "generateContent" in m.supported_generation_methods]
        except:
            continue
    return []

FETCHERS = {
    "openai":     fetch_openai_models,
    "anthropic":  fetch_anthropic_models,
    "google":     fetch_google_models,
}

def register_cli(app):
    @app.cli.command("db-init")
    @with_appcontext
    def db_init():
        db.create_all()
        click.echo("Initialized DB ✅")

    @app.cli.command("providers-init")
    @with_appcontext
    def providers_init():
        if Provider.query.count():
            click.echo("Providers already present; skipping.")
            return
        provs = [Provider(name=n) for n in FETCHERS.keys()]
        db.session.add_all(provs)
        db.session.commit()
        click.echo("Providers inserted ✅")

    @app.cli.command("models-init")
    @with_appcontext
    def models_init():
        """Fetch all models from each provider and insert into llm_model."""
        if not Provider.query.count():
            click.echo("No providers found. Run `flask providers-init` first.")
            return

        # clear out old models so we can re-seed cleanly
        LLMModel.query.delete()

        for prov in Provider.query:
            fetch = FETCHERS.get(prov.name)
            if not fetch:
                continue
            click.echo(f"Fetching {prov.name} models…")
            for model_id in fetch():
                db.session.add(LLMModel(
                    provider_id = prov.id,
                    model_id    = model_id,
                    display_name= model_id,
                    enabled     = False
                ))
            click.echo(f"  → inserted {LLMModel.query.filter_by(provider_id=prov.id).count()} models")
        db.session.commit()
        click.echo("Model seeding complete ✅")
