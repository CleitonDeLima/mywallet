document.addEventListener("DOMContentLoaded", event => {
  const fields = document.querySelectorAll(".flatpickr-input");
  for (const el of fields) {
    const options = JSON.parse(el.dataset.flatpickrOptions);
    flatpickr(el, options);
  }
});
