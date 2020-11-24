from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   url_for, jsonify)
from restaurants.dao.like_manager import LikeManager
from restaurants.dao.restaurant_availability_manager import \
    RestaurantAvailabilityManager
from restaurants.dao.restaurant_manager import RestaurantManager
from restaurants.dao.restaurant_rating_manager import RestaurantRatingManager
from restaurants.dao.table_manager import TableManager
from restaurants.models.restaurant import Restaurant, geolocator
from restaurants.models.restaurant_availability import RestaurantAvailability
from restaurants.models.restaurant_rating import RestaurantRating
from restaurants.models.table import Table
from datetime import datetime


restaurants = Blueprint('restaurants', __name__)


def restaurant_sheet(restaurant_id):
    """This method returns a single restaurant
        Linked to route /restaurant/{restaurant_id} [GET]
    Args:
        restaurant_id (int): univocal identifier of the restaurant
    Returns: 
        Invalid request if the restaurant does not exists
        A json specifying the info needed to render the restaurant page otherwise
    """
    restaurant = RestaurantManager.retrieve_by_id(id_=restaurant_id)
    if restaurant is None:
        return jsonify({'status': 'Bad request',
                        'message': 'The provided restaurant_id is not linked to any restaurant'
                        }), 400

    average_rate = RestaurantRatingManager.calculate_average_rate(restaurant)

    return jsonify({'status': 'Success',
                    'message': 'The restaurant details have been correctly fetched',
                    'restaurant_sheet': {'restaurant': restaurant.serialize(), 
                                        'average_rate': average_rate,
                                        'max_rate': RestaurantRating.MAX_VALUE,
                                        'is_open': restaurant.is_open_date()}
                    }), 200


def get_by_op_id(op_id : int):
    """Returns the restaurant owned by the operator
    specified by the op_id
        Linked to /restaurant/by_operator_id/<op_id>

    Args:
        op_id (int): Operator unique identifier
    """
    print('op_id:', op_id)
    restaurant = RestaurantManager.retrieve_by_operator_id(op_id)
    print(restaurant)
    if restaurant is None:
        print('ERROR: The provided op_id is not linked to any restaurant.\nOp_id provided: ', op_id)
        return jsonify({'status': 'Bad request',
                        'message': 'The provided op_id is not linked to any restaurant'
                        }), 400

    average_rate = RestaurantRatingManager.calculate_average_rate(restaurant)

    return jsonify({'status': 'Success',
                    'message': 'The restaurant details have been correctly fetched',
                    'restaurant_sheet': {'restaurant': restaurant.serialize(), 
                                        'average_rate': average_rate,
                                        'max_rate': RestaurantRating.MAX_VALUE,
                                        'is_open': restaurant.is_open_date()}
                    }), 200


def get_all_restaurants():
    """This method returns a all restaurant
        Linked to route /restaurant/all [GET]
    Returns:
        Bad request
        Internal server error
        A json including all the restaurants
    """
    restaurants = RestaurantManager.retrieve_all()
    if restaurants is None:
        return jsonify({'status': 'Bad request',
                        'message': 'Can\'t get any restaurant'
                        }), 500
    restaurants = [r.serialize() for r in restaurants]
    return jsonify({'status': 'Success',
                    'message': 'All the restaurants have been correctly retrieved',
                    'restaurants': restaurants
                    }), 200

def search_by(search_filter, search_field):
    """
        Linked to /resturant/search_by/{search_filter}/{search_field}

    Args:
        search_filter (string): [description]
        search_field (string): [description]

    Returns:
        [type]: [description]
    """
    restaurants = None
    if search_field == "Name":
        restaurants = RestaurantManager.retrieve_by_restaurant_name(search_filter)
    elif search_field == "City":
        restaurants = RestaurantManager.retrieve_by_restaurant_city(search_filter)
    elif search_field == "Menu Type":
        restaurants = RestaurantManager.retrieve_by_menu_type(search_filter)
    if restaurants is None:
        return jsonify({'status': 'Bad request',
                        'message': 'Can\'t get any restaurant'
                        }), 400
    restaurants = [r.serialize() for r in restaurants]
    return jsonify({'status': 'Success',
                    'message': 'The restaurant have been retrieved according to the specified search',
                    'restaurants': restaurants
                    }), 200

