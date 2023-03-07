from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def register(request):

    # this method "register" is a view that renders the template users/register.html
    # this method can be called in two ways by django
    #   1. when a user navigates to the register page
    #       in this case, the "request" argument of the function will not have any form data in it
    #   2. when a user is already in the register page, and enters data in the form, and presses the submit button.
    #       in this case, the "request" argument will have the form data like username etc, because,
    #       pressing the "Submit" button will make a POST request, so, it will redirect to the same page but with
    #       the user-entered data in it

    if request.method == 'POST':
        # the "if" statement passed, that means, the page is being requested because user pressed the submit button, so,
        # it has user-submitted data in it

        form = UserCreationForm(request.POST)
        # the above creates an instance of the form with the post data, so that, if the
        # user submitted data is not valid, then, the fields will still have the data (i.e. they won't be cleared)

        if form.is_valid():
            form.save()  # this will save the new user to database

            # now we will display a flash message
            # a flash message is displayed only once and it disappears in the next request
            username = form.cleaned_data.get('username')  # cleaned_data is a dictionary
            messages.success(request, f"Account created for {username}!")

            # now, as the form is valid and the new user is created, we redirect the user to other page, because
            # it can be confusing if the form is displayed again
            return redirect("image-filters-home")
    else:
        # we are in the "else" block, that means "request method is not POST", in other words,
        # a user navigated to the register page, so we just create an empty form here in the next line

        form = UserCreationForm()

    # the following line renders a template html and passes the above form variable to it
    return render(request, 'users/register.html', context={'form': form})  # the key-value pairs of the context argument
    # will be accessible in the template users/register.html. The string keys will be the names of the variables that
    # can be used in the template's code-blocks and variable-access-blocks
