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

blog_title = "My Very Own Blog"
blog_description = "Yay! I've got a blog!"
blog_language = 'en'
url = "http://your.domain.here/cgi-bin/bacon.cgi"
blog_author = "Blog D. Author"
blog_author_email = "blog@your.domain.here"
blog_author_url = url
default_flavour = "html"
item_limit = 20

site_path = "/home/me/public_html"
upload_path = site_path+"/files"
template_path = "/home/me/site_data/stories"
story_path = "/home/me/site_data/stories"
story_extension = "txt"
comment_path = "/home/me/site_data/comments"
comment_extension = "comment"
update_path = "/home/me/site_data/stories"
update_extension = "update"
plugin_path = "/home/me/site_data/plugins"
plugin_state_path = plugin_path+"/state"

allowed_tags = ['p', 'i', 'em', 'b', 'strong', 'a']
