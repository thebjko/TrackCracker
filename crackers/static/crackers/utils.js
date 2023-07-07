const toggleBtn = (targetId, btnId) => {
  document.getElementById(targetId).classList.toggle('d-none')
  const btn = document.getElementById(btnId)
  btn.textContent == '닫기' ? btn.textContent = '자세히 보기' : btn.textContent = '닫기'
}