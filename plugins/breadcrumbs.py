from Plugin import Plugin

class breadcrumbs(Plugin):
  type = "breadcrumbs"
  def __init__(self, category):
    self.sep = ' | '
    self.root = 'root'
    self.breadcrumbs = '' 
    path_str = Config.url
    self.breadcrumbs = '<a href="'+Config.url+'">'+self.root+'</a>'
    if len(category) > 1:
      for cat in category:
        path_str = os.path.join(path_str, cat)
        self.breadcrumbs = self.breadcrumbs + self.sep+'<a href="'+path_str+'">'+cat+'</a>'

__breadcrumbs = breadcrumbs(opts['category'])
plugins.append(__breadcrumbs)
