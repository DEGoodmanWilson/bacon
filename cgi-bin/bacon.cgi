#!/usr/bin/env python
"""
Bacon blog backend

Generates webpages (and other formats, including Atom 0.3) from textfiles

Visit http://bacon.artificial-science.org/ for the latest version

Required: Python 2.1 or later
"""

__version__ = "1.1"
__license__ = "Python"
__copyright__ = "Copyright 2005, Donald E. Goodman, Jr."
__author__ = "Donald E. Goodman, Jr. <dgoodman@artificial-science.org>"

"""
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

name = "Bacon"

import cgi
import cgitb; cgitb.enable()
import os
import string
import Config
import sys

opts ={}
opts['form']  = cgi.FieldStorage()
path_info = ''
if os.environ.has_key("PATH_INFO") and len(os.environ["PATH_INFO"]) > 1:
  #we want to ignore the spurious case of just "/"
  #we have extra path information after the script name in the URL. we need
  #to parse this
  path_info = os.environ["PATH_INFO"][1:]
  if path_info[-1] == '/':
    path_info = path_info[:-1]
else:
  path_info = ''
path_info =  path_info.split('/')

cat = []
date = []
#first things first. path_info will take one of three forms:
# '' : the default. just dump everything
# ['foo' {, 'bar' {...}}]': a logical category. dump everything within that category
# ['yyyy' {, 'mm' {, 'dd'}}]': a dative category. dump everything on that date
# ['foo' ...., 'yyyy']: a category followed by a date. same as above. load by date then category
#additionally, the last item in path_info /may/ be a filename!
#in this case, we recognize it by the presence of a '.' in the filename.
#moreover, if the filename sans extension is 'index', we just treat that as if
#it hadn't been appended, but note the flavour

name = None
flavor = flavour = None
fname = None
if '.' in path_info[-1]:
  fn = path_info[-1]
  path_info = path_info[:-1]
  fname,ext = os.path.splitext(fn)
  flavor = flavour = ext[1:]
#  if fname == 'index': name = None
#  else:
  name = fname+'.'+Config.story_extension
else:
  name = 'index.'+Config.story_extension

state = 'cat'
for item in path_info:
  try:
    int(item)
    state = 'date'
  except: pass
  if state == 'cat':
    cat.append(item)
  else:
    try:
      date.append(int(item))
    except: pass
#make date conform to [yyyy,mm,dd]
if len(date)>3: date = date[:3]
else:
  for i in range(3-len(date)):
    date.append(None)
opts['category'] = cat
opts['date'] = date

#now, let's extract the flavour, if it's specified in the opts
#if opts['form'].getfirst('flav') != None:
#  flavor = flavour =  opts['form'].getfirst('flav')

import ContentType
ct = ContentType.ContentType(flavor)
ct.loadTemplate()
sys.stdout.write(ct.render()+'\n')

import Blog
blog = Blog.Blog(string.join(opts['category'],'/'), name, flavour, opts)
blog.vars['flavour'] = flavour
blog.vars['flavor'] = flavor
blog.vars['path_info'] = string.join(opts['category'], '/')

#now, execute the plugins
plugins = []
for plugin in os.listdir(Config.plugin_path):
  if os.path.isfile(os.path.join(Config.plugin_path,plugin)):
    if os.path.splitext(plugin)[-1] == '.py':
      execfile(os.path.join(Config.plugin_path,plugin))

for plugin in plugins:
  blog.plugins.append(plugin)
blog.loadTemplate()
for plugin in blog.plugins:
  plugin.postLoadTemplate()
blog.preloadContent()
for plugin in blog.plugins:
  plugin.postPreloadContent()
blog.loadContent()
for plugin in blog.plugins:
  plugin.postLoadContent()
sys.stdout.write(blog.render())
for plugin in blog.plugins:
  plugin.postRender()
