
By Akhila Podupuganti:



This project is to redact the sensitive information form the files like names, dates, phone numbers, .. etc. to specify the what to be redacted and where to store the resulted files we are sending command line arguments. 

before trying with nltk used other packages 

- commonregex
- humannames
- spacy
- GeoText
- gender
- genderize
- gender-detecto
- gender-guesser 
- address

in which few are not supporting with the instance. spacy is really good one from my experience. even commonregex

For passing command line arguments used argparse. Since we are sending the --input flag I'm considering append mode for this flag which will read in the form of list containing glob type for the files.

parser.add_argument("--input", type=glob.glob, required=True, action='append', nargs = '?',
                         help="Please make sure there are .text input files in current or specified folder.")

considering the other flags like names, gender, phones, dates, addresses with action = "store_true" which indicates to be considered for redacting
another flag concept for redacting the whole information related to it. flag output and stats are for storing the output files and display or store the stats to stdout,stderr, or to any specified files


getfiles() - for getting all the list of files from the specified folder and current folder in arguments. here Im checking for is the files are .txt files are not and only considering text files if not displaying msg to the user(stderr,stdout,any stats file). and then after going through all the files for given flags

redact_names() - using nltk and sent_tokenize , word_tokenize , pos_tag for fetching tagged words from PERSON which gives all the person names from the given text

    document = ' '.join([i for i in text.split() if i not in stop]) // removing stopwords
    sentences = nltk.sent_tokenize(document) // to sentences
    sentences = [nltk.word_tokenize(sent) for sent in sentences] // to words
    sentences = [nltk.pos_tag(sent) for sent in sentences] // giving parts of speech tag to each word
    # print(sentences)
    for tagged_sentence in sentences:
        # print(tagged_sentence)
        for chunk in nltk.ne_chunk(tagged_sentence): // chunking
            if type(chunk) == nltk.tree.Tree: 
                if(chunk.label() == 'PERSON'): // checking check is PERSON or not
                    c1 = ' '.join([c1[0] for c1 in chunk])
                    names.append(c1)
                    b1 = "█"*(len(c1)) // calculating the block of word
                    red_names = red_names.replace(c1,b1) // replacing 


redact_locs() - same as redact_names where using GPE tag for getting locations

redact_phones() - for redacting phones by using regex 

    phone = re.compile(r'''((?:(?<![\d-])(?:\+?\d{1,3}[-.\s*]?)?(?:\(?\d{3}\)?[-.\s*]?)?\d{3}[-.\s*]?\d{4}(?![\d-]))|(?:(?<![\d-])(?:(?:\(\+?\d{2}\))|(?:\+?\d{2}))\s*\d{2}\s*\d{3}\s*\d{4}(?![\d-])))''')

redact_dates_times() - for redacting dates and times from the given text. used regex for finding dates and times

    date = re.compile(r'(?:(?<!\:)(?<!\:\d)[0-3]?\d(?:st|nd|rd|th)?\s+(?:of\s+)?(?:jan\.?|january|feb\.?|february|mar\.?|march|apr\.?|april|may|jun\.?|june|jul\.?|july|aug\.?|august|sep\.?|september|oct\.?|october|nov\.?|november|dec\.?|december)|(?:jan\.?|january|feb\.?|february|mar\.?|march|apr\.?|april|may|jun\.?|june|jul\.?|july|aug\.?|august|sep\.?|september|oct\.?|october|nov\.?|november|dec\.?|december)\s+(?<!\:)(?<!\:\d)[0-3]?\d(?:st|nd|rd|th)?)(?:\,)?\s*(?:\d{4})?|[0-3]?\d[-\./][0-3]?\d[-\./]\d{2,4}', re.IGNORECASE)
    time = re.compile(r'\d{1,2}:\d{2} ?(?:[ap]\.?m\.?)?|\d[ap]\.?m\.?', re.IGNORECASE)

redact_concept() - this is most time taken one for me . where I tried fetching the most similar words of given concept and redacted the sentence.

    used wordnet for getting all the synsets for given concept and also each and every word of the given text. then after found the i.wup_similarity(j) Wu-Palmer Similarity and did mean of the top similar once (by > .5 %) the synsets and considering only the one which is having 0.9% avg Similarity

    for i in w1:
    for j in w2:
        if (i.wup_similarity(j) is not None and i.wup_similarity(j) > 0.5 ):
            print(str(i.wup_similarity(j))+"===>"+str(i)+"===="+str(j))
            all.append(i.wup_similarity(j))
    average = 0
    if all:
    average = mean(all)
    print("avg:" + str(average))

    output :

    w1
    [Synset('prison.n.01'), Synset('prison.n.02')]
    w2
    [Synset('jail.n.01'), Synset('imprison.v.01')]
    0.9090909090909091===>Synset('prison.n.01')====Synset('jail.n.01')
    avg:0.9090909090909091






redact_gender() - taken a predefined list of male and female words to check for the gender based words and then redacting it

    male_words=['guy','spokesman','chairman',"men's",'man','men','him',"he's",'his','boy','boyfriend','boyfriends','boys','brother','brothers','dad','dads','dude','father','fathers','fiance','gentleman','gentlemen','god','grandfather','grandpa','grandson','groom','he','himself','husband','husbands','king','male','man','mr','nephew','nephews','priest','prince','son','sons','uncle','uncles','waiter','widower','widowers']
    female_words=['heroine','spokeswoman','chairwoman',"women's",'woman','actress','women',"she's",'her','aunt','aunts','bride','daughter','daughters','female','fiancee','girl','girlfriend','girlfriends','girls','goddess','granddaughter','grandma','grandmother','herself','ladies','lady','lady','mom','moms','mother','mothers','mrs','ms','niece','nieces','priestess','princess','queens','she','sister','sisters','waitress','widow','widows','wife','wives','woman']

