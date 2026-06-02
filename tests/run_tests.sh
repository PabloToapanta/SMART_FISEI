#!/bin/bash
echo "=== Configurando datos de prueba ==="
python setup_test_data.py

echo ""
echo "=== Ejecutando pruebas por módulo ==="
python manage.py test tests.test_sistema_completo.AutenticacionTests -v 2
python manage.py test tests.test_sistema_completo.TurnosTests -v 2
python manage.py test tests.test_sistema_completo.TramitesTests -v 2
python manage.py test tests.test_sistema_completo.DocumentosTests -v 2
python manage.py test tests.test_sistema_completo.RutasTests -v 2
python manage.py test tests.test_sistema_completo.HistorialTests -v 2
python manage.py test tests.test_sistema_completo.EstructurasDatosTests -v 2

echo ""
echo "=== Resumen total ==="
python manage.py test tests -v 1
