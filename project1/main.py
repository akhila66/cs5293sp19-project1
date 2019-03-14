# import getopt
import glob
import argparse
import re
import nltk
import os
import ntpath
from datetime import datetime  
import sys
from nltk import tag 
from copy import deepcopy
from nltk.corpus import wordnet 
# nltk.download('wordnet')
from nltk.corpus import stopwords
# nltk.download('stopwords')
stop = stopwords.words('english')
from statistics import mean 
def getfiles(inp):
    filelist = []
    msgs = []
    for all in inp:
        for file in all:
            if file.endswith('.txt'):
                filelist.append(file)
            else:
                msgs.append("\n"+"="*20+" MSG : Only text files are considered. Please try again"+"="*20+"\n")
                break
    if not filelist:
        msgs.append("="*40+" MSG : There are no text files. please check "+"="*40+"\n")
    else:
        msgs.append("\nall considered files from current and specifed folder(s) are \n")
        for f in filelist:
            msgs.append(f)

    return filelist,msgs     

def redact_names(text):
    names = []
    # red_names_locs = document 
    red_names = deepcopy(text)
    document = ' '.join([i for i in text.split() if i not in stop])
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    # print(sentences)
    for tagged_sentence in sentences:
        # print(tagged_sentence)
        for chunk in nltk.ne_chunk(tagged_sentence):
            if type(chunk) == nltk.tree.Tree: 
                if(chunk.label() == 'PERSON'):
                    c1 = ' '.join([c1[0] for c1 in chunk])
                    names.append(c1)
                    b1 = "█"*(len(c1))
                    red_names = red_names.replace(c1,b1)
    return red_names,names

def redact_locs(text):
    locs = []
    # red_names_locs = document 
    red_locs = deepcopy(text)
    document = ' '.join([i for i in text.split() if i not in stop]) #removing stop words
    sentences = nltk.sent_tokenize(document) #get sentences
    sentences = [nltk.word_tokenize(sent) for sent in sentences] #get words from sentences
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    # print(sentences)
    for tagged_sentence in sentences:
        # print(tagged_sentence)
        for chunk in nltk.ne_chunk(tagged_sentence):
            if type(chunk) == nltk.tree.Tree: 
                if(chunk.label() == 'GPE'):
                    c2 = ' '.join([c2[0] for c2 in chunk])
                    locs.append(c2)
                    b2 = "█"*(len(c2))
                    red_locs = red_locs.replace(c2,b2)
                
    return red_locs,locs

def redact_phones(text):
    red = deepcopy(text)
    phone = re.compile(r'''((?:(?<![\d-])(?:\+?\d{1,3}[-.\s*]?)?(?:\(?\d{3}\)?[-.\s*]?)?\d{3}[-.\s*]?\d{4}(?![\d-]))|(?:(?<![\d-])(?:(?:\(\+?\d{2}\))|(?:\+?\d{2}))\s*\d{2}\s*\d{3}\s*\d{4}(?![\d-])))''')
    phones = re.findall(phone,text)
    for j in phones:
        b1 = "█"*(len(j))
        red = red.replace(j,b1)
    return red,phones

def redact_dates_times(text):
    red = deepcopy(text)
    date = re.compile(r'(?:(?<!\:)(?<!\:\d)[0-3]?\d(?:st|nd|rd|th)?\s+(?:of\s+)?(?:jan\.?|january|feb\.?|february|mar\.?|march|apr\.?|april|may|jun\.?|june|jul\.?|july|aug\.?|august|sep\.?|september|oct\.?|october|nov\.?|november|dec\.?|december)|(?:jan\.?|january|feb\.?|february|mar\.?|march|apr\.?|april|may|jun\.?|june|jul\.?|july|aug\.?|august|sep\.?|september|oct\.?|october|nov\.?|november|dec\.?|december)\s+(?<!\:)(?<!\:\d)[0-3]?\d(?:st|nd|rd|th)?)(?:\,)?\s*(?:\d{4})?|[0-3]?\d[-\./][0-3]?\d[-\./]\d{2,4}', re.IGNORECASE)
    dates = re.findall(date,text)
    time = re.compile(r'\d{1,2}:\d{2} ?(?:[ap]\.?m\.?)?|\d[ap]\.?m\.?', re.IGNORECASE)
    times = re.findall(time,text)
    for i in dates:
        b1 = "█"*(len(i))
        red = red.replace(i,b1)
    for k in times:
        b1 = "█"*(len(k))
        red = red.replace(k,b1)
    return red,dates,times

