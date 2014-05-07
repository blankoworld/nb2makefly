Cette documentation est en anglais. Référez-vous à celle en Français dans le fichier README.md

## Installation

Required: python 2

The installation is easy: just copy the **nb2makefly.py** file into your Nanoblogger blog directory.

## How to use it

Create 2 directories in your Nanoblogger blog directory:

   * src
   * db

Then launch nb2makefly script as this:

    python nb2makefly.py

It will fill **src** and **db** directory.

**WARNING**: the default nb2makefly configuration will be enough. However you should change the given variable to have the right website address: **nanoblogger_url** (Cf. *nb2makefly configuration*).

## nb2makefly configuration

The **nb2makefly.py** file contains some configuration variables. Here is their name and their utility:

  * limit : give the maximum number of article/post to import/process
  * nanoblogger_conf : name of the Nanoblogger configuration file. For an example: blog.conf
  * datadir : directory in which are stored Nanoblogger articles/posts
  * data\_ext : extension of these files
  * cat\_ext : extension used by Nanoblogger database
  * nanoblogger\_url : your final website URL address
  * extension : Makefly post/article's extension
  * db\_ext : Makefly metadata's extension
  * default\_type : default type for Makefly's new post/article
  * default\_tag : default tag of new posts/articles. It's used if no tag found in your Nanoblogger post.
  * default\_url : default URL address for Makefly
  * targetdir : target directory of new articles/posts content
  * dbtargetdir : target directory for metadata of articles/posts
  * url\_replacement\_dict : contains a list of URL address that you want to modify. For an example to change all */joueb/* by the URL address contened into *default_url* variable, we do this:

    {
       '/joueb/': default_url,
    }

## Old Nanoblogger links and redirections

To redirect old Nanoblogger links to Makefly, on you web server (Apache2), use permanent redirection.

    Redirect permanent /ancienlien http://monsite.tld/nouveau_lien

> How to have the list of old links?

Just go to the **archives** directory (in Nanoblogger) and do `ls -R`.
