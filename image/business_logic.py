

# todo - Delete this business logic after Artem's approval

# from image.models import Image
#
# """Path to upload image for different apps request"""
# def user_directory_path(instance, filename):
#     if hasattr(instance, 'company_logo'):   # works for company request
#         purpose = 'company_logo'
#         company_id = instance.company_logo.id
#     elif hasattr(instance, 'location_logo'):   # works for location request
#         purpose = 'location_logo'
#         company_id = instance.location_logo.company.id
#     last_img = Image.objects.last()     # search for last upload image.id. then makes actual name for new image
#     img_id = last_img.id + 1 if last_img else 1
#     result = 'company_{company_id}/{purpose}/{instance_id}_{filename}'.format(
#         company_id=company_id,
#         purpose=purpose,
#         instance_id=img_id,
#         filename=filename,
#     )
#     return result
