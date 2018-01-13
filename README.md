# Deprecated

Entire script with few new features are created in JS right now and distributed is by NPM.

See: https://github.com/MrMaxie/get-google-fonts.

# Get Google Fonts

![status: depraced](https://img.shields.io/badge/status-depraced-lightgrey.svg)
![python: 2.7](https://img.shields.io/badge/python-2.7-blue.svg)

Tool to download font files from [Google Fonts](https://fonts.google.com/) with a properly converted CSS file.

```
Usage: get-google-fonts.exe [OPTIONS]

Options:

  -i, --input TEXT   URL for Google Fonts' css file or only query (everything
                     after question mark in URL).
  -o, --output TEXT  Output directory for fonts files.
  -p, --path TEXT    Relative path to fonts. This path will be inserted
                     before each font in the CSS file.
  --font-name TEXT   Template string for result name fonts.
  --css-name TEXT    Name of css file.
  -a, --agent TEXT   User agent for request.
  -c, --config TEXT  Path to configuration file.
  --gen-config       Generate default config file.
  --help             Show this message and exit.
```

### Input helper
Input will accept either incorrect URLs for Google Fonts. The only thing you have to give is query. For example: ```family=Source+Sans+Pro``` will works as ```https://fonts.googleapis.com/css?family=Source+Sans+Pro```.

### Configuration file
By default, the script attempts to use the file ```.\getgooglefonts.ini``` if exists, and by default ```--gen-config```  will generate this file for you. With ```--config``` you can to point custom ini file for script or for generating as well. 

### Forcing other extensions
If you want to force older extensions of fonts inside downloaded CSS file you must to use proper User-Agent. Actually inside "default configuration" is used User-Agent for Google Chrome v57 under Win10 which gets **.woff2**. For example ```Wget/1.9.1``` will force to use **.ttf** extension.

### Name of font template 
```--font-name``` will be used as template for new names of fonts. You can to use following variables therein:
- ```%(comment)s``` - Name of languages character range located before font-face in comment. e.g. **latin**
- ```%(family)s``` - Font-family (whitespace will be replaced with underscore) e.g. **Source_Sans_Pro**
- ```%(weight)s``` - Font-weight e.g. **400**
- ```%(name)s``` - Name of original file e.g. **ODelI1aHBYDBqgeIAH2zlC2Q8seG17bfDXYR_jUsrzg**
- ```%(ext)s``` - Original extension e.g. **woff2**

### How to use
Script requires **Click** package if you want to interprate it independently with **Python 2.7** (other version were not tested).
##### [...or download .exe](https://github.com/MrMaxie/get-google-fonts/releases)
