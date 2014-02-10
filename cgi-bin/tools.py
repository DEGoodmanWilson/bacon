import os.path

def find_template(config, path, name):
  #path needs to have a leading "/", like the story's category
  #finds the closest instance of template name.flavour
  while path != "/":
    f_path = os.path.join(config.datadir, os.path.join(path[1:], name+"."+config.flavour))
    if os.path.exists(f_path):
      return f_path
    else:
      path = os.path.split(path)[0]
  f_path = os.path.join(config.datadir, name+"."+config.flavour)
  if os.path.exists(f_path):
    return f_path
  else:
    return None


if __name__ == "__main__":
  class Config:
    pass
  config = Config()
  config.datadir = "data"
  config.flavour = "html"
  print find_template(config, "/art/photos/series", "story")
  print find_template(config, "/engineering/maintainence", "story")
  print find_template(config, "/", "story")
  print find_template(config, "/engineering/maintainence", "foo")
