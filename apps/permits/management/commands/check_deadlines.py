"""
Management command to check approval deadlines and auto-redirect
يفحص المهل الزمنية للموافقات ويحول تلقائياً عند التجاوز
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.permits.models import PendingApproval


class Command(BaseCommand):
    help = 'Check approval deadlines and auto-redirect overdue requests'

    def handle(self, *args, **options):
        """
        فحص جميع الموافقات المعلقة وتحويل المتأخرة
        """
        self.stdout.write(self.style.SUCCESS('🔍 Checking approval deadlines...'))
        
        # Get all pending approvals that are not completed or redirected
        pending_approvals = PendingApproval.objects.filter(
            completed=False,
            redirected=False
        )
        
        total_checked = 0
        total_redirected = 0
        
        for approval in pending_approvals:
            total_checked += 1
            
            # Check deadline
            was_redirected = approval.redirected
            approval.check_deadline()
            
            if not was_redirected and approval.redirected:
                total_redirected += 1
                self.stdout.write(
                    self.style.WARNING(
                        f'⚠️  Redirected: {approval.permit.permit_number} '
                        f'from {approval.workflow.approver.username} '
                        f'to {approval.redirected_to.username}'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Checked {total_checked} pending approvals\n'
                f'📤 Redirected {total_redirected} overdue requests'
            )
        )

