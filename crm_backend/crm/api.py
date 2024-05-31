from .models import Customer, Lead, User, Interaction, Product, Order, OrderItem, Payment, Feedback, Subscription,SubscribedCustomer,CalcPoints, LoyaltyModel, Promotion, PromotionRedemption
from .schemas import  CustomerSchema, LeadSchema, UserSchema,  InteractionSchema,  ProductSchema, DurationUnitChoices, OrderSchema,  OrderItemSchema, PaymentSchema, FeedbackSchema,  SubscriptionSchema,SubscribedCustomerSchema,CalcPointsSchema, LoyaltyModelSchema,  PromotionSchema,  PromotionRedemptionSchema
from crm.schemas import (
    StatusChoices,
    SourceChoices,
    RoleChoices,
    InteractionTypeChoices,
    ParticipantTypeChoices,
    CoinChoices,
    OrderStatusChoices,
    PaymentMethodChoices,
    SubscriptionStatusChoices,
    TierChoices,
    PromotionTypeChoices,
    DiscountTypeChoices,
    CategoryChoices,
    DurationUnitChoices
)
from django.http import JsonResponse # type: ignore
from django.core.serializers import serialize # type: ignore
from django.shortcuts import get_object_or_404 # type: ignore
from django.core.exceptions import ObjectDoesNotExist # type: ignore
from django.utils import timezone # type: ignore
from ninja import  NinjaAPI # type: ignore
from datetime import datetime,timedelta
api = NinjaAPI()

# lsit of models


def get_data(queryset):
    data = list(queryset.values())  # Convert QuerySet to list of dictionaries
    return JsonResponse(data, safe=False)

@api.get("/customers/")
def get_customers(request):
    customers = Customer.objects.all()
    return get_data(customers)

@api.get("/leads/")
def get_leads(request):
    leads = Lead.objects.all()
    return get_data(leads)

@api.get("/users/")
def get_users(request):
    users = User.objects.all()
    return get_data(users)

@api.get("/interactions/")
def get_interactions(request):
    interactions = Interaction.objects.all()
    return get_data(interactions)

@api.get("/products/")
def get_products(request):
    products = Product.objects.all()
    return get_data(products)

@api.get("/orders/")
def get_orders(request):
    orders = Order.objects.all()
    return get_data(orders)

@api.get("/orderitems/")
def get_order_items(request):
    order_items = OrderItem.objects.all()
    return get_data(order_items)

@api.get("/payments/")
def get_payments(request):
    payments = Payment.objects.all()
    return get_data(payments)

@api.get("/feedbacks/")
def get_feedbacks(request):
    feedbacks = Feedback.objects.all()
    return get_data(feedbacks)

@api.get("/subscriptions/")
def get_subscriptions(request):
    subscriptions = Subscription.objects.all()
    return get_data(subscriptions)

@api.get("/subscribedCustomers/")
def get_subscribed_customers(request):
    subscribed_customers = SubscribedCustomer.objects.all()
    return get_data(subscribed_customers)

@api.get("/calcpoints/")
def get_calc_points(request):
    calc_points = CalcPoints.objects.all()
    return get_data(calc_points)

@api.get("/loyaltymodels/")
def get_loyalty_models(request):
    loyalty_models = LoyaltyModel.objects.all()
    return get_data(loyalty_models)

@api.get("/promotions/")
def get_promotions(request):
    promotions = Promotion.objects.all()
    return get_data(promotions)

@api.get("/promotionredemptions/")
def get_promotion_redemptions(request):
    promotion_redemptions = PromotionRedemption.objects.all()
    return get_data(promotion_redemptions)

#-----------------------------------------------
#creation:



