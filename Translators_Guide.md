# Translators' Guide #

sK1 internationalization is based on conventional gettext infrastructure. All translatable messages are collected in sk1.pot file which is a translation template. Using this file translators create human-readable PO-file for each language. After that PO files are compiled into binary MO files for actual use by applications.

The sk1.pot template us updated (**build\_pot\_file** option) during of the application build and this task is controlled by project developers. The same is for MO files. Translator only has to provide a completed PO file. All existing PO files can be downloaded from here:

http://sk1.svn.sourceforge.net/viewvc/sk1/trunk/sK1/po/

## Translation steps ##

  1. Download PO file for your language (for example, for German this will be **de.po** file). If such file is absent for your language, just contact developers or create it yourself, if you know how to do it.
  1. While you can edit PO files in a simple text editor, we recommend using specialized PO editors like Lokalize (KDE), GTranslator (GNOME) or poEdit. All of them are usually available from package repositories for your Linux distribution. Here is poEdit screenshot with uploaded German PO file: <br> <img src='http://sk1project.org/images/wiki/poedit.png' />
<ol><li>Translate all messages in PO file. You might like checking of previously translated messages are OK as well, sometimes they need fixing.<br>
</li><li>Save your PO file and send it to developers.</li></ol>

<b>Notes:</b>
Some messages contain technical characters like <b>%i</b>, <b>%s</b>, <b>\n</b>, <b>\t</b> etc. These are variables and supposed to be substituted with text or numbers in the application. E.g. "Save %s files" is likely to be displayed as "Save 3 files" or something like that. Make sure you understand where every translatable message appears and feel free to change position of such variables, if rules in your native language demand that, just don't delete variables. As for multiline messages, please keep line splits intact.<br>
<br>
We highly recommend testing your translations as you translate and definitely testing them before you send them to us. If you have any questions, don't hesitate to contact developers!<br>
<br>
<h2>Desktop resource file</h2>

To translate messages for system menu you have to update sk1.desktop file. This file can be downloaded here:<br>
<br>
<a href='http://sk1.svn.sourceforge.net/viewvc/sk1/trunk/sK1/src/'>http://sk1.svn.sourceforge.net/viewvc/sk1/trunk/sK1/src/</a>

Just open this file in your text editor of choice and you will see which lines you need adding and translating. After translation send this file to developers.<br>
<br>
<h2>Testing translation result</h2>
The simplest way is compiling and installing sK1 from source code. Use following commands:<br>
<br>
<b>python setup.py bdist-rpm</b> (for RPM distros: Mandriva, OpenSuSE, Fedora etc.)<br>
<b>python setup.py bdist-deb</b>  (For Debian based distros: Ubuntu, Mint etc.)<br>
<br>
As a result you will get packages for your system. Please note that sK1 depends on <b>sk1libs</b> and <b>sk1sdk</b> packages. So they should be compiled also.