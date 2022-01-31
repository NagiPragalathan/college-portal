/**
 *
 * @param {HTMLFormElement} form
 * @param {SubmitEvent} event
 */
function submit_form(form, event) {
  console.log("inside form");
  event.preventDefault();

  const btn = form.querySelector("button");
  const old_class = btn.classList;
  const old_font_size = parseFloat(
    window.getComputedStyle(btn).getPropertyValue("font-size")
  );
  const old_innertext = btn.innerText;

  btn.classList.toggle("btn--disabled");
  btn.style.fontSize = old_font_size - old_font_size / 5 + "px";
  btn.innerText = "Please Wait...";

  const form_value = get_form_values(form);
  console.log(form_value);

  const api_data = backend_api("/common/login-val", form_value);
  api_data.then((data) => {
    console.log(data);

    if (data["status"] == true) {
      // window.location.href = data["redirect_url"];
      window.location.replace(data["redirect_url"]);
    } else {
      /**@type {HTMLLabelElement} */
      var username_err_lbl = document.getElementById("form-username-err");
      var password_err_lbl = document.getElementById("form-password-err");
      const username_err = data["errors"]["form-username-input-field"];
      const password_err = data["errors"]["form-password-input-field"];
      var username_parent_classList = username_err_lbl.parentElement.classList;
      var password_parent_classList = password_err_lbl.parentElement.classList;
      if (username_err != "") {
        username_err_lbl.innerText = username_err;
        username_err_lbl.style.opacity = 1;
        username_parent_classList.add("input-text-anim--focus-err");
        document.getElementById("form-username-input-field").select();
      } else {
        if (username_parent_classList.contains("input-text-anim--focus-err")) {
          username_parent_classList.remove("input-text-anim--focus-err");
        }
        username_err_lbl.style.opacity = 0;
      }
      if (password_err != "") {
        password_err_lbl.innerText = password_err;
        password_err_lbl.style.opacity = 1;
        password_err_lbl.parentElement.classList.add(
          "input-pass-anim--focus-err"
        );
        document.getElementById("form-password-input-field").select();
      } else {
        if (password_parent_classList.contains("input-pass-anim--focus-err")) {
          password_parent_classList.remove("input-pass-anim--focus-err");
        }
        password_err_lbl.style.opacity = 0;
      }
    }

    btn.classList.toggle("btn--disabled");
    btn.style.fontSize = old_font_size + "px";
    btn.innerText = old_innertext;
  });
}
