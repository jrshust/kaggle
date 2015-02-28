from ConfigParser import ConfigParser

def parse_config_file(config_path):
	''' Given a config file, parse it '''

	# define the parser
	parser = ConfigParser()
	parser.read(config_path)

	# get the feature parameters
	feat_params = dict(parser.items('feature_params'))

	return feat_params