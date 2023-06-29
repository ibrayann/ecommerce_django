from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model

User = get_user_model()

# Obtén el permiso deseado
try:
    permission = Permission.objects.get(codename='view_product')
except Permission.DoesNotExist:
    # Si el permiso no existe, créalo
    permission = Permission.objects.create(
        codename='view_product',
        name='Can view product',
        content_type=None
    )

# Crea un grupo y asigna el permiso
group = Group.objects.create(name='Grupo de usuarios')
group.permissions.add(permission)

# Crea un usuario y asigna el permiso
user = User.objects.create_user(username='usuario', password='contraseña')
user.user_permissions.add(permission)

# Asigna el usuario al grupo
user.groups.add(group)
