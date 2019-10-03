"""programs views"""

from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView
)

from .forms import (
    ProgramModelForm,
    RunOnceProgramModelForm,
    PeriodicProgramModelForm,
    WeeklyProgramModelForm,
)
from .models import Program

#pylint: disable=arguments-differ


class ProgramsHomeView(ListView):
    "General info about the programs"
    template_name = "programs/home.html"
    queryset = Program.objects.filter(enabled=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # additional context
        context["pagetitle"] = "Programs"
        return context


class ProgramListView(ListView):
    "Display the list of all Programs"
    template_name = "programs/list.html"
    queryset = Program.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # additional context
        context["pagetitle"] = "List of Programs"
        return context


class ProgramDetailView(DetailView):
    "Dispaly the details of Program given by id"
    template_name = "programs/detail.html"
    queryset = Program.objects.all()  # optional filter

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Program, id=id_)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # additional context
        context["pagetitle"] = "Program Details"
        return context


class ProgramCreateView(View):
    "Create a new program"
    template_name = "programs/create.html"

    def get(self, request, *args, **kwargs):
        "GET request handler"
        context = {
            "pagetitle": "Create New Program"
        }
        return render(request, self.template_name, context)


class ProgramUpdateView(UpdateView):
    "Update a program"
    #TODO switch on program type 
    template_name = "programs/create.html"
    form_class = ProgramModelForm

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Program, id=id_)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # additional context
        context["pagetitle"] = "Update Program"
        return context

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class ProgramDeleteView(DeleteView):
    "Create a new program"
    template_name = "programs/delete.html"

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Program, id=id_)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # additional context
        context["pagetitle"] = "Delete Program"
        return context

    def get_success_url(self):
        return reverse("programs:home")


class CreateViewMixin(object):
    "Create View methods common for all program types"

    def get_context_data(self, **kwargs):
        "Set additional key-value pairs"
        context = super().get_context_data(**kwargs)
        context["pagetitle"] = "Create New Program"
        return context

    def form_valid(self, form):
        "Validation method"
        print(form.cleaned_data)
        return super().form_valid(form)


class RunOnceProgramCreateView(CreateViewMixin, CreateView):
    "Create a new program"
    template_name = "programs/create_run-once.html"
    form_class = RunOnceProgramModelForm


class PeriodicProgramCreateView(CreateViewMixin, CreateView):
    "Create a new program"
    template_name = "programs/create_periodic.html"
    form_class = PeriodicProgramModelForm


class WeeklyProgramCreateView(CreateViewMixin, CreateView):
    "Create a new program"
    template_name = "programs/create_weekly.html"
    form_class = WeeklyProgramModelForm