def like_toggle(restaurant_id):
    """Updates the like count
        Linked ot /restaurant/like/<restaurant_id> [PUT]
    Args:
        restaurant_id (int): univocal identifier of the restaurant

    Returns:
        Redirects to the single page for a restaurant
    """
    try:
        json_data = request.get_json()
        user_id = json_data['user_id']
    except Exception as e:
        return jsonify({'status': 'Bad request',
                        'message': 'The provided user_id is not valid.\n' + str(e) 
                        }), 404

    try:
        toggle_like(user_id, restaurant_id)
    except Exception as e:
        return jsonify({'status': 'Internal server error',
                'message': 'Error in toggling the like.\n' + str(e)
                }), 500

    return jsonify({'status': 'Success',
                    'message': 'The like was correctly toggled'
                    }), 200


def post_add():
    """Creates a new restaurant
        Linked to /restaurant [POST]

    Returns:
        Invalid response if the request method or the form are not correct 
        Confirms the creation of the restaurant otherwise
    """
    try:
        json_data = request.get_json()
        name = json_data['name']
        address = json_data['address']
        city = json_data['city']
        phone = json_data['phone']
        menu_type = json_data['menu_type']
        operator_id = json_data['op_id']
    except Exception as e:
        return jsonify({'status': 'Bad request',
                        'message': 'The data provided were not correct.\n' + str(e)
                        }), 400
    location = geolocator.geocode(address+" "+city)
    lat = 0
    lon = 0
    if location is not None:
        lat = location.latitude
        lon = location.longitude
    restaurant = Restaurant(name, address, city, lat, lon, phone, menu_type)
    restaurant.owner_id = operator_id
    try:
        RestaurantManager.create_restaurant(restaurant)
    except Exception as e:
        return jsonify({'status': 'Internal server error',
                        'message': 'Error in saving the restaurant in the db.\n' + str(e)
                        }), 500
    return jsonify({'status': 'Success',
                    'message': 'Restaurant succesfully added'
                    }), 200


def add_tables(restaurant_id):
    """This method gives the operator the possibility to add tables to his restaurant
        Linked to /restaurant/tables/restaurant_id> [POST]
    Args:
        restaurant_id (int): univocal identifier of the restaurant

    Returns:
        Invalid request if the tables data are not valid
        Tables successfully added otherwise
    """
    restaurant = RestaurantManager.retrieve_by_id(restaurant_id)
    if restaurant is None:
        return jsonify({'message': 'No restaurant with this id',
                        'status': 'Bad Request'}), 400

    post_data = request.get_json()
    num_tables = post_data.get('number')
    capacity = post_data.get('max_capacity')
    try:
        for _ in range(0, num_tables):
            table = Table(capacity=capacity, restaurant=restaurant)
            TableManager.create_table(table)
    except Exception as e:
        return jsonify({'message': 'DB ERROR\n' + str(e),
                        'status': 'Internal Server Error'}), 500
        
    return jsonify({'message': 'Tables successfully added'}), 200


def add_time(restaurant_id):
    """This method gives the operator the possibility to add opening hours to his restaurant
        Linked to /restaurant/time/<int:restaurant_id> [POST]
    Args:
        restaurant_id (int): univocal identifier of the restaurant
    Returns:

    """
    restaurant = RestaurantManager.retrieve_by_id(restaurant_id)
    if restaurant is None:
        return jsonify({'message': 'No restaurant with this id',
                        'status': 'Bad Request'}), 400
    post_data = request.get_json()
    try:
        day = post_data.get('day')
        start_time = post_data.get('start_time')
        end_time = post_data.get('end_time')
        start_time = datetime.strptime(start_time, '%H:%M:%S').time()
        end_time = datetime.strptime(end_time, '%H:%M:%S').time()
    except Exception as e:
        return jsonify({'message': 'Error during opening hours updating\n' + str(e),
                        'status': 'Bad Request'
                        }), 400
    try:
        restaurant = RestaurantManager.retrieve_by_id(restaurant_id)
        validate_ava(restaurant, day, start_time, end_time)
    except Exception as e:
        return jsonify({'message': 'DB ERROR\n' + str(e),
                        'status': 'Internal Server Error'
                        }), 500
    return jsonify({'message': 'Opening Hours updated',
                    'status': 'Success'}), 200


