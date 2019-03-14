
By Akhila Podupuganti:



This project is to redact the sensitive information form the files like names, dates, phone numbers, .. etc. to specify the what to be redacted and where to store the resulted files we are sending command line arguments. 
For passing command line arguments used argparse. Since we are sending the --input flag I'm considering append mode for this flag which will read in the form of list containing glob type for the files.

before trying with nltk used other packages 

-commonregex
-humannames
-spacy
-GeoText
-gender
-genderize
-gender-detecto
-gender-guesser 
-address

in which few are not supporting with the instance. spacy is really good one from my experience. even commonregex

parser.add_argument("--input", type=glob.glob, required=True, action='append', nargs = '?',
                         help="Please make sure there are .text input files in current or specified folder.")

considering the other flags like names, gender, phones, dates, addresses with action = "store_true" which indicates to be considered for redacting
another flag concept for redacting the whole information related to it. flag output and stats are for storing the output files and display or store the stats to stdout,stderr, or to any specified files
///-----------------
getfiles() - for getting all the list of files from the specified folder and current folder in arguments. here Im checking for is the files are .txt files are not and only considering text files if not displaying msg to the user(stderr,stdout,any stats file). and then after going through all the files for given flags
redact_names() - using nltk and sent_tokenize , word_tokenize , pos_tag for fetching tagged words from PERSON which gives all the person names from the given text
redact_locs() - same as redact_names where using GPE tag for getting locations
redact_phones() - for redacting phones by using regex 

    phone = re.compile(r'''((?:(?<![\d-])(?:\+?\d{1,3}[-.\s*]?)?(?:\(?\d{3}\)?[-.\s*]?)?\d{3}[-.\s*]?\d{4}(?![\d-]))|(?:(?<![\d-])(?:(?:\(\+?\d{2}\))|(?:\+?\d{2}))\s*\d{2}\s*\d{3}\s*\d{4}(?![\d-])))''')

redact_dates_times() - for redacting dates and times from the given text. used regex for finding dates and times

    date = re.compile(r'(?:(?<!\:)(?<!\:\d)[0-3]?\d(?:st|nd|rd|th)?\s+(?:of\s+)?(?:jan\.?|january|feb\.?|february|mar\.?|march|apr\.?|april|may|jun\.?|june|jul\.?|july|aug\.?|august|sep\.?|september|oct\.?|october|nov\.?|november|dec\.?|december)|(?:jan\.?|january|feb\.?|february|mar\.?|march|apr\.?|april|may|jun\.?|june|jul\.?|july|aug\.?|august|sep\.?|september|oct\.?|october|nov\.?|november|dec\.?|december)\s+(?<!\:)(?<!\:\d)[0-3]?\d(?:st|nd|rd|th)?)(?:\,)?\s*(?:\d{4})?|[0-3]?\d[-\./][0-3]?\d[-\./]\d{2,4}', re.IGNORECASE)
    time = re.compile(r'\d{1,2}:\d{2} ?(?:[ap]\.?m\.?)?|\d[ap]\.?m\.?', re.IGNORECASE)

redact_concept() - this is most time taken one for me . where I tried fetching the most similar words of given concept and redacted the sentence.

    used wordnet for getting all the synsets for given concept and also each and every word of the given text. then after found the i.wup_similarity(j) Wu-Palmer Similarity and did mean of all the synsets and considering only the one which is having 0.9% Similarity

redact_gender() - taken a predefined list of male and female words to check for the gender based words and then redacting it

    male_words=['guy','spokesman','chairman',"men's",'man','men','him',"he's",'his','boy','boyfriend','boyfriends','boys','brother','brothers','dad','dads','dude','father','fathers','fiance','gentleman','gentlemen','god','grandfather','grandpa','grandson','groom','he','himself','husband','husbands','king','male','man','mr','nephew','nephews','priest','prince','son','sons','uncle','uncles','waiter','widower','widowers']
    female_words=['heroine','spokeswoman','chairwoman',"women's",'woman','actress','women',"she's",'her','aunt','aunts','bride','daughter','daughters','female','fiancee','girl','girlfriend','girlfriends','girls','goddess','granddaughter','grandma','grandmother','herself','ladies','lady','lady','mom','moms','mother','mothers','mrs','ms','niece','nieces','priestess','princess','queens','she','sister','sisters','waitress','widow','widows','wife','wives','woman']

update_stats() - storing all the msgs to the global list and then depending on the user commad saving stats to the files

    this stats include (msg if the given files are not test) (if not text to redact) (if not files in the folder) (display each redacted status and stats like no of words/sents that are redacted from file that too based on given flags) (specify where the file is saved with .redacted)
    based on the user commad if stderr - save to stderr.log file and if stdout - printout and save it on stdout.log 
    if not save it on other given file. if no file is given then save it on to the default stats file

store_output() - based on the user arguments save all the .redacted files into the specified folder if not into the default folder


