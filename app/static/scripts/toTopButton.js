const backToTopBtn = document.createElement('button');

backToTopBtn.id = 'btn-back-to-top';
backToTopBtn.className = 'back-to-top btn btn-dark rounded-circle position-fixed bottom-0 end-0 m-2 m-md-3  d-none';
backToTopBtn.title = 'Наверх';
backToTopBtn.innerHTML = '<i class="bi bi-arrow-up fs-1 fs-md-6" ></i>'
document.body.insertAdjacentElement('beforeend', backToTopBtn);


window.addEventListener('scroll', () => {
  if (window.scrollY > 300) {
    backToTopBtn.classList.remove("d-none");
  } else {
    backToTopBtn.classList.add("d-none");

  }
});

backToTopBtn.addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});
