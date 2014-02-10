import os.path
import string
import cgi
from Plugin import Plugin

#TODO trackbacks!

class writeback(Plugin):
  type = "writeback"
  spamwords = ['tramadol', 'fioricet', 'lipitor', 'glucophage', 'levitra', 'prozac', 'phentermine', 'fluoxetine', 'soma', 'cialis', 'claritin', 'zyprexa', 'adipex', 'meridia', 'pharmacy', 'paxil', 'propecia', 'viagra', 'zimmer', 'movado', 'debt consolidation', 'equity loan', 'debt collection', 'debt counselors', 'debt financing', 'debt negotiation', 'debt consolodation', 'debt management', 'credit score', 'rolex', 'debt counseling', 'debt service', 'mortgage caculator', 'trimox', 'mortgage broker', 'free webpage', 'credit history', 'dotmoment.com', 'metoprolol', 'norvasc', 'tenoretic', 'zestril', 'digoxin', 'warfarin', 'celebrex', 'nexium', 'pravachol', 'synthroid', 'proventil', 'omepazole', 'albuterol', 'protonix', 'ranitidine', 'premarin', 'prevacid', 'ambien', 'plavix', 'debt-consolidation', 'online poker', 'online gambling', 'online casino', 'forex', 'online-travel', 'credit card offers', 'credit check', 'credit card services', 'You are invited to', 'Please check some', 'whackingpud', 'holdem']

  def makesafe(self, str):
    str = str.replace("&", "&amp;")
    str = str.replace("$","&#36;")
#    str = str.replace(">","&gt;")
#    str = str.replace("<","&lt;")
    return str

  def __init__(self, form, fname, blog):
    if form.getfirst('postwb', '') != '' and fname != None:
      import commands
      id = commands.getoutput('uuidgen')
      title = self.makesafe(form.getfirst('title', ''))
      author = self.makesafe(form.getfirst('author', ''))
      link = self.makesafe(form.getfirst('link', ''))
      body = self.makesafe(form.getfirst('body', ''))
      if body == '': return
      for spamword in self.spamwords:
        if spamword in string.lower(body) or spamword in string.lower(title) or spamword in string.lower(link) or spamword in string.lower(author):
          print "SPAM!"
          return

      newfilename = fname+'.'+id+'.'+Config.comment_extension
      if not os.path.exists(os.path.join(Config.comment_path,blog.path)):
        os.makedirs(os.path.join(Config.comment_path,blog.path), 0775)
      outfilename = os.path.join(os.path.join(Config.comment_path,blog.path), newfilename)
      outfile = file(outfilename, 'w')
      outfile.write(title+'\n')
      outfile.write(author+'\n')
      outfile.write(link+'\n')
      newbody = ''
      for line in body.split('\n'):
        newbody = newbody + '<p>'+line.strip()+'</p>\n'
      body = newbody
      outfile.write(body+'\n')
      outfile.close()

__writeback = writeback(opts['form'], fname, blog)
plugins.append(__writeback)
