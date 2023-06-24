document.addEventListener('DOMContentLoaded', (_) => {
  document.body.addEventListener('change-offcanvas-title', (e) => {
    document.querySelector('.offcanvas-title').textContent = e.detail.title
  })
})