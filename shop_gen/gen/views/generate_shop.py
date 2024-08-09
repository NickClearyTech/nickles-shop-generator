from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from gen.forms.generate_shop import GenerateShopForm

from logging import getLogger

logger = getLogger(__name__)


@csrf_protect
def generate_shop(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = GenerateShopForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            logger.error("Form submitted :D")
            return HttpResponseRedirect("/thanks/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = GenerateShopForm()

    return render(request, "generate_shop.html", {"form": form})