document.addEventListener('DOMContentLoaded', (_) => {
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
  document.body.addEventListener('change-detail-btn', (e) => {
    document.getElementById(e.detail.btnId).outerHTML = e.detail.outerHTML
  })
  document.body.addEventListener('update-paginator', (e) => {
    const paginator = document.getElementById(e.detail.paginatorId)
    paginator.innerHTML = e.detail.innerHTML
    htmx.process(paginator)
  })
  document.body.addEventListener('give-alert', (e) => {
    alert(e.detail.message)
    console.log('hello')
  })
})
