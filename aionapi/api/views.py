from .models import User, Business, Team, Employee, Project, Role, Task, UserProjectRole
from .serializers import UserSerializer, UserRegistrationSerializer,UserLoginSerializer, BusinessSerializer, TeamSerializer, EmployeeSerializer, ProjectSerializer, RoleSerializer, TaskSerializer, UserProjectRoleSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from datetime import datetime
from django.db.models import Count


class UserRegistration(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user.id,
                'username': user.username,
                'ts': int(datetime.now().timestamp()) # Retrieves in microseconds
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
                user = serializer.validated_data
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': user.id,
                    'username': user.username,
                    'ts': int(datetime.now().timestamp()) # Retrieves in microseconds
                }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogout(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        refresh_token = request.data.get('rTkn')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Refresh token not provided'}, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
            return Response({'username': user.username}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class BusinessList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, business_id=None):
        if (business_id):
            try:
                business = Business.objects.get(id=business_id)
                # Check if the user is an employee of the business
                is_employee = Employee.objects.filter(user=request.user, business=business).exists()
                if not is_employee:
                    return Response({'error': 'You are not an employee of this business'}, status=status.HTTP_403_FORBIDDEN)
                serializer = BusinessSerializer(business)
            except Business.DoesNotExist:
                return Response({'error': 'Business not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Get businesses where the user is an employee
            businesses = Business.objects.filter(employee__user=request.user)
            serializer = BusinessSerializer(businesses, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = BusinessSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(id=request.user.id)
                business = serializer.save(owner=user)
                Employee.objects.create(user=user, business=business)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            business_id = request.data.get('business')
            print(business_id)
            business = Business.objects.get(id=business_id)
            # Check if the user is the owner of the business
            is_owner = business.owner != request.user
            if is_owner:
                return Response({'error': 'You are not authorized to update this business'}, status=status.HTTP_403_FORBIDDEN)
            serializer = BusinessSerializer(business, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Business.DoesNotExist:
            return Response({'error': 'Business not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, business_id):
        try:
            business = Business.objects.get(id=business_id)
            has_permission = business.owner != request.user
            if has_permission:
                return Response({'error': 'You do not have permission to delete this business'}, status=status.HTTP_403_FORBIDDEN)

            business.delete()
            return Response({'message': 'Business deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Business.DoesNotExist:
            return Response({'error': 'Business not found'}, status=status.HTTP_404_NOT_FOUND)

class TeamList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, business_id, team_id=None):
        try:
            business = Business.objects.get(id=business_id)
            if not Employee.objects.filter(user=request.user, business=business).exists():
                return Response({'error': 'You are not an employee of this business'}, status=status.HTTP_403_FORBIDDEN)
            
            if team_id:
                try:
                    team = Team.objects.get(id=team_id, business=business)
                    serializer = TeamSerializer(team)
                    return Response(serializer.data)
                except Team.DoesNotExist:
                    return Response({'error': 'Team not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                teams = Team.objects.filter(business=business)
                serializer = TeamSerializer(teams, many=True)
                return Response(serializer.data)
        except Business.DoesNotExist:
            return Response({'error': 'Business not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        # Check if the user is the owner of the business
        try:
            business = Business.objects.get(id=request.data.get('business'))
            if business.owner != request.user:
                return Response({'error': 'You do not have permission to create a team'}, status=status.HTTP_403_FORBIDDEN)
        except Business.DoesNotExist:
            return Response({'error': 'Business not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            team_id = request.data.get('id')

            if not team_id:
                return Response({'error': 'Team ID is required'}, status=status.HTTP_400_BAD_REQUEST)

            team = Team.objects.get(id=team_id)
            
            if team.business.owner != request.user:
                return Response({'error': 'You do not have permission to update this team'}, status=status.HTTP_403_FORBIDDEN)
            
            serializer = TeamSerializer(team, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'id': serializer.data['id'],
                    'name': serializer.data['name'],
                    'description': serializer.data['description']
                })
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Team.DoesNotExist:
            return Response({'error': 'Team not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, business_id, team_id):
        try:
            business = Business.objects.get(id=business_id)
            if business.owner != request.user:
                return Response({'error': 'You do not have permission to delete this team'}, status=status.HTTP_403_FORBIDDEN)

            team = Team.objects.get(id=team_id, business=business)
            team.delete()
            return Response({'message': 'Team deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Business.DoesNotExist:
            return Response({'error': 'Business not found'}, status=status.HTTP_404_NOT_FOUND)
        except Team.DoesNotExist:
            return Response({'error': 'Team not found'}, status=status.HTTP_404_NOT_FOUND)

class EmployeeList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, business_id=None, team_id=None):
        if not business_id:
            return Response({'error': 'business_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user is an employee of the requested business
        if not Employee.objects.filter(user=request.user, business_id=business_id).exists():
            return Response({'error': 'You do not have permission to view employees of this business'}, status=status.HTTP_403_FORBIDDEN)

        employees = Employee.objects.filter(business_id=business_id).select_related('user', 'team')

        if team_id:
            employees = employees.filter(team_id=team_id)

        employee_data = [
            {
                'username': employee.user.username,
                'fullname': employee.user.fullname,
                'team_name': employee.team.name if employee.team else None,
                'avatar': employee.user.picture
            }
            for employee in employees
        ]
        return Response(employee_data)

    def post(self, request):
        username = request.data.get('username')
        business_id = request.data.get('business')
        team_id = request.data.get('team')

        try:
            user = User.objects.get(username=username)
            business = Business.objects.get(id=business_id)
            team = Team.objects.get(id=team_id) if team_id else None

            # Check if the requesting user is the owner of the business
            if business.owner != request.user:
                return Response({'error': 'You do not have permission to add employees to this business'}, status=status.HTTP_403_FORBIDDEN)

            # Check if the user is already an employee of the business
            if Employee.objects.filter(user=user, business=business).exists():
                return Response({'error': 'User is already an employee of this business'}, status=status.HTTP_400_BAD_REQUEST)

            employee = Employee.objects.create(user=user, business=business, team=team)
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Business.DoesNotExist:
            return Response({'error': 'Business not found'}, status=status.HTTP_404_NOT_FOUND)
        except Team.DoesNotExist:
            return Response({'error': 'Team not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        business_id = request.data.get('business')
        username = request.data.get('username')
        team_id = request.data.get('team')

        try:
            business = Business.objects.get(id=business_id)
            if business.owner != request.user:
                return Response({'error': 'You do not have permission to update employees in this business'}, status=status.HTTP_403_FORBIDDEN)

            user = User.objects.get(username=username)
            employee = Employee.objects.get(user=user, business=business)

            if team_id:
                team = Team.objects.get(id=team_id)
            else:
                team = None

            employee.team = team
            employee.save()

            serializer = EmployeeSerializer(employee)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Business.DoesNotExist:
            return Response({'error': 'Business not found'}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)
        except Team.DoesNotExist:
            return Response({'error': 'Team not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, username=None, business_id=None):
        if not business_id:
            return Response({'error': 'Business ID must be specified'}, status=status.HTTP_400_BAD_REQUEST)
        if not username:
            return Response({'error': 'Username must be specified'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            business = Business.objects.get(id=business_id)
            if business.owner != request.user:
                return Response({'error': 'You do not have permission to delete this employee'}, status=status.HTTP_403_FORBIDDEN)

            user = User.objects.get(username=username)
            employee = Employee.objects.get(user=user, business=business)

            if employee.user == business.owner:
                # If the owner is being removed, find the next employee to be the new owner
                next_employee = Employee.objects.filter(business=business).exclude(user=user).first()
                if next_employee:
                    business.owner = next_employee.user
                    business.save()
                else:
                    return Response({'error': 'Cannot remove the last employee (owner) of the business'}, status=status.HTTP_400_BAD_REQUEST)

            employee.delete()
            return Response({'message': 'Employee deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Business.DoesNotExist:
            return Response({'error': 'Business not found'}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)
        
class ProjectList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    def delete(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
            if project.owner != request.user:
                return Response({'error': 'You do not have permission to delete this project'}, status=status.HTTP_403_FORBIDDEN)
            
            project.delete()
            return Response({'message': 'Project deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Project.DoesNotExist:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, project_id=None):
        if project_id:
            try:
                project = Project.objects.select_related('business').get(id=project_id)
                if not UserProjectRole.objects.filter(user=request.user, project=project).exists():
                    return Response({'error': 'You do not have access to this project'}, status=status.HTTP_403_FORBIDDEN)
                serializer = ProjectSerializer(project)
                response_data = serializer.data
                response_data['business_name'] = project.business.name if project.business else None
                # Calculate progression
                total_tasks = Task.objects.filter(project=project).count()
                done_tasks = Task.objects.filter(project=project, status='DONE').count()
                response_data['progress'] = round((done_tasks / total_tasks) * 100, 1) if total_tasks > 0 else 0
                return Response(response_data)
            except Project.DoesNotExist:
                return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            user_projects = UserProjectRole.objects.filter(user=request.user).values_list('project', flat=True)
            projects = Project.objects.filter(id__in=user_projects)
            serializer = ProjectSerializer(projects, many=True)
            response_data = serializer.data
            for project in response_data:
                total_tasks = Task.objects.filter(project_id=project['id']).count()
                done_tasks = Task.objects.filter(project_id=project['id'], status='DONE').count()
                project['progress'] = round((done_tasks / total_tasks) * 100, 1) if total_tasks > 0 else 0
            return Response(response_data)

    def post(self, request):
        data = request.data.copy()
        data['owner_id'] = request.user.id  # Assuming the user is authenticated and request.user is available
        serializer = ProjectSerializer(data=data)
        if serializer.is_valid():
            project = serializer.save()
            UserProjectRole.objects.create(user=User.objects.get(id=project.owner_id), project=project, role=Role.objects.get(name='Owner'))            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        project_id = request.data.get('project_id')
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

        if project.owner != request.user:
            return Response({'error': 'You do not have permission to update this project'}, status=status.HTTP_403_FORBIDDEN)

        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class Stats(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        if not project_id:
            return Response({'error': 'project_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user has access to the project
        user_project_role = UserProjectRole.objects.filter(user=request.user, project_id=project_id).first()
        if not user_project_role:
            return Response({'error': 'You do not have access to this project'}, status=status.HTTP_403_FORBIDDEN)

        # Retrieve stats for the project
        total_tasks = Task.objects.filter(project_id=project_id).count()
        completed_tasks = Task.objects.filter(project_id=project_id, status='completed').count()
        pending_tasks = Task.objects.filter(project_id=project_id, status='pending').count()

        # If the request URL contains '/priority/', filter tasks by priority
        if '/priority/' in request.path:
            priority_counts = Task.objects.filter(project_id=project_id).values('priority').annotate(count=Count('id'))
            counted_priorities = {
                'H': sum(item['count'] for item in priority_counts if item['priority'] == 'H'),
                'M': sum(item['count'] for item in priority_counts if item['priority'] == 'M'),
                'L': sum(item['count'] for item in priority_counts if item['priority'] == 'L') 
            }
            return Response({'priority_counts': counted_priorities}, status=status.HTTP_200_OK)
        elif '/status/' in request.path:
            status_counts = Task.objects.filter(project_id=project_id).values('status').annotate(count=Count('id'))
            counted_statuses = {
                'DONE': sum(item['count'] for item in status_counts if item['status'] == 'DONE'),
                'IN_PROGRESS': sum(item['count'] for item in status_counts if item['status'] == 'IN_PROGRESS'),
                'TODO': sum(item['count'] for item in status_counts if item['status'] == 'TODO')
            }
            return Response({'status_counts': counted_statuses}, status=status.HTTP_200_OK)
        elif '/workload/' in request.path:
            workload_counts = Task.objects.filter(project_id=project_id).values('user_assigned').annotate(count=Count('id'))
            counted_workloads = {}
            for user in workload_counts:
                username = User.objects.filter(id=user['user_assigned']).values_list('username', flat=True).first()
                if username:
                    counted_workloads[username] = user['count']
            return Response({'workload_counts': counted_workloads}, status=status.HTTP_200_OK)
        else:
            done_tasks_count = Task.objects.filter(project_id=project_id, status='DONE').count()
            return Response({
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks,
                'pending_tasks': pending_tasks,
                'done_tasks_count': done_tasks_count,
            }, status=status.HTTP_200_OK)


class RoleList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)

class TaskList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user is part of the project
        user_project_role = UserProjectRole.objects.filter(user=request.user, project=task.project).first()
        if not user_project_role:
            return Response({'error': 'You do not have access to this task'}, status=status.HTTP_403_FORBIDDEN)

        # Check if the user role has sufficient permissions
        if user_project_role.role.name == 'Guest' or user_project_role.role.perm < 7:
            return Response({'error': 'You do not have sufficient permissions to edit this task'}, status=status.HTTP_403_FORBIDDEN)

        if 'user_assigned' in request.data:
            username = request.data['user_assigned']
            user = User.objects.filter(username=username).first()
            if user:
                request.data['user_assigned'] = user.id
            else:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user is part of the project
        user_project_role = UserProjectRole.objects.filter(user=request.user, project=task.project).first()
        if not user_project_role:
            return Response({'error': 'You do not have access to this task'}, status=status.HTTP_403_FORBIDDEN)

        # Check if the user role is not a guest and has sufficient permissions
        if user_project_role.role.name == 'Guest' or user_project_role.role.perm < 7:
            return Response({'error': 'You do not have sufficient permissions to delete this task'}, status=status.HTTP_403_FORBIDDEN)

        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, project_id=None, task_id=None, user_id=None):
        if task_id:
            try:
                task = Task.objects.select_related('user_assigned', 'team_assigned', 'project').get(id=task_id)
            except Task.DoesNotExist:
                return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

            # Check if the user has access to the project
            user_project_role = UserProjectRole.objects.filter(user=request.user, project=task.project).first()
            if not user_project_role:
                return Response({'error': 'You do not have access to this task'}, status=status.HTTP_403_FORBIDDEN)

            task_info = {
                'id': task.id,
                'name': task.name,
                'description': task.description,
                'user': task.user_assigned.username if task.user_assigned else None,
                'priority': task.get_priority_display(),
                'start_date': task.start_date,
                'end_date': task.end_date,
                'status': task.get_status_display(),                
                'team': task.team_assigned.name if task.team_assigned else None,
            }
            return Response(task_info)
        
        elif project_id:
            # Check if the user has access to the project
            user_project_role = UserProjectRole.objects.filter(user=request.user, project_id=project_id).first()
            if not user_project_role:
                return Response({'error': 'You do not have access to this project'}, status=status.HTTP_403_FORBIDDEN)
            
            tasks = Task.objects.filter(project_id=project_id).select_related('user_assigned', 'team_assigned')
            
            task_data = []
            for task in tasks:
                task_info = {
                    'id': task.id,
                    'name': task.name,
                    'description': task.description,
                    'user': task.user_assigned.username if task.user_assigned else None,
                    'priority': task.get_priority_display(),
                    'start_date': task.start_date,
                    'end_date': task.end_date,
                    'status': task.get_status_display(),                
                    'team': task.team_assigned.name if task.team_assigned else None
                }
                task_data.append(task_info)
            
            return Response(task_data)
        
        elif user_id:
            if '/team/' in request.path:
                # Get tasks for the user's team, excluding tasks with status DONE
                user = User.objects.get(id=user_id)
                user_teams = Team.objects.filter(employee__user=user)
                tasks = Task.objects.filter(team_assigned__in=user_teams).exclude(status='DONE').select_related('user_assigned', 'team_assigned', 'project')
            else:
                # Get tasks for the user making the request, excluding tasks with status DONE
                tasks = Task.objects.filter(user_assigned=request.user).exclude(status='DONE').select_related('user_assigned', 'team_assigned', 'project')
            
            task_data = []
            for task in tasks:
                task_info = {
                    'id': task.id,
                    'name': task.name,
                    'description': task.description,
                    'user': task.user_assigned.username if task.user_assigned else None,
                    'priority': task.get_priority_display(),
                    'start_date': task.start_date,
                    'end_date': task.end_date,
                    'status': task.get_status_display(),                
                    'team': task.team_assigned.name if task.team_assigned else None,
                    'project': task.project.name
                }
                task_data.append(task_info)
            return Response(task_data)        
    def post(self, request):
        # Check if the user has sufficient permissions
        user_project_role = UserProjectRole.objects.filter(user=request.user, project_id=request.data.get('project')).first()
        if not user_project_role or user_project_role.role.perm < 7:
            return Response({'error': 'You do not have sufficient permissions to create a task'}, status=status.HTTP_403_FORBIDDEN)

        # Get the User instance based on the provided username
        user_assigned = User.objects.filter(username=request.data.get('user_assigned')).first()
        if not user_assigned:
            return Response({'error': 'Invalid username provided for user_assigned'}, status=status.HTTP_400_BAD_REQUEST)

        # Update the request data with the User instance
        request_data = request.data.copy()
        request_data['user_assigned'] = user_assigned.id

        serializer = TaskSerializer(data=request_data)
        if serializer.is_valid():
            task = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProjectRoleList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id=None):
        if not project_id:
            return Response({'error': 'project_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the requester user is on the specified project
        user_project_role = UserProjectRole.objects.filter(user=request.user, project_id=project_id).first()
        if not user_project_role:
            return Response({'error': 'You do not have access to this project'}, status=status.HTTP_403_FORBIDDEN)

        user_project_roles = UserProjectRole.objects.filter(project_id=project_id)
        serializer = UserProjectRoleSerializer(user_project_roles, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Check if the user has sufficient permissions on the project
        project_id = request.data.get('project')
        user_project_role = UserProjectRole.objects.filter(user=request.user, project_id=project_id).first()
        if not user_project_role or user_project_role.role.perm < 31:
            return Response({'error': 'You do not have sufficient permissions to create a user project role'}, status=status.HTTP_403_FORBIDDEN)

        username = request.data.get('user')
        project_id = request.data.get('project')
        role_id = request.data.get('role')

        try:
            user = User.objects.get(username=username)
            project = Project.objects.get(id=project_id)
            role = Role.objects.get(id=role_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Project.DoesNotExist:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
        except Role.DoesNotExist:
            return Response({'error': 'Role not found'}, status=status.HTTP_404_NOT_FOUND)

        user_project_role, created = UserProjectRole.objects.get_or_create(user=user, project=project, role=role)
        if created:
            return Response(UserProjectRoleSerializer(user_project_role).data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'UserProjectRole already exists'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id=None, username=None):
        if not project_id or not username:
            return Response({'error': 'project_id and username are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the requester is on the same project
        requester_role = UserProjectRole.objects.filter(user=request.user, project_id=project_id).first()
        if not requester_role:
            return Response({'error': 'You do not have access to this project'}, status=status.HTTP_403_FORBIDDEN)

        # Get the user to be deleted
        try:
            user_to_delete = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Get the role of the user to be deleted
        user_to_delete_role = UserProjectRole.objects.filter(user=user_to_delete, project_id=project_id).first()
        if not user_to_delete_role:
            return Response({'error': 'User to delete is not on this project'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the requester has higher role permissions
        if requester_role.role.perm <= user_to_delete_role.role.perm:
            return Response({'error': 'You do not have sufficient permissions to delete this user from the project'}, status=status.HTTP_403_FORBIDDEN)

        # Delete the user's role from the project
        user_to_delete_role.delete()
        return Response({'message': 'User removed from project successfully'}, status=status.HTTP_200_OK)
        
    def put(self, request):
        project_id = request.data.get('project')
        if not project_id:
            return Response({'error': 'project_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user has sufficient permissions on the project
        requester_role = UserProjectRole.objects.filter(user=request.user, project_id=project_id).first()
        if not requester_role or requester_role.role.perm < 31:
            return Response({'error': 'You do not have sufficient permissions to update a user project role'}, status=status.HTTP_403_FORBIDDEN)

        username = request.data.get('user')
        role_id = request.data.get('role')

        try:
            user = User.objects.get(username=username)
            project = Project.objects.get(id=project_id)
            role = Role.objects.get(id=role_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Project.DoesNotExist:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
        except Role.DoesNotExist:
            return Response({'error': 'Role not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user to be modified exists in the project
        user_to_modify_role = UserProjectRole.objects.filter(user=user, project=project).first()
        if user_to_modify_role:
            # Check if the requester has higher role permissions than the user to be modified
            if requester_role.role.perm <= user_to_modify_role.role.perm:
                return Response({'error': 'You do not have sufficient permissions to modify this user\'s role'}, status=status.HTTP_403_FORBIDDEN)

        user_project_role, created = UserProjectRole.objects.update_or_create(
            user=user,
            project=project,
            defaults={'role': role}
        )

        serializer = UserProjectRoleSerializer(user_project_role)
        return Response(serializer.data)
    
class UserProjects(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            # Check if the JWT token owner is the same as the user_id provided in the URL
            if request.user.id != user_id:
                return Response({'error': 'Unauthorized access'}, status=status.HTTP_403_FORBIDDEN)

            user_project_roles = UserProjectRole.objects.filter(user_id=user_id).select_related('role', 'project')
            projects_data = []
            for upr in user_project_roles:
                project_data = ProjectSerializer(upr.project).data
                project_data['role_perm'] = upr.role.perm if upr.role else None
                projects_data.append(project_data)

            for project in projects_data:
                total_tasks = Task.objects.filter(project_id=project['id']).count()
                done_tasks = Task.objects.filter(project_id=project['id'], status='DONE').count()
                project['progress'] = round((done_tasks / total_tasks) * 100, 1) if total_tasks > 0 else 0
            
            return Response(projects_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ProjectUsers(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        try:
            # Check if the user has access to the project
            if not UserProjectRole.objects.filter(user=request.user, project_id=project_id).exists():
                return Response({'error': 'Unauthorized access'}, status=status.HTTP_403_FORBIDDEN)

            user_project_roles = UserProjectRole.objects.filter(project_id=project_id).select_related('user', 'role')
            user_data = []
            for upr in user_project_roles:
                user_data.append({
                    'username': upr.user.username,
                    'role_id': upr.role.id if upr.role else None,
                    'role_perm': upr.role.perm if upr.role else None,
                    'role_name': upr.role.name if upr.role else None
                })
            return Response(user_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserBusiness(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            # Check if the JWT token owner is the same as the user_id provided in the URL
            if request.user.id != user_id:
                return Response({'error': 'Unauthorized access'}, status=status.HTTP_403_FORBIDDEN)

            # Get businesses where the user is an employee
            user_businesses = Business.objects.filter(employee__user_id=user_id).distinct()
            serializer = BusinessSerializer(user_businesses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserTeams(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            # Check if the JWT token owner is the same as the user_id provided in the URL
            if request.user.id != user_id:
                return Response({'error': 'Unauthorized access'}, status=status.HTTP_403_FORBIDDEN)

            # Check if the user is an employee of any business
            employee_businesses = Employee.objects.filter(user_id=user_id)
            is_employee = employee_businesses.exists()
            
            if not is_employee:
                return Response({'error': 'User is not an employee of any business'}, status=status.HTTP_400_BAD_REQUEST)
            
            if is_employee:
                user_teams = Team.objects.filter(employee__in=employee_businesses).distinct()
                team_data = []
                for team in user_teams:
                    business = team.business
                    team_data.append({
                        'team': TeamSerializer(team).data,
                        'business_name': business.name if business else None
                    })
            
            return Response(team_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UsernameSearch(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, username, business_id=None):
        try:
            print("Starting username search")
            if 'employees/username/' in request.path:
                print("Searching for employees")
                # Get the business of the requester
                if business_id:
                    business = Business.objects.filter(id=business_id).first()

                    if not business:
                        return Response({'error': 'Business not found'}, status=status.HTTP_404_NOT_FOUND)  
                    
                    requester_business = Employee.objects.filter(user=request.user, business=business).first()
                    print(f"Requester's business: {requester_business}")
                    # Get employees of the same business
                    employees = Employee.objects.filter(business=business)
                    print(f"Number of employees in the same business: {employees.count()}")
                    # Get users who are employees of the same business and match the username
                    users = User.objects.filter(username__icontains=username, employee__in=employees)
                    print(f"Number of matching users: {users.count()}")
                else:
                    return Response({'error': 'Business ID is required for employee search'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                print("Searching for all users")
                users = User.objects.filter(username__icontains=username)
                print(f"Number of matching users: {users.count()}")
            
            serializer = UserSerializer(users, many=True)
            usernames = [user['username'] for user in serializer.data]
            print(f"Matching usernames: {usernames}")
            return Response(usernames, status=status.HTTP_200_OK)      
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
