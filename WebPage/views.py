from typing import Any
from datetime import datetime
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from WebPage.models import CarModel
from WebPage.Parsing import CopartParse


class CarsView(TemplateView):
    template_name = 'WebPage/index2.html'

    def get_context_data(self, **kwargs):
        context = super(CarsView, self).get_context_data()
        context['title'] = 'Cars'
        context['cars'] = CarModel.objects.all()

        return context


class CarsListView(ListView):
    model = CarModel
    template_name = 'WebPage/index2.html'

    def get_context_data(self, **kwargs):
        context = super(CarsListView, self).get_context_data()
        context['title'] = 'Cars'
        context['cars'] = CarModel.objects.all()

        return context

def refresh_bd(request):
    CarModel.objects.filter(date__lt=datetime.now()).delete()
    copart = CopartParse(url='https://www.copart.com/lotSearchResults?free=false&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%22VEHT%22:%5B%22vehicle_type_code:VEHTYPE_V%22%5D,%22ODM%22:%5B%22odometer_reading_received:%5B0%20TO%209999999%5D%22%5D,%22YEAR%22:%5B%22lot_year:%5B2019%20TO%202024%5D%22%5D%7D,%22searchName%22:%22%22,%22watchListOnly%22:false,%22freeFormSearch%22:false%7D%20&displayStr=Search%20vehicles&from=%2FvehicleFinder', count_page=1)
    copart.parse()
    copart.quit()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
