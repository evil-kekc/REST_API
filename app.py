import json
import uuid

from flask import Flask, jsonify, Response
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

posts = {
    1: {
        'id': str(uuid.uuid4()),
        'post': 'some_post_1'
    },
    2: {
        'id': str(uuid.uuid4()),
        'post': 'some_post_2'
    },
    3: {
        'id': str(uuid.uuid4()),
        'post': 'some_post_3'
    },
}


class PostsById(Resource):
    def get(self, post_id):
        """GET request to getting a post by id

        :param post_id: ID of the post
        :return: response at json/text representation
        """

        try:
            if post_id == 0:
                response = app.response_class(response=json.dumps(posts),
                                              status=200,
                                              mimetype='application/json')
                return response
            else:
                response = app.response_class(response=json.dumps(posts[post_id]),
                                              status=200,
                                              mimetype='application/json')
                return response
        except KeyError:
            return Response(f'No post id={post_id}', status=404)

    def delete(self, post_id):
        """DELETE request to delete a post by id

        :param post_id: ID of the post
        :return: response at json/text representation
        """

        try:
            del posts[post_id]
            return jsonify(posts)
        except KeyError:
            return Response(f'No post id={post_id}', status=404)

    def post(self, post_id):
        """POST request to adding a post by id

        :param post_id: ID of the post
        :return: response at json/text representation
        """

        try:
            parser = reqparse.RequestParser()
            parser.add_argument("id", type=str)
            parser.add_argument("post", type=str)
            posts[post_id] = parser.parse_args()
            response = app.response_class(response=json.dumps(posts),
                                          status=200,
                                          mimetype='application/json')
            return response
        except Exception as ex:
            return Response(f'Some error: {repr(ex)}', status=404)

    def put(self, post_id):
        """PUT request to update a post by id

        :param post_id: ID of the post
        :return: response at json/text representation
        """

        try:
            if post_id in posts.keys():
                parser = reqparse.RequestParser()
                parser.add_argument("id", type=str)
                parser.add_argument("post", type=str)
                posts[post_id] = parser.parse_args()
                response = app.response_class(response=json.dumps(posts),
                                              status=200,
                                              mimetype='application/json')
                return response
            else:
                response = app.response_class(response=f'{posts}\n[ERROR] This post id does not exist: {post_id}',
                                              status=200,
                                              mimetype='text/html')
                return response
        except Exception as ex:
            return Response(f'Some error: {repr(ex)}', status=404)


class AllPosts(Resource):
    def get(self):
        """PUT request to update a post by id

        :param post_id: ID of the post
        :return: response at json/text representation
        """

        response = app.response_class(response=json.dumps(posts),
                                      status=200,
                                      mimetype='application/json')
        return response


api.add_resource(PostsById, '/api/posts/<int:post_id>')
api.add_resource(AllPosts, '/api/posts/')
api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=8087)
