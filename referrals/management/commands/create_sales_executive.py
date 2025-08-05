from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Role
from referrals.models import SalesExecutive, ReferralCode

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a sales executive user'

    def add_arguments(self, parser):
        parser.add_argument('--username', required=True, help='Username for the sales executive')
        parser.add_argument('--email', required=True, help='Email for the sales executive')
        parser.add_argument('--password', required=True, help='Password for the sales executive')
        parser.add_argument('--first_name', required=True, help='First name')
        parser.add_argument('--last_name', required=True, help='Last name')
        parser.add_argument('--employee_id', required=True, help='Employee ID')
        parser.add_argument('--phone', required=True, help='Phone number')
        parser.add_argument('--discount', type=float, default=10.0, help='Default discount percentage')

    def handle(self, *args, **options):
        # Get or create sales_executive role
        role, created = Role.objects.get_or_create(
            name='sales_executive',
            defaults={'description': 'Sales Executive'}
        )
        
        # Create user
        user = User.objects.create_user(
            username=options['username'],
            email=options['email'],
            password=options['password'],
            first_name=options['first_name'],
            last_name=options['last_name'],
            role=role
        )
        
        # Create sales executive
        sales_executive = SalesExecutive.objects.create(
            user=user,
            employee_id=options['employee_id'],
            phone=options['phone']
        )
        
        # Create default referral code
        ReferralCode.objects.create(
            sales_executive=sales_executive,
            discount_percentage=options['discount']
        )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created sales executive: {user.get_full_name()} ({options["employee_id"]})'
            )
        )