update_stats() - storing all the msgs to the global list and then depending on the user commad saving stats to the files

    this stats include (msg if the given files are not .txt) (if not .txt give msg) (if no files in the folder) (display each redacted status and stats like number of words/sents that are redacted from file that too based on given flags) (specify where the file is saved with .redacted)
    based on the user commad if stderr - save to stderr.log file and if stdout - printout and save it on stdout.log 
    if not save it on other given file. if no file is given then save it on to the default stats file

    sample stats:

        $$2019-03-14 04:48:35.723604$$

        all considered files from current and specifed folder(s) are 

        stats.txt
        data1.txt
        data2.txt
        datafilesfolder/mermaid.txt
        datafilesfolder/grant.txt
        datafilesfolder/ghandhi.txt
        datafilesfolder/threebear.txt

        ==========================stats.txt============================


        CONCEPT REDACTION 
        There are no similar or exact concept sentences to redact


        NAMES REDACTION 
        There are no names to redact


        ADDRESS REDACTION 
        There are no addresses to redact

        DATES REDACTION 
        There are total :: 2 words which are redacted from this file 
        ['19-03-13']['20:27']


        GENDER REDACTION 
        There are no gender words to redact


        save all redacted files to the given folder called : outputfiles

        final redacted file name :stats.redacted

        ==========================data1.txt============================


        CONCEPT REDACTION 
        There are no similar or exact concept sentences to redact


        NAMES REDACTION 
        There are total :: 31 words which are redacted from this file 
        ['Barack', 'Hussein Obama II', 'Honolulu', 'Harvard Law School', 'Harvard Law Review', 'Illinois Senate', 'Hillary Clinton', 'John McCain', 'Obama', 'Patient Protection Affordable Care Act', 'Ask', 'Job Creation', 'Great Recession', 'Budget Control American Taxpayer Relief Acts', 'Libya', 'Muammar Gaddafi', 'Gaddafi', 'Osama', 'Laden', 'Yemeni', 'Donald', 'John Trump', 'Queens', 'Wharton School', 'Queens Brooklyn Manhattan', 'Trump', 'Miss Universe Miss', 'Trump', 'Trump', 'Trump', 'Hillary Clinton']


        ADDRESS REDACTION 
        There are total :: 14 words which are redacted from this file 
        ['American', 'United States', 'U.S.', 'Hawaii', 'Chicago', 'U.S.', 'U.S.', 'Afghanistan', 'United', 'Iraq', 'United States', 'New York City', 'Forbes', 'American']


        DATES REDACTION 
        There are total :: 3 words which are redacted from this file 
        ['August 4, 1961', 'January 20, 2009', 'June 14, 1946'][]
        ....
        ...


store_output() - based on the user arguments save all the .redacted files into the specified folder if not into the default folder

    ├── project1
    │   ├── __pycache__
    │   │   └── main.cpython-37.pyc
    │   ├── default_outputfiles
    │   │   ├── grant.redacted
    │   │   └── mermaid.redacted
        time = re.compile(r'\d{1,2}:\d{2} ?(?:[ap]\.?m\.?)?|\d[ap]\.?m\.?', re.IGNORECASE)
    │   ├── default_stats
    │   ├── empty.txt
    │   ├── grant.txt
    │   ├── main.py
    │   ├── mermaid.txt
    │   ├── otherfiles
    │   │   ├── data1.txt
    │   │   └── emptydata.txt
    │   └── outputfiles
    │       ├── data1.redacted
    │       ├── data2.redacted
    │       ├── gandhi.redacted
    │       ├── grant.redacted
    │       ├── mermaid.redacted
    │       └── threebears.redacted


Excecute file:
    
    python main.py --input '*.txt' --input 'datafilesfolder/*.txt' --names --addresses --phones --dates --gender --concept 'prison' --output 'outputfiles' --stats stderr

    sample redacted file :

        maiden name: Nicholson
        SSN: 138-50-9017
        CCN: 341415130141714
        Drivers: a███████
        Passport: █████████
        Password: june @ 8 !
        bank account: 5328713-589
        DoB: █████████
        Address: 1726, ██████████, ███████████, CA, 90017, US
        Phone: ████████████
        emp id: Z009846S
        As of ████████████ the SSNs below could not have been issued by the Social Security Administration and are therefore "fake." So you can view this file in Identity Finder we are placing one real SSN below. The purpose of this file is to show how Identity Finder eliminates false positives even when they look absolutely real .
        ████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████ ████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████

        ████████████████████████████████████████████████████████████████████████████████████ Their perceived opponents may be imprisoned for political crimes, often without trial or other legal due process; this use is illegal under most forms of international law governing fair administration of justice. In times of war, prisoners of war or

        ███ is a good ████
        ██ is trying to

run test files using : pipenv run python setup.py test
There are 6 test files

        ├── test_concept.py
        ├── test_dates.py
        ├── test_gender.py
        ├── test_locs.py
        ├── test_names.py
        └── test_phones.py

