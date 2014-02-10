from Plugin import Plugin
import Globals
import calendar
import datetime
import time

class cal(Plugin):
  type = "calendar"
  def __init__(self, blog, date):
    self.blog = blog
    self.date = date
    self.month_calendar = ''
    self.year_calendar = 'TODO'

  def postLoadContent(self):
    cache = self.blog.cache
    curdate = time.time()
    curdate =  datetime.datetime.fromtimestamp(curdate)
    if self.date[1] != None:
      mo_num = self.date[1]
    elif self.blog.mo_num != None:
      mo_num = self.blog.mo_num
    else:
      mo_num = curdate.month

    if self.date[0] != None:
      yr = self.date[0]
    elif self.blog.yr != None:
      yr = self.blog.yr
    else:
      yr = curdate.year
    mo_num = int(mo_num)
    yr = int(yr)

    prev_yr = yr
    next_yr = yr
    prev_mo = mo_num - 1
    next_mo = mo_num + 1
    if mo_num == 1:
      prev_mo = 12
      prev_yr = yr - 1
    if mo_num == 12:
      next_mo = 1
      next_yr = yr + 1

    #get list of dates for which posts were made for this month. whee.
    dates = []
    cache = self.blog.cache
    for key in cache.cache.items.keys():
      d = datetime.datetime.fromtimestamp(cache.cache.items[key][0])
      if d.month == mo_num and d.year == yr:
        if not d.day in dates:
          dates.append(d.day)
    dates.sort()

    self.month_calendar = '<table class="month-calendar"> <caption class="month-calendar-head"> <a href="'+Config.url+'/'+str(prev_yr)+'/'+str(prev_mo)+'/">&larr;</a> <a href="'+Config.url+'/'+str(yr)+'/'+str(mo_num)+'/">'+Globals.months[mo_num][:3]+' '+str(yr)+'</a> <a href="'+Config.url+'/'+str(next_yr)+'/'+str(next_mo)+'/">&rarr;</a> </caption>\n'

    self.month_calendar += '<tr>\n'
    for day in range(7):
      self.month_calendar += '<th class="month-calendar-day-head '+Globals.days[day]+'">'+Globals.days[day][0]+'</th>\n'
    self.month_calendar += '</tr>\n'

    ct = calendar.monthcalendar(yr,mo_num)
    for row in ct:
      self.month_calendar += '<tr>\n'
      for day in range(7):
        if row[day] == 0:
          self.month_calendar += '<td class="month-calendar-day-noday '+Globals.days[day]+'">&nbsp;</td>\n'
        elif row[day] in dates:
          self.month_calendar += '<td class="month-calendar-day-link '+Globals.days[day]+'"><a href="'+Config.url+'/'+str(yr)+'/'+str(mo_num)+'/'+str(row[day])+'">'+str(row[day])+'</a></td>\n'
        else:
          self.month_calendar += '<td class="month-calendar-day-nolink '+Globals.days[day]+'">'+str(row[day])+'</td>\n'
      self.month_calendar += '</tr>\n'

    self.month_calendar += '</table>\n'

__cal = cal(blog, opts['date'])
plugins.append(__cal)
