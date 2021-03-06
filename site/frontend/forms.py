from django import forms

# default is required = True
class TagCloudForm(forms.Form):
	help_text = {
			# input type
			'body' : 'Paste your text inline (eg. into this box)',
			'url' : 'Retrieve text from the specified url.',
			'file' : 'Upload a file',
			'freqs' : "Enter in a dictionary of word:frequency counts",

			# required info
			'width' : 'Width of the div containing the tag cloud (px). Default none.',
			'height' : 'Height of the div containing the tag cloud (px). Default None.',
			'max_words' : 'Maximum number of words to be included in the tag cloud (will always truncate least frequent words)',

			# advanced options
			'strip' : 'Strip any html markup. Default is True.',
			'normalize' : "Normalize the case of all words, making 'Hello' and 'hello' equivalent",
			'stopwords' : "Remove (exclude) common english words (so-called 'stop words'), such as 'the' and 'it'. Default True.",
			'custom_stopwords': 'a comma separated list of custom stop words. can be used in addition to, or instead of, standard english stopwords.',
			'tokenizer' : 'Specify a custom tokenizer, by passing in a <a href="http://docs.python.org/library/re.html">python regular expression</a>',
			'sort_order' : 'What order should the words be sorted in?',
			'equation': 'Equation family to use for extrapolation of word sizes. options are "linear," "log," and "exp."',
			'slope': 'If a linear equation style is chosen, the slope can be customized (default 0.15).',
			'css_id': 'a custom css id to include in the div for the word cloud',
			'css_class': 'a custom css class to include for each word in the word cloud.',
			'link_to': 'each word in the word cloud can be a link. if so, specify the link prefix here. (eg. if each word is a category, the tag cloud can link to that category page by inserting the url prefix here). specify "wordnik" to link to fun wordnik definitions.',
			'layout': 'layout algorithm: either svg (recommended) or text',
			}

	allowed_sort_orders = [('random', 'random'), ('frequency', 'frequency'),
			('alphabetical', 'alphabetical')]

	allowed_layouts = [('svg', 'svg'), ('text', 'text')]

	body = forms.CharField(widget=forms.Textarea(attrs={'rows':'20', 'cols':60 }), help_text = help_text['body'], required=False, label="Text")
	url =           forms.CharField(help_text = help_text['url'], required=False)
	file =          forms.FileField(help_text = help_text['file'], required=False)
	# this is an option in the API but not likely to be useful in the frontend
	#freqs =         forms.CharField(help_text = help_text['freqs'], required=False)

	# required
	width =         forms.IntegerField(help_text = help_text['width'], required=False)
	height =        forms.IntegerField(help_text = help_text['height'], required=False)
	max_words =     forms.IntegerField(help_text = help_text['max_words'], required=False)

	# aesthetics
	start_color =   forms.CharField(required=False)
	end_color =     forms.CharField(required=False)
	color_steps =   forms.IntegerField(required=False)

	# word handling
	strip =         forms.BooleanField(initial=True, help_text = help_text['strip'], required=False)
	normalize =     forms.BooleanField(initial=True, help_text = help_text['normalize'], required=False)
	remove_stopwords = forms.BooleanField(initial=True, help_text = help_text['stopwords'], 
			required=False)
	custom_stopwords = forms.CharField(help_text = help_text['custom_stopwords'], 
			required=False)
	tokenizer =     forms.CharField(help_text = help_text['tokenizer'], required=False)
	sort_order =    forms.ChoiceField(help_text= help_text['sort_order'], required=False, 
			choices = allowed_sort_orders)
	equn =			forms.CharField(help_text=help_text['equation'], required=False)
	slope =			forms.FloatField(help_text=help_text['slope'], required=False)
	css_id =		forms.CharField(help_text=help_text['css_id'], required=False)
	css_class =		forms.CharField(help_text=help_text['css_class'], required=False)
	link_prefix	=	forms.CharField(help_text=help_text['link_to'], required=False)
	layout =		forms.ChoiceField(help_text= help_text['layout'], required=False, 
			choices = allowed_layouts)


	def clean(self):
		cleaned_data = self.cleaned_data
		url = cleaned_data.get('url')
		body = cleaned_data.get('body')
		file = cleaned_data.get('file')
		if not url and not body and not file:
			raise forms.ValidationError('You must specify one of "url", "body" or "file" fields')
		if (url and body) or (url and file) or (body and file):
			raise forms.ValidationError('Specify only one of "url" or "body" or "file" fields')

		# if specifying color, need all three of start_color, end_color and
		# color_steps.
		start_color = cleaned_data.get('start_color')
		end_color = cleaned_data.get('end_color')
		color_steps = cleaned_data.get('color_steps')
		if start_color or end_color or color_steps:
			if not (start_color and end_color and color_steps):
				raise forms.ValidationError('To customize the color scheme, please enter all color scheme information: start color, end color, and number of steps to extrapolate in between.')
		
		return cleaned_data

class NewTopicForm(forms.Form):
	name = forms.CharField()

	def __init__(self, *args, **kwargs):
		num_file_sources = kwargs.pop('file_sources', None)
		num_web_sources = kwargs.pop('web_sources', None)
		print num_file_sources
		print num_web_sources
		super(NewTopicForm, self).__init__(*args, **kwargs)
		while num_file_sources:
			self.fields['file_%d' % num_file_sources] = forms.FileField()
			num_file_sources -= 1
		while num_web_sources:
			self.fields['web_%d' % num_web_sources] = forms.CharField()
			num_web_sources -= 1




