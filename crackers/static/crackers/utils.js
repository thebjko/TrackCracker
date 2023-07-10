const toggleBtn = (targetId, btnId) => {
  document.getElementById(targetId).classList.toggle('d-none')
  const btn = document.getElementById(btnId)
  btn.textContent == 'Close' ? btn.textContent = 'Detail' : btn.textContent = 'Close'
}