from django.db import models # type: ignore

from django.contrib.auth.models import User # type: ignore
from django.utils import timezone # type: ignore

from django.core.exceptions import ValidationError


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)
    last_contacted = models.DateTimeField(null=True)
 

    def __str__(self):
        return f"Customer {self.pk}"


class Lead(models.Model):
    STATUS_CHOICES = [
        ("New", "New"),
        ("Contacted", "Contacted"),
    ]
    SOURCE_CHOICES = [
        ("Website_Form", "Website_Form"),
        ("Referral", "Referral"),
        ("Cold_Call", "Cold_Call"),
        ("Ads", "Ads"),
    ]

    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    source = models.CharField(max_length=100, choices=SOURCE_CHOICES)
    created_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    

    def __str__(self):
        return f"Lead {self.pk}"

class User(models.Model):
    ROLE_CHOICES = [
        ("Sales_Representative", "Sales_Representative"),
        ("Customer_Support_Agent", "Customer_Support_Agent"),
        ("Account_Manager", "Account_Manager"),
    
    ]

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    role = models.CharField(max_length=100, choices=ROLE_CHOICES)


class Interaction(models.Model):
    INTERACTION_TYPE_CHOICES = [
        ("Phone_Call", "Phone_Call"),
        ("Email", "Email"),
        ("Meeting", "Meeting"),
    ]
    
    PARTICIPANT_TYPES_CHOICES = [
        ("Lead", "Lead"),
        ("Customer", "Customer")
    ]
    
    id = models.AutoField(primary_key=True)
    participant_type = models.CharField(max_length=20, choices=PARTICIPANT_TYPES_CHOICES, null=True)
    participant_id = models.IntegerField(null=True)  # Assuming this is an integer field storing the ID of either Lead or Customer
    interaction_type = models.CharField(max_length=100, null=True, choices=INTERACTION_TYPE_CHOICES)
    interaction_details = models.TextField(null=True)
    outcome = models.CharField(max_length=100, blank=True)
    responsible_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    interaction_date = models.DateTimeField(null=True)
    follow_up_required = models.BooleanField(default=False)

    def clean(self):
        if self.participant_type == 'Lead':
            try:
                # Fetch the Lead instance based on the provided participant_id
                lead_instance = Lead.objects.get(id=self.participant_id)
                self.participant_id = lead_instance.id  # Assign the ID of the Lead instance
            except Lead.DoesNotExist:
                raise ValidationError('Lead with the provided ID does not exist.')
        elif self.participant_type == 'Customer':
            try:
                # Fetch the Customer instance based on the provided participant_id
                customer_instance = Customer.objects.get(id=self.participant_id)
                self.participant_id = customer_instance.id  # Assign the ID of the Customer instance
            except Customer.DoesNotExist:
                raise ValidationError('Customer with the provided ID does not exist.')

