"""
Copyright 2005, Donald E. Goodman, Jr.
This file is part of Bacon.

Bacon is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

Bacon is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Bacon; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

"""
  Item is the base class for all things like stories, comments, and the blog itself.
  It has a template (loaded from a file), and optional interpolation on that
  template (which, for security reasons, things like comments won't use)
  and other useful thingies.
"""

import XYAPTU
from cStringIO import StringIO
import Config
import os.path
import sys
import datetime
import time
import Globals
import Local

class Item:
  def __init__(self, path=None, filename=None, flavour=None, opts=None):
    self.sortfunc = None
    if path == None:
      self.path = ''
    else:
      self.path = path
    self.filename = filename
    self.name = None
    self.ext = None
    if filename != None:
      self.name, self.ext = os.path.splitext(filename)
      self.path_name = os.path.join(self.path, self.name)
    else:
      self.path_name = self.path
    self.classType = 'item'
    self.posttime = 0
    self.opts = opts
    self.vars = {}
    self.plugins = []
    for v in Config.__dict__.keys():
      if v[:2] != '__' and v != 'vars':
        self.vars[v] = Config.__dict__[v]
    if flavour == None:
      self.flavour = self.vars['default_flavour']
    else:
      self.flavour = flavour
    self.template = ''
    self.children = {} #dictionary of lists. key is the classType
    self.prev = None
    self.next = None
    self.mo_num = None
    self.yr = None

  def loadTemplate(self):
    #think about the children!
    for key in self.children.keys():
      for child in self.children[key]:
        #HACK!
        for p in self.plugins:
          child.plugins.append(p)
        child.loadTemplate()
    pathtotemplate = os.path.join(Config.template_path, self.path)
    #find the closest template
    while pathtotemplate != Config.template_path:
      if os.path.exists(os.path.join(pathtotemplate, self.classType+'.'+self.flavour)):
        break
      else:
        pathtotemplate = os.path.split(pathtotemplate)[0]

    filename = os.path.join(pathtotemplate, self.classType+'.'+self.flavour)
    try:
      f = file(filename)
    except:
#      print "Cannot find flavour <strong>"+self.flavour+"</strong>"
      filename = os.path.join(pathtotemplate, self.classType+'.'+Config.default_flavour)
      f = file(filename)
#      sys.exit()
      #TODO need to handle this better
    line = f.readline()
    while(line != ''):
      self.template = self.template + line
      line = f.readline()
    f.close()


  def preloadContent(self):
    #think about the children!
    for key in self.children.keys():
      for child in self.children[key]:
        child.preloadContent()
        #if posttime is in the future....
        if self.opts != None and self.opts.has_key('form') and self.opts['form'].getfirst('future') == None:
          if child.posttime > time.time():
            self.children[key].remove(child)
      self.children[key].sort(self.sortfunc)
    if self.classType == 'blog': return #HACK!
    self.pathtocontent = os.path.join(self.vars[self.classType+"_path"],self.path)
    try:
      self.posttime = os.path.getmtime(os.path.join(self.pathtocontent, self.filename))
    except: return
    date = datetime.datetime.fromtimestamp(self.posttime, Local.Local)
    self.datetime = date
    self.ISOtime = date.isoformat()
    self.yr = "%0.4d"%(date.year,)
    self.mo_num = "%0.2d"%(date.month,)
    self.mo = Globals.months[date.month]
    self.da = "%0.2d"%(date.day,)
    self.dw = Globals.days[time.localtime(self.posttime)[6]]
    self.hr = "%0.2d"%(date.hour,)
    self.min = "%0.2d"%(date.minute,)
    self.timezone = date.tzname()
    #stub

  def loadContent(self):
    #think about the children!
    for key in self.children.keys():
      l = len(self.children[key])
      i = 0
      for child in self.children[key]:
        child.loadContent()
#      for i in range(l):
        if self.classType == 'blog': #HACK!
          if i == 0: child.next = None
          else: child.next = self.children[key][i-1]
          if i == l-1: child.prev = None
          else: child.prev = self.children[key][i+1]
        else:
          if i == 0: child.prev = None
          else: child.prev = self.children[key][i-1]
          if i == l-1: child.next = None
          else: child.next = self.children[key][i+1]
        i = i + 1
    #stub

  def render(self):
    #think about the children!
    for key in self.children.keys():
      self.__dict__[key] = ''
      for child in self.children[key]:
        self.__dict__[key] += child.render()

    if self.classType == 'blog':
      self.vars.update(self.__dict__)
    else:
      self.vars[self.classType] = self

    for p in self.plugins:
      self.vars[p.type] = p

    #do interpolation; return fully rendered Item. Requires 3 passes!
    # can we fix this?
    retvalStream = StringIO()
    templateStream = StringIO(self.template)
    xcp = XYAPTU.xcopier(self.vars, ouf=retvalStream)
    xcp.xcopy(templateStream)
    templateStream.close()

    templateStream = StringIO(retvalStream.getvalue())
    retvalStream.close()
    retvalStream = StringIO()
    xcp = XYAPTU.xcopier(self.vars, ouf=retvalStream)
    xcp.xcopy(templateStream)
    templateStream.close()

    templateStream = StringIO(retvalStream.getvalue())
    retvalStream.close()
    retvalStream = StringIO()
    xcp = XYAPTU.xcopier(self.vars, ouf=retvalStream)
    xcp.xcopy(templateStream)
    retval = retvalStream.getvalue()
    retvalStream.close()
    return retval

  def __lt__(self, other):
    return self.posttime < other.posttime
  def __le__(self, other):
    return self.posttime <= other.posttime
  def __gt__(self, other):
    return self.posttime > other.posttime
  def __ge__(self, other):
    return self.posttime >= other.posttime
#  def __ne__(self, other):
#    return self.posttime != other.posttime
#  def __eq__(self, other):
#    if other == None: return 0
#    return self.posttime == other.posttime
