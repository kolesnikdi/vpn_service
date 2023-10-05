# from celery_app.celery import app
#
# @app.task
# def companies_statistics():
#     """
#     Sends company statistics for managers
#     """
#     all_companies = Company.objects.all()
#
#     for company in all_companies:
#         send_company_statistics.delay(company_id=company.id) # delay(takes arguments for the function) --> execute.
#         we can use only when calling function in the decorator
#
#
# @app.task
# def send_company_statistics(company_id):
#     """
#     Args:
#         company_id (company.models.Company.id):
#     """
#     company = Company.objects.filter(
#         id=company_id,
#     ).prefetch_related(
#         'users',
#         'locations',
#         'locations__users',
#         'locations__vehicles',
#         'locations__vehicles__employee',
#         'locations__company__users',
#         'vehicles',
#         'vehicles__employee',
#     ).first()
#
#     data = CompanyStatisticsSerializer(instance=company).data
#
#     company.send_statistics(data)
#
#
# app.autodiscover_tasks('[tasks]') even don't know if we need it
