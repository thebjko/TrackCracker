const toggleBtn = (targetId, btnId) => {
  document.getElementById(targetId).classList.toggle('d-none')
  const btn = document.getElementById(btnId)
  btn.textContent === 'Close' ? btn.textContent = 'Detail' : btn.textContent = 'Close'
}

const selectAll = () => {
  const all = document.getElementById('select-all')
  const boxes = document.querySelectorAll('[id^=delete-checkbox-for]')
  boxes.forEach((box) => {
    box.checked = all.checked
  })
}

const allChecked = () => {
  const boxes = document.querySelectorAll('[id^=delete-checkbox-for]')
  let allSelected = true
  boxes.forEach((box) => {
    allSelected &= box.checked
  })
  return allSelected
}

const updateSelectAll = () => {
  const all = document.getElementById('select-all')
  all.checked = allChecked()
}