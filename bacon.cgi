#!/usr/bin/env python

# Bacon
# Author: Donald E Goodman, Jr <dgoodman@artificial-science.org>
# URL/docs/licensing: http://bacon.artificial-science.org
# Copyright 2004, Donald E Goodman, Jr
# Released under the GPL TODO

name = "Bacon"
version = "0+1i"

class Config:
  pass
config = Config()

import os.path

#################################################################################
## CONFIGURATION
## edit this stuff to reflect your site
#################################################################################
config.blog_title = "Site Title"
config.blog_description = "Site Byline"
config.blog_language = "en"
config.blog_author = "Me!!"
config.url = "http://www.mysite.com"

config.datadir = "/home/me/bacon/data"
config.depth = 0
config.num_entries = 10 #for no limit, use None

config.file_extension = "txt"
config.default_flavour = "html"

config.show_future_entries = False

config.plugin_dir = "/home/me/bacon/plugins"
config.plugin_state_dir = os.path.join(config.plugin_dir, "state")

config.default_content_type = 'Content-Type: text/html; charset="UTF-8"'
#################################################################################
## LEAVE SHIT ALONE BELOW HERE
#################################################################################
import os
import sys
import XYAPTU
import story
import sorter
import renderer
import cgi
import cgitb; cgitb.enable() 

DNS = {}
DNS['bacon'] = "Bacon"
DNS['version'] = "0+1i"

#let's grab the parameters. let's also for now just assume one
#value per field...perhaps dangerous, but I'm lazy
form = cgi.FieldStorage()
for key in form.keys():
  config.__dict__['param.'+key] = form[key].value

category = ""
if os.environ.has_key("PATH_INFO") and len(os.environ["PATH_INFO"]) > 1:
  #we want to ignore the spurious case of just "/"
  #we have extra path information after the script name in the URL. we need
  #to parse this
  category = os.environ["PATH_INFO"]

#now, strip leading or trailing "/"'s from the path_info
if len(category) > 0:
  if category[-1] == os.path.sep: category = category[:-1]
  if category[0] == os.path.sep:
    category = category[1:]
config.path_info = '/'+category

#now, there are two possibilities: this is either a category request
#or a date request. here's how we'll differentiate
#if each of the elements in the PATH_INFO are an int or "*" (wildcard)
# then we have a date
#else we have a category; we may have an option filename at the end that we
# need to take into account, too. this is best handled by the CategorySorter,
# I think

#first things first: see if there's a filename at the end of the url.
#if so, use that...
filename,flavour = os.path.splitext(os.path.split(category)[-1])
if flavour != '': #it's a filename! because it has an extension like
              #".html" or something
  category = os.path.split(category)[0] #don't want the filename in the category
  config.flavour = flavour[1:] #remove leading "."
  if filename == "index":
    filename = None #spurious case to handle index.[flavor]
else:
  filename = None
  if config.__dict__.has_key('param.flav'):
    config.flavour = config.__dict__['param.flav']
  else:
    config.flavour = config.default_flavour

#first case: check if all elements are numbers or "*":
isdate = True
items = category.split(os.path.sep)
for i in range(len(items)):
  if items[i] != "*":
    try:
      items[i] = int(items[i])
    except:
      isdate = False

#now, if isdate is still True...we have a little postprocessing to do
if isdate:
  for i in range(len(items)):
    if items[i] == "*": items[i] = None
    else: items[i] = "%0.2d"%(items[i],)
  if items[0] != None and len(items[0]) == 2: items[0] = "20"+items[0]
  if len(items) == 1: items.append(None)
  if len(items) == 2: items.append(None)
  sort = sorter.DateSorter(config, items[0], items[1], items[2], filename)
else:
  sort = sorter.CategorySorter(config, category, filename)

for var in config.__dict__:
  DNS[var] = config.__dict__[var]

if config.__dict__.has_key("param.start"):
  start = int(config.__dict__["param.start"])
else:
  start = 0
stories, numstories = sort.getStories(config.num_entries, start) #TODO
DNS['stories'] = stories
DNS['storystart'] = start
DNS['storyend'] = config.num_entries+start
DNS['numstories'] = numstories

#now, execute the plugins
plugins = []
for plugin in os.listdir(config.plugin_dir):
  if os.path.isfile(os.path.join(config.plugin_dir,plugin)):
    if os.path.splitext(plugin)[-1] == '.py':
      execfile(os.path.join(config.plugin_dir,plugin))

for plugin in plugins:
  DNS[plugin.type] = plugin
  DNS = plugin.setup(DNS)

render = renderer.BaseRenderer(config, DNS)
render.render(sys.stdout)
