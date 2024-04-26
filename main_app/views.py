from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Finch, Cage
from .forms import FeedingForm


# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def finches_index(request):
    finches = Finch.objects.all()
    return render(request, 'finches/index.html', {
        'finches': finches
    })
def finch_detail(request, finch_id):
    finch = Finch.objects.get(id=finch_id)
    id_list = finch.cages.all().values_list('id')
    cages_that_finch_dosent_have = Cage.objects.exclude(id__in=id_list)
    feeding_form = FeedingForm()
    return render(request, 'finches/details.html', {
        'finch': finch,
        'feeding_form': feeding_form,
        'cages': cages_that_finch_dosent_have    
    })

def assoc_cage(request, finch_id, cage_id):
  Finch.objects.get(id=finch_id).cages.add(cage_id)
  return redirect('detail', finch_id=finch_id)

def unassoc_cage(request, finch_id, cage_id):
  Finch.objects.get(id=finch_id).cages.remove(cage_id)
  return redirect('detail', finch_id=finch_id)

class FinchCreate(CreateView):
    model = Finch
    fields = '__all__'

class FinchUpdate(UpdateView):
    model = Finch
    fields = ('color', 'size')

class FinchDelete(DeleteView):
    model = Finch
    success_url = '/all_finches/'

def add_feeding(request, finch_id):
  # create a ModelForm instance using 
  # the data that was submitted in the form
  form = FeedingForm(request.POST)
  # validate the form
  if form.is_valid():
    # We want a model instance, but
    # we can't save to the db yet
    # because we have not assigned the
    # cat_id FK.
    new_feeding = form.save(commit=False)
    new_feeding.finch_id = finch_id
    new_feeding.save()
  return redirect('detail', finch_id=finch_id)


class CageList(ListView):
  model = Cage

class CageDetail(DetailView):
  model = Cage

class CageCreate(CreateView):
  model = Cage
  fields = '__all__'

class CageUpdate(UpdateView):
  model = Cage
  fields = ['material', 'color']

class CageDelete(DeleteView):
  model = Cage
  success_url = '/cages'