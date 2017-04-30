# main.py
import urllib2, click, imp, os, sys, ConfigParser, re
from string import Template

# get directory of executable / script
def main_is_frozen():
	return (hasattr(sys, "frozen") or
			hasattr(sys, "importers") or
			imp.is_frozen("__main__"))

def get_main_dir():
	if main_is_frozen():
		return os.path.dirname(sys.executable)
	return os.path.dirname(os.path.realpath(__file__))

SCRIPT_ROOT = get_main_dir()

# options
@click.command()
@click.option(
	'--input', '-i',
	default=None,
	help='URL for Google Fonts\' css file or only query (everything after question mark in URL).')
@click.option(
	'--output', '-o',
	default=None,
	help='Output directory for fonts files.')
@click.option(
	'--path', '-p',
	default=None,
	help='Relative path to fonts. This path will be inserted before each font in the CSS file.')
@click.option(
	'--name-font',
	default=None,
	help='Template string for result name fonts.')
@click.option(
	'--name-css',
	default=None,
	help='Name of css file.')
@click.option(
	'--agent', '-a',
	default=None,
	help='User agent for request.')
@click.option(
	'--config', '-c',
	default=None,
	help='Path to configuration file.')
@click.option(
	'--gen-config',
	is_flag=True,
	default=False,
	help='Generate default config file.')

# main
#def main(input, output, path, name_font, name_css, agent, config, gen_config):
def main(**args):
	# default config
	cfg = {}
	cfg['input']     = 'https://fonts.googleapis.com/css?family=Roboto'
	cfg['output']    = '.\\fonts'
	cfg['path']      = '/'
	cfg['name_font'] = '%(family)s-%(weight)s-%(comment)s.%(ext)s'
	cfg['name_css']  = 'fonts.css'
	cfg['agent']     = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
	cfg['config']    = os.path.abspath(SCRIPT_ROOT + '\\getgooglefonts.ini')

	if args['config'] is None:
		args['config'] = cfg['config']
	args['config'] = os.path.abspath(args['config'])

	config_section = 'Get Google Fonts'

	# generate config
	if args['gen_config'] is True:
		# override ?
		if os.path.exists(args['config']):
			if not click.confirm('Config file already exists. Override?'):
				return
		cfg_file = open(args['config'], 'w')
		Config = ConfigParser.ConfigParser()
		Config.add_section(config_section)
		for x in cfg:
			if not x == 'config':
				Config.set(config_section, x, cfg[x])
		Config.write(cfg_file);
		cfg_file.close();
		click.echo('File generated successfully!')
		return

	# reading configuration file
	if os.path.exists(args['config']):
		click.echo('Reading' + (' default' if cfg['config'] == args['config'] else '') + ' config file...')
		Config = ConfigParser.ConfigParser()
		Config.read(args['config'])
		temp_cfg = {}
		for x in Config.options(config_section):
			try:
				temp_cfg[x] = Config.get(config_section, x)
				if temp_cfg == -1:
					temp_cfg.pop(x, None)
			except:
				continue
		for x in cfg:
			if not x == 'config':
				if x in temp_cfg:
					cfg[x] = temp_cfg[x]

	# arguments into configuration dictionary
	for x in cfg:
		if x == 'config':
			continue
		if x in args and args[x] is not None:
			cfg[x] = args[x]

	# repair input
	m = re.search(r'^(?:(?:[^?\s]+)?\?)?([^?\s]+)\s*$', cfg['input'])
	if m is None:
		click.echo('The input isn\'t valid...')
		return;
	cfg['input'] = 'https://fonts.googleapis.com/css?' + m.group(1)

	# User-Agent is empty?
	if not cfg['agent']:
		cfg['agent'] = 'Wget/1.9.1'

	# request
	try:
		request = urllib2.Request(
			cfg['input'],
			headers= {"User-Agent": cfg['agent']} )
		css = urllib2.urlopen(request).read();
	except urllib2.HTTPError, e:
		print "HTTP Error:", e.code, cfg['input']
	except urllib2.URLError, e:
		print "URL Error:", e.reason, cfg['input']

	# new-filename => url
	fonts = {}

	# regexs
	regex_font_faces  = re.compile(r'\s*(?:\/\*\s*(.*?)\s*\*\/)?[^@]*?@font-face\s*{(?:[^}]*?)}\s*', re.IGNORECASE)
	regex_font_family = re.compile(r'[^$]*font-family\s*:\s*(?:\'|")?([^;]*?)(?:\'|")?\s*;[^$]*', re.IGNORECASE)
	regex_font_weight = re.compile(r'[^$]*font-weight\s*:\s*([^;]*?)\s*;[^$]*', re.IGNORECASE)
	regex_font_src    = re.compile(r'(src\s*:[^;]*?url\s*\(\s*(?:\'|")?\s*)([^;]*?)(\s*(?:\'|")?\s*\)[^;]*?;)', re.IGNORECASE)
	regex_filename    = re.compile(r'^.*\/(.*?)\.(.*?)(?:$|\?.*?$)', re.IGNORECASE)

	def regex_cb_ff(m_ff):
		ff_css = m_ff.group(0)
		comment = ''
		family  = ''
		weight  = ''
		if m_ff.group(1) is not None:
			comment = m_ff.group(1)
		m = regex_font_family.match(ff_css)
		if m is not None:
			family = m.group(1)
		m = regex_font_weight.match(ff_css)
		if m is not None:
			weight = m.group(1)
		def regex_cb_src(m_src):
			font_url = m_src.group(2)
			font_name = ''
			font_ext = ''
			m = regex_filename.match(font_url)
			if m is not None:
				if m.group(1) is not None:
					font_name = m.group(1)
				if m.group(2) is not None:
					font_ext = m.group(2)
			font_new_name = cfg['name_font'] % {
				'comment': comment,
				'family': family,
				'weight': weight,
				'name': font_name,
				'ext': font_ext
				}
			i = ''
			while True:
				true_font_new_name = str(i) + font_new_name
				if not true_font_new_name in fonts:
					break
				if i == '':
					i = 1
					continue
				i = i + 1
			fonts[true_font_new_name] = font_url
			return m_src.group(1) + "'" + cfg['path'] + font_new_name + "'" + m_src.group(3)
		return re.sub(regex_font_src, regex_cb_src, ff_css)
	css = re.sub(regex_font_faces, regex_cb_ff, css)

	# creating directory if needed
	if not os.path.exists(os.path.abspath(cfg['output'])):
		os.makedirs(os.path.abspath(cfg['output']))

	# writing new css
	local_css = open(os.path.abspath(cfg['output'] + '\\' + cfg['name_css']), 'wb')
	local_css.write(css)

	def download_font(url, file, filename):
		try:
			f = urllib2.urlopen(url)
			print "Downloading: " + filename

			with open(file, 'wb') as local_file:
				local_file.write(f.read())

		except urllib2.HTTPError, e:
			print "HTTP Error:", e.code, cfg['input']
		except urllib2.URLError, e:
			print "URL Error:", e.reason, cfg['input']

	for filename, url in fonts.items():
		download_font(url, os.path.abspath(cfg['output'] + '\\' + filename), filename)

	print 'Done!' 

# execute
if __name__ == '__main__':
	main()

