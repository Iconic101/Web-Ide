from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Project
from .serializers import *
import subprocess
class ProjectListCreateView(APIView):
    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ProjectDetailView(APIView):
    def get(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
            project.delete()
            return Response({"message": "Project deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
            serializer = ProjectSerializer(project, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                print("saved: \n", serializer.data)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)


class ExecuteCodeView(APIView):
    def post(self, request):
        code = request.data.get('code', '')
        language = request.data.get('language', 'python')  # Default to Python

        if not code:
            return Response({"error": "Code is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if language == 'python':
                # Execute Python code using subprocess
                result = subprocess.run(
                    ['python', '-c', code],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=5  # Prevent infinite loops
                )
                return Response({
                    "stdout": result.stdout,
                    "stderr": result.stderr
                }, status=status.HTTP_200_OK)

            elif language == 'javascript':
                # Execute JavaScript (Node.js) code
                result = subprocess.run(
                    ['node', '-e', code],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=5
                )
                return Response({
                    "stdout": result.stdout,
                    "stderr": result.stderr
                }, status=status.HTTP_200_OK)

            elif language == 'ruby':
                # Execute Ruby code
                result = subprocess.run(
                    ['ruby', '-e', code],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=5
                )
                return Response({
                    "stdout": result.stdout,
                    "stderr": result.stderr
                }, status=status.HTTP_200_OK)

            else:
                return Response({"error": "Language not supported."}, status=status.HTTP_400_BAD_REQUEST)

        except subprocess.TimeoutExpired:
            return Response({"error": "Code execution timed out."}, status=status.HTTP_408_REQUEST_TIMEOUT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FileView(APIView):
    def get(self, request, project_id, file_id=None):
        if file_id:
            try:
                file = File.objects.get(pk=file_id, project_id=project_id)
                serializer = FileSerializer(file)
                return Response(serializer.data)
            except File.DoesNotExist:
                return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            files = File.objects.filter(project_id=project_id)
            serializer = FileSerializer(files, many=True)
            return Response(serializer.data)

    def post(self, request, project_id):
        try:
            project = Project.objects.get(pk=project_id)
            serializer = FileSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(project=project)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, project_id, file_id):
        try:
            file = File.objects.get(pk=file_id, project_id=project_id)
            serializer = FileSerializer(file, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except File.DoesNotExist:
            return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, project_id, file_id):
        try:
            file = File.objects.get(pk=file_id, project_id=project_id)
            file.delete()
            return Response({"message": "File deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except File.DoesNotExist:
            return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)