def add_measure(restaurant_id):
    """This method gives the operator the possibility to add precaution meausures 
    to his restaurant
        Linked to /restaurant/measure/<restaurant_id> [PUT]
    Args:
        restaurant_id (int): univocal identifier of the restaurant

    Returns:

    """
    restaurant = RestaurantManager.retrieve_by_id(restaurant_id)
    if restaurant is None:
        return jsonify({'message': 'No restaurant with this id',
                        'status': 'Bad Request'}), 400
    post_data = request.get_json()
    try:
        measure = post_data.get('measure')
        list_measure = restaurant.measures.split(',')
        if measure not in list_measure:
            list_measure.append(measure)
        string = ','.join(list_measure)
        restaurant.set_measures(string)
    except Exception as e:
        return jsonify({'message': 'Invalid json data\n' + str(e),
                        'status': 'Bad Request'
                        }), 400
    try:
        RestaurantManager.update_restaurant(restaurant)
    except Exception as e:
        return jsonify({'message': 'DB ERROR\n' + str(e),
                        'status': 'Internal Server Error'
                        }), 500
    return jsonify({'message': 'Measure added successfully',
                    'status': 'success'
                    }), 200


def add_avg_stay(restaurant_id):
    """This method gives the operator the possibility to add the average
    stay time to his restaurant
        Linked to /restaurant/avg_stay/<restaurant_id> [PUT]
    Args:
        restaurant_id (int): univocal identifier of the restaurant

    Returns:

    """
    restaurant = RestaurantManager.retrieve_by_id(restaurant_id)
    if restaurant is None:
        return jsonify({'message': 'No restaurant with this id',
                        'status': 'Bad Request'}), 400
    try:
        post_data = request.get_json()
        hours = post_data.get('hours')
        minute = post_data.get('minutes')
        minute = (hours * 60) + minute
        restaurant.set_avg_stay(minute)
    except Exception as e:
        return jsonify({'message': 'Invalid json data\n' + str(e),
                        'status': 'Bad request'
                        }), 400
    try:
        RestaurantManager.update_restaurant(restaurant)
    except Exception as e:
        return jsonify({'message': 'Error during avg stay updating\n' + str(e),
                        'status': 'Internal Server Error'
                        }), 500
    return jsonify({'message': 'Average stay time successfully added'
                    }), 200


def put_edit_restaurant(restaurant_id):
    """This method allows the operator to edit the information about his restaurant
        Linked to /restaurant/<restaurant_id> [PUT]
    Args:
        restaurant_id (int): univocal identifier of the restaurant

    Returns:
        
    """
    json_data = request.get_json()
    restaurant = RestaurantManager.retrieve_by_id(restaurant_id)
    if restaurant is None:
        return jsonify({'message': 'No restaurant with this id',
                        'status': 'Bad Request'}), 400    
    try:
        name = json_data['name']
        restaurant.set_name(name)
        address = json_data['address']
        restaurant.set_address(address)
        city = json_data['city']
        restaurant.set_city(city)
        phone = json_data['phone']
        restaurant.set_phone(phone)
        menu_type = json_data['menu_type']
        restaurant.set_menu_type(menu_type)
    except Exception as e:
        return jsonify({'message': 'Invalid json data\n' + str(e),
                        'status': 'Bad request'
                        }), 400
    try:
        RestaurantManager.update_restaurant(restaurant)
    except Exception as e:
        return jsonify({'message': 'Error during restaurant updating\n' + str(e),
                        'status': 'Internal Server Error'
                        }), 500
    return jsonify({'status': 'Success',
                    'message': 'Restaurant correctly modified'
                    }), 200

