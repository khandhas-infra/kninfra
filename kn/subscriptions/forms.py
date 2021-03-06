from django import forms

from kn.leden.forms import EntityChoiceField
import kn.leden.entities as Es

def get_add_event_form(user, superuser=False):
    class AddEventForm(forms.Form):
        name = forms.RegexField(label='Korte naam', regex=r'^[a-z0-9-]+$')
        humanName = forms.CharField(label='Naam')
        description = forms.CharField(label='Beschrijving',
                widget=forms.Textarea)
        subscribedMailBody = forms.CharField(label='E-Mail wanneer aangemeld',
            widget=forms.Textarea,
            initial="Hallo %(firstName)s,\n\n"+
                "Je hebt je aangemeld voor %(eventName)s.\n"+
                "\n"+
                "Je opmerkingen waren:\n"+
                "%(notes)s\n"+
                "\n"+
                "Met een vriendelijke groet,\n\n"+
                "%(owner)s")
        invitedMailBody = forms.CharField(
            label='E-Mail wanneer uitgenodigd',
            widget=forms.Textarea,
            initial="Hallo %(firstName)s,\n\n"+
                "Je bent door %(by_firstName)s uitgenodigd "+
                    "voor %(eventName)s.\n"+
                "\n"+
                "%(by_firstName)s opmerkingen waren:\n"+
                "%(by_notes)s\n"+
                "\n"+
                "Om deze uitnodiging te bevestigen, bezoek:\n"
                "  %(confirmationLink)s\n"+
                "\n"+
                "Met een vriendelijke groet,\n\n"+
                "%(owner)s")
        cost = forms.DecimalField(label='Kosten')
        date = forms.DateField(label='Datum')
        owner = EntityChoiceField(label="Eigenaar")
        has_public_subscriptions = forms.BooleanField(required=False,
                label='Inschrijvingen openbaar')
    return AddEventForm

# vim: et:sta:bs=2:sw=4:
