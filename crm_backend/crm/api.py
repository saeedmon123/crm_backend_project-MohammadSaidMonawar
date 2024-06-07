from .models import Customer, Lead, Profile,Interaction, Product, Order, OrderItem, Payment, Feedback, Subscription,SubscribedCustomer, LoyaltyModel,LoyaltyThreshold,loyalRedemption,Promotion, PromotionRedemption
from .schemas import  CustomerSchema, LeadSchema, InteractionSchema,  ProductSchema, DurationUnitChoices, OrderSchema,  OrderItemSchema, PaymentSchema, LoyaltyThresholdSchema,FeedbackSchema, loyaltyRedepmtionSchema, SubscriptionSchema,SubscribedCustomerSchema, PromotionSchema,  PromotionRedemptionSchema
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
    PromotionTypeChoices,
    DiscountTypeChoices,
    CategoryChoices,
    DurationUnitChoices
)
from django.db.models import Count
from django.contrib.auth.models import User
from django.http import JsonResponse
import json

from django.shortcuts import get_object_or_404
from django.utils import timezone
from ninja import  NinjaAPI
from datetime import datetime,timedelta
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
import logging
from django.conf import settings
logger = logging.getLogger(__name__)
api = NinjaAPI()

# # lsit of models


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

@api.get("/loyaltythresholds/")
def get_calc_points(request):
    loyaltyThreshold = LoyaltyThreshold.objects.all()
    return get_data(loyaltyThreshold)

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

@api.get('/interactions')
def IdInteraction(request, participant_id: int, participant_type: ParticipantTypeChoices):
    try:
        # Get the ContentType object for the provided participant type
        content_type = get_object_or_404(ContentType, model=participant_type.value.lower())

        # Filter interactions based on participant_id and participant_type
        interactions = Interaction.objects.filter(participant_id=participant_id, participant_type=content_type)

        if not interactions.exists():
            return JsonResponse({'message': f'No interactions found for the participant with ID {participant_id} and type {participant_type.value}'}, status=404)

        interaction_data = []
        for interaction in interactions:
            # Serialize responsible user
            responsible_user_data = {
                'username': interaction.responsible_user.username,
            }
            interaction_item = {
                'id': interaction.id,
                'participant_type':content_type.model
                ,
                'participant_id': interaction.participant_id,
                'interaction_type': interaction.interaction_type,
                'interaction_details': interaction.interaction_details,
                'outcome': interaction.outcome,
                'responsible_user': responsible_user_data,  # Serialize responsible user
                'interaction_date': interaction.interaction_date.isoformat(),
                'follow_up_required': interaction.follow_up_required,
            }
            interaction_data.append(interaction_item)

        return JsonResponse({'interactions': interaction_data}, safe=False)
    except ContentType.DoesNotExist:
        return JsonResponse({'error': f'Invalid participant type: {participant_type.value}'}, status=400)

@api.get('/customerprofiles')
def get_customer_profiles(request, customer_id: int):
    try:
        # Retrieve customer details
        customer = get_object_or_404(Customer,pk=customer_id)
        customer_data = {
            'first_name': customer.first_name,
            'last_name': customer.last_name,
            'email': customer.email,
            'phone_number': customer.phone_number,
            'address': customer.address,
            'city': customer.city,
            'state': customer.state,
            'country': customer.country,
            'postal_code': customer.postal_code,
            'date_created': customer.date_created.isoformat(),
            'last_contacted': customer.last_contacted.isoformat() if customer.last_contacted else None
        }

        # Retrieve orders for the customer
        orders = Order.objects.filter(customer=customer)
        order_data = []
        for order in orders:
            order_item = {
                'id': order.id,
                'order_date': order.order_date.isoformat(),
                'total_amount': order.total_amount,
                'promotion_id': order.promotion_id,
                'status': order.status,
            }
            order_data.append(order_item)

        # Retrieve interactions for the customer
        interactions = Interaction.objects.filter(participant_id=customer_id)
        interaction_data = []
        for interaction in interactions:
            # Serialize responsible user
            responsible_user_data = {
                'username': interaction.responsible_user.username,
            }
            interaction_item = {
                'id': interaction.id,
                'participant_type': 'Customer',
                'participant_id': interaction.participant_id,
                'interaction_type': interaction.interaction_type,
                'interaction_details': interaction.interaction_details,
                'outcome': interaction.outcome,
                'responsible_user': responsible_user_data,  # Serialize responsible user
                'interaction_date': interaction.interaction_date.isoformat(),
                'follow_up_required': interaction.follow_up_required,
            }
            interaction_data.append(interaction_item)
        return JsonResponse({
            'customer_data': customer_data,
            'order_data': order_data,
            'interaction_data': interaction_data
        }, safe=False)
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)





