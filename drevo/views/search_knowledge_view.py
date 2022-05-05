import urllib
from django.urls import reverse_lazy
from ..forms import *
from django.views.generic.edit import FormView
from ..models import *
from django.core.paginator import Paginator
from django.db.models import (Q,
                              QuerySet,
                              Count)
from .search_engine import SearchEngineMixin
from django.forms import formset_factory


class KnowledgeSearchView(FormView, SearchEngineMixin):
    template_name = "drevo/search_knowledge.html"
    form_class = KnowledgeSearchForm
    success_url = reverse_lazy("search_knowledge")

    def get_published_knowledges_with_filter(self,
                                             main_search_parameter=None,
                                             knowledge_type_parameter=None,
                                             knowledge_category_parameter=None,
                                             author_parameter=None,
                                             edge_kind_parameter=None,
                                             tag_parameters=None):
        knowledges = (Znanie.objects.filter(is_published=True)
                      .order_by('name')
                      .select_related('author', 'tz', 'category')
                      .prefetch_related('related__tr', 'labels'))

        extra_query = None

        if knowledge_type_parameter:
            # Ищем знания по виду знаний
            query = self.get_query(fields_name='tz__name',
                                   parameter_value=knowledge_type_parameter)

            extra_query = query if not extra_query else extra_query & query

        if knowledge_category_parameter:
            # Ищем знания по категории знания
            query = self.get_query(fields_name='category__name',
                                   parameter_value=knowledge_category_parameter)

            extra_query = query if not extra_query else extra_query & query

        if author_parameter:
            # Ищем знания по автору знания
            query = self.get_query(fields_name='author__name',
                                   parameter_value=author_parameter)

            extra_query = query if not extra_query else extra_query & query

        if edge_kind_parameter:
            # Ищем знания по виду связи к знанию
            query = self.get_query(fields_name='related__tr__name',
                                   parameter_value=edge_kind_parameter)

            extra_query = query if not extra_query else extra_query & query

        if tag_parameters:
            # Ищем знания по виду тегам
            tag_queries = []
            for tag_name in tag_parameters:
                query = Q(labels__name=tag_name)
                tag_queries.append(query)
                # extra_query = query if not extra_query else extra_query & query

        from django.db import connection
        from pprint import pprint
        if extra_query:
            knowledges = knowledges.filter(extra_query)

        if tag_parameters:
            for query in tag_queries:
                knowledges = knowledges.filter(query)

        exclude_query = None
        if main_search_parameter:
            # Ищем знания по главному полю
            # Вначале необходимо получить наборы слов в виде общего списка
            # После чего беру набор и ищу через или
            parameter_value_combinations = self.get_parameter_combinations(
                main_search_parameter)
            combination_queries = []
            for combination in parameter_value_combinations:
                query_previously = None
                for value in combination:
                    query = Q(name__contains=value)
                    query = query | Q(content__contains=value)
                    query = query | Q(source_com__contains=value)

                    if value != value.upper():
                        query = query | Q(name__contains=value.upper())
                        query = query | Q(content__contains=value.upper())
                        query = query | Q(source_com__contains=value.upper())

                    if value != value.lower():
                        query = query | Q(name__contains=value.lower())
                        query = query | Q(content__contains=value.lower())
                        query = query | Q(source_com__contains=value.lower())

                    if value != value.capitalize():
                        query = query | Q(name__contains=value.capitalize())
                        query = query | Q(content__contains=value.capitalize())
                        query = query | Q(
                            source_com__contains=value.capitalize())

                    if query_previously:
                        query = query & query_previously

                    query_previously = query

                if not exclude_query:
                    combination_queries.append(query)
                    exclude_query = ~query
                else:
                    combination_queries.append(query & exclude_query)
                    exclude_query = ~query & exclude_query

        if main_search_parameter:
            knowledges_list = []
            # Первые запросы в списке соответствуют комбинациям с большим количеством слов
            # Этим добиваемся выдачи вначале знаний с большим совпадением слов
            for query in combination_queries:
                knowledges_tmp = knowledges.filter(query)
                knowledges_list.extend(list(knowledges_tmp))
            return knowledges_list
        return knowledges

    @classmethod
    def get_tag_formset(cls, request):
        tag_factory = formset_factory(KnowledgeSearchForm.Tag, extra=1)
        if 'tags-TOTAL_FORMS' in request.GET:
            tags_dict = {k: v for k, v in request.GET.items()
                         if ('tags' in k) and v}

            tag_formset = tag_factory(
                tags_dict, prefix='tags')

        else:
            tag_formset = tag_factory(prefix='tags')

        return tag_formset

    @classmethod
    def get_tag_names(cls, request):
        import re

        RE_TAG = re.compile(r'tags-\d+-tag')
        tags = []
        for parameter_name, parameter_value in request.GET.items():
            if RE_TAG.findall(parameter_name) and parameter_value.strip():
                tags.append(parameter_value.strip())
        return tags

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Поиск знаний'
        main_search_parameter = self.request.GET.get('main_search')
        knowledge_type_parameter = self.request.GET.get('knowledge_type')
        knowledge_category_parameter = self.request.GET.get(
            'knowledge_category')
        author_parameter = self.request.GET.get('author')
        edge_kind_parameter = self.request.GET.get('edge_kind')

        tag_parameters = KnowledgeSearchView.get_tag_names(self.request)

        context['tag_formset'] = KnowledgeSearchView.get_tag_formset(
            self.request)
        # Для сохранения любого пользовательского ввода в форме
        # Валидация формы под капотам класса
        context['form'] = KnowledgeSearchForm(self.request.GET)

        if tag_parameters and not context['tag_formset'].is_valid():
            return context

        if (main_search_parameter
            or knowledge_type_parameter
            or knowledge_category_parameter
            or author_parameter
            or edge_kind_parameter
                or tag_parameters):

            # Для соединение с параметрами пагинации
            context['search_string_parameters'] = self.get_parameters_string(
                exclude_params=['page'])

            knowledges = self.get_published_knowledges_with_filter(
                main_search_parameter=main_search_parameter,
                knowledge_type_parameter=knowledge_type_parameter,
                knowledge_category_parameter=knowledge_category_parameter,
                author_parameter=author_parameter,
                edge_kind_parameter=edge_kind_parameter,
                tag_parameters=tag_parameters
            )

            paginator = Paginator(knowledges, 10)

            cur_page_number = self.request.GET.get('page')

            page_obj = paginator.get_page(cur_page_number)

            context['paginator'] = paginator
            context['page_obj'] = page_obj
        return context
