from rest_framework.throttling import UserRateThrottle

class ReviewDetailThrottle(UserRateThrottle):
    scope = 'throttling_for_revie_detail'
    
class ReviewListThrottle(UserRateThrottle):
    scope = 'throttling_for_review_list'