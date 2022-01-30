/**
 *
 * @param {HTMLFormElement} form
 * @param {SubmitEvent} event
 */
function submit_form(form, event) {
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

  //   const api_data = backend_api("/admin/login-val", form_value);
  //   api_data.then((data) => {
  //     console.log(data);

  //     if (data["status"] == true) {
  //       //   window.location.href = data["redirect_url"];
  //       window.location.replace(data["redirect_url"]);
  //     } else {
  //       /**@type {HTMLLabelElement} */
  //       var username_err_lbl = document.getElementById(
  //         "admin-login-form__username-input-err"
  //       );
  //       var password_err_lbl = document.getElementById(
  //         "admin-login-password-input-err"
  //       );

  //       username_err_lbl.style.opacity = 1;
  //       password_err_lbl.style.opacity = 1;

  //       username_err_lbl.innerHTML =
  //         data["errors"]["admin-login-form__username-input-field"];
  //       password_err_lbl.innerHTML =
  //         data["errors"]["admin-login-form__password-input-field"];
  //     }

  //     btn.className = old_class;
  //     btn.style.fontSize = old_font_size;
  //     btn.innerText = old_innertext;
  //   });
}
