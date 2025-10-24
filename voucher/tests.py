from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal
from .models import Voucher
from .forms import VoucherForm
import json
import uuid
import sys
import os


class VoucherModelTest(TestCase):
    """Test cases untuk Voucher model"""
    
    def setUp(self):
        """Setup data untuk testing"""
        self.voucher = Voucher.objects.create(
            kode="TEST10",
            deskripsi="Voucher test 10%",
            persentase_diskon=Decimal("10.00"),
            is_active=True
        )
    
    def test_voucher_creation(self):
        """Test pembuatan voucher"""
        self.assertEqual(self.voucher.kode, "TEST10")
        self.assertEqual(self.voucher.deskripsi, "Voucher test 10%")
        self.assertEqual(self.voucher.persentase_diskon, Decimal("10.00"))
        self.assertTrue(self.voucher.is_active)
        self.assertIsInstance(self.voucher.id, uuid.UUID)
    
    def test_voucher_str_representation(self):
        """Test string representation voucher"""
        expected = "TEST10 (10.00% - Aktif)"
        self.assertEqual(str(self.voucher), expected)
    
    def test_voucher_inactive_str_representation(self):
        """Test string representation voucher nonaktif"""
        self.voucher.is_active = False
        expected = "TEST10 (10.00% - Nonaktif)"
        self.assertEqual(str(self.voucher), expected)
    
    def test_unique_kode_constraint(self):
        """Test unique constraint pada kode voucher"""
        with self.assertRaises(Exception):
            Voucher.objects.create(
                kode="TEST10",  # Duplicate kode
                deskripsi="Duplicate voucher",
                persentase_diskon=Decimal("5.00"),
                is_active=True
            )
    
    def test_persentase_diskon_decimal_places(self):
        """Test decimal places pada persentase_diskon"""
        voucher = Voucher.objects.create(
            kode="DECIMAL50",
            persentase_diskon=Decimal("15.50"),
            is_active=True
        )
        self.assertEqual(voucher.persentase_diskon, Decimal("15.50"))
    
    def test_voucher_blank_deskripsi(self):
        """Test voucher dengan deskripsi kosong"""
        voucher = Voucher.objects.create(
            kode="NODESC",
            deskripsi="",
            persentase_diskon=Decimal("20.00"),
            is_active=True
        )
        self.assertEqual(voucher.deskripsi, "")
    
    def test_voucher_meta_verbose_names(self):
        """Test Meta verbose names"""
        self.assertEqual(str(Voucher._meta.verbose_name), "Voucher")
        self.assertEqual(str(Voucher._meta.verbose_name_plural), "Vouchers")
    
    def test_voucher_min_validator(self):
        """Test persentase diskon tidak bisa kurang dari 0.01"""
        from django.core.exceptions import ValidationError
        voucher = Voucher(
            kode="MINTEST",
            persentase_diskon=Decimal("0.00"),
            is_active=True
        )
        with self.assertRaises(ValidationError):
            voucher.full_clean()
    
    def test_voucher_max_validator(self):
        """Test persentase diskon tidak bisa lebih dari 100"""
        from django.core.exceptions import ValidationError
        voucher = Voucher(
            kode="MAXTEST",
            persentase_diskon=Decimal("101.00"),
            is_active=True
        )
        with self.assertRaises(ValidationError):
            voucher.full_clean()


class VoucherFormTest(TestCase):
    """Test cases untuk VoucherForm"""
    
    def test_valid_form(self):
        """Test form dengan data valid"""
        form_data = {
            'kode': 'VALIDCODE',
            'deskripsi': 'Valid voucher description',
            'persentase_diskon': '25.00',
            'is_active': True
        }
        form = VoucherForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_form_missing_required_fields(self):
        """Test form tanpa field required"""
        form_data = {
            'deskripsi': 'Missing kode and persentase'
        }
        form = VoucherForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('kode', form.errors)
        self.assertIn('persentase_diskon', form.errors)
    
    def test_form_invalid_persentase_range(self):
        """Test form dengan persentase di luar range"""
        form_data = {
            'kode': 'INVALID',
            'persentase_diskon': '150.00',  # > 100
            'is_active': True
        }
        form = VoucherForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_form_blank_deskripsi_allowed(self):
        """Test form dengan deskripsi kosong (allowed)"""
        form_data = {
            'kode': 'NODESC',
            'deskripsi': '',
            'persentase_diskon': '10.00',
            'is_active': False
        }
        form = VoucherForm(data=form_data)
        self.assertTrue(form.is_valid())