def redact_concept(text,concept):

    w1 = wordnet.synsets(concept)
    # print(w1) 
    red_concept = deepcopy(text)
    # document = ' '.join([i for i in text.split() if i not in stop]) #removing stop words
    sentences = nltk.sent_tokenize(text) #get sentences
    all_sim_words = []
    all_red_sents = []
    for sent in sentences:
        sim_words = []
        words = nltk.word_tokenize(sent)
        for word in words:
            w2 = wordnet.synsets(word)
            average = 0
            if w2:
                all = []
                for i in w1:
                    for j in w2:
                        if (i.wup_similarity(j) is not None and i.wup_similarity(j) > 0.5 ):
                            # print(str(i.wup_similarity(j))+"==="+str(i)+"===="+str(j))
                            all.append(i.wup_similarity(j))
                
                if all:
                    average = mean(all)
                # print(average)
            if(average >= 0.9):
                # print(word)
                sim_words.append(word)

        if sim_words:
            # print(sim_words)           
            b= "█"*(len(sent))
            # print(sent)
            red_concept = red_concept.replace(sent,b)
            all_red_sents.append(sent)
            all_sim_words.extend(sim_words)
    # print(red_concept)
    return red_concept,all_sim_words,all_red_sents

def redact_gender(text):
    red_gender = deepcopy(text)
    # http://nealcaren.github.io/text-as-data/html/times_gender.html
    male_words=['guy','spokesman','chairman',"men's",'man','men','him',"he's",'his','boy','boyfriend','boyfriends','boys','brother','brothers','dad','dads','dude','father','fathers','fiance','gentleman','gentlemen','god','grandfather','grandpa','grandson','groom','he','himself','husband','husbands','king','male','man','mr','nephew','nephews','priest','prince','son','sons','uncle','uncles','waiter','widower','widowers']
    female_words=['heroine','spokeswoman','chairwoman',"women's",'woman','actress','women',"she's",'her','aunt','aunts','bride','daughter','daughters','female','fiancee','girl','girlfriend','girlfriends','girls','goddess','granddaughter','grandma','grandmother','herself','ladies','lady','lady','mom','moms','mother','mothers','mrs','ms','niece','nieces','priestess','princess','queens','she','sister','sisters','waitress','widow','widows','wife','wives','woman']
    gender_words = []
    # -------------- using some asumptions this peice of code is made
    # for m in male_words:
    #     b1 = "\n"+"█"*(len(m))+" "
    #     m1 = '(?i)\n('+re.escape(m)+')\s'
    #     red_gender = re.sub(m1,b1,red_gender)
    #     b2 = " "+"█"*(len(m))+"\n"
    #     m2 = '(?i)\s('+re.escape(m)+')\n'
    #     red_gender = re.sub(m2,b2,red_gender)
    #     b3 = " "+"█"*(len(m))
    #     m3 = '(?i)\s('+re.escape(m)+')[\.|\!|\,|\;]'
    #     red_gender = re.sub(m3,b3,red_gender)
    #     b4 = " "+"█"*(len(m))+" "
    #     m4 = '(?i)\s('+re.escape(m)+')\s'
    #     red_gender = re.sub(m4,b4,red_gender)
    #     print(m)
    #     gender_words.append(m)  
    # for f in female_words:
    #     b1 = "\n"+"█"*(len(f))+" "
    #     f1 = '(?i)\n('+re.escape(f)+')\s'
    #     red_gender = re.sub(f1,b1,red_gender)
    #     b2 = " "+"█"*(len(f))+"\n"
    #     f2 = '(?i)\s('+re.escape(f)+')\n'
    #     red_gender = re.sub(f2,b2,red_gender)
    #     b3 = " "+"█"*(len(f))
    #     f3 = '(?i)\s('+re.escape(f)+')[\.|\!|\,|\;]'
    #     red_gender = re.sub(f3,b3,red_gender)
    #     b4 = " "+"█"*(len(f))+" "
    #     f4 = '(?i)\s('+re.escape(f)+')\s'
    #     red_gender = re.sub(f4,b4,red_gender)
    #     print(f)
    #     gender_words.append(f)
    # print(red_gender)
    # --------- using this can detokonize but cannot maintain the same indentation and spaces its following
    sents = text.split("\n")
    red_sents = []
    for sent in sents:
        red_words = []
        words = nltk.word_tokenize(sent)
        for word in words:
            if word.upper() in (name.upper() for name in male_words) or word.upper() in (name.upper() for name in female_words):
            # if word in male_words or word in female_words:
                gender_words.append(word)
                b = "█"*(len(word))
                red_words.append(b)
            else:
                red_words.append(word)
        red_sents.append(" ".join(red_words))
    red_text = "\n".join(red_sents)
    step1 = red_text.replace("`` ", '"').replace(" ''", '"')
    step2 = step1.replace(" ( ", " (").replace(" ) ", ") ")
    step3 = re.sub(r' ([.,:;?!%]+)([ \'"`])', r"\1\2", step2)
    step4 = re.sub(r' ([.,:;?!%]+)$', r"\1", step3)
    step5 = step4.replace(" '", "'").replace(" n't", "n't").replace("can not", "cannot")
    step6 = step5.replace(" ` ", " '")
    red_text = step6.strip()
    # print(red_text)
    return red_text,gender_words

def update_stats(statsfile,msgs):
    if statsfile == "stderr" :
        er = open('stderr.log','w+') 
        sys.stderr = er 
        for m in msgs:
            print(m, file=sys.stderr)
                    
    elif statsfile == "stdout" :
        out = open('stdout.log','w+')
        sys.stdout = out
        for m in msgs:
            print(m)
    else:
        f = open(statsfile,'w+')
        for m in msgs:
            f.write(m)

