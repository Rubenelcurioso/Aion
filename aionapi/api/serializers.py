from rest_framework import serializers
from .models import User, Business, Team, Employee, Project, Role, Task, UserProjectRole
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate, get_user_model
import re

AuthUser = get_user_model()

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        str_username = data.get('username')
        str_password = data.get('password')
        obj_user = User.objects.filter(username=str_username).first()
        obj_user = authenticate(username=str_username, password=str_password)
        if obj_user:
            return obj_user
        else:
            raise serializers.ValidationError('Invalid credentials')


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'fullname', 'birthday', 'phone', 'password', 'password2']

    def validate(self, attrs):
        b_username_exists = User.objects.filter(username=attrs['username']).exists()
        if b_username_exists:
            raise serializers.ValidationError({'username': 'Username already exists'})
        b_email_exists = User.objects.filter(email=attrs['email']).exists()
        if b_email_exists:
            raise serializers.ValidationError({'email': 'Email already exists'})
        b_passwords_match = attrs['password'] == attrs['password2']
        if not b_passwords_match:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        str_password = validated_data.pop('password')
        str_email = validated_data.pop('email')
        str_username = validated_data.pop('username')
        obj_user = User.objects.create_user(username=str_username, email=str_email, password=str_password, **validated_data)
        return obj_user


class BusinessSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    class Meta:
        model = Business
        fields = '__all__'

    def validate_email(self, value):
        # Get the current instance if it exists (it will exist for updates)
        obj_instance = getattr(self, 'instance', None)

        # Check if the email exists, excluding the current instance
        b_email_exists = Business.objects.filter(email=value).exclude(pk=obj_instance.pk if obj_instance else None).exists()
        if b_email_exists:
            raise serializers.ValidationError("A business with this email already exists.")
        return value

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Name field cannot be empty.")
        return value

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Project
        fields = '__all__'

    def validate(self, data):
        b_date_valid = data['start_date'] and data['end_date'] and data['start_date'] <= data['end_date']
        if not b_date_valid:
            raise serializers.ValidationError("Start date must be before or equal to end date.")
        b_name_format_valid = re.match("^[A-Za-z0-9 ]*$", data['name'])
        if not b_name_format_valid:
            raise serializers.ValidationError("Project name must contain only numbers, spaces, and letters.")
        return data

    def create(self, validated_data):
        int_owner_id = validated_data.pop('owner_id')
        obj_owner = User.objects.get(id=int_owner_id)
        obj_project = Project.objects.create(owner=obj_owner, **validated_data)
        return obj_project
    
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def to_internal_value(self, data):
        # Convert priority
        dict_priority_mapping = {'LOW': 'L', 'MEDIUM': 'M', 'HIGH': 'H'}
        if 'priority' in data:
            data['priority'] = dict_priority_mapping.get(data['priority'].upper(), data['priority'])

        # Convert status
        dict_status_mapping = {
            'todo': 'TODO',
            'to do': 'TODO',
            'in progress': 'IN_PROGRESS',
            'inprogress': 'IN_PROGRESS',
            'in_progress': 'IN_PROGRESS',
            'done': 'DONE'
        }
        if 'status' in data:
            data['status'] = dict_status_mapping.get(data['status'].lower(), data['status'])
        return super().to_internal_value(data)
    def validate(self, data):
        b_date_valid = data.get('start_date') and data.get('end_date') and data['start_date'] <= data['end_date']
        if not b_date_valid:
            raise serializers.ValidationError("Start date must be before end date.")

        return data
class UserProjectRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProjectRole
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def validate_username(self, value):
        b_username_valid = re.match("^[A-Za-z0-9]*$", value)
        if not b_username_valid:
            raise serializers.ValidationError("Username must contain only numbers and letters.")
        return value
