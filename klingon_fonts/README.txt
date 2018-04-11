Notes on using Klingon fonts


FOR LINUX USERS

With most modern Linux terminals (gnome-terminal, konsole, lxterminal, 
xfce4-terminal, mate-terminal) simply having the font installed system-wide 
is enough. The terminal will fall back to it for the Klingon, meaning that 
you don't have to select the font in your terminal settings. 

This also means that if you want a particular Klingon font, you should only 
install this one. There maybe a way to have them all installed, and to select 
the fallback Klingon using fontconfig. I’m not sure, but you can find more 
information here:

	https://www.freedesktop.org/wiki/Software/fontconfig/
	https://wiki.archlinux.org/index.php/font_configuration 

Fonts may need to be set manually as fallbacks in .Xresources for older 
terminals, such as urxvt and xterm.


GENERAL NOTES

The reason ‘Horta’ has it’s own shorter character set, because the last four 
Klingon characters seem to show up as other symbols in most terminals. Also, 
'Horta' seems not to work at all in Konsole.

The fonts in this repository were pointed out to me by David Lachut. The 
fonts, listed by license, are from the following sites.

- Open Font License:
    
    https://fontlibrary.org/en/font/horta
    http://www.evertype.com/fonts/tlh/

- Microsoft Public License:
    https://blogs.msdn.microsoft.com/shawnste/2013/05/20/piqad-font-for-bings-klingon-translator/

- Shareware:
    http://www.fontspace.com/james-kass/code2000

See the file 'pIquD_fonts_demo.png' for a look at each font.

Feel free to message me on reddit (/u/weilian82) or submit a pull request if 
you’d like to add anything to these instructions! Instructions for Mac or 
Windows might be useful.


INSTALLATION

On Gnu/Linux: 

- Put the .ttf files in /usr/share/fonts/ or the .fonts directory of your 
  home folder, then run "fc-cache -fv"

For Windows 7 and later:

- Right-click the font file(s) and choose "Install".

Mac OS X 10.3 or above (including the FontBook)

- Double-click the font file and hit "Install font" button at the bottom of 
  the preview.

