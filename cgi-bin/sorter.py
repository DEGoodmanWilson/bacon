import os.path
import story
import sys

class NullSorter:
  def __init__(self, config, filename = None):
    self.config = config
    self.stories = []
    self.filename = filename

  def parsedir(self, args, dirname, names):
    for name in names:
      fn, extension = os.path.splitext(name)
      extension = extension[1:] #get rid of leading".". TODO betterway
      if extension == self.config.file_extension:
        s = story.Story(self.config)
#        s.read(dirname, name) #TODO should be relative path
        path = dirname[len(self.config.datadir):] #rem datadir, make it relative path
#filter it out if it's beyond the config.depth
        if self.config.depth >= 0:
          if path == '/':
            temp1 = path[1:]
          else:
            temp1 = path
          if self.config.path_info == '/':
            temp2 = self.config.path_info[1:]
          else:
            temp2 = self.config.path_info
          if (len(temp1.split(os.path.sep))-len(temp2.split(os.path.sep))) > self.config.depth:
            return
        s.read(path, name)
        self.stories.append(s)

  def openfile(self, path, fn):
    s = story.Story(self.config)
    s.read(path, fn)
    self.stories.append(s)

  def getStories(self, max=None, start=0):
    os.path.walk(self.config.datadir, self.parsedir, None)
    self.stories.sort()
    self.stories.reverse()
    return self.stories[start:max], len(self.stories)

######################################################################

class CategorySorter(NullSorter):
  def __init__(self, config, category, filename = None):
    self.category = category
    NullSorter.__init__(self, config, filename)

  def getStories(self, max=None, start=0):
    if self.filename != None: #just one file, in base folder
      self.openfile(self.category, self.filename+"."+self.config.file_extension)
    else:
      os.path.walk(os.path.join(self.config.datadir, self.category), self.parsedir, None)
      self.stories.sort()
      self.stories.reverse()
    return self.stories[start:max], len(self.stories)

######################################################################

class DateSorter(NullSorter):
  def __init__(self, config, year=None, month=None, day=None, filename=None):
    self.year = year
    self.month = month
    self.day = day
    NullSorter.__init__(self,config,filename)

  def parsedir(self, args, dirname, names):
    for name in names:
      if name.split(".")[-1] == self.config.file_extension:
        s = story.Story(self.config)
        path = dirname[len(self.config.datadir):] #rem datadir, make it relative path
        s.read(path, name)
#        print self.day, s.da, type(self.day), type(s.da)
        if ((self.year == s.yr) or (self.year == None)) \
           and ((self.month == s.mo_num) or (self.month == None)) \
           and ((self.day == s.da) or (self.day == None)) \
           and ((self.filename == None) or (self.filename == s.fn)):
          self.stories.append(s)

  def getStories(self, max=None, start=0):
    os.path.walk(self.config.datadir, self.parsedir, self.filename)
    self.stories.sort()
    self.stories.reverse()
    return self.stories[start:max], len(self.stories)
