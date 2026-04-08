import calendar
from datetime import datetime

class MonthCalendar:
    def __init__(self, year=None, month=None):
        now = datetime.now()
        self.year = year or now.year
        self.month = month or now.month
        self.day_today = now.day if (self.year == now.year and self.month == now.month) else None
        
        # Названия месяцев для вывода
        self.months_ru = [
            "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
            "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
        ]

    def get_month_name(self):
        return self.months_ru[self.month - 1]

    def get_days_matrix(self):
        # Возвращает недели как списки чисел (0 для пустых дней)
        cal = calendar.Calendar(firstweekday=0)
        return cal.monthdayscalendar(self.year, self.month)

    def is_today(self, day):
        return day == self.day_today