class Promotion(models.Model):
    TYPE_CHOICES = [
        ("Coupon", "Coupon"),
        ("Offer", "Offer"),
        ("Discount_Code", "Discount_Code"),
        # Add more types here if needed
    ]
    DISCOUNT_TYPE_CHOICES = [
        ("Percentage", "Percentage"),
        ("Fixed_Amount", "Fixed_Amount"),
    ]
    CATEGORY_CHOICES = [
        ("Electronics", "Electronics"),
        ("Clothing", "Clothing"),
        ("Books", "Books"),
        ("Furniture", "Furniture"),
        ("Food", "Food"),
        ("Toys", "Toys"),
        ("Tools", "Tools"),
        ("Healthcare", "Healthcare"),
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    start_date = models.DateTimeField()
    category = models.CharField(max_length=100,choices=CATEGORY_CHOICES,default="Electronics")
    end_date = models.DateTimeField()
    discount_type = models.CharField(max_length=100, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.FloatField()
    expiration_date = models.DateTimeField(null=True,blank=True)
    usage_limits = models.IntegerField()

    @classmethod
    def check_usage_limits(cls,promotion_id):
        promotion = cls.objects.get(id = promotion_id)
        if promotion.usage_limits == 0:
            promotion.expiration_date=timezone.now()
            promotion.save()


class Order(models.Model):
    STATUS_CHOICES = [
        ("UnPaid", "UnPaid"),
        ("Paid", "Paid"),

    ]

    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.FloatField()
    promotion = models.ForeignKey(Promotion,on_delete=models.CASCADE,null=True,blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)


class Product(models.Model):

    COIN_CHOICES = [
        ("US_Dollar", "US_Dollar"),
        ("Euro", "Euro"),
        ("British_Pound", "British_Pound"),
        ("Japanese_Yen", "Japanese_Yen"),
        # Add more coin types here if needed
    ]
    CATEGORY_CHOICES = [
        ("Electronics", "Electronics"),
        ("Clothing", "Clothing"),
        ("Books", "Books"),
        ("Furniture", "Furniture"),
        ("Food", "Food"),
        ("Toys", "Toys"),
        ("Tools", "Tools"),
        ("Healthcare", "Healthcare"),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100,choices=CATEGORY_CHOICES,default="Electronics")
    unit_price = models.FloatField()
    quantity_available = models.IntegerField()
    br_code = models.CharField(max_length=100)
    coin_type = models.CharField(max_length=50, choices=COIN_CHOICES,default="US_Dollar")



class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.FloatField()

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("Credit_Card", "Credit_Card"),
        ("Debit_Card", "Debit_Card"),
        ("PayPal", "PayPal"),
        ("Bank_Transfer", "Bank_Transfer"),
        # Add more payment methods here if needed
    ]

    id = models.AutoField(primary_key=True)
    order= models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.FloatField()
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=100, choices=PAYMENT_METHOD_CHOICES)

class Feedback(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.TextField()
    feedback_date = models.DateTimeField(auto_now_add=True)


class Subscription(models.Model):
    DURATION_UNIT_CHOICES = [
        ("Days", "Days"),
        ("Months", "Months"),
        ("Years", "Years"),
    ]

    id = models.AutoField(primary_key=True)
    types = models.JSONField(default=list[str])  # Assuming types will be stored as a JSON list
    price = models.JSONField(default=list[int])
    discount=models.JSONField(default=list[int])  # Assuming prices will be stored as a JSON list
    duration = models.IntegerField(null=True)
    duration_unit = models.CharField(max_length=20, choices=DURATION_UNIT_CHOICES,default="Months")

class SubscribedCustomer(models.Model):
    SUBSCRIBED_STATUS_CHOICES= [
        ("Active", "Active"),
        ("Cancelled", "Cancelled"),
        ("Expired", "Expired"),
    ]

    id = models.AutoField(primary_key=True)
    subscription = models.ForeignKey(Subscription,on_delete=models.CASCADE,null=True)
    subscription_type=models.CharField(max_length=500,null=True)
    customer= models.ForeignKey(Customer,on_delete=models.CASCADE) # Foreign key referencing Customer
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=SUBSCRIBED_STATUS_CHOICES,default="Active")

    def save(self, *args, **kwargs):
        if self.end_date <= timezone.now():
            self.status = "Expired"
        super().save(*args, **kwargs)



class CalcPoints(models.Model):
    id=models.AutoField(primary_key=True)
    onepointforXdollar=models.IntegerField(default=0)

class LoyaltyModel(models.Model):
    TIER_CHOICES = [
        ("Bronze","Bronze"),
        ("Silver", "Silver"),
        ("Gold", "Gold"),
        ("Platinum", "Platinum"),
    ]

    id = models.AutoField(primary_key=True)
    CalcPoints=models.ForeignKey(CalcPoints,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    tier = models.CharField(max_length=100, choices=TIER_CHOICES)
    last_updated = models.DateTimeField(auto_now=True)


    @classmethod
    def upgrade_tier(cls, loyalty_model_id):
        loyalty_model = LoyaltyModel.objects.get(id=loyalty_model_id)
        if loyalty_model.points >= 1500:
            loyalty_model.tier = 'Platinum'
        elif loyalty_model.points >= 1000:
            loyalty_model.tier = 'Gold'
        elif loyalty_model.points >= 500:
            loyalty_model.tier = 'Silver'
        else:
            loyalty_model.tier = 'Bronze'
        loyalty_model.save()

    




class PromotionRedemption(models.Model):
    id = models.AutoField(primary_key=True)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    redemption_date = models.DateTimeField(auto_now_add=True)
