import json
from import_export import resources, exceptions

from .models import ImportLog


def print_result_error(result):
    if result.has_errors:
        for e in result.base_errors:
            print(f'base error:{e.error}')
        for i, errors in result.row_errors():
            for e in errors:
                print(f'row error-row: {i} with e:{e.error}')


def run_resouce(resource, dataset, file_name):
    headers = dataset.headers
    result = resource.import_data(dataset, dry_run=True, file_name=file_name)
    if not result.has_errors():
        dataset.headers = headers
        result = resource.import_data(
            dataset, dry_run=False, file_name=file_name)
    else:
        print(f'import {file_name} error:')
        print_result_error(result)
    return result


class HeaderMixin:
    field2header_tuple = ()

    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        self.f2h_map = fhmap = dict(self.field2header_tuple)
        header_fields = tuple(self.f2h_map.values())
        if not header_fields:
            header_fields = tuple(
                f.column_name for f in self.get_import_fields())
        if sorted(header_fields) != sorted(dataset.headers):
            raise exceptions.ImportExportError('导入文件数据格式不符合要求，请确认标题列是否正确。')
        headers = list(dataset.headers)
        for f in self.get_import_fields():
            hname = fhmap.get(f.column_name)
            try:
                headers[headers.index(hname)] = f.column_name
            except ValueError:
                pass
        # print(f'HeaderMixin:{dataset.headers}->{headers}')
        dataset.headers = headers


class PartHeaderMixin:
    field2header_tuple = ()

    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        self.f2h_map = fhmap = dict(self.field2header_tuple)
        header_fields = tuple(self.f2h_map.values())
        if not header_fields:
            header_fields = tuple(
                f.column_name for f in self.get_import_fields())
        headers = list(dataset.headers)
        for f in self.get_import_fields():
            hname = fhmap.get(f.column_name)
            try:
                headers[headers.index(hname)] = f.column_name
            except ValueError:
                pass
        # print(f'PartHeaderMixin:{dataset.headers}->{headers}')
        dataset.headers = headers


class LogMixin:
    def after_import(self, dataset, result, using_transactions, dry_run, **kwargs):
        if (kwargs.get('user') and kwargs.get('file_name')):
            ImportLog.objects.create(user=kwargs.get('user'),
                                     file_name=kwargs.get('file_name'),
                                     resource_cls=str(self.__class__),
                                     totals=json.dumps(result.totals))