def delete_restaurant(restaurant_id):
    """This method allows the operator to delete the restaurant
        Linked to /restaurant/{restaurant_id} [DELETE]
    Args:
        restaurant_id (int): univocal identifier of the restaurant

    Returns:
        Invalid request if the restaurant are not valid
        Restaurant successfully deleted
    """
    restaurant = RestaurantManager.retrieve_by_id(restaurant_id)
    if restaurant is None:
        return jsonify({'message': 'No restaurant with this id',
                        'status': 'Bad Request'}), 400
    try:
        RestaurantManager.delete_restaurant(restaurant)
    except Exception as e:
        return jsonify({'message': 'Error during avg stay updating\n' + str(e),
                        'status': 'Internal Server Error'
                        }), 500
    return jsonify({'message': 'Restaurant successfully deleted'
                    }), 200



def add_review():
    """This method allows a customer to leave a review in a restaurant that he has been in.
    Only one review is possible.
        Linked to /restaurant/review [POST]

    """
    json_data = request.get_json()
    try:
        restaurant_id = json_data['restaurant_id']
        customer_id = json_data['customer_id']
        customer_name = json_data['customer_name']
        value = json_data['value'],
        review = json_data['review']
    except Exception as e:
        return jsonify({'message': 'Invalid json data\n' + str(e),
                        'status': 'Bad request'
                        }), 400
    if RestaurantRatingManager.check_existence(restaurant_id, customer_id):
        return jsonify({'status': 'Success',
                'message': 'Review already added',
                'already_written': True
                }), 200
    else:
        rest_rating = RestaurantRating(
            customer_id,
            restaurant_id,
            customer_name,
            value,
            review
        )
        RestaurantRatingManager.create_rating(rest_rating)
        return jsonify({'status': 'Success',
                        'message': 'Review correctly added',
                        'already_written': False
                        }), 201


def get_rating_bounds():
    """This method allows a customer to leave a review in a restaurant that he has been in.
    Only one review is possible.
        Linked to /restaurants/rating_bounds [GET]

    """
    return jsonify({'status': 'Success',
            'message': 'Review already written',
            'bounds': {'min_value': RestaurantRating.MIN_VALUE, 'max_value': RestaurantRating.MAX_VALUE}
            }), 200


##### Helper methods #####

def toggle_like(user_id, restaurant_id):
    restaurant = RestaurantManager.retrieve_by_id(restaurant_id)
    if restaurant is None:
        raise ValueError
    if LikeManager.like_exists(user_id, restaurant_id):
        LikeManager.delete_like(user_id, restaurant_id)
    else:
        LikeManager.create_like(user_id, restaurant_id)


def convert_avg_stay_format(avg_stay):
    if avg_stay is not None:
        h_avg_stay = avg_stay // 60
        m_avg_stay = avg_stay - (h_avg_stay * 60)
        avg_stay = "%dH:%dM" % (h_avg_stay, m_avg_stay)
    else:
        avg_stay = 0
    return str(avg_stay)


def validate_ava(restaurant, day, start_time, end_time):
    """This method validates the restaurant opening hours 

    Args:
        restaurant (restaurant): the actual restaurant
        day (String):
        start_time (time): opening hour
        end_time (time): closing hour

    Returns:
        Boolean: True if the opening hours has been added correctly otherwise returns false 
    """
    availabilities = restaurant.availabilities
    restaurant_id = restaurant.id
    present = False
    if end_time > start_time:
        for ava in availabilities:
            if ava.day == day:
                ava.set_times(start_time, end_time)
                RestaurantAvailabilityManager.update_availability(ava)
                present = True
        if not present:
            time = RestaurantAvailability(restaurant_id, day, start_time, end_time)
            RestaurantAvailabilityManager.create_availability(time)
        return True
    else:
        raise ValueError