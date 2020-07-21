from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse

# my imports
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User,Listing,Categorie,Comment,Bid, Watchlist
from django.db.models import Max

# FORMS
class NewListingForm(forms.Form):
    title= forms.CharField(max_length=50,label="Title")
    categorie= forms.ModelChoiceField(queryset=Categorie.objects.all())
    description= forms.CharField(widget=forms.Textarea)
    image_url = forms.CharField(widget=forms.URLInput)
    base_bid= forms.DecimalField(max_digits=6,decimal_places=2)

class NewCommentForm(forms.Form):
    comment= forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control',
        'rows':3}))

class NewBidForm(forms.Form):
    bid= forms.DecimalField(decimal_places=2, max_digits=6)

# VIEWS
def index(request):
    return render(request, "auctions/index.html",{
            "listings": Listing.objects.all()
        })

def listing(request, listing_id):
    try:
        listing= Listing.objects.get(id=listing_id)
        comments= Comment.objects.filter(listing_id=listing_id)
    except Listing.DoesNotExist:
        raise Http404("Listing doesn't found")
    
    user_autentidate=request.user.is_authenticated
    max_bid = Bid.objects.filter(listing_id = listing_id).aggregate(Max('bid'))

    if request.method=="POST":

        if 'watchlist_button' in request.POST:
            if user_autentidate:
                watchlist,created = Watchlist.objects.update_or_create(
                    listing= listing,
                    author= request.user,
                    defaults={'watchlist': True},
                    )

                messages.info(request, 'Item have added to watchlist')
                return HttpResponseRedirect(reverse('listing',args=[listing_id]))
            else:
                messages.error(request,'You should be authenticated to add item to watchlist')
                return HttpResponseRedirect(reverse('listing',args=[listing_id]))
            
        elif 'bid_submit' in request.POST:
            bid_form = NewBidForm(request.POST)

            if user_autentidate and bid_form.is_valid():
                bid_price= bid_form.cleaned_data["bid"]

                print(f"{max_bid['bid__max']}")
                if bid_price >= listing.base_bid and bid_price > float(-1 if max_bid['bid__max'] is None else max_bid['bid__max'] ):
                    bid= Bid.objects.create(
                        author=request.user,
                        listing=listing,
                        bid= bid_form.cleaned_data["bid"]
                    )
                    bid.save()

                    listing=Listing.objects.get(id=listing_id)
                    listing.current_bid= bid_price
                    listing.save(update_fields=['current_bid'])

                    messages.info(request, 'Your bid have been added')
                    return HttpResponseRedirect(reverse('listing',args=[listing_id]))
                else:
                    messages.warning(request, "Your bid should be more higt that current bid")
                    return HttpResponseRedirect(reverse('listing',args=[listing_id]))
            else:
                messages.error(request,'You should be authenticated make a bid')
                return render(request,"auctions/listing.html",{
                    'listing': listing,
                    'comments': comments,
                    'form': NewCommentForm(),
                    'bid_form': NewBidForm()
                })
        elif 'Close_bid_submit' in request.POST:
            listing=Listing.objects.get(id=listing_id)
            listing.state= False
            listing.save(update_fields=['state'])

            messages.warning(request, 'Your have been close this listing')
            return HttpResponseRedirect(reverse('listing',args=[listing_id]))
            
        elif 'comment_submit' in request.POST:
            form= NewCommentForm(request.POST)

            if user_autentidate:
                if form.is_valid():
                    comment=Comment.objects.create(
                            author= request.user,
                            listing=listing,
                            comment= form.cleaned_data["comment"]
                        )
                    comment.save()
                    return HttpResponseRedirect(reverse('listing',args=[listing_id]))
            else:
                messages.error(request,'You should be authenticated make a bid')
                return render(request,"auctions/listing.html",{
                    'listing': listing,
                    'comments': comments,
                    'form': NewCommentForm(),
                    'bid_form': NewBidForm()
                })
    
    if max_bid['bid__max'] is not None:
        # bid=Bid.objects.get(listing_id= listing_id, bid=max_bid['bid__max'])    
        bid= Bid.objects.get(listing_id=listing_id,bid=max_bid['bid__max'])
    else:
        bid= None

    print(f"{max_bid['bid__max']}")
    return render(request, "auctions/listing.html",{
                'listing': listing,
                'comments': comments,
                'form': NewCommentForm(),
                'bid_form': NewBidForm(),
                'bid': bid
                })

# modify
@login_required(redirect_field_name='my_redirect_field')
def categories(request):
    return render(request,"auctions/categories.html",{
        'categories': Categorie.objects.all()
    })

@login_required(redirect_field_name='my_redirect_field')
def categorie_page(request,name):
    return render(request,"auctions/categorie_name.html",{
        'listings': Listing.objects.filter(categorie__categorie_name=name)
    })

@login_required(redirect_field_name='my_redirect_field')
def watchlist(request):

    if request.method == "POST":
        listing_id = request.POST["build"]
        
        watchlist = Watchlist.objects.get(listing_id= listing_id, author= request.user )
        watchlist.watchlist=False
        watchlist.save(update_fields=['watchlist'])

        messages.warning(request, 'Element have been removed from your watchlist successfully!')
        return render(request,"auctions/watchlist.html",{
        'watchlists': Watchlist.objects.filter(author=request.user)
        })
    else:
        return render(request,"auctions/watchlist.html",{
            'watchlists': Watchlist.objects.filter(author=request.user)
        })

@login_required(redirect_field_name='my_redirect_field')
def new_listing(request):

    if request.method == "POST":
        form= NewListingForm(request.POST)
        
        if form.is_valid():
            listing = Listing.objects.create(
                title= form.cleaned_data['title'],
                categorie= form.cleaned_data['categorie'],
                description= form.cleaned_data['description'],
                image_url= form.cleaned_data['image_url'],
                base_bid= form.cleaned_data['base_bid'],
                author= request.user
            )
            listing.save()
            messages.info(request, 'Your listing has been added successfully!')
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request,"auctions/new-listing.html",{
                    'forms': NewListingForm()
            })
    else:
        return render(request,"auctions/new-listing.html",{
            'forms': NewListingForm()
        })

# old version
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
