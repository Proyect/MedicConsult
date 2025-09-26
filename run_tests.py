#!/usr/bin/env python
"""
Script para ejecutar todos los tests del proyecto MedicConsult
"""

import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

def run_tests():
    """Ejecutar todos los tests"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crud.settings_test')
    django.setup()
    
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(['history.tests'])
    
    if failures:
        sys.exit(1)
    else:
        print("\n✅ Todos los tests pasaron exitosamente!")
        sys.exit(0)

if __name__ == '__main__':
    run_tests()

