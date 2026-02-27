from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, UpdateView
from .models import Objective
from .forms import ObjectiveForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator


@login_required
def FinishedObjectiveView(request, pk):
    objective = get_object_or_404(Objective, id=pk)
    objective.status = True
    objective.save()
    return redirect('home:list_objective')

# class IndexView(TemplateView):
#     template_name = 'home/index.html'


class ObjectiveListView(LoginRequiredMixin, ListView):
    model = Objective
    template_name = 'home/index.html'
    context_object_name = 'objectives'
    paginate_by = 10


class CreateObjectiveView(LoginRequiredMixin, CreateView):
    model = Objective
    form_class = ObjectiveForm
    # fields = ['title', 'description']
    template_name = 'home/create.html'
    success_url = reverse_lazy('home:list_objective')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_list= Objective.objects.all()
        paginator = Paginator(context_list, 5)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['objectives'] = page_obj
        # print(Objective.objects.all())
        return context

class DeleteObjectiveView(LoginRequiredMixin, DeleteView):
    model = Objective
    template_name = 'home/index.html'
    success_url = reverse_lazy('home:list_objective')

class UpdateObjectiveView(LoginRequiredMixin, UpdateView):
    model = Objective
    form_class = ObjectiveForm
    template_name = 'home/update.html'
    success_url = reverse_lazy('home:list_objective')

    def dispatch(self, request, *args, **kwargs):
        objective = self.get_object()
        if objective.status:
            return HttpResponseForbidden("this task is completed and can not be edited")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        objective = form.instance

        if not form.cleaned_data.get('title'):
            form.instance.title = self.get_object().title
        if not form.cleaned_data.get('description'):
            form.instance.description = self.get_object().description

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_list= Objective.objects.all()
        paginator = Paginator(context_list, 5)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['objectives'] = page_obj
        # print(Objective.objects.all())
        return context