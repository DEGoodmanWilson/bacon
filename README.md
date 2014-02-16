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

Flavouring
----------

In order for Bacon to render your stories, it needs a set of templates to know how to put everything together. A complete set of templates is called a flavour. You can have multiple flavours for one blog, allowing you to create a number of different looks for your site. Moreover, you can use flavours to do some fun tricks. For example, if you can create a flavour that contains a form to allow vistors to post comments to your site.

There are five different parts of your blog that can be flavoured: the content type header, the overall page, individual stories, updates to these stories, and comments to these stories. Maximally, for a given flavour there will be one flavour file that corresponds to each of these parts.

Creating flavours is straigtforward. The flavour files go in your data directory, with your stories. You can put the flavour files in any subdirectory, too; these will only kick in when all of the stories being viewed are in that folder or deeper; that is, you can create subsections of your site that are flavoured differently. Also, you can create alternate flavours for only particular parts of the page, like stories or comments; if a flavour requested is not found, Bacon defaults to the default chosen in the Config.py file. So, for example, to create an alternate story flavour that shows the comments attached to the story, you need only create a flavour file for that part.

Anyway, any flavour will contain at most the following files (where flav is the name of the flavour you are creating, suchas html or xml:

* content-type.flav
* blog.flav
* story.flav
* update.flav
* comment.flav

"html" is a good name for your default flavour.

Each flavour will have a number of variables, or placeholders, in them, along with maybe some straight Python code. This is what makes the flavours so flexible. Before we get into the specifics of what each template file should have in them, take a moment to examine the variables that are available to use. I'll wait here.

Done? Let's assume that your flavour will be in HTML 4.01, because that's the default that the sample flavour uses. Of course, your flavours might be XHTML, some other variety of XML, SGML, or in fact anything (binary formats, like PDF, will need the help of a plugin to work right). At least one of the plugins and the trackback/comment functionality provided assumes some variant of HTML; this will be addressed in a future release. So let's just, for now, procede with HTML. We'll call our flavour html. Let's walk through the creation of the ecessary flavour files: content-type.html blog.html, story.html, update.html and comment.html. Then we'll cover how you can use variables and Python code to spice things up.

First, in your data directory (specified in the config.datadir variables in the configuration section of bacon.cgi), create with a text editor a file called head.html. The head.html and foot.html files will be used to brace the stories in the final output; that is, Bacon will first processes head.html, then each story, then finally foot.html. So we want to include everything that will occur above the stories.

Here's a minimal content-type.html; this file informs webservers and browsers about the kind of data to expect:
```
Content-type: text/html
```
Very simple.
Here's the sample blog.html that comes included with Bacon:

```
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<title>$blog_title</title>
<head>

<body>
  <div id="header">
    <h1>$blog_title</h1>
    <h2>$blog_description</h2>
  </div>

  <div id="main">
  $stories
  </div>
</body>
</html>
```

Pretty straightforward, ne? This just defines the usual HTML header, with a full doctype, and sets the title of the page to the blog title. Then, in the body, we create a div id'd as header (so that we can apply CSS later to make it pretty if we want) with the blog title and description in it. Next, we open a new div for the meat of the page, leaving it open as the stories will be inserted after that. The $stories variable instructs Bacon to insert the stories at that point. Then everything is closed off. As you can see, using variables is very simple.

Now we need a story.html to contain our content. First, a little about the structure of Bacon.

Bacon organizes dynamic content into stories. Each story represents a single piece of information. This document is an example of a story. Each story has a title, a date, a category and some content. When a request is made for Bacon to render a page, there is some set of stories that will get rendered based on the request. The default is to render the 10 most recent stories, regardless of category. One can also ask Bacon to render the stories from only one category (including that category's children), or all the stories from a particular date. Each individual story is rendered according to the story flavour file. Here's the story.html flavour file from the sample flavour:

```
<div class="blogbody">
  <h3 class="titleline">${story.title}, ${story.dw}, ${story.da} ${story.mo}, ${story.yr}
     ${story.hr}:${story.min}</h3>
  ${story.body}
</div>
```

In this example, we simply create a div containing the story. We put the title of the story, along with the time and date of the story, in a level-3 header. Finally, we insert the body of the story. Note that the variables here are references to a Python class called story. Since the variable names have .'s in them, we have to enclose the variable name in curly braces.

This is all very simple; I want something more complex. Let's group stories by date by only printing the date when it changes between stories. That is, I don't want a particular date to render to the screen more than once; if more than one story was posted on the same day, they will share a date header. We can easily specify the conditions under which a bit of our HTML is rendered by calling upon Python. First, though, we have to explore a particular issue. The story variable is really an alias. Bacon maintains a linked list of all stories to be rendered. story is just a pointer to the current element in that list being rendered. This way, we don't have to know anything about the story order in our story flavour file: otherwise, we'd have to have a seperate flavour file for each story! This won't do. However, we can reference this list; moreover, we know the current story's position in the list through the ${story.prev} and ${story.next} variables.

With that in mind, here is how one executes a Python conditional:
```
  <py-open code="if cond:"/>
    HTML to include if "cond" is true
  <py-clause code="else:"/>
    HTML to include if "cond" is false
  <py-close/>
```
Knowing all this, we can construct a date header that only prints once for each day, rather than once for each story.
Here is the final story.html code, then:
```
  <py-open code="if story.next == None or story.da != story.next.da:"/>
    <h3>${story.dw}, ${story.da} ${story.mo} ${story.yr}</h3>
  <py-close/>

  <div class="blogbody">
    <h4 class="titleline">${story.title}, ${story.hr}:${story.min}</h4>
    ${story.body}
    ${story.updates}
  </div>
```
This is much the same as before, except we've added a Python condition. If the story is the first story (the story at the top of the page; that is, there is no next story in the linked list), print the date header. Otherwise, if the story's day of posting is different from the next story (one story up). Otherwise, don't. I've also added a call to insert any updates to the story that are present; we'll cover updating stories in the section on creating stories.
Of course, you can use arbitrary Python code in your flavours and your stories, using the py-line element:
```
  <py-line code="put python code here"/>
```
Any variables created or modified are remembered for the remainder of the rendering session, so you can create a new variable in the head.html, and it will still be valid in the foot.html; of course you can reference it using the $ notation as well.
Lastly, at the very least, you should create empty update.html and comment.html files.

The rest of the flavours work similarly; I'll leave the creation of new ones an excercise for the reader; have a look at the samples provided for guidance.



[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/DEGoodmanWilson/bacon/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

