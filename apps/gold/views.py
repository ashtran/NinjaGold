from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime

def goldrandom(lower,upper): # random gold generator function
    import random
    goldvalue=random.randrange(lower,upper)
    return goldvalue

def index(request):
    return render(request, 'gold/index.html')

def process(request,location):
    goldearn={'farm': goldrandom(10,21),'cave': goldrandom(5,11),'house': goldrandom(2,6),'casino': goldrandom(-50,51)}
    #<--- location & gold earned--->#
    request.session['gold']=goldearn[location]
    gold= request.session['gold']
    time= datetime.now().strftime(" - added on %H:%M %p, %B %d, %Y")
    #<--- gold total --->#
    try:
        request.session['total']
    except KeyError:
        request.session['total']=0
    request.session['total']+=gold
    #<--- activity log--->#
    if 'activities' not in request.session:
        request.session['activities']=[]
    else:
        request.session['activities']=request.session['activities']

    if gold>0:
        activity= "Earned {} golds from the {}! {}".format(gold,location,time)
    else:
        activity= "Entered a {} and lost {} golds... Ouch.. {}".format(location,gold,time)

    log={'activity':activity}
    request.session['activities'].append(log) # append the activity log
    return redirect('/')

def clear(request):
    del request.session['total']
    del request.session['activities']
    return redirect('/')
