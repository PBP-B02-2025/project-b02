"""
Run voucher tests with coverage report
Usage: 
  cd voucher
  python run_voucher_tests.py
"""

import os
import sys

# Add parent directory to path for Django imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ballistic.settings')
django.setup()

try:
    import coverage
except ImportError:
    print("❌ Coverage package not found. Installing...")
    os.system("pip install coverage")
    import coverage

# Get current directory (voucher folder)
voucher_dir = os.path.dirname(os.path.abspath(__file__))

# Start coverage with specific source files
cov = coverage.Coverage(
    source=[voucher_dir],
    omit=[
        '*/tests.py',
        '*/test_*.py',
        '*/migrations/*',
        '*/htmlcov/*',
        '*/__pycache__/*',
        '*/run_voucher_tests.py',
    ]
)
cov.start()

# Run tests
from django.core.management import call_command
from django.test.utils import get_runner
from django.conf import settings

TestRunner = get_runner(settings)
test_runner = TestRunner(verbosity=2, interactive=True, keepdb=False)

print("\n" + "="*70)
print("🧪 RUNNING VOUCHER MODULE TESTS")
print("="*70 + "\n")

failures = test_runner.run_tests(["voucher"])

# Stop coverage
cov.stop()
cov.save()

# Display coverage report
print("\n" + "="*70)
print("📊 COVERAGE REPORT FOR VOUCHER MODULE")
print("="*70 + "\n")

# Only show coverage for forms, views, and models
include_files = [
    os.path.join(voucher_dir, 'forms.py'),
    os.path.join(voucher_dir, 'views.py'),
    os.path.join(voucher_dir, 'models.py'),
]
cov.report(show_missing=True, include=include_files)

print("\n" + "="*70)
print("📁 HTML Report: voucher/htmlcov/index.html")
print("="*70 + "\n")

# Generate HTML report
html_dir = os.path.join(voucher_dir, 'htmlcov')
cov.html_report(directory=html_dir)

# Exit with appropriate code
sys.exit(bool(failures))
