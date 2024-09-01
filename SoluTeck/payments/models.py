from django.db import models  
import datetime

from accounts.models import Student  

class TuitionFee(models.Model):  
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  
    amount = models.DecimalField(max_digits=10, decimal_places=2)  
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  
    due_date = models.DateField()  
    is_paid = models.BooleanField(default=False)  
    payment_method = models.CharField(max_length=50, choices=[  
        ('cash', 'Espèces'),  
        ('orange_money', 'Orange Money'),  
        ('mtn_money', 'MTN Mobile Money'),  
    ])  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):  
        return f"{self.student} - {self.amount} FCFA"  

class Invoice(models.Model):  
    student = models.ForeignKey(Student, on_delete=models.CASCADE)    
    amount = models.DecimalField(max_digits=10, decimal_places=2)  
    due_date = models.DateField(default=datetime.date.today)  
    is_paid = models.BooleanField(default=False)  

    def __str__(self):  
        return f"Invoice for {self.student} - Amount: {self.amount}"  

# Exemple de création d'une facture dans une vue  
from decimal import Decimal
from django.http import HttpResponseBadRequest

def create_invoice(request):  
    if request.method == "POST":  
        student_id = request.POST.get("student_id")  
        amount = request.POST.get("amount")  
        
        if not student_id or not amount:
            return HttpResponseBadRequest("ID de l'étudiant et montant requis.")
        
        try:  
            student_instance = Student.objects.get(id=student_id)  
            invoice = Invoice.objects.create(student=student_instance, amount=Decimal(amount))  
            # Rediriger ou traiter après la création  
        except Student.DoesNotExist:  
            print("L'étudiant avec cet ID n'existe pas.")
        except ValueError:
            print("Le montant doit être un nombre valide.")
from django.db import models
from django.core.exceptions import ValidationError

def validate_positive(value):
    if value < 0:
        raise ValidationError(f"{value} n'est pas un nombre positif.")

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_positive])

    def __str__(self):
        return self.name