@api.post("/orders/")
def create_order(request,participant_id:int,participant_type:ParticipantTypeChoices,product_ids:list[int],quantities:list[int],promotion_id:int=None):
    # Initialize promotion variable
    promotion = None
    try:
        if promotion_id:
            promotion = Promotion.objects.get(id=promotion_id)
    except Promotion.DoesNotExist:
                # Handle case where promotion does not exist
                promotion = None
    #CHECK IF LEAD
    if participant_type == ParticipantTypeChoices.Lead:
        # CREATE CUSTOEMR BASED ON THE DATA OF THE LEAD
        lead = Lead.objects.get(id=participant_id)
        customer = Customer.objects.create(
            first_name=lead.first_name,
            last_name=lead.last_name,
            email=lead.email,
            phone_number=lead.phone_number,
            address=lead.address,
            city=lead.city,
            state=lead.state,
            country=lead.country,
            postal_code=lead.postal_code
        )
        lead.delete()
    else:
        # Assume participant is already a customer
        customer = Customer.objects.get(id=participant_id)
    

    #INITIALIZE TOTALAMOUNT =0
    total_amount = 0
    
     # Create the order
    order = Order.objects.create(
        customer=customer,
        order_date=timezone.now(),
        total_amount=total_amount,
        promotion=promotion,
        status="UnPaid"
    )
   # Initialize total_amount and discount_amount
    total_amount = 0
    discount_amount = 0

    # Create order items and calculate total amount
    for product_id, quantity in zip(product_ids, quantities):
        product = Product.objects.get(id=product_id)
        total_amount += quantity * product.unit_price

        try:
        # Check if there's a promotion and it applies to the product's category
            if promotion_id:
                promotion = Promotion.objects.get(id=promotion_id)
                if promotion.category == product.category:
                    discount = calculate_discount(product.unit_price, promotion.discount_type, promotion.discount_value)
                    # Apply the discount to the product's price and accumulate the discount amount
                    discount_amount += min(discount * quantity, product.unit_price * quantity)
        except Promotion.DoesNotExist:
                # Handle case where promotion does not exist
                promotion = None
                
                
        # Create order item
        OrderItem.objects.create(
            order=order,
            product_id=product_id,
            quantity=quantity,
            unit_price=product.unit_price
        )

    original_amount=total_amount
    total_amount = total_amount-discount_amount

    subscribed_customer = SubscribedCustomer.objects.filter(customer=customer, status="Active").first()
    if subscribed_customer:
        subscription = subscribed_customer.subscription
        subscription_index = subscription.types.index(subscribed_customer.subscription_type)
        subscription_discount = subscription.discount[subscription_index]
        total_amount -= total_amount * (subscription_discount / 100)
    # Update the total amount in the order


    order.total_amount = total_amount
    order.save()

    if promotion_id and not subscribed_customer:
        return JsonResponse({'message': 'Order created successfully', 'original_amount': original_amount, 'after promotion: ': total_amount})
    elif subscribed_customer and not promotion_id:
        return JsonResponse({'message': 'Order created successfully', 'original_amount': original_amount, 'after subscription_discount: ': total_amount})
    elif subscribed_customer and promotion_id:    
        return JsonResponse({'message': 'Order created successfully', 'original_amount': original_amount, 'after promotion and subscription discount: ': total_amount})
    

    return JsonResponse({'message': 'Order created successfully', 'total_amount': original_amount})


@api.post("/calcpoints/")
def create_clacpoints(request,pointforxdollar:int):
    CalcPoints.objects.create(
        onepointforXdollar = pointforxdollar
    )
    return JsonResponse({'message': 'calcpoints created successfully'})




@api.post('/loyalties/')
def creat_loyalty(request,calcpoints_id:int,customer_id:int):
    calc_points = get_object_or_404(CalcPoints, pk=calcpoints_id)
    customer = get_object_or_404(Customer,pk=customer_id)
    LoyaltyModel.objects.create(
        CalcPoints = calc_points,
        customer=customer,
        points=0,
        tier="Bronze",
        last_updated=timezone.now()
    )
    return JsonResponse({'message': 'LoyaltyModel created successfully'})



@api.post('/payments/')
def create_payment(request,order_id:int,payment_method:PaymentMethodChoices,):
    
    order = Order.objects.get(id=order_id)
    if order.status == 'Paid':
        return JsonResponse({'message': 'the order is already paid'})
    # change order status to Paid
    order.status = "Paid"
    order.save()

    #get total_amount 
    total_amount = order.total_amount

    #updateLoyalty
    try:
        loyalty = LoyaltyModel.objects.get(customer=order.customer)
        loyalty.points = total_amount // loyalty.CalcPoints.onepointforXdollar
        loyalty.last_updated = timezone.now()
        loyalty.save()
    except ObjectDoesNotExist:
        pass



    # decrease the quantity of each product
    
    order_items = OrderItem.objects.filter(order=order_id)

    for item in order_items:
        product = item.product
        product.quantity_available -= item.quantity
        product.save()

   #updateUsageLimits
   # Update usage limits and create PromotionRedemption if applicable
    promotion = order.promotion
    if promotion:
        promotion.usage_limits -= 1
        promotion.save()
        Promotion.check_usage_limits(promotion.id)
    
        customer = Customer.objects.get(id=order.customer.id)
        PromotionRedemption.objects.create(
            promotion=promotion,
            customer=customer,
            redemption_date=timezone.now()
        )


    #create Payment
    Payment.objects.create(
        order = order,
        amount=total_amount,
        payment_date=timezone.now(),
        payment_method =payment_method,
    )
    return JsonResponse({'message': 'payment created successfully,loyalty point updated,order_item quantity updated'})




@api.post('/interactions/')
def create_interaction(request,participant_type:ParticipantTypeChoices,participant_id:int,interaction_type:InteractionTypeChoices,interaction_details:str,outcome:str,responsible_user_id:int,follow_up_required:bool):
    if participant_type.value == ParticipantTypeChoices.Lead:
        lead = Lead.objects.get(id=participant_id)
        lead.status = "Contacted"
        lead.save()
    
    user = User.objects.get(id=responsible_user_id)

    Interaction.objects.create(
        participant_type = participant_type.value,
        participant_id = participant_id,
        interaction_type=interaction_type.value,
        interaction_details=interaction_details,
        outcome=outcome,
        responsible_user= user,
        interaction_date=timezone.now(),
        follow_up_required=follow_up_required
    )  
    return JsonResponse({'message': 'interaction created successfully'})


