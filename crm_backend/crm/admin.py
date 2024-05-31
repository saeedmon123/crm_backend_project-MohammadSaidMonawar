from django.contrib import admin # type: ignore
from .models import Customer, Lead, User, Interaction, Product, Order, OrderItem, Payment, Feedback, Subscription,SubscribedCustomer, CalcPoints, LoyaltyModel, Promotion, PromotionRedemption

admin.site.register(Customer)
admin.site.register(Lead)
admin.site.register(User)
admin.site.register(Interaction)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(Feedback)
admin.site.register(Subscription)
admin.site.register(CalcPoints)
admin.site.register(LoyaltyModel)
admin.site.register(Promotion)
admin.site.register(PromotionRedemption)
admin.site.register(SubscribedCustomer)
