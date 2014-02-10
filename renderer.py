import XYAPTU
import os.path
from cStringIO import StringIO
import string
import tools
import sys

#TODO THIS NEEDS TO BE CLEANED UP...A LOT!
class BaseRenderer:
  def __init__(self, config, DNS):
    self.config = config
    self.DNS = DNS
    self.stories = DNS['stories']

  def render(self, outstream, flavour=None):
    templateString = ''

    if flavour == None:
      flavour == self.config.flavour

    paths = ['/']

    for story in self.stories:
      paths.append(story.path)
    ct_path = tools.find_template(self.config, os.path.commonprefix(paths), "content_type")
    if(ct_path) == None:
      templateString = self.config.default_content_type+"\n\n"
    else:
      infile = file(ct_path)
      templateString = infile.read()+"\n\n"
      infile.close()

    #second, find the closest head.flavour to use
    head_path = tools.find_template(self.config, os.path.commonprefix(paths), "head")
    foot_path = tools.find_template(self.config, os.path.commonprefix(paths), "foot")

    if (head_path == None) or (foot_path == None):
      outstream.write("unknown flavour "+flavour+"\n")
      return
    infile = file(head_path)
    templateString = templateString + infile.read()
    infile.close()

    i = 0
    for story in self.stories:
      #find the story template first
      story_path = tools.find_template(self.config, story.path, "story")
      if story_path == None:
        break#just skip to the next story...
      #ok, we have the template...let's preprocess
      infile = file(story_path)
      temp = story.getText(infile.read(), i, self.DNS)
      templateString += temp
      infile.close()
      i += 1

    #load the tail
    infile = file(foot_path)
    templateString = templateString + infile.read()
    infile.close()

    #render away!
    templateStream = StringIO(templateString)
    xcp = XYAPTU.xcopier(self.DNS, ouf=outstream)
    xcp.xcopy(templateStream)
