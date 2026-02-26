from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, UpdateView
from .models import Objective
from .forms import ObjectiveForm
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy



def FinishedObjectiveView(request, pk):
    objective = get_object_or_404(Objective, id=pk)
    objective.status = True
    objective.save()
    return redirect('home:list_objective')

# class IndexView(TemplateView):
#     template_name = 'home/index.html'


class ObjectiveListView(ListView):
    model = Objective
    template_name = 'home/index.html'
    context_object_name = 'objectives'
    paginate_by = 10

class CreateObjectiveView(CreateView):
    model = Objective
    form_class = ObjectiveForm
    # fields = ['title', 'description']
    template_name = 'home/index.html'
    success_url = reverse_lazy('home:list_objective')

class DeleteObjectiveView(DeleteView):
    model = Objective
    template_name = 'home/index.html'
    success_url = reverse_lazy('home:list_objective')

class UpdateObjectiveView(UpdateView):
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