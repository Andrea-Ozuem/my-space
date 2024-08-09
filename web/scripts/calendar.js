const isLeapYear = (year) => {
    return (
      (year % 4 === 0 && year % 100 !== 0 && year % 400 !== 0) ||
      (year % 100 === 0 && year % 400 === 0)
    );
  };

const getFebDays = (year) => {
    return isLeapYear(year) ? 29 : 28;
  };

let calendar = document.querySelector('.calendar');

const month_names = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December',
  ];
let month_picker = document.querySelector('.month');
  
const generateCalendar = (month, year) => {
    let calendar_days = document.querySelector('.days');
    calendar_days.innerHTML = '';
    let calendar_header_year = document.querySelector('.year');
    let days_of_month = [
      31,
      getFebDays(year),
      31,
      30,
      31,
      30,
      31,
      31,
      30,
      31,
      30,
      31,
    ];
    
    let currentDate = new Date();
    
    month_picker.innerHTML = month_names[month].toUpperCase();
    
    calendar_header_year.innerHTML = year;
    
    let first_day = new Date(year, month);
  
  
  for (let i = 0; i <= days_of_month[month] + first_day.getDay() - 1; i++) {
  
      let day = document.createElement('div');
  
      if (i >= first_day.getDay()) {
        day.innerHTML = i - first_day.getDay() + 1;

        if (i - first_day.getDay() + 1 === currentDate.getDate() &&
          year === currentDate.getFullYear() &&
          month === currentDate.getMonth()
        ) {
          day.classList.add('active');
        }
      }
      calendar_days.appendChild(day);
    }
  };
  
let currentDate = new Date();
let currentMonth = { value: currentDate.getMonth() };
let currentYear = { value: currentDate.getFullYear() };
generateCalendar(currentMonth.value, currentYear.value);