document.addEventListener('DOMContentLoaded', (_) => {
  document.body.addEventListener('change-offcanvas-title', (e) => {
    document.querySelector('.offcanvas-title').textContent = e.detail.title
  })
  document.body.addEventListener('change-achievement-width', (e) => {
    const progress = document.getElementById(e.detail.identifier)
    progress.setAttribute('style', `width: ${e.detail.width}%`)
    progress.textContent = e.detail.width + '% Achieved'
  })
  document.body.addEventListener('change-supertask-achievement-width', (e) => {
    const progress = document.getElementById(e.detail.identifier)
    progress.setAttribute('style', `width: ${e.detail.width}%`)
    progress.textContent = e.detail.width + '% Achieved'
  })
  document.body.addEventListener('supertask-marked-complete', (e) => {
    const progress = document.getElementById(e.detail.identifier)
    progress.setAttribute('style', `width: 100%; opacity: .3;`)
    progress.textContent = 'Marked Complete'
  })
  document.body.addEventListener('task-marked-complete', (e) => {
    const progress = document.getElementById(e.detail.identifier)
    progress.setAttribute('style', `width: 100%;`)
    progress.textContent = 'Marked Complete'
  })
})
