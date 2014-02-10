#!/usr/bin/env python
"""
Bacon Blogger/metaWeblog/MoveableType API system
part of the Bacon blog backend

Maintains a Bacon blog using the Blogger, metaWeblog or MoveableType XML-RPC APIs

Visit http://bacon.artificial-science.org/ for the latest version

Required: Python 2.1 or later
"""

__version__ = "1.0"
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

name = "Bacon Weblog XML-RPC API"
version = "1.0"

from SimpleXMLRPCServer import CGIXMLRPCRequestHandler
import xmlrpclib
import Config
import sys
import os.path
import string
import time
import Local
import datetime

__user__ = 'dgoodman'
__password__ = 'foobar'

def checkPass(user, password):
  if __password__ == '':
    raise Exception('No Password Set')
  if user == __user__ and password == __password__:
    return True
  else: raise Exception('Unauthorized access')

def B1newPost(appkey, blogid, username, password, content, publish):
  if checkPass(username, password):
    cat = ''
    filename = time.strftime('%Y%m%d%H%M') +'.'+Config.story_extension
    #TODO HACK
    #TODO: if publish is false, set extension to somethingelse!
#TODO check to make sure we're not writing over crap!
#TODO make sure to create non-existant categories
    fullname = os.path.join(Config.story_path, filename)
    title, content = content.split('</title>')
    title = string.replace(title, '<title>', '')
    outfile = file(fullname, 'w')
    outfile.write(title+'\n')
    outfile.write(content)
    outfile.close()
    return filename[:-len(Config.story_extension)-1]

def B1editPost(appkey, postid, username, password, content, publish):
  if checkPass(username, password):
    path = os.path.join(Config.story_path, postid+'.'+Config.story_extension)
    posttime = os.path.getmtime(path)
    #TODO: if publish is false, set extension to somethingelse!
#TODO check to make sure we're not writing over crap!
#TODO make sure to create non-existant categories
    title, content = content.split('</title>')
    title = string.replace(title, '<title>', '')
    outfile = file(path, 'w')
    outfile.write(title+'\n')
    outfile.write(content)
    outfile.close()
    os.utime(path, (posttime,posttime))
    return True

def B1deletePost(appkey, postid, username, password, publish):
  if checkPass(username, password):
    os.remove(os.path.join(Config.story_path, postid+'.'+Config.story_extension))
    return True

def B1getPost(appkey, postid, username, password):
  if checkPass(username, password):
    path = os.path.join(Config.story_path, postid+'.'+Config.story_extension)
    url = Config.url+'/'+postid+'.'+Config.default_flavour
    posttime = os.path.getmtime(path)
    date = datetime.datetime.fromtimestamp(posttime, Local.Local).isoformat()
    infile = file(path, 'r')
    title = infile.readline().strip()
    body = '<title>'+title+'</title>'+infile.read()
    infile.close()
    return {'userid':1, 'content':body, 'dateCreated':xmlrpclib.DateTime(date), 'postid':postid}

def B1getRecentPosts(appkey, blogid, username, password, numberOfPosts):
  if checkPass(username, password):
    import Blog
    blog = Blog.Blog()
    blog.item_limit = numberOfPosts
    blog.loadTemplate()
    blog.preloadContent()
    blog.loadContent()
    retval = []
    for story in blog.children['stories']:
      url = Config.url+'/'+story.path_name+'.'+Config.default_flavour
      date = story.ISOtime
      retval.append({'userid':1, 'content':'<title>'+story.title+'</title>'+story.body, 'dateCreated':xmlrpclib.DateTime(date), 'postid':story.path_name})
    return retval

def B1getUsersBlogs(appkey, username, password):
  if checkPass(username, password):
    #for now, bacon only supports single-author single-blog systems
      return [{'blogID':'1', 'blogid':'1', 'url':Config.url, 'blogName':Config.blog_title}]

def B1getUserInfo(appkey, username, password):
  if checkPass(username, password):
    return {'userid':1, 'firstname':Config.blog_author.split()[0], 'lastname':string.join(Config.blog_author.split()[:-1], ' '), 'nickname':Config.blog_author, 'email':Config.blog_author_email, 'url':Config.url}

def mWnewPost(blogid, username, password, content, publish):
  if checkPass(username, password):
    cat = ''
    if content.has_key('categories'):
      cat = content['categories'][0] #ignore all but first category
    filename = str(content['dateCreated']) +'.'+Config.story_extension
    if 'fn:' in content['title']:
      filename = content['title'].split('fn:')[-1].strip()+'.'+Config.story_extension
      content['title'] = content['title'].split('fn:')[0].strip()
    fullpath = os.path.join(Config.story_path, cat)
    if not os.path.exists(fullpath):
      os.makedirs(fullpath, 0775)
    fullname = os.path.join(fullpath, filename)
    if os.path.exists(fullname):
      raise Exception("Story with that filename already exists!")
    outfile = file(fullname, 'w')
    outfile.write(content['title']+'\n')
    outfile.write(content['description'])
    outfile.close()
    if cat == '' or cat == '/':
      return filename[:-len(Config.story_extension)-1]
    else:
      return os.path.join(cat, filename[:-len(Config.story_extension)-1])

def mWeditPost(postid, username, password, content, publish):
  if checkPass(username, password):
    path = os.path.join(Config.story_path, postid+'.'+Config.story_extension)
    posttime = os.path.getmtime(path)
    #TODO: allow altering of category!
#TODO make sure to create non-existant categories
    fullname = os.path.join(Config.story_path, postid)
    outfile = file(path, 'w')
    outfile.write(content['title']+'\n')
    outfile.write(content['description'])
    outfile.close()
    os.utime(path, (posttime,posttime))
    return True