def store_output(output_folder,filename,text):
    head, tail = ntpath.split(filename)
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    f= open(output_folder+"/"+tail,"w+")
    f.write(text)
    f.close() 

if __name__ == '__main__':
    # print("MAIN FILE RUNNING")
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=glob.glob, required=True, action='append', nargs = '?',
                         help="Please make sure there are .text input files in current or specified folder.")
    parser.add_argument("--names",action='store_true')
    parser.add_argument("--dates",action='store_true')
    parser.add_argument("--addresses",action='store_true')
    parser.add_argument("--gender",action='store_true')
    parser.add_argument("--phones",action='store_true')
    parser.add_argument("--concept", type=str)
    parser.add_argument("--output", type=str)
    parser.add_argument("--stats",type=str)
    args = parser.parse_args()
    # print(args)
    msgs = []
    if args.input:
        inputs = args.input
        msgs.append("\n$$"+str(datetime.now())+"$$")
        (files,m) = getfiles(inputs)
        msgs.extend(m)
        for file in files:
            msgs.append("\n=========================="+file+"============================\n")
            fileopen = open(file, "r") 
            string =  fileopen.read() 
            if(string != ""):
                if args.concept:
                    (string,similar_words,red_s) = redact_concept(string,args.concept)
                    if similar_words:
                        msgs.append("\nCONCEPT REDACTION \n"+"There are total :: "+str(len(similar_words))+" similar words from this file \n "+str(similar_words)+"\n")
                        msgs.append("\nTotal redacted sentences from this similar concepts are :: "+str(len(red_s))+"\n")
                        for i,s in enumerate(red_s):
                            msgs.append("======\n[ "+str(i)+" ]-"+s+"\n")
                    else:
                        msgs.append("\nCONCEPT REDACTION \n"+"There are no similar or exact concept sentences to redact\n")
                if args.names:
                    (string,names) = redact_names(string)
                    if names:
                        msgs.append("\nNAMES REDACTION \n"+"There are total :: "+str(len(names))+" words which are redacted from this file \n "+str(names)+"\n")
                    else:
                        msgs.append("\nNAMES REDACTION \n"+"There are no names to redact\n")
                if args.addresses:
                    (string,locs) = redact_locs(string)
                    if locs:
                        msgs.append("\nADDRESS REDACTION \n"+"There are total :: "+str(len(locs))+" words which are redacted from this file \n "+str(locs)+"\n")
                    else:
                        msgs.append("\nADDRESS REDACTION \n"+"There are no addresses to redact")
                if args.phones:
                    (string,phones)= redact_phones(string)
                    if phones:
                        msgs.append("\nPHONE NUMBER REDACTION \n"+"There are total :: "+str(len(phones))+" numbers which are redacted from this file \n "+str(phones)+"\n")
                    else:
                        msgs.append("\nPHONE NUMBER REDACTION \n"+"There are no phone numbers to redact")
                if args.dates:
                    (string,dates,times)= redact_dates_times(string)
                    if dates or times:
                        msgs.append("\nDATES REDACTION \n"+"There are total :: "+str(len(dates)+len(times))+" words which are redacted from this file \n "+str(dates)+str(times)+"\n")
                    else:
                        msgs.append("\nDATES REDACTION \n"+"There are no dates or times to redact")
                if args.gender:
                    (string,gender)= redact_gender(string)
                    if gender:
                        msgs.append("\nGENDER REDACTION \n"+"There are total :: "+str(len(gender))+" words which are redacted from this file \n "+str(gender)+"\n")
                    else:
                        msgs.append("\nGENDER REDACTION \n"+"There are no gender words to redact\n")
                if args.output:
                    msgs.append("\nsave all redacted files to the given folder called : " + args.output)
                    msgs.append("\nfinal redacted file name :"+file[:-4]+".redacted")
                    store_output(args.output,file[:-4]+".redacted",string)
                else:
                    msgs.append("\nNo output folder is given - saves it to the default folder called outputfiles\n")
                    msgs.append("\nfinal redacted file name :"+file[:-4]+".redacted")
                    store_output("default_outputfiles",file[:-4]+".redacted",string)
            else:
                msgs.append("\nNO DATA to redact")
    if args.stats:
        msgs.append("\nEND OF STATS : saving stats into the file "+ args.stats+"\n\n")
        update_stats(args.stats,msgs)
    else:
        msgs.append("\nNo stats file is given - saves it to the default file called default_stats\n")
        msgs.append("\nEND OF STATS : saving stats into the file default_stats\n\n")
        update_stats("default_stats",msgs)
                
                
                # print(string)ls


    # print(args.names,args.addresses,args.dates,args.phones,args.concept,args.output,args.stats)
# python3 firsttest.py --input '*.txt' --input 'datafilesfolder/*.txt' --names --addresses --dates --gender --concept 'akhila' --output 'outputfiles' --stats staerr
# args = (parser.parse_args("--input *.txt --input datafilesfolder/*.txt --input *.py --names --addresses --dates --gender --concept mining".split()))

