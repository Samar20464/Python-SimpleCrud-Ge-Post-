from flask import Flask, redirect, render_template, request, url_for

from database import get_db, init_db

app = Flask(__name__)


@app.get("/")
def index():
    with get_db() as conn:
        users = conn.execute("SELECT * FROM users ORDER BY id").fetchall()
    return render_template("index.html", users=users)


@app.get("/new")
def new_user():
    return render_template(
        "user_form.html", title="New user", user=None, action=url_for("create_user"), method="post"
    )


@app.post("/")
def create_user():
    with get_db() as conn:
        conn.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (request.form["name"], request.form["email"]),
        )
    return redirect(url_for("index"))


@app.get("/<int:user_id>/edit")
def edit_user(user_id):
    with get_db() as conn:
        user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if user is None:
        return "User not found", 404
    return render_template(
        "user_form.html",
        title="Update user (PUT)",
        user=user,
        action=url_for("update_user", user_id=user_id),
        method="put",
    )


@app.put("/<int:user_id>")
def update_user(user_id):
    with get_db() as conn:
        conn.execute(
            "UPDATE users SET name = ?, email = ? WHERE id = ?",
            (request.form["name"], request.form["email"], user_id),
        )
    return "", 200


@app.get("/<int:user_id>/patch")
def patch_form(user_id):
    with get_db() as conn:
        user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if user is None:
        return "User not found", 404
    return render_template(
        "patch_form.html",
        user=user,
        action=url_for("patch_user", user_id=user_id),
    )


@app.patch("/<int:user_id>")
def patch_user(user_id):
    with get_db() as conn:
        user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        if user is None:
            return "User not found", 404
        name = request.form.get("name") or user["name"]
        email = request.form.get("email") or user["email"]
        conn.execute(
            "UPDATE users SET name = ?, email = ? WHERE id = ?",
            (name, email, user_id),
        )
    return "", 200


@app.delete("/<int:user_id>")
def delete_user(user_id):
    with get_db() as conn:
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    return "", 200


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
