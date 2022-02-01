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

  alert("Submitting Form!!!");

  const api_data = backend_api("", form_value);
  api_data.then((data) => {
    console.log(data);
    // To be handled in future
  });

  btn.classList.toggle("btn--disabled");
  btn.style.fontSize = old_font_size + "px";
  btn.innerText = old_innertext;
}
