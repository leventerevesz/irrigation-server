"""program forms"""

from django import forms

from .models import Program


class ProgramModelForm(forms.ModelForm):
    "Default Model Form"
    class Meta:
        model = Program
        fields = [
            "name",
            "description",
            "program_type",
            "date_start",
            "date_end",
            "days_of_week",
            "time_start",
            "duration",
            "period",
            "priority",
            "enabled",
        ]

    def __init__(self, *args, **kwargs):
        "Update field definitions with custom attributes"
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({
            "class": "w3-input w3-border",
            "style": "width:20em; display:inline-block;"
        })
        self.fields["description"].widget.attrs.update(
            {"class": "w3-input w3-border", "rows": 3})
        self.fields["program_type"].widget.attrs.update({
            "class": 'w3-select w3-border',
            "style": "width:8em;"
        })
        self.fields["date_start"].widget.attrs.update({
            "class": "w3-input w3-border",
            "style": "width:15em; display:inline-block;",
            "placeholder": "yyyy-mm-dd"
        })
        self.fields["date_end"].widget.attrs.update({
            "class": "w3-input w3-border",
            "style": "width:15em; display:inline-block;",
            "placeholder": "yyyy-mm-dd"
        })
        self.fields["time_start"].widget.attrs.update({
            "class": "w3-input w3-border",
            "style": "width:15em; display:inline-block;",
            "placeholder": "(hh:)mm:ss"
        })
        self.fields["duration"].widget.attrs.update({
            "class": "w3-input w3-border",
            "style": "width:15em; display:inline-block;",
            "placeholder": "(hh:)mm:ss"
        })
        self.fields["period"].widget.attrs.update({
            "class": "w3-input w3-border",
            "style": "width:15em; display:inline-block;",
            "placeholder": "(days) hh:mm(:ss)"
        })
        self.fields["priority"].widget.attrs.update({
            "class": "w3-input w3-border",
            "style": "width:4em; display:inline-block;"
        })
        self.fields["enabled"].widget.attrs.update(
            {"class": "w3-check"})

    def clean_time_start(self):
        "Raise error if field is required but empty"
        time_start = self.cleaned_data.get("time_start")
        if self.cleaned_data.get("program_type") in ("weekly",):
            if time_start is None:
                raise forms.ValidationError(
                    "This field is required for the selected program type.")
        return time_start

    def clean_duration(self):
        "Raise error if field is required but empty"
        duration = self.cleaned_data.get("duration")
        if self.cleaned_data.get("program_type") in ("run-once", "periodic", "weekly"):
            if duration is None:
                raise forms.ValidationError(
                    "This field is required for the selected program type.")
        return duration

    def clean_period(self):
        "Raise error if field is required but empty"
        period = self.cleaned_data.get("period")
        if self.cleaned_data.get("program_type") in ("periodic",):
            if period is None:
                raise forms.ValidationError(
                    "This field is required for the selected program type.")
        return period


class ProgramFormMixin(object):
    "Set common attributes for all program types"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            "class": "w3-input"})
        self.fields['description'].widget.attrs.update({
            "class": "w3-input",
            "rows": 2})
        self.fields['date_start'].required = True
        self.fields['date_start'].widget.attrs.update({
            "class": "w3-input w3-border",
            "placeholder": "yyyy-mm-dd",
            "style": "max-width: 10em"})
        self.fields['time_start'].required = True
        self.fields['time_start'].widget.attrs.update({
            "class": "w3-input w3-border",
            "placeholder": "(hh:)mm:ss",
            "style": "max-width: 10em"})
        self.fields['duration'].widget.attrs.update({
            "class": "w3-input w3-border",
            "placeholder": "(d) (hh:)mm:ss",
            "style": "max-width: 10em"})
        self.fields['priority'].required = True
        self.fields['priority'].widget.attrs.update({
            "class": "w3-input w3-border",
            "type": "number", "min": "1", "max": "10",
            "style": "max-width:4em"})
        self.fields['enabled'].widget.attrs.update({
            "class": "w3-check"})


class RunOnceProgramModelForm(ProgramFormMixin, forms.ModelForm):
    "Run-Once Program Model Form"
    program_type = forms.ChoiceField(
        choices=Program.PROGRAM_TYPES,
        widget=forms.HiddenInput(),
        initial="run-once",
    )

    class Meta:
        model = Program
        fields = [
            "name", "description", "program_type", "date_start", "time_start",
            "duration", "priority", "enabled"
        ]
        widgets = {
            "description": forms.Textarea(),
            "program_type": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super().__init__(*args, **kwargs)
        self.fields['program_type'].initial = "run-once"


class PeriodicProgramModelForm(ProgramFormMixin, forms.ModelForm):
    "Periodic Program Model Form"

    class Meta:
        model = Program
        fields = [
            "name", "description", "program_type", "date_start", "date_end",
            "time_start", "duration", "period", "priority", "enabled"
        ]
        widgets = {
            "description": forms.Textarea(),
            "program_type": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super().__init__(*args, **kwargs)
        self.fields['program_type'].initial = "periodic"
        self.fields['date_end'].widget.attrs.update({
            "class": "w3-input w3-border",
            "placeholder": "yyyy-mm-dd",
            "style": "max-width: 10em"})
        self.fields['period'].required = True
        self.fields['period'].widget.attrs.update({
            "class": "w3-input w3-border",
            "placeholder": "days",
            "style": "max-width: 10em"})


class WeeklyProgramModelForm(ProgramFormMixin, forms.ModelForm):
    "Weekly Program Model Form"
    days_of_week = forms.MultipleChoiceField(
        choices=Program.DAYS_OF_WEEK,
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    class Meta:
        model = Program
        fields = [
            "name", "description", "program_type", "date_start", "date_end",
            "days_of_week", "time_start", "duration", "priority", "enabled"
        ]
        widgets = {
            "description": forms.Textarea(),
            "program_type": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super().__init__(*args, **kwargs)
        self.fields['program_type'].initial = "weekly"
        self.fields['date_end'].widget.attrs.update({
            "class": "w3-input w3-border",
            "placeholder": "yyyy-mm-dd",
            "style": "max-width: 10em"})
        self.fields['days_of_week'].widget.attrs.update({
            "class": "w3-check"})

    def clean_days_of_week(self):
        "Transforms the List of selected days to a String"
        days_of_week = self.cleaned_data.get("days_of_week")
        days_of_week_str = "".join(days_of_week)
        return days_of_week_str
