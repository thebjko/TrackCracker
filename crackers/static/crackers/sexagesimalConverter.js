const converterBtns = document.querySelectorAll('[id^=sexagesimal-to-decimal-btn]')
  converterBtns.forEach((btn) => {
    btn.addEventListener('click', (e) => {
      const sexagesimalInput = document.querySelector(`input#${btn.dataset.inputId}`)
      let inputValue = Number(sexagesimalInput.value)
      let convertedValue = 0
      let power = 0
      let flag = true
      while (inputValue) {
        const mod = inputValue % 100
        if (mod >= 60) {
          flag = false
          alert('올바른 60진수를 입력하세요.\nex. 5시간 15분 23초 → 51523')
          break
        }
        convertedValue += mod * Math.pow(60, power)
        inputValue = Math.floor(inputValue/100)
        power ++
      }
      if (flag) {
        const temp = sexagesimalInput.value
        sexagesimalInput.value = convertedValue
        alert(`${temp}에서 ${convertedValue}로 변경되었습니다.`)
      }
    })
  })