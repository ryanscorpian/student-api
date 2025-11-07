document.addEventListener("DOMContentLoaded", () => {
  const display = document.getElementById("display");
  const buttons = document.querySelectorAll(".button");
  const historyList = document.getElementById("history-list");
  let history = [];

  buttons.forEach(button => {
    button.addEventListener("click", () => {
      const value = button.innerText;

      if (value === "C") {
        display.value = "";
      } 
      else if (value === "DEL") {
        display.value = display.value.slice(0, -1);
      } 
      else if (value === "=") {
        try {
          const result = eval(display.value);
          addToHistory(display.value, result);
          display.value = result;
        } catch {
          display.value = "Error";
        }
      } 
      else if (value === "√") {
        display.value = Math.sqrt(parseFloat(display.value) || 0);
      } 
      else if (value === "x²") {
        display.value = Math.pow(parseFloat(display.value) || 0, 2);
      } 
      else if (value === "1/x") {
        display.value = 1 / (parseFloat(display.value) || 1);
      }
      else {
        display.value += value;
      }
    });
  });

  // Keyboard input support
  document.addEventListener("keydown", e => {
    if (/[0-9+\-*/.%]/.test(e.key)) {
      display.value += e.key;
    } else if (e.key === "Enter") {
      try {
        const result = eval(display.value);
        addToHistory(display.value, result);
        display.value = result;
      } catch {
        display.value = "Error";
      }
    } else if (e.key === "Backspace") {
      display.value = display.value.slice(0, -1);
    } else if (e.key === "Escape") {
      display.value = "";
    }
  });

  // Function to add calculations to history
  function addToHistory(expression, result) {
    const entry = `${expression} = ${result}`;
    history.unshift(entry);
    updateHistoryUI();
  }

  function updateHistoryUI() {
    historyList.innerHTML = "";
    history.slice(0, 10).forEach(item => {
      const li = document.createElement("li");
      li.textContent = item;
      historyList.appendChild(li);
    });
  }
});
