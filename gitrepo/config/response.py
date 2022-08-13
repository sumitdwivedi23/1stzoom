from rest_framework.response import Response
from rest_framework.exceptions import APIException


class CustomResponse(Response):

    def __init__(self, data=None, status=200):
        result = {'data': data, 'status': status}
        super().__init__(result, status)


def get_custom_error_message(message=None, error_location='server', status=400):
    data= {}
    error= {
                "location":error_location,
                "message":message,
            }
    data['error']= error
    data['status']= status

    return data

class CustomApiException(APIException):

    #public fields
    detail= None
    status_code= None
    location= None

    # create constructor
    def __init__(self, status_code, message, location):
        #override public fields
        CustomApiException.status_code= status_code
        CustomApiException.detail= message
        CustomApiException.location= location