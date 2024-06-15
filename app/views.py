from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from .models import Agenda, CentroMedico, Especialista, Cita
from .forms import AgendaForm, CitaForm

class HomeView(TemplateView):
    template_name = 'home.html'

class ContactView(TemplateView):
    template_name = 'contacto.html'

class AgendaListView(ListView):
    model = Agenda
    template_name = 'agendas.html'
    context_object_name = 'agendas'
    paginate_by = 10

    def get_queryset(self):
        queryset = Agenda.objects.all()
        centro_medico = self.request.GET.get('centro_medico')
        especialista = self.request.GET.get('especialista')
        fecha_disponible = self.request.GET.get('fecha_disponible')

        if centro_medico:
            queryset = queryset.filter(centro_medico__id=centro_medico)
        if especialista:
            queryset = queryset.filter(especialista__id=especialista)
        if fecha_disponible:
            queryset = queryset.filter(fecha_disponible=fecha_disponible)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['centros_medicos'] = CentroMedico.objects.all()
        context['especialistas'] = Especialista.objects.all()
        return context

class AgendaDetailView(DetailView):
    model = Agenda
    template_name = 'agenda_detail.html'
    context_object_name = 'agenda'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cita_form'] = CitaForm()
        return context

@method_decorator(login_required, name='dispatch')
class AgendaCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Agenda
    form_class = AgendaForm
    template_name = 'agenda_form.html'
    success_url = reverse_lazy('agendas')

    def test_func(self):
        return self.request.user.tipo_usuario == 'admin'

@login_required
def create_cita(request, pk):
    agenda = get_object_or_404(Agenda, pk=pk)
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.agenda = agenda
            cita.usuario = request.user
            cita.save()
            return redirect('agenda_detail', pk=pk)
    else:
        form = CitaForm()
    return render(request, 'agenda_detail.html', {'agenda': agenda, 'cita_form': form})