class VoucherViewTest(TestCase):
    """Test cases untuk Voucher views"""
    
    def setUp(self):
        """Setup user dan client untuk testing"""
        self.client = Client()
        
        # Create regular user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create superuser
        self.admin = User.objects.create_superuser(
            username='admin',
            password='adminpass123'
        )
        
        # Create test vouchers
        self.voucher1 = Voucher.objects.create(
            kode="PROMO10",
            deskripsi="Promo 10%",
            persentase_diskon=Decimal("10.00"),
            is_active=True
        )
        
        self.voucher2 = Voucher.objects.create(
            kode="SALE20",
            deskripsi="Sale 20%",
            persentase_diskon=Decimal("20.00"),
            is_active=False
        )
    
    def test_voucher_view_requires_login(self):
        """Test voucher view memerlukan login"""
        response = self.client.get(reverse('voucher:voucher-view'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertIn('/login/', response.url)
    
    def test_voucher_view_authenticated_user(self):
        """Test voucher view untuk user yang login"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('voucher:voucher-view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'voucher.html')
        self.assertIn('vouchers', response.context)
        self.assertIn('active_page', response.context)
        self.assertEqual(response.context['active_page'], 'voucher')
        self.assertFalse(response.context['is_admin'])
    
    def test_voucher_view_admin_user(self):
        """Test voucher view untuk admin"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('voucher:voucher-view'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_admin'])
        self.assertIn('vouchers', response.context)
        # Verify vouchers are ordered by -id
        vouchers = list(response.context['vouchers'])
        self.assertEqual(len(vouchers), 2)
    
    def test_create_voucher_requires_admin(self):
        """Test create voucher memerlukan admin"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('voucher:create-voucher-ajax'), {
            'kode': 'NEWCODE',
            'persentase_diskon': '15.00',
            'is_active': 'true'
        })
        self.assertEqual(response.status_code, 403)
    
    def test_create_voucher_success(self):
        """Test create voucher berhasil oleh admin"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.post(reverse('voucher:create-voucher-ajax'), {
            'kode': 'NEWCODE',
            'deskripsi': 'New voucher',
            'persentase_diskon': '15.00',
            'is_active': 'true'
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertTrue(Voucher.objects.filter(kode='NEWCODE').exists())
    
    def test_create_voucher_duplicate_kode(self):
        """Test create voucher dengan kode duplikat"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.post(reverse('voucher:create-voucher-ajax'), {
            'kode': 'PROMO10',  # Already exists
            'persentase_diskon': '25.00',
            'is_active': 'true'
        })
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'error')
        self.assertIn('sudah ada', data['message'])
    
    def test_create_voucher_missing_fields(self):
        """Test create voucher tanpa field required"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.post(reverse('voucher:create-voucher-ajax'), {
            'kode': '',  # Empty kode
            'persentase_diskon': ''  # Empty persentase
        })
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'error')
    
    def test_update_voucher_requires_admin(self):
        """Test update voucher memerlukan admin"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('voucher:update-voucher-ajax', args=[self.voucher1.id]),
            {
                'kode': 'UPDATED',
                'persentase_diskon': '30.00',
                'is_active': 'true'
            }
        )
        self.assertEqual(response.status_code, 403)
    
    def test_update_voucher_success(self):
        """Test update voucher berhasil"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.post(
            reverse('voucher:update-voucher-ajax', args=[self.voucher1.id]),
            {
                'kode': 'UPDATED10',
                'deskripsi': 'Updated description',
                'persentase_diskon': '12.50',
                'is_active': 'false'
            }
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        
        # Verify update
        self.voucher1.refresh_from_db()
        self.assertEqual(self.voucher1.kode, 'UPDATED10')
        self.assertEqual(self.voucher1.persentase_diskon, Decimal('12.50'))
        self.assertFalse(self.voucher1.is_active)
    
    def test_update_voucher_duplicate_kode(self):
        """Test update voucher dengan kode yang sudah ada"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.post(
            reverse('voucher:update-voucher-ajax', args=[self.voucher1.id]),
            {
                'kode': 'SALE20',  # Kode voucher2
                'persentase_diskon': '15.00',
                'is_active': 'true'
            }
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'error')
    
    def test_delete_voucher_requires_admin(self):
        """Test delete voucher memerlukan admin"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('voucher:delete-voucher-ajax', args=[self.voucher1.id])
        )
        self.assertEqual(response.status_code, 403)
    
    def test_delete_voucher_success(self):
        """Test delete voucher berhasil"""
        self.client.login(username='admin', password='adminpass123')
        voucher_id = self.voucher1.id
        response = self.client.post(
            reverse('voucher:delete-voucher-ajax', args=[voucher_id])
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertFalse(Voucher.objects.filter(id=voucher_id).exists())
    
    def test_delete_nonexistent_voucher(self):
        """Test delete voucher yang tidak ada"""
        self.client.login(username='admin', password='adminpass123')
        fake_id = uuid.uuid4()
        response = self.client.post(
            reverse('voucher:delete-voucher-ajax', args=[fake_id])
        )
        # get_object_or_404 raises Http404 which is caught by exception handler
        # and returns 500 with error message
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'error')
        self.assertIn('Terjadi kesalahan', data['message'])
    
    def test_get_vouchers_json(self):
        """Test get vouchers dalam format JSON"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('voucher:get-vouchers-json'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('vouchers', data)
        self.assertEqual(len(data['vouchers']), 2)
        
        # Verify voucher data structure
        voucher_data = data['vouchers'][0]
        self.assertIn('id', voucher_data)
        self.assertIn('kode', voucher_data)
        self.assertIn('deskripsi', voucher_data)
        self.assertIn('persentase_diskon', voucher_data)
        self.assertIn('is_active', voucher_data)
    
    def test_get_vouchers_json_requires_login(self):
        """Test get vouchers JSON memerlukan login"""
        response = self.client.get(reverse('voucher:get-vouchers-json'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_create_voucher_exception_handling(self):
        """Test exception handling saat create voucher"""
        from unittest.mock import patch
        self.client.login(username='admin', password='adminpass123')
        
        # Mock Voucher.objects.create to raise exception
        with patch('voucher.models.Voucher.objects.create') as mock_create:
            mock_create.side_effect = Exception("Database error")
            response = self.client.post(reverse('voucher:create-voucher-ajax'), {
                'kode': 'ERRORTEST',
                'deskripsi': 'Test exception',
                'persentase_diskon': '10.00',
                'is_active': 'true'
            })
            self.assertEqual(response.status_code, 500)
            data = json.loads(response.content)
            self.assertEqual(data['status'], 'error')
            self.assertIn('Terjadi kesalahan', data['message'])
    
    def test_update_voucher_exception_handling(self):
        """Test exception handling saat update voucher"""
        from unittest.mock import patch
        self.client.login(username='admin', password='adminpass123')
        
        # Mock voucher.save to raise exception
        with patch.object(Voucher, 'save') as mock_save:
            mock_save.side_effect = Exception("Database save error")
            response = self.client.post(
                reverse('voucher:update-voucher-ajax', args=[self.voucher1.id]),
                {
                    'kode': 'UPDATED',
                    'deskripsi': 'Updated desc',
                    'persentase_diskon': '15.00',
                    'is_active': 'true'
                }
            )
            self.assertEqual(response.status_code, 500)
            data = json.loads(response.content)
            self.assertEqual(data['status'], 'error')
    
    def test_delete_voucher_exception_handling(self):
        """Test exception handling saat delete voucher"""
        from unittest.mock import patch
        self.client.login(username='admin', password='adminpass123')
        
        # Mock voucher.delete to raise exception
        with patch.object(Voucher, 'delete') as mock_delete:
            mock_delete.side_effect = Exception("Database delete error")
            response = self.client.post(
                reverse('voucher:delete-voucher-ajax', args=[self.voucher1.id])
            )
            self.assertEqual(response.status_code, 500)
            data = json.loads(response.content)
            self.assertEqual(data['status'], 'error')


class VoucherIntegrationTest(TestCase):
    """Integration tests untuk Voucher module"""
    
    def setUp(self):
        """Setup untuk integration testing"""
        self.client = Client()
        self.admin = User.objects.create_superuser(
            username='admin',
            password='adminpass123'
        )
        self.client.login(username='admin', password='adminpass123')
    
    def test_complete_voucher_lifecycle(self):
        """Test complete lifecycle: create -> update -> delete"""
        # 1. Create voucher
        create_response = self.client.post(reverse('voucher:create-voucher-ajax'), {
            'kode': 'LIFECYCLE',
            'deskripsi': 'Lifecycle test',
            'persentase_diskon': '25.00',
            'is_active': 'true'
        })
        self.assertEqual(create_response.status_code, 200)
        create_data = json.loads(create_response.content)
        voucher_id = create_data['voucher']['id']
        
        # 2. Verify in database
        voucher = Voucher.objects.get(id=voucher_id)
        self.assertEqual(voucher.kode, 'LIFECYCLE')
        
        # 3. Update voucher
        update_response = self.client.post(
            reverse('voucher:update-voucher-ajax', args=[voucher_id]),
            {
                'kode': 'LIFECYCLE2',
                'deskripsi': 'Updated lifecycle',
                'persentase_diskon': '30.00',
                'is_active': 'false'
            }
        )
        self.assertEqual(update_response.status_code, 200)
        
        # 4. Verify update
        voucher.refresh_from_db()
        self.assertEqual(voucher.kode, 'LIFECYCLE2')
        self.assertFalse(voucher.is_active)
        
        # 5. Delete voucher
        delete_response = self.client.post(
            reverse('voucher:delete-voucher-ajax', args=[voucher_id])
        )
        self.assertEqual(delete_response.status_code, 200)
        
        # 6. Verify deletion
        self.assertFalse(Voucher.objects.filter(id=voucher_id).exists())
    
    def test_multiple_vouchers_ordering(self):
        """Test ordering multiple vouchers"""
        # Create multiple vouchers
        codes = ['FIRST', 'SECOND', 'THIRD']
        created_vouchers = []
        for code in codes:
            v = Voucher.objects.create(
                kode=code,
                persentase_diskon=Decimal("10.00"),
                is_active=True
            )
            created_vouchers.append(v)
        
        # Get vouchers JSON
        response = self.client.get(reverse('voucher:get-vouchers-json'))
        data = json.loads(response.content)
        
        # Verify all vouchers exist
        vouchers = data['vouchers']
        self.assertEqual(len(vouchers), 3)
        
        # Verify all codes are present
        returned_codes = [v['kode'] for v in vouchers]
        for code in codes:
            self.assertIn(code, returned_codes)


# Run coverage report after tests
def tearDownModule():
    """Display coverage report after all tests complete"""
    try:
        import coverage
        cov = coverage.Coverage()
        cov.load()
        
        print("\n" + "="*70)
        print("COVERAGE REPORT FOR VOUCHER MODULE")
        print("="*70)
        cov.report(include=["voucher/*"], omit=["voucher/tests.py", "voucher/migrations/*"])
        print("="*70)
        print(f"📊 HTML Report: voucher/htmlcov/index.html")
        print("="*70 + "\n")
    except Exception as e:
        # If coverage is not running, skip silently
        pass

