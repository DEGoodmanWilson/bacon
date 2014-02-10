import os.path
import string
from Plugin import Plugin

class fileinc(Plugin):
  type = "fileinc"
  def __getattr__(self, attr):
    try:
      return self.__dict__[attr]
    except:
      #it's not already here...so it's a file that is wanted to be opened
      filename = os.path.join(os.path.join(Config.plugin_state_path, "files"), attr)
      try: infile = file(filename)
      except:
        raise AttributeError, "Could Not Open %s for opening"%filename
      retval = infile.read()
      infile.close()
      return retval

__fileinc = fileinc()
plugins.append(__fileinc)
