from dajaxice.decorators import dajaxice_register
from forms import ExampleForm

@dajaxice_register
def send_form(request, form):
    dajax = Dajax()
    form = ExampleForm(form)
    if form.is_valid():
        dajax.remove_css_class('#my_form input','error')
        dajax.alert("This form is_valid(), your username is: %s" % form.cleaned_data.get('username'))
    else:

        dajax.remove_css_class('#my_form input','error')
        for error in form.errors:
        dajax.add_css_class('#id_%s' % error,'error')

    return dajax.json()