@api.get('/interactions')
def IdInteraction(request, participant_id: int, participant_type: ParticipantTypeChoices):
    interactions = Interaction.objects.filter(participant_id=participant_id, participant_type=participant_type.value)

    if not interactions.exists():
        return JsonResponse({'message': f'No interactions found for the participant with ID {participant_id} and type {participant_type.value}'}, status=404)

    interactions_data = []
    for interaction in interactions:
        interaction_data = {
            'id': interaction.id,
            'participant_type': interaction.participant_type,
            'participant_id': interaction.participant_id,
            'interaction_type': interaction.interaction_type,
            'interaction_details': interaction.interaction_details,
            'outcome': interaction.outcome,
            'responsible_user_id': interaction.responsible_user_id,
            'interaction_date': interaction.interaction_date.isoformat(),
            'follow_up_required': interaction.follow_up_required,
        }
        interactions_data.append(interaction_data)

    return JsonResponse({'interactions': interactions_data}, safe=False)



@api.post('/promotions/')
def create_promotion(request,name: str,description: str,type: PromotionTypeChoices,start_date: datetime,end_date: datetime,discount_type: DiscountTypeChoices,discount_value: float,usage_limits: int
    ,category:CategoryChoices):
    Promotion.objects.create(
        name=name,
        description=description,
        type=type.value,  
        start_date=start_date,
        end_date=end_date,
        discount_type=discount_type.value,  
        discount_value=discount_value,
        expiration_date= None,
        usage_limits=usage_limits,
        category=category.value  
    )
    return JsonResponse({'message': 'Promotion created successfully'})







@api.post('/subscriptions/')
def create_subscription(request,types:list[str],prices:list[int],discounts:list[int],duration:int,duration_unit:DurationUnitChoices):
    Subscription.objects.create(
        types=types,
        price=prices,
        discount=discounts,
        duration=duration,
        duration_unit=duration_unit.value
    )
    return JsonResponse({'message': 'Subscription created successfully'})






@api.post('/subscribedCustomers/')
def create_customer_subscription(request,customer_id:int,subscription_id:int,subscription_type:str):
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)

    try:
        subscription = Subscription.objects.get(id=subscription_id)
    except Subscription.DoesNotExist:
        return JsonResponse({'error': 'Subscription not found'}, status=404)

    if subscription_type not in subscription.types:
        return JsonResponse({'error': f'the subscription type you inserted is not existed in the types of the subscription of id {subscription_id}'})
         
    # Check if the customer is already subscribed to this subscription
    existing_subscription = SubscribedCustomer.objects.filter(customer=customer, subscription=subscription, subscription_type=subscription_type, status="Active").exists()
    if existing_subscription:
        return JsonResponse({'error': 'Customer is already subscribed to this subscription'}, status=400)
  
    if subscription.duration_unit == DurationUnitChoices.Days.value:
        end_date = timezone.now() + timedelta(days=subscription.duration)
    elif subscription.duration_unit == DurationUnitChoices.Months.value:
        end_date = timezone.now() + timedelta(days=30 * subscription.duration)
    elif subscription.duration_unit == DurationUnitChoices.Years.value:
        end_date = timezone.now() + timedelta(days=365 * subscription.duration)
    else:
        return JsonResponse({'error': 'Invalid duration unit for subscription'}, status=400)

    SubscribedCustomer.objects.create(
        customer = customer,
        subscription=subscription,
        subscription_type=subscription_type,
        start_date=timezone.now(),
        end_date=end_date,
        status="Active"
    )
    return JsonResponse({'message': 'customer subscribed  successfully'})
    

@api.post('/feedbacks/')
def create_feedback(request,customer_id:int,order_id:int,rating:int,review:str):
    if rating >5 or rating <0:
                return JsonResponse({'error': 'rating should be between 1 and 5'})
    
    try:
        # Get Customer and Order objects
        customer = Customer.objects.get(id=customer_id)
        order = Order.objects.get(id=order_id)

        # Create Feedback object
        feedback = Feedback.objects.create(
            customer=customer,
            order=order,
            rating=rating,
            review=review
        )

        return JsonResponse({'message': 'Feedback created successfully', 'feedback_id': feedback.id})
    except Customer.DoesNotExist:
        return JsonResponse({'message': 'Customer does not exist'}, status=404)
    except Order.DoesNotExist:
        return JsonResponse({'message': 'Order does not exist'}, status=404)

#function to be used
#---------------------------------
def calculate_discount(total_amount: float, discount_type: str, discount_value: float) -> float:
    if discount_type == "Percentage":
        discount_amount = total_amount * (discount_value / 100)
    elif discount_type == "Fixed_Amount":
        discount_amount = discount_value
    else:
        raise ValueError("Invalid discount type")
    
    return discount_amount

