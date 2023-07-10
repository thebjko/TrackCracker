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
          alert('Enter appropriate sexagesimal number.\nex. 5 hours 15 minutes 23 seconds → 51523')
          break
        }
        convertedValue += mod * Math.pow(60, power)
        inputValue = Math.floor(inputValue/100)
        power ++
      }
      if (flag) {
        const temp = sexagesimalInput.value
        sexagesimalInput.value = convertedValue
        alert(`Converted successfully from ${temp} to ${convertedValue}.`)
      }
    })
  })