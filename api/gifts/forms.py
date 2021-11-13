import random
import gifts.models as models
from django.utils.safestring import mark_safe

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout


class GiftForm(forms.Form):
    class Meta:
        model = models.Gift

    address = forms.CharField(
        label=mark_safe('<strong>Address</strong>'),
        required=True,
        widget=forms.Textarea(attrs={
            'rows': 3,
        }),
    )
    choice = forms.ChoiceField(
        label=mark_safe('<strong>Choice</strong>'),
        required=True,
        widget=forms.RadioSelect,
    )
    suggestion = forms.CharField(
        label=mark_safe('<strong>Suggestions</strong>'),
        required=False,
        widget=forms.Textarea(
            attrs={
                'rows': 3,
                'placeholder': 'What other local businesses should we support?'
            }),
    )

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('Submit', 'Submit', css_class='btn btn-success'))
    helper.layout = Layout(
        'choice',
        'address',
        'suggestion',
    )

    def __init__(self, gift, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # prepopulate address with latest gift address
        if models.Gift.objects.filter(user=gift.user).count() > 1:
            self.fields['address'].initial = models.Gift.objects.filter(
                user=gift.user).exclude(
                    id=gift.id).order_by('created').last().address

        choices = [(x.id, ' {}'.format(x.title)) for x in gift.choices.all()]
        random.shuffle(choices)
        choices += [(
            0,
            mark_safe(' Defer <i>(If you don\'t like any of these, we\'ll carry over your ${:,.2f} gift the next time you get chosen)</i>'
            .format(gift.get_amount() / 100)),
        )]

        self.fields['choice'].choices = choices
        self.fields['choice'].label = mark_safe(
            '<strong>Choice (${:,.2f} Gift Cards)</strong>'.format(
                gift.get_amount() / 100))
