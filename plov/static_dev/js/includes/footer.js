let currentYearNode = document.querySelector("#current-year");

let clientYear = new Date().getFullYear();

function updateYear() {
      let differenceInYears = clientYear - serverYear;

      if (differenceInYears != 0) {
          let browserDate = new Date();
          let timezoneOffset = browserDate.getTimezoneOffset();
          let utcBrowserDate = new Date(browserDate.getTime() + browserDate.getTimezoneOffset() * 60000);

          let differenceInDays = Math.abs((utcBrowserDate.getTime() - Date.UTC(serverYear, 0, 1))) / (1000 * 60 * 60 * 24);

          if (differenceInDays > 1) {
              currentYearNode.innerHTML = serverYear;
          } else {
              currentYearNode.innerHTML = clientYear;
          }
      } else {
          currentYearNode.innerHTML = clientYear;
      }
  }

if (typeof Date !== "undefined") { // Проверка, что JS включен
    updateYear();
}