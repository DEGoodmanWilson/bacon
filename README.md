bacon
=====

Bacon is a 'blogging tool written entirely in Python in the spirit of Blosxom. Bacon aims to be a small-footprint, lightweight and flexible system for maintaining dynamic content on the web. It's designed for the Vi person who wants to start a 'blog without a lot of bells and whistles.

I like to keep things simple; I've tried to keep Bacon as simple to use as possible. Well, OK, mostly. If you can use UNIX, you can use Bacon. Which is one reason why I said it was perfect for the Vi person. The other reason is that 'blog entries and updates are simple text files in HTML format. The fun part is Bacon's templating system; Bacon uses HTML templates with embedded Python to transform these plain-text files into HTML, PDF, or just about any format you might like, on the fly.

This means that you need only type your content in to a text file. No need to mess with database systems, complex web frontends, or anything more complex than plain-text files. Installation is (mostly) a matter of putting the files in your cgi-bin folder.

Bacon allows 'Blog entries and HTML templates allow embedded Python code to allow for maximum flexibility. This is just freaking cool. Honestly. It cuts down on the number of templates needed (making maintainence easier), and means that creating new functionality is often much simpler than writing a new plugin.

Speaking of which, Bacon does have a plugin system. In the current release, it's functional if a bit primitive, but it will grow. Of course, Bacon does quite a lot out of the box, including comments and story updates. Moreover, Bacon comes bundled with a handful of useful plugins for including the contents of arbitrary files, leaving breadcrumbs, and so forth. Plus I'm writing new plugins all the time as my needs grow.

Installing
----------

1. Copy bacon.cgi, and all of the .py files to your CGI folder, often public_html/cgi-bin. If you don't know where to put CGI files, ask your system administrator. Be sure that your web server doesn't treat files with a .py extension as scripts to be executed.

2. Create folders for your entires and your plugins. These folders can be named anything, but should not be in a folder that is accessed by your webserver. For example, if you put files for your website in the public_html folder, do not put them there. I like to create a bacon folder, and then use bacon/data and bacon/plugins for my entry and plugin folders respectively. Also create a folder for plugins to store state information, for example bacon/plugins/state. Be sure that your webserver can read these folders, and read and write the state folder. Also, if you intend to use comments, create a folder for those, such as bacon/comments, and be sure that the webserver can write to this folder as well.

3. Edit the Config.py file in the cgi-bin folder so that Bacon knows where all these folders are located. Of particular importance, be sure to list the folders created above in the appropriate locations. Use full path names; do not use shortcuts like ~.

4. Create a set of flavour files in the folder you instructed Bacon to look in in the step above. You will need at the very least one of each of the following for the default template you listed in the Config.py file (default: HTML): blog.html, content-type.html, story.html, update.html, and comment.html (if you won't be using comments, you still need at least an empty file). Sample templates can be downloaded to get you started.
There is no step five.

Using
-----

To post a story to your new blog, just create a textfile in the stories directory. This directory is specified in the Config.py configuration file. Give it an extension of .txt—the filename can be anything, otherwise. For example, your first post might be called firstpost.txt.

There is a little formatting you will have to do. The first line of the text file will become the story title. The remaining lines are the story body. It might be helpful, at least if you plan on generating HTML or XHTML, to enclose paragraphs in &lt;p&gt; &lt;/p&gt; pairs. Of course, after the first line, you could also use RTF (Rich-Text Format) control codes or whatnot, if you are using, say, an RTF flavour for formatting the output.

Stories can also be sorted into different categories (although currently Bacon is limited to assigned exactly one category to each story) by placing the textfile in a subdirectory. So, for example, to categorize your story as a rant, create a subdirectory called rant and place the story in there. Nested directories to create a category hierarchy are supported.

Stories can be updated later with new content by creating a new textfile of the name story.foo.update in the same directory as the original story, where story is the original filename (sans .txt extension), and foo is anything you like. As with the story file, the first line is the (possible empty) title, and the remainder is the body. Updates will only show up if you fill in the update flavour file as covered in the flavouring tutorial.



[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/DEGoodmanWilson/bacon/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