def mWgetPost(postid, username, password):
  if checkPass(username, password):
    path = os.path.join(Config.story_path, postid+'.'+Config.story_extension)
    url = Config.url+'/'+postid+'.'+Config.default_flavour
    posttime = os.path.getmtime(path)
    date = datetime.datetime.fromtimestamp(posttime, Local.Local).isoformat()
    infile = file(path, 'r')
    title = infile.readline().strip()
    body = infile.read()
    infile.close()
    path = ''
    if os.path.split(postid)[0] != '' > 1:
      path = os.path.split(postid)[0]
    return {'title':title, 'permalink':url, 'link':url, 'description':body, 'dateCreated':xmlrpclib.DateTime(date), 'postid':postid, 'categories':[path]}

def mWgetCategories(blogid, username, password):
  if checkPass(username, password):
    #TODO require Cache plugin
    infile = file(os.path.join(Config.plugin_state_path,'story.cache'),'r')
    retval = []
    line = infile.readline()
    while line != '':
      path = line.split()[0]
      cat = string.join(path.split('/')[:-1], '/')
      if cat not in retval:
        retval.append(cat)
      line = infile.readline()
    infile.close()
    return retval

def mWgetRecentPosts(blogid, username, password, numberOfPosts):
  if checkPass(username, password):
    import Blog
    blog = Blog.Blog()
    blog.item_limit = numberOfPosts
    blog.loadTemplate()
    blog.preloadContent()
    blog.loadContent()
    retval = []
    for story in blog.children['stories']:
      url = Config.url+'/'+story.path_name+'.'+Config.default_flavour
      date = story.ISOtime
      retval.append({'title':story.title, 'permalink':url, 'link':url, 'description':story.body, 'dateCreated':xmlrpclib.DateTime(date), 'postid':story.path_name, 'categories':[story.path]})
    return retval

def mWnewMediaObject(blogid, username, password, content):
  if checkPass(username, password):
    path = os.path.join(Config.upload_path, content['name'])
    #TODO catch this shit!
    #TODO mkdirs!
    outfile = file(path, 'wb')
    outfile.write(content['bits'].data)
    outfile.close()
    return os.path.join(os.path.join(Config.url, Config.upload_path[len(Config.site_path)+1:]),content['name'])

def MTgetRecentPostTitles(blogid, username, password, numberOfPosts):
  if checkPass(username, password):
    import Blog
    blog = Blog.Blog()
    blog.item_limit = numberOfPosts
    blog.loadTemplate()
    blog.preloadContent()
    blog.loadContent()
    retval = []
    i = 0
    for story in blog.children['stories']:
      url = Config.url+'/'+story.path_name+'.'+Config.default_flavour
      date = story.ISOtime
      retval.append({'title':story.title, 'dateCreated':xmlrpclib.DateTime(date), 'postid':story.path_name, 'userid':1})
      i = i + 1
    return retval

def MTgetCategoryList(blogid, username, password):
  if checkPass(username, password):
    cats = mWgetCategories(blogid, username, password)
    retval = []
    for cat in cats:
      retval.append({'categoryId':cat, 'categoryName':cat})
    return retval

def MTgetPostCategories(postid, username, password):
  if checkPass(username, password):
    return [{'categoryName':os.path.split(postid)[0], 'categoryId':os.path.split(postid)[0], 'isPrimary':True}]

def MTsetPostCategories(postid, username, password, categories):
  if checkPass(username, password):
    newcat = categories[0]['categoryId'] #TODO be smarter about this.
    oldpath = os.path.join(Config.story_path, postid)+'.'+Config.story_extension
    fn = os.path.split(postid)[1]
    newpath = os.path.join(os.path.join(Config.story_path, newcat),fn)+'.'+Config.story_extension
    os.rename(oldpath, newpath)
    return True

def MTsupportedMethods():
  return [] #TODO

def MTsupportedTextFilters():
#  return [{'none':'No formatting'}] #TODO, gee this sounds kinda cool
  return []

def MTgetTrackbackPings(postid):
  return [] #TODO when we have TrackBacks, anyway

def MTpublishPost(postid, username, password):
  return True

handler = CGIXMLRPCRequestHandler()
handler.register_function(B1newPost, 'blogger.newPost')
handler.register_function(B1editPost, 'blogger.editPost')
handler.register_function(B1deletePost, 'blogger.deletePost')
handler.register_function(B1getRecentPosts, 'blogger.getRecentPosts')
handler.register_function(B1getUsersBlogs, 'blogger.getUsersBlogs')
handler.register_function(B1getUserInfo, 'blogger.getUserInfo')
handler.register_function(B1getPost, 'blogger.getPost')
handler.register_function(mWnewPost, 'metaWeblog.newPost')
handler.register_function(mWeditPost, 'metaWeblog.editPost')
handler.register_function(mWgetPost, 'metaWeblog.getPost')
handler.register_function(mWgetCategories, 'metaWeblog.getCategories')
handler.register_function(mWgetRecentPosts, 'metaWeblog.getRecentPosts')
handler.register_function(mWnewMediaObject, 'metaWeblog.newMediaObject')
#handler.register_function(MTgetRecentPostTitles, 'mt.getRecentPostTitles')
#handler.register_function(MTgetCategoryList, 'mt.getCategoryList')
#handler.register_function(MTgetPostCategories, 'mt.getPostCategories')
#handler.register_function(MTsupportedMethods, 'mt.supportedMethods')
#handler.register_function(MTsupportedTextFilters, 'mt.supportedTextFilters')
#handler.register_function(MTgetTrackbackPings, 'mt.getTrackbackPings')
#handler.register_function(MTsetPostCategories, 'mt.setPostCategories')
#handler.register_function(MTpublishPost, 'mt.publishPost')
handler.handle_request()
