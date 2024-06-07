
from ninja import Schema
from typing import List, Optional
from datetime import datetime

from enum import Enum




class StatusChoices(Enum):
    New = "New"
    Contacted = "Contacted"
    Converted="Converted"

class SourceChoices(Enum):
    Website_Form = "Website_Form"
    Referral = "Referral"
    Cold_Call = "Cold_Call"
    Ads = "Ads"

class RoleChoices(Enum):
    Sales_Representative = "Sales_Representative"
    Customer_Support_Agent = "Customer_Support_Agent"
    Account_Manager = "Account_Manager"

class InteractionTypeChoices(Enum):
    Phone_Call = "Phone_Call"
    Email = "Email"
    Meeting = "Meeting"

class ParticipantTypeChoices(str,Enum):
    Lead = "Lead"
    Customer = "Customer"

class CoinChoices(Enum):
    US_Dollar = "US_Dollar"
    Euro = "Euro"
    British_Pound = "British_Pound"
    Japanese_Yen = "Japanese_Yen"

class OrderStatusChoices(Enum):
    UnPaid = "UnPaid"
    Paid = "Paid"

class PaymentMethodChoices(Enum):
    Credit_Card = "Credit_Card"
    Debit_Card = "Debit_Card"
    PayPal = "PayPal"
    Bank_Transfer = "Bank_Transfer"

class SubscriptionStatusChoices(Enum):
    Active = "Active"
    Cancelled = "Cancelled"
    Expired = "Expired"

class TierChoices(Enum):
    Bronze = "Bronze"
    Silver = "Silver"
    Gold = "Gold"
    Platinum = "Platinum"

class PromotionTypeChoices(Enum):
    Coupon = "Coupon"
    Offer = "Offer"
    Discount_Code = "Discount_Code"

class DiscountTypeChoices(str,Enum):
    Percentage = "Percentage"
    Fixed_Amount = "Fixed_Amount"

class CategoryChoices(str,Enum):
    Electronics = "Electronics"
    Clothing = "Clothing"
    Books = "Books"
    Furniture = "Furniture"
    Food = "Food"
    Toys = "Toys"
    Tools = "Tools"
    Healthcare = "Healthcare"

class DurationUnitChoices(Enum):
    Days = "Days"
    Months = "Months"
    Years = "Years"
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------

class CustomerSchema(Schema):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    address: str
    city: str
    state: str
    country: str
    postal_code: str
    date_created: datetime
    last_contacted: datetime

class LeadSchema(Schema):
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str
    address: str
    city: str
    state: str
    country: str
    postal_code: str
    status: str
    source: str
    created_date: datetime
    notes: str


class InteractionSchema(Schema):
    participant_type: str
    participant_id: int
    interaction_type: str
    interaction_details: str
    outcome: str
    responsible_user: str
    interaction_date: datetime
    follow_up_required: bool

class ProductSchema(Schema):
    id: int
    name: str
    description: str
    category: str
    unit_price: float
    quantity_available: int
    br_code: str
    coin_type: str

class OrderSchema(Schema):
    id: int
    customer: int
    order_date: datetime
    total_amount: float
    original_amount:float
    loyalty_point_used :int
    promotion_id:int
    status: str

class OrderItemSchema(Schema):
    id: int
    order: int
    product: int
    quantity: int
    unit_price: float

class PaymentSchema(Schema):
    id: int
    order: int
    amount: float
    payment_date: datetime
    payment_method: str

class FeedbackSchema(Schema):
    id: int
    customer: int
    order: int
    rating: int
    review: str
    feedback_date: datetime

class LoyaltyThresholdSchema(Schema):
    onepointforXdollar: int  # Points earned per X dollars spent
    minimum_order_amount: float  # Minimum order amount to earn points
    min_points_to_redeem: int  # Minimum points required to start redeeming
    points_expiry_days: int  # Number of days before points expire
    tier_name: list[str]  # Name of the tier (e.g., Bronze, Silver, Gold)
    points_for_next_tier: list[int]  # Points required to reach the next tier
    tier_discount: list[float]  # Discount percentage for this tier

class LoyaltyModelSchema(Schema):
    loyaltyThreshold: int
    customer: int
    points: int
    tier: str
    last_updated: datetime
    
class loyaltyRedepmtionSchema(Schema):
    id:int
    LoyaltyModel:int
    Customer:int
    points_used:int
    redemption_date:int





class PromotionSchema(Schema):
    id: int
    name: str
    description: str
    type: str
    start_date: datetime
    
    end_date: datetime
    discount_type: str
    discount_value: float
    expiration_date: datetime
    usage_limits: int
    category:CategoryChoices = CategoryChoices.Electronics

class PromotionRedemptionSchema(Schema):
    id: int
    promotion: int
    customer: int
    redemption_date: datetime


class SubscriptionSchema(Schema):
    id: int
    types: List[str]
    price: List[int]
    duration: int
    duration_unit: str  

class SubscribedCustomerSchema(Schema):
    id: int
    customer_id: int
    subscribtion:str
    subscribtion_type:str
    start_date: datetime
    end_date: datetime
    status: str  
