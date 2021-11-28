from rest_framework.renderers import JSONRenderer
from rest_framework import status


class CustomJSONRenderer(JSONRenderer):
    '''
    custom renderer class to streamline the response format
    '''
    media_type = 'application/json'
    format = 'json'
    charset = 'utf-8'
    render_style = 'text'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_status = renderer_context.get("response").status_code
        POSITIVE_STATUS_LIST = [
            status.HTTP_200_OK, status.HTTP_201_CREATED, status.HTTP_204_NO_CONTENT]

        if response_status in POSITIVE_STATUS_LIST:
            if response_status == status.HTTP_204_NO_CONTENT:
                response_data = {
                    "status": response_status,
                    "success": True
                }
            else:
                response_data = {
                    "data": data,
                    "status": response_status,
                    "success": True
                }
        else:
            response_data = data

        if response_status == status.HTTP_200_OK:
            response_data.update({
                "message": "Data Fetched Successfully"
            })
        elif response_status == status.HTTP_201_CREATED:
            response_data.update({
                "message": "Data Created Successfully"
            })

        response = super(CustomJSONRenderer, self).render(
            response_data, accepted_media_type, renderer_context
        )

        return response
