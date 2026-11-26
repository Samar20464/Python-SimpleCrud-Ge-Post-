document.querySelectorAll("form[data-method]").forEach(function (form) {
  form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const method = form.dataset.method.toUpperCase();
    const options = { method: method };

    if (method === "PUT" || method === "PATCH") {
      options.body = new FormData(form);
    }

    await fetch(form.action, options);

    if (form.dataset.redirect) {
      window.location = form.dataset.redirect;
    } else {
      location.reload();
    }
  });
});
