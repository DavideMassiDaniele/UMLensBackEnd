from flask import jsonify as json


class ApiResponse:

    @staticmethod
    def success(data):
        return json(data)

    @staticmethod
    def bad_request():
        return json({
            'code': 400,
            'message': 'Bad Request. Check your input data.',
        }), 400
