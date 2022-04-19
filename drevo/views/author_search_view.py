import urllib
from django.urls import reverse_lazy
from ..forms import *
from django.views.generic.edit import FormView
from ..models import *
from django.core.paginator import Paginator
from django.db.models import (Q,
                              QuerySet)
from .search_engine import SearchEngineMixin


class AuthorSearchView(FormView, SearchEngineMixin):
    template_name = "drevo/search.html"
    form_class = AuthorSearchForm
    success_url = reverse_lazy("search_author")

    def get_authors_with_filter(self,
                                main_search_parameter=None,
                                author_type_parameter=None,
                                ):

        authors = Author.objects.all()
        if main_search_parameter:
            # Ищем знания по главному полю
            authors = self.get_filtered_queryset(input_queryset=authors,
                                                 fields_name=['name',
                                                              'info',
                                                              ],
                                                 parameter_value=main_search_parameter,
                                                 lookup='__contains',
                                                 connector='OR')

        if author_type_parameter:
            # Ищем знания по типу автора
            authors = self.get_filtered_queryset(input_queryset=authors,
                                                 fields_name='atype__name',
                                                 parameter_value=author_type_parameter)

        return authors

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Поиск авторов'
        main_search_parameter = self.request.GET.get('main_search')
        author_type_parameter = self.request.GET.get('author_type')

        # Для сохранения любого пользовательского ввода в форме
        context['form'] = AuthorSearchForm(self.request.GET)

        if (main_search_parameter
                or author_type_parameter):

            # Для соединение с параметрами пагинации
            context['search_string_parameters'] = self.get_parameters_string(
                exclude_params=['page'])

            authors = self.get_authors_with_filter(
                main_search_parameter=main_search_parameter,
                author_type_parameter=author_type_parameter
            )

            authors = authors.select_related('atype')

            paginator = Paginator(authors, 10)

            cur_page_number = self.request.GET.get('page')

            page_obj = paginator.get_page(cur_page_number)

            context['paginator'] = paginator
            context['page_obj'] = page_obj

        return context
