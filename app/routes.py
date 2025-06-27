from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Provider, LLMModel, ChatMessage
from .forms import ChatForm
from .providers import PROVIDER_FUNCS
from . import db

bp = Blueprint("main", __name__)

##########  CHAT  ##########
@bp.route("/", methods=["GET", "POST"])
@bp.route("/chat", methods=["GET", "POST"])
def chat():
    enabled_models = (
        db.session.execute(
            db.select(LLMModel).where(LLMModel.enabled == True)
        ).scalars().all()
    )
    choices = [(f"{m.provider.name}:{m.model_id}", m.display_name or m.model_id)
               for m in enabled_models]
    form = ChatForm()
    form.model.choices = choices

    messages = []

    if form.validate_on_submit():
        provider_name, model_id = form.model.data.split(":", 1)
        func = PROVIDER_FUNCS[provider_name]
        user_msg = ChatMessage(role="user", content=form.prompt.data, model_id=model_id)
        db.session.add(user_msg)
        db.session.commit()

        try:
            reply = func(model_id, form.prompt.data)
            ai_msg = ChatMessage(role="assistant", content=reply, model_id=model_id)
            db.session.add(ai_msg)
            db.session.commit()
            messages = [user_msg, ai_msg]
        except Exception as e:
            flash(str(e), "danger")

    return render_template("chat.html", form=form, messages=messages)

##########  ADMIN: providers list  ##########
@bp.route("/admin/providers")
def providers():
    provs = Provider.query.all()
    return render_template("admin/providers.html", providers=provs)

##########  ADMIN: toggle models  ##########
@bp.route("/admin/providers/<int:pid>/models", methods=["GET", "POST"])
def provider_models(pid):
    prov = Provider.query.get_or_404(pid)

    if request.method == "POST":
        for mdl in prov.models:
            mdl.enabled = str(mdl.id) in request.form
        db.session.commit()
        flash("Model list updated ✅", "success")
        return redirect(url_for(".providers"))

    return render_template("admin/provider_models.html", provider=prov)
