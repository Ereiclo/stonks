from rest_framework.exceptions import APIException

class UserNotEnoughMoney(APIException):
    status_code = 400
    default_detail = 'User does not have enough money to perform this action.'
    default_code = 'api_not_enough_money'