@api.get('/activesubscriptions/')
def get_active_subscriptions(request):
    try:
        active_subscriptions = SubscribedCustomer.objects.filter(status='Active')
        return get_data(active_subscriptions)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=400)
   



@api.get("/interaction-analysis/")
def interaction_analysis(request):
    try:
        # Example: Count interactions by type
        interaction_type_count = list(Interaction.objects.values('interaction_type').annotate(count=Count('interaction_type')))

        # Example: Count interactions by outcome
        outcome_count = list(Interaction.objects.values('outcome').annotate(count=Count('outcome')))

        # Example: Count interactions by responsible user
        user_count = list(Interaction.objects.values('responsible_user__username').annotate(count=Count('responsible_user')))

        return {
            "interaction_type_count": interaction_type_count,
            "outcome_count": outcome_count,
            "user_count": user_count
        }
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


#-----------------------------------------------
#creation:

@api.post("/customers/")
def create_customer(request, data: CustomerSchema):
    try:
        # Create a new customer using the validated data
        customer = Customer.objects.create(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            phone_number=data.phone_number,
            address=data.address,
            city=data.city,
            state=data.state,
            country=data.country,
            postal_code=data.postal_code
        )
        return JsonResponse({'message': 'Customer created successfully', 'customer_id': customer.id}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api.post("/orders/")
def create_order(request, participant_id: int, participant_type: ParticipantTypeChoices, product_ids: list[int], quantities: list[int], promotion_id: int = None,UseLoyalty:bool = False,RedeemPoints:int=None):
    try:

        # Check product availability before starting the transaction
        for product_id, quantity in zip(product_ids, quantities):
            product = Product.objects.filter(id=product_id).first()
            if not product:
                return JsonResponse({'error': f'Product with ID {product_id} not found'}, status=404)
            if product.quantity_available < quantity:
                return JsonResponse({'error': f'The product {product.id} with the name {product.name} currently has only {product.quantity_available} units available in stock.'}, status=404)
            
        with transaction.atomic():

            if UseLoyalty == False and RedeemPoints != None:
                return JsonResponse({'message': 'Cannot redeem points without using loyalty.'}, status=400)
            
            # Check if the provided promotion exists
            promotion = None
            if promotion_id:
                promotion = Promotion.objects.filter(id=promotion_id, expired=False).first()
                if not promotion:
                    return JsonResponse({'error': 'Promotion not found or expired'}, status=404)

            # Check if the participant is a lead or a customer
            if participant_type == ParticipantTypeChoices.Lead:
                lead = Lead.objects.filter(id=participant_id).first()
                if not lead:
                    return JsonResponse({'error': 'Lead not found'}, status=404)
                if lead.status != "Converted":
                    # Create a customer based on lead data if not already converted
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
                    lead.status = "Converted"
                    lead.save()
                else:
                    return JsonResponse({'message': 'The lead is already converted'})
            else:
                # Retrieve the customer if participant is not a lead
                customer = Customer.objects.filter(id=participant_id).first()
                if not customer:
                    return JsonResponse({'error': 'Customer not found'}, status=404)

      

            # Create a dictionary
            order_message_dict = {"key": "value"}

            # Serialize the dictionary to JSON
            order_message_json = json.dumps(order_message_dict)

            # Create the order with the serialized JSON as the order_message
            order = Order.objects.create(
                customer=customer,
                order_date=timezone.now(),
                total_amount=0,
                order_message=order_message_json,  # Assign the serialized JSON
                promotion=promotion,
                loyalty_point_used=RedeemPoints,
                status="UnPaid"
            )
            # Initialize total_amount and discount_amount
            total_amount = 0
            discount_amount = 0

            # Create order items and calculate total amount
            for product_id, quantity in zip(product_ids, quantities):
                product = Product.objects.filter(id=product_id).first()
                if not product:
                    return JsonResponse({'error': f'Product with ID {product_id} not found'}, status=404)
                total_amount += quantity * product.unit_price

                # Apply promotion discount if applicable
                if promotion and promotion.category == product.category:
                    discount = calculate_discount(product.unit_price, promotion.discount_type, promotion.discount_value)
                    discount_amount += min(discount * quantity, product.unit_price * quantity)

                # Create order item
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    unit_price=product.unit_price
                )

            # Calculate total amount after discounts
            original_amount=total_amount
            total_amount -= discount_amount

            # Apply subscription discount if applicable
            subscribed_customer = SubscribedCustomer.objects.filter(customer=customer, status="Active").first()
            if subscribed_customer:
                subscription = subscribed_customer.subscription
                subscription_index = subscription.types.index(subscribed_customer.subscription_type)
                subscription_discount = subscription.discount[subscription_index]
                total_amount -= total_amount * (subscription_discount / 100)

            # Update total amount in the order
            order.total_amount = total_amount
            order.save()

            if UseLoyalty == True:
                loyaltymodel = get_object_or_404(LoyaltyModel,customer=customer)
                if loyaltymodel.loyaltyThreshold.minimum_order_amount > total_amount:
                    return JsonResponse({"message",f"you don't reach the minimum order amount to use loyal points the minimum order points is {loyaltymodel.loyaltyThreshold.minimum_order_amount}"})
          # Return response
            response_data = {'message': 'Order created successfully', 'original_amount': original_amount}
            if promotion_id and not subscribed_customer:
                response_data['after_promotion'] = total_amount
            elif subscribed_customer and not promotion_id:
                response_data['after_subscription_discount'] = total_amount
            elif subscribed_customer and promotion_id:
                response_data['after_promotion_and_subscription_discount'] = total_amount


            if UseLoyalty == True:
                loyaltymodel = get_object_or_404(LoyaltyModel, customer=customer)

                min_point_to_redeem = loyaltymodel.loyaltyThreshold.min_points_to_redeem
                # Check if the points to redeem are valid
                if RedeemPoints >= min_point_to_redeem:
                    total_amount=  redeem_points(loyaltymodel.id, RedeemPoints, total_amount)

                    
                else:
                    return JsonResponse({"message":f"you don't reach the minimum point to redeem {min_point_to_redeem}"})


              

                # Update the total amount in the order
                order.total_amount = total_amount
                order.save()

                # Include the total amount after loyalty in the response data
                response_data['after_loyalty'] = total_amount
                        

            order.order_message=response_data
            order.save()
            return JsonResponse(response_data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



@api.post('/loyaltythresholds/')
def create_loyalty_threshold(request, payload: LoyaltyThresholdSchema):
    try:
        # Create LoyaltyThreshold
        loyalty_threshold = LoyaltyThreshold.objects.create(
            onepointforXdollar=payload.onepointforXdollar,
            minimum_order_amount=payload.minimum_order_amount,
            min_points_to_redeem=payload.min_points_to_redeem,
            points_expiry_days=payload.points_expiry_days,
            tier_name=payload.tier_name,
            points_for_next_tier=payload.points_for_next_tier,
            tier_discount=payload.tier_discount,

        )
        return {'message': 'LoyaltyThreshold created successfully', 'id': loyalty_threshold.id}
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@api.post('/loyaltymodels/')
def create_loyalty_model(request, loyalty_threshold_id: int, customer_id: int):
    try:
        # Fetch the LoyaltyThreshold and Customer instances
        loyalty_threshold = get_object_or_404(LoyaltyThreshold, id=loyalty_threshold_id)
        customer = get_object_or_404(Customer, id=customer_id)

        # Check if the customer already has a LoyaltyModel
        existing_loyalty_model = LoyaltyModel.objects.filter(customer=customer).exists()
        if existing_loyalty_model:
            return JsonResponse({"message": "The customer already has a loyalty model"}, status=400)

        # Create LoyaltyModel
        loyalty_model = LoyaltyModel.objects.create(
            loyaltyThreshold=loyalty_threshold,
            customer=customer,
            tier=loyalty_threshold.tier_name[0],  # Set initial tier to the first tier name
            points=0,
            last_updated=timezone.now()
        )
        return {'message': 'LoyaltyModel created successfully', 'id': loyalty_model.id}
    
    except LoyaltyThreshold.DoesNotExist:
        return JsonResponse({"error": "LoyaltyThreshold not found"}, status=404)
    
    except Customer.DoesNotExist:
        return JsonResponse({"error": "Customer not found"}, status=404)
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@api.post('/payments/')
def create_payment(request, order_id: int, payment_method: PaymentMethodChoices):
    try:
        with transaction.atomic():
            order = get_object_or_404(Order, id=order_id)
            if order.status == 'Paid':
                return JsonResponse({'message': 'The order is already paid'})

            order.status = "Paid"
            order.save()

            loyalty_model = LoyaltyModel.objects.filter(customer=order.customer).first()
            if loyalty_model:
                if order.loyalty_point_used:
                    if loyalty_model.points >= order.loyalty_point_used:
                        loyalty_model.points -= order.loyalty_point_used
                        loyalty_model.save()

                        loyalRedemption.objects.create(
                            LoyaltyModel=loyalty_model,  # Use the LoyaltyModel instance directly
                            Customer=order.customer,  # Use the Customer instance directly
                            points_used=order.loyalty_point_used,
                            redemption_date=timezone.now()
                        )
                    else:
                        return JsonResponse({'message': f'Not enough loyalty points. You have only {loyalty_model.points} points'}, status=400)

                total_amount = order.total_amount

                loyalty_model.points += total_amount // loyalty_model.loyaltyThreshold.onepointforXdollar
                loyalty_model.save()
                loyalty_model.last_updated = timezone.now()
                loyalty_model.save()
                loyalty_model.upgrade_tier(loyalty_model_id=loyalty_model.id)

            order_items = OrderItem.objects.filter(order=order)
            for item in order_items:
                product = item.product
                product.quantity_available -= item.quantity
                product.save()

            promotion = order.promotion
            if promotion:
                promotion.usage_limits -= 1
                promotion.save()
                Promotion.check_usage_limits(promotion.id)

                PromotionRedemption.objects.create(
                    promotion=promotion,  # Use the promotion instance directly
                    customer=order.customer,  # Use the customer instance directly
                    redemption_date=timezone.now()
                )

            Payment.objects.create(
                order=order,
                amount=order.total_amount,
                payment_date=timezone.now(),
                payment_method=payment_method.value,
            )
            
            try:
                send_payment_notification(order.customer, order, loyalty_model, order.order_message)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)

            return JsonResponse({'message': 'Payment created successfully, loyalty points updated, order items quantity updated'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api.post('/interactions/')
def create_interaction(request, participant_type: ParticipantTypeChoices, participant_id: int, interaction_type: InteractionTypeChoices, interaction_details: str, outcome: str, responsible_user: str):
    participant_type_str = participant_type.value
    participant_model = None
    if participant_type_str == 'Lead':
        participant_model = Lead
    elif participant_type_str == 'Customer':
        participant_model = Customer
    else:
        # Handle invalid participant type
        return JsonResponse({'message': 'Invalid participant type'}, status=400)

    try:
        participant_content_type = ContentType.objects.get_for_model(participant_model)
    except ContentType.DoesNotExist:
        return JsonResponse({'message': 'Participant content type not found'}, status=400)

    try:
        user = User.objects.get(username=responsible_user)
    except User.DoesNotExist:
        return JsonResponse({'message': 'Responsible user not found'}, status=400)

    try:
        # Create the interaction
        interaction = Interaction.objects.create(
            participant_type=participant_content_type,
            participant_id=participant_id,
            interaction_type=interaction_type.value,
            interaction_details=interaction_details,
            outcome=outcome,
            responsible_user=user,
            interaction_date=timezone.now(),
        )

        # Update lead status or customer last_contacted based on participant type
        if participant_type_str == 'Lead':
            # Update lead status
            try:
                lead = get_object_or_404(Lead,pk=participant_id)
                lead.status = "Contacted"
                lead.save()
            except Lead.DoesNotExist:
                return JsonResponse({'message': 'Lead not found'}, status=400)
        elif participant_type_str == 'Customer':
            # Update customer last_contacted
            try:
                customer = get_object_or_404(Customer,pk=participant_id)
                customer.last_contacted = timezone.now()
                customer.save()
            except Customer.DoesNotExist:
                return JsonResponse({'message': 'Customer not found'}, status=400)

        return JsonResponse({'message': 'Interaction created successfully'})
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=400)

@api.post('/followup/')
def need_followup(request, interaction_id: int, follow_up_date: datetime, follow_up_note: str):
    try:
        interaction = get_object_or_404(Interaction, id=interaction_id)
        interaction.schedule_follow_up(follow_up_date, follow_up_note)
        return JsonResponse({'message': 'Follow-up created successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api.post('/clearfollowup')
def clear_followup(request, interaction_id: int):
    try:
        interaction = get_object_or_404(Interaction, id=interaction_id)
        interaction.clear_follow_up()
        return JsonResponse({'message': 'Follow-up cleared successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api.post('/promotions/')
def create_promotion(request, name: str, description: str, type: PromotionTypeChoices, start_date: datetime, end_date: datetime, discount_type: DiscountTypeChoices, discount_value: float, usage_limits: int, category: CategoryChoices):
    try:
        promotion = Promotion.objects.create(
            name=name,
            description=description,
            type=type.value,  
            start_date=start_date,
            end_date=end_date,
            discount_type=discount_type.value,  
            discount_value=discount_value,
            expiration_date=None,
            usage_limits=usage_limits,
            category=category.value  
        )
        return JsonResponse({'message': 'Promotion created successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)





@api.post('/subscriptions/')
def create_subscription(request,types:list[str],prices:list[int],discounts:list[int],duration:int,duration_unit:DurationUnitChoices):
    try:
        Subscription.objects.create(
            types=types,
            price=prices,
            discount=discounts,
            duration=duration,
            duration_unit=duration_unit.value
        )
        return JsonResponse({'message': 'Subscription created successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)







@api.post('/subscribedCustomers/')
def create_customer_subscription(request,customer_id:int,subscription_id:int,subscription_type:str):
    try:
        try:
            customer = get_object_or_404(Customer,id=customer_id)
        except Customer.DoesNotExist:
            return JsonResponse({'error': 'Customer not found'}, status=404)

        try:
            subscription = get_object_or_404(Subscription,id=subscription_id)
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
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


    

@api.post('/feedbacks/')
def create_feedback(request,customer_id:int,order_id:int,rating:int,review:str):
    if rating >5 or rating <0:
                return JsonResponse({'error': 'rating should be between 1 and 5'})
    
    try:
        # Get Customer and Order objects
        customer = get_object_or_404(Customer,id=customer_id)
        order = get_object_or_404(Order,id=order_id)

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



@api.post('/profiles')
def create_profile(request,    username: str,role: RoleChoices):
    try:
        # Get the admin User instance
        admin_user = get_object_or_404(User,username=username)
        
        # Create the Profile instance with the provided role for the admin user
        Profile.objects.create(user=admin_user, role=role.value)
        
        return JsonResponse({'message': 'Profile created successfully'}, status=201)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Admin user not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



#update

@api.patch('/renewals/')
def renew_subscription(request, customer_id: int, subscription_id: int):
    try:
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return JsonResponse({'error': 'Customer not found'}, status=404)

        try:
            subscription = Subscription.objects.get(id=subscription_id)
        except Subscription.DoesNotExist:
            return JsonResponse({'error': 'Subscription not found'}, status=404)


        try:
            subscribedCustomer = SubscribedCustomer.objects.get(customer=customer)
        except SubscribedCustomer.DoesNotExist:
            return JsonResponse({'error':'customer is not susbscribed'})
        
        subscribedCustomer.status="Active"
        subscribedCustomer.start_date=timezone.now()
        if subscription.duration_unit == DurationUnitChoices.Days.value:
            end_date = timezone.now() + timedelta(days=subscription.duration)
        elif subscription.duration_unit == DurationUnitChoices.Months.value:
            end_date = timezone.now() + timedelta(days=30 * subscription.duration)
        elif subscription.duration_unit == DurationUnitChoices.Years.value:
            end_date = timezone.now() + timedelta(days=365 * subscription.duration)
        
        subscribedCustomer.end_date=end_date
        subscribedCustomer.save()



        return JsonResponse({'message': 'Subscription renewed successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)




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


def redeem_points(loyalty_model_id: int, points_to_redeem: int, total_amount: float) -> float:
    try:
        # Get the LoyaltyModel instance
        loyalty_model = LoyaltyModel.objects.get(id=loyalty_model_id)

        # Check if the loyalty model exists
        if loyalty_model:
            current_points = loyalty_model.points
       
            # Check if the points to redeem are valid
            if points_to_redeem <= current_points:
                tier_index = loyalty_model.loyaltyThreshold.tier_name.index(loyalty_model.tier)
                discount = loyalty_model.loyaltyThreshold.tier_discount[tier_index]

                discounted_amount = points_to_redeem*discount


                # Calculate the discounted total amount
                total_amount -= discounted_amount
           
                return total_amount
             
            else:
                raise ValueError(f"You don't have enough points to redeem {points_to_redeem} points.")
        else:
            raise ValueError("Loyalty model not found.")
    except LoyaltyModel.DoesNotExist:
        raise ValueError("Loyalty model not found.")
    except Exception as e:
        raise ValueError(str(e))
    


from django.core.mail import EmailMessage
from django.conf import settings
import logging


def send_payment_notification(customer, order, loyalty_model=None,order_message=dict):
    try:
        subject = 'Payment Confirmation'

        # Format order items
        order_items = OrderItem.objects.filter(order=order)
        item_details = "\n".join([
            f"<tr><td>{item.product.name}</td><td>{item.quantity}</td><td>${item.unit_price:.2f}</td></tr>"
            for item in order_items
        ])

        message = f"""
        <html>
        <body>
        <p>Dear {customer.first_name} {customer.last_name},</p>

        <p>Thank you for your payment.</p>

        <p>Here are the details of your purchase:</p>

        <table border="1" cellspacing="0" cellpadding="5">
            <tr>
                <th>Order ID</th>
                <td>{order.id}</td>
            </tr>
            <tr>
                <th>Date</th>
                <td>{order.order_date.strftime('%Y-%m-%d %H:%M:%S')}</td>
            </tr>
        </table>

        <h3>Items:</h3>
        <table border="1" cellspacing="0" cellpadding="5">
            <tr>
                <th>Product Name</th>
                <th>Quantity</th>
                <th>Price</th>
            </tr>
            {item_details}
        </table>

        """
        if order_message:
            message += "<h3>Order Details:</h3>"
            for key, value in order_message.items():
                if key != "message":
                    message += f"<p><strong>{key.capitalize()}:</strong> {value}</p>"
                
        # Add loyalty points information if available
        if loyalty_model:
            loyalty_points_earned = order.total_amount // loyalty_model.loyaltyThreshold.onepointforXdollar
            message += f"""
            <p><strong>Loyalty Points Used:</strong> {order.loyalty_point_used}</p>
            <p><strong>Loyalty Points Earned:</strong> {loyalty_points_earned}</p>
            """

        message += """
        <p>If you have any questions, please contact our support team.</p>

        <p>Best regards,<br>Your Company Name</p>
        </body>
        </html>
        """
    
        email_message = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[customer.email]
        )
        email_message.content_subtype = "html"  # Main content is now text/html

        # Set SMTP server settings
        email_message.extra_headers = {'X-SMTPAPI': '{"category": "PaymentNotification"}'}
        email_message.send()

        logger.info(f"Payment notification sent to {customer.email} successfully.")

    except Exception as e:
        logger.error(f"Failed to send payment notification to {customer.email}: {str(e)}")
        raise  # Re-raise the exception for the